"""The build's assertions, run on the cut pack: the bar block (labels R1 to R7, the bar's own rule numbers and not the
chain's results, which are named here by their analysis keys), every semantic fork (SF1 to SF16), each result's band
and the margin to every hurried figure, the mess, the input gates, the realism sweep and the author-side truth runs.

    G = run(target, gen_dir)        fills RESULTS with (label, ok, detail); make.py stops on any False

Nothing here is a solver: every pass is this generator's own implementation of a named method (results.py).
"""
import csv
import hashlib
import inspect
import io
import json
import os
import re
import zipfile

import numpy as np
import pandas as pd

import analysis as A
import effort_passes as EP
import golden as GD
import load
import pack
import params as P
import results as RS
import runner as R
import sweep as S

RESULTS = []
N3 = len(GD.KEYS) / 3.0


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), str(detail)))
    return bool(cond)


def grades(res):
    return {k: RS.grade(res, k) for k in GD.KEYS}


def right(res):
    return [k for k in GD.KEYS if RS.grade(res, k) == "right"]


def _read(target, key):
    return os.path.join(target, pack.FILES[key])


def truth():
    """What each shortlisted configuration really scores, from the author-side runs (never shipped)."""
    out = {}
    for j in S.truth_specs():
        try:
            o = R.load(j["train"])
        except Exception:
            return None, None
        out.setdefault((j["name"].split("-")[1], j["train"]["lr"]), []).append(float(o["final"][4]))
    clean = {}
    for j in S.clean_truth_specs():
        try:
            clean[j["name"]] = float(R.load(j["train"])["final"][4])
        except Exception:
            return None, None
    return {k: float(np.mean(v)) for k, v in out.items()}, clean


def true_costs(clean):
    """What each route's labels really add per tenth: the benchmark's own score of the pilot's trials (never shipped
    for a vendor-label run) against a run on as many expert-quality labels (author side)."""
    cells_ = {}
    for j in S.pilot_specs():
        t = j["train"]
        if j["stage"] != "vend" or j["fate"] != "finished":
            continue
        try:
            cells_.setdefault((t["width"], t["nA"], t["nB"], t["nC"]), []).append(float(R.load(t)["final"][4]))
        except Exception:
            return None
    out = {"contractor": {}, "map": {}}
    for (w, a, b, c), v in sorted(cells_.items()):
        base = clean.get("clean-w%d-%dk" % (w, (a + b + c) // 1000))
        if base is None:
            continue
        tenths = 10.0 * (b + c) / (a + b + c)
        out["contractor" if b else "map"]["w%d %dk+%dk" % (w, a // 1000, (b + c) // 1000)] = (float(np.mean(v)) - base) / tenths
    return out


def run(target, gen_dir, prompt_path=None):
    RESULTS.clear()
    G = GD.compute(target)
    F = GD.figures(G)
    g, c, q = G["golden"], G["careful"], G["quick"]
    rows, facts, yr = G["rows"], G["facts"], G["yr"]
    B = RS.BANDS
    files = sorted(os.listdir(target))

    # ---------------------------------------------------------------- R1 the field's raw material ships
    need = ["metrics", "runs", "items", "devsplit", "shards", "bench", "ckpt"]
    ok("R1 every result reads shipped rows", all(os.path.exists(_read(target, k)) for k in need),
       "tracking metrics and runs, item scores, development split, shard register, benchmark rows, store listing")
    ok("R1 the shortlist is read from the pack", load.shortlist(target) == S.SHORTLIST, "the shortlist workbook equals the generator's")
    heads = {}
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                heads[f] = next(csv.reader(fh))
    banned = re.compile(r"benchmark_equiv|expected|forecast|expert_loss|route_cost|true|golden|answer", re.I)
    hits = [(f, h) for f, hs in heads.items() for h in hs if banned.search(h)]
    ok("R1 no shipped column holds a result", not hits, hits)
    ok("R1 per-step logs at the grain the field works at", facts["items"] == sum(P.DEV_MIX.values()) and len(yr) == 128,
       "%d item rows for %d final checkpoints" % (facts["items"], len(yr)))

    # ---------------------------------------------------------------- R2 every mess item is real and neutral
    bench_final, bfacts, joined = load.benchmark_scores(target)
    mid = joined[(joined["status"] == "SCORED") & (joined["final"] == False)]
    rows_mid = [dict(r, bench=float(mid[mid["run_id"] == r["run_id"]]["log_loss"].iloc[0])) if r["run_id"] in set(mid["run_id"])
                else r for r in rows]
    gm = RS.run_pass(rows_mid, dict(facts, sub_final=facts["sub_scored"]), RS.GOLDEN)
    off = [k for k in GD.KEYS if RS.grade(gm, k) != "right"]
    ok("R2 part-way benchmark uploads taken for final scores move no result out of its band", not off and RS.grade(gm, "counts") != "right",
       "outside its band: %s; the count of scored finals is the only thing that changes" % (off or "none"))
    # the receipt counted twice puts 4,000 more contractor points in every run whose range holds shard 19; emulated
    # at the trial's own total (a larger shift in share than the 132,000 of 260,000 it would really give)
    rows_dup = [dict(r, nB=r["nB"] + P.SHARD, nA=r["nA"] - P.SHARD) if r["nB"] >= 80000 else r for r in rows]
    gd = RS.run_pass(rows_dup, facts, RS.GOLDEN)
    off = [k for k in GD.KEYS if RS.grade(gd, k) != "right"]
    ok("R2 the superseded shard receipt counted twice moves no result out of its band", not off, off or "every result inside")
    m = pd.read_csv(_read(target, "metrics"))
    runs = pd.read_csv(_read(target, "runs"))
    m["k"] = m["key"].replace({"val_loss": "dev/loss"})
    dev = m[m["k"] == "dev/loss"]
    fin = runs[runs["status"] == "FINISHED"]
    last = dev.merge(fin[["run_id", "max_steps"]], on="run_id")
    last = last[last["step"] == last["max_steps"]]
    ok("R2 a resumed job's repeated steps never touch the final step", last.groupby("run_id").size().max() == 1 and
       last["run_id"].nunique() == len(fin), "%d finished runs, one final development loss each" % last["run_id"].nunique())
    rep = dev.groupby(["run_id", "step"]).size()
    ok("R2 resumed jobs log repeated steps", int((rep > 1).sum()) > 20, "%d run-steps logged twice" % int((rep > 1).sum()))
    ok("R2 two logger vocabularies in the export", set(m["key"]) >= {"val_loss", "dev/loss", "loss", "train/loss"}, sorted(set(m["key"])))
    item_cols = set(pd.read_csv(_read(target, "items"), nrows=1).columns) - {"item"}
    ok("R2 unfinished runs and the lost dump carry no item scores", item_cols < set(fin["run_id"]) and len(item_cols) == 128,
       "%d of %d finished runs have item scores" % (len(item_cols), len(fin)))
    sub = pd.read_csv(_read(target, "bench"), dtype=str)
    dup = sub[sub["status"].str.startswith("DUPLICATE_OF")]
    ok("R2 a repeated upload carries no second score", len(dup) == 2 and dup["log_loss"].isna().all(), "%d repeats" % len(dup))

    # ---------------------------------------------------------------- R3 each result's hurried figure
    gq, gc = grades(q), grades(c)
    ok("R3 the quick pass earns a third or less", len(right(q)) <= N3, right(q))
    ok("R3 the careful pass earns the trial and the costs, half of the expected losses, and nothing else",
       right(c) == ["trial", "costs"] and gc["expected"] == "partly" and [gc[k] for k in ("level", "range", "call")] == ["missed"] * 3, gc)
    ok("R3 the thorough pass earns every result", right(g) == GD.KEYS, grades(g))
    ok("R3 careful: the 512,000 level sits below its band", B["level"][0] - c["level"] >= 0.010, "%.4f against %.3f" % (c["level"], B["level"][0]))
    ok("R3 careful: C and D sit below their bands", B["expected"]["C"][0] - c["expected"]["C"] >= 0.020 and B["expected"]["D"][0] - c["expected"]["D"] >= 0.015,
       "C %.4f, D %.4f" % (c["expected"]["C"], c["expected"]["D"]))
    ok("R3 careful: A and B sit inside their bands, and are priced as earned", RS.cells(c, "expected") == [True, True, False, False],
       "A %.4f, B %.4f" % (c["expected"]["A"], c["expected"]["B"]))
    ok("R3 careful: its C sits below even the last doubling's gain carried on undiminished",
       G["bound_last"]["expected"]["C"] - c["expected"]["C"] >= 0.020, "%.4f against %.4f" % (c["expected"]["C"], G["bound_last"]["expected"]["C"]))
    ok("R3 careful: names C on its own expected values", c["call"]["pick"] == "C" and c["call"]["margin"] >= 0.005,
       "%s by %.4f" % (c["call"]["pick"], c["call"]["margin"]))
    ok("R3 careful: its range is drawn round C", c["range"]["config"] == "C", c["range"]["config"])
    ok("R3 careful: every held-back miss falls on the same side, and the pass keeps its curve", all(v < 0 for v in c["_miss"].values()) and
       c["heldback"] >= 0.025 and c["heldback"] - g["heldback"] >= 0.010,
       "%s; gap %.4f against %.4f" % ({k: round(v, 4) for k, v in c["_miss"].items()}, c["heldback"], g["heldback"]))
    ok("R3 quick: names C on the logged loss", q["call"]["pick"] == "C" and q["expected"]["C"] < 0.5, "C %.3f" % q["expected"]["C"])
    ok("R3 quick: the logged loss puts the map trial far below its band", B["trial"]["exp128k_map384k"][0] - G["logged_trial"] >= 0.1,
       "%.3f" % G["logged_trial"])
    ok("R3 quick: the logged loss turns both routes' costs negative", q["costs"]["ctr_per10"] < -0.002 and q["costs"]["map_per10"] < -0.002,
       "contractor %.4f, map transfer %.4f" % (q["costs"]["ctr_per10"], q["costs"]["map_per10"]))
    ln = G["line"]
    ok("R3 the ladder's straight line names C and loses the level", ln["call"]["pick"] == "C" and B["level"][0] - ln["level"] >= 0.03,
       "level %.4f" % ln["level"])
    sr = G["seed_range"]["range"]
    ok("R3 seed spread alone gives a range too narrow for its band", B["range"]["half"][0] - RS.half_width(sr) >= 0.003 and
       RS.grade(G["seed_range"], "range") == "partly", "half-width %.4f against %.3f" % (RS.half_width(sr), B["range"]["half"][0]))
    ok("R3 the band's narrow end is what run-to-run spread and the yardstick's error give together",
       abs(RS.Z80 * (g["range"]["parts"]["run"] ** 2 + g["range"]["parts"]["yardstick"] ** 2) ** 0.5 - B["range"]["half"][0]) < 0.0005,
       "%.4f" % (RS.Z80 * (g["range"]["parts"]["run"] ** 2 + g["range"]["parts"]["yardstick"] ** 2) ** 0.5))

    # ---------------------------------------------------------------- R4 no plant
    series = {}
    for rid, grp in dev.groupby("run_id"):
        series[rid] = hashlib.sha1(",".join("%.6f" % v for v in grp.sort_values(["timestamp_ms"])["value"]).encode()).hexdigest()
    ok("R4 no run's logged series is a copy of another's", len(set(series.values())) == len(series), "%d distinct series" % len(series))
    digests = {f: hashlib.sha1(open(os.path.join(target, f), "rb").read()).hexdigest() for f in files}
    ok("R4 no file is a copy of another", len(set(digests.values())) == len(files), "%d files" % len(files))
    notes = open(_read(target, "notes"), encoding="utf-8").read()
    ok("R4 the notes state no loss, forecast or belief about an option", not re.search(r"\b0\.\d{2,}", notes) and
       not re.search(r"\b(thinks|believes|should win|looks best|favou?rite|prefers?)\b", notes, re.I), "no figure and no belief")
    with zipfile.ZipFile(_read(target, "shortlist")) as z:
        wbxml = z.read("xl/workbook.xml").decode()
    ok("R4 the shortlist workbook hides nothing", "hidden" not in wbxml and "definedName" not in wbxml, "no hidden sheet or defined name")
    sl = load.shortlist(target)
    ok("R4 no shipped artifact ranks the options", "rank" not in notes.lower() or "ranked on the expected value" in notes, "the only ranking word is the programme's rule")

    # ---------------------------------------------------------------- R5 no one thing
    lg = G["logged_gap"]
    ok("R5 the logged loss sits above the benchmark-equivalent loss in every run", min(min(v) for v in lg.values()) > 0.03 and
       sum(len(v) for v in lg.values()) == 128, {k: (round(min(v), 3), round(max(v), 3), len(v)) for k, v in lg.items()})
    ok("R5 the tabled learning rate costs every ladder width", all(min(v.values()) > 0.015 for v in G["lr_cost"].values()),
       {w: {k: round(x, 4) for k, x in v.items()} for w, v in G["lr_cost"].items()})
    line = A.ladder_line(yr, 128, "y", "matched")[0]
    lv = g["_levels"]
    above = {t: lv[t] - line(t) for t in (256000, 512000)}
    ok("R5 the level sits above the ladder's line at every total past the pool", above[256000] > 0.004 and above[512000] > 0.03,
       {k: round(v, 4) for k, v in above.items()})
    cells_above = [k for k in G["rm"]["cells"] if sum(k) > 128000]
    ok("R5 the bend is carried by every trial above 128,000 examples, at both widths", len(cells_above) == 6 and
       len(A.vendor_cells(yr, 256)) == 3, "%d width-128 trials and 3 at width 256" % len(cells_above))
    wg = g["_width"]["g256"]
    ok("R5 the width step is in every total", all(v > 0 for v in wg.values()) and wg[512000] > wg[32000], {k: round(v, 4) for k, v in wg.items()})
    q_y = RS.run_pass(rows, facts, dict(RS.QUICK, score="yardstick"))
    newly = [k for k in right(q_y) if k not in right(q)]
    ok("R5 the yardstick alone, given to the quick pass, rescues a third or less", len(newly) <= N3, newly)
    ln_m = RS.run_pass(rows, facts, dict(RS.LINE, lr_fix="matched"))
    newly = [k for k in right(ln_m) if k not in right(ln)]
    ok("R5 the matched learning rate alone, given to the straight line, rescues a third or less", len(newly) <= N3, newly)
    newly = [k for k in right(G["hint_levels"]) if k not in right(c)]
    ok("R5 the level past the pool alone, given to the careful pass, rescues a third or less", len(newly) <= N3,
       "%s, carried on by its %s form" % (newly, G["hint_levels"]["_habit_form"]))
    newly = [k for k in right(G["hint_every"]) if k not in right(c)]
    ok("R5 a level at every total, given to the careful pass, rescues half and no more", newly == ["level", "expected", "call"] and
       len(newly) <= len(GD.KEYS) / 2.0 and RS.grade(G["hint_every"], "range") == "partly",
       "%s, carried on by its %s form; the range stays Partly" % (newly, G["hint_every"]["_habit_form"]))

    # ---------------------------------------------------------------- R6 the one-fact test, computed
    E = EP.build(G, F)
    HALF = len(GD.KEYS) / 2.0
    for (sentence, kind), h in zip(EP.HINTS, E["hints"]):
        ok("R6 hint executed: %s" % kind, h["rescues"] == [EP.ID_OF[k] for k in EP.rescued(G, kind)] and len(h["rescues"]) <= HALF,
           "rescues %s" % (h["rescues"] or "nothing the careful pass lacks"))
    by_kind = {kind: h["rescues"] for (sentence, kind), h in zip(EP.HINTS, E["hints"])}
    ok("R6 the most useful single sentence rescues half the results and no more (a method choice, nothing hidden)",
       by_kind["every"] == ["R3", "R4", "R6"] and max(len(v) for v in by_kind.values()) == 3 and by_kind["levels"] == ["R3", "R6"],
       {k: v for k, v in by_kind.items()})

    # ---------------------------------------------------------------- R7 the rivals
    fam = G["rivals"]
    out_of_band = {name: [k for k in GD.KEYS if RS.grade(res, k) != "right"] for name, res in fam.items()}
    out_of_band = {k: v for k, v in out_of_band.items() if v}
    ok("R7 every member of the family lands inside every band", not out_of_band and len(fam) == 49,
       out_of_band or "%d analyses, each run end to end" % len(fam))
    ok("R7 every member of the family names B", {res["call"]["pick"] for res in fam.values()} == {"B"} and
       min(res["call"]["margin"] for res in fam.values()) >= 0.008 and
       min(res["call"]["margin"] for name, res in fam.items() if RS.central(name)) >= 0.025,
       "by %.4f at the least, %.4f to %.4f on the golden's continuation" % (
           min(res["call"]["margin"] for res in fam.values()),
           min(res["call"]["margin"] for name, res in fam.items() if RS.central(name)),
           max(res["call"]["margin"] for name, res in fam.items() if RS.central(name))))
    def room(fn, band):
        vals = [fn(res) for res in fam.values()]
        return min(min(vals) - band[0], band[1] - max(vals))
    rooms = {"trial": room(lambda r_: r_["trial"]["exp128k_map384k"], B["trial"]["exp128k_map384k"]),
             "contractor": room(lambda r_: r_["costs"]["ctr_per10"], B["costs"]["ctr_per10"]) * 10,
             "map transfer": room(lambda r_: r_["costs"]["map_per10"], B["costs"]["map_per10"]) * 10,
             "level": room(lambda r_: r_["level"], B["level"]),
             "range half": room(lambda r_: RS.half_width(r_["range"]), B["range"]["half"])}
    rooms.update({k: room(lambda r_, k=k: r_["expected"][k], B["expected"][k]) for k in "ABCD"})
    ok("R7 the family sits clear of every band edge", min(rooms.values()) >= 0.0015, {k: round(v, 4) for k, v in rooms.items()})
    last_c = [res["expected"]["C"] for name, res in fam.items() if name.endswith("the last gain carried on undiminished")]
    none_c = [res["expected"]["C"] for name, res in fam.items() if name.endswith("no gain past the largest runs")]
    ok("R7 the band on C is the two bounds on what more examples return", B["expected"]["C"][0] < min(last_c) and max(none_c) < B["expected"]["C"][1] and
       min(last_c) - B["expected"]["C"][0] < 0.004 and B["expected"]["C"][1] - max(none_c) < 0.004,
       "last gain carried on %.4f to %.4f, no gain %.4f to %.4f" % (min(last_c), max(last_c), min(none_c), max(none_c)))
    al = G["also"]
    fl, qd = G["ls_floor"], fam[RS.QUADRATIC]
    ok("R7 a least-squares floor through the levels lands at the last-gain bound and names B", fl["call"]["pick"] == "B" and
       abs(fl["expected"]["C"] - G["bound_last"]["expected"]["C"]) <= 0.005 and abs(fl["expected"]["D"] - G["bound_last"]["expected"]["D"]) <= 0.005,
       "C %.4f against %.4f, D %.4f against %.4f, names %s" % (fl["expected"]["C"], G["bound_last"]["expected"]["C"], fl["expected"]["D"],
                                                              G["bound_last"]["expected"]["D"], fl["call"]["pick"]))
    held = {"the golden": g["heldback"], "least-squares floor": fl["heldback"], "quadratic": qd["heldback"],
            "straight line": al["the straight line through the levels"]["heldback"], "one curve through every run": c["heldback"]}
    ok("R7 the runs held back separate the level-based forecasts from the single curve and the straight line",
       max(held["the golden"], held["least-squares floor"], G["hint_every"]["heldback"]) <= 0.017 and held["one curve through every run"] >= 0.025 and
       held["straight line"] >= 0.035, {k: round(v, 4) for k, v in held.items()})
    ok("R7 the quadratic through the levels lands between the two bounds", RS.cells(qd, "expected") == [True] * 4 and qd["call"]["pick"] == "B",
       "C %.4f, D %.4f, names %s" % (qd["expected"]["C"], qd["expected"]["D"], qd["call"]["pick"]))
    nm = al["routes read against the ladder as it ran"]
    ok("R7 read against the ladder as it ran, contractor labels come out better than expert labels", nm["costs"]["ctr_per10"] < 0 and
       RS.grade(nm, "costs") == "missed" and RS.grade(nm, "level") != "right",
       "contractor %.4f, map transfer %.4f, level %.4f" % (nm["costs"]["ctr_per10"], nm["costs"]["map_per10"], nm["level"]))
    raw = al["expert items read without the benchmark calibration"]
    ok("R7 expert items read raw sit below the benchmark on the scored runs", G["cal"]["a"] + (G["cal"]["b"] - 1) * 0.68 > 0.008 and
       RS.grade(raw, "trial") != "right", "offset %.4f" % (G["cal"]["a"] + (G["cal"]["b"] - 1) * 0.68))

    opt = g["_lr_opt"]
    grid = {}
    for r_ in yr:
        if r_["nA"] == 32000 and r_["nB"] + r_["nC"] == 0:
            grid.setdefault(r_["width"], {}).setdefault(r_["lr"], []).append(r_["y"])
    argmin = {w: min(v, key=lambda lr: np.mean(v[lr])) for w, v in grid.items()}

    def carry(best, widths):
        sl, ic = np.polyfit(np.log2(widths), np.log10([best[w] for w in widths]), 1)
        return float(10 ** (ic + sl * 10))
    rates = {"curve through the cells round each best, four widths": g["rate"], "the same, widest three": carry(opt, [128, 256, 512]),
           "lowest cell of each grid, four widths": carry(argmin, [64, 128, 256, 512]),
           "lowest cell of each grid, widest three": carry(argmin, [128, 256, 512]), "half the 512 rate": S.TUNED_LR[512] / 2.0}
    ok("R7 every way of carrying the best rate one doubling lands inside the rate's band", all(B["rate"][0] <= v <= B["rate"][1] for v in rates.values()),
       {k: "%.2e" % v for k, v in rates.items()})
    ok("R7 the rate of the job that ran out of walltime sits outside the rate's band", S.TUNED_LR[512] > B["rate"][1], "%.1e" % S.TUNED_LR[512])

    # ---------------------------------------------------------------- the semantic forks
    scored = [r for r in yr if r["bench"] is not None]
    d = [r["dev"] - r["bench"] for r in scored]
    ok("SF1 the benchmark's score is not the logged loss", min(d) > 0.05, "logged minus benchmark %.3f to %.3f on %d scored runs" % (min(d), max(d), len(d)))
    ok("SF2 trained once is filed", "It is trained once, with the recipe the proposal states" in notes, "notes, section 1")
    ok("SF3 the range is for the single result", "fall\n  in four times out of five" in notes or "fall in four times out of five" in notes.replace("\n  ", " "), "notes, section 1")
    lastlog = m.groupby("run_id")["step"].max()
    unf = runs[~((runs["status"] == "FINISHED") & (runs["run_id"].map(lastlog) == runs["max_steps"]))]
    ck = pd.read_csv(_read(target, "ckpt"))
    has_final = set(p.split("/")[-2] for p in ck["path"] if p.endswith("ckpt_final.pt"))
    ok("SF4 finished means FINISHED at the last step of the schedule", len(runs) - len(unf) == facts["complete"] == 129 and
       set(unf["status"]) <= {"KILLED", "FAILED"} and not (set(unf["run_id"]) & has_final),
       "%d unfinished, none with a final checkpoint" % len(unf))
    ok("SF5 final checkpoints the benchmark scored", (bfacts["rows"], bfacts["scored"], bfacts["final"], bfacts["part_way"], bfacts["duplicates"]) == (32, 30, 28, 2, 2), bfacts)
    reg = pd.read_csv(_read(target, "shards"))
    train = reg[(reg["use"] == "train")]
    ok("SF6 examples by the register equal shards times 4,000", (train["points"] == P.SHARD).all() and train["shard_id"].is_unique and
       int((reg["use"] == "superseded").sum()) == 1 and all(r["nA"] % P.SHARD == 0 for r in rows), "one superseded receipt, counted once")
    prompt = open(prompt_path, encoding="utf-8").read() if prompt_path and os.path.exists(prompt_path) else ""
    ok("SF7 the swap's direction is in the asking sentence", (not prompt) or "moved from expert to contractor labels" in prompt, "prompt")
    ok("SF8 the size, width and rate of the level are in the asking sentence", (not prompt) or "512,000 expert labels would give at width 128 and learning rate 0.002" in prompt, "prompt")
    trial_runs = [r_["y"] for r_ in yr if r_["stage"] == "vend" and r_["width"] == 128 and
                  (r_["nA"], r_["nB"], r_["nC"]) == RS.BIG_CELLS["exp128k_map384k"]]
    tb = B["trial"]["exp128k_map384k"]
    ok("SF9 the trial is its three runs, and each of them alone stays inside the band", len(trial_runs) == 3 and
       all(tb[0] <= v <= tb[1] for v in trial_runs), ["%.4f" % v for v in trial_runs])
    yml = open(_read(target, "defaults"), encoding="utf-8").read()
    ok("SF10 one learning rate on a cosine schedule", len(re.findall(r"^\s+lr:", yml, re.M)) == 1 and "schedule: cosine" in yml and
       "still needs a\n  learning rate" in notes, "defaults file and notes")
    pb = G["carried"]
    ok("SF11 the carried loss for every run names B as well and stays inside every band", pb["call"]["pick"] == "B" and pb["call"]["margin"] > 0.02 and
       right(pb) == GD.KEYS and pb["expected"]["A"] - g["expected"]["A"] > 0.02, "B by %.4f, A %.4f" % (pb["call"]["margin"], pb["expected"]["A"]))
    ok("SF12 the final step of every finished run is logged once", last.groupby("run_id").size().max() == 1, "later row or earlier row, the same figure")
    ok("SF13 the two vocabularies are one scalar", set(runs["logger"]) == {"sedinet-log 1", "sedinet-log 2"} and
       "split: dev_split_items.csv" in yml and runs.groupby("logger")["code_rev"].nunique().min() >= 1, sorted(set(runs["logger"])))
    ok("SF14 the named configuration is the lowest expected loss", "Teams are ranked on the expected value" in notes and "All fit the slot" in notes,
       "notes, sections 1 and 2")
    ok("SF15 rounding is asked once, at the close", (not prompt) or prompt.strip().endswith("Losses to three decimals, the per-tenth costs to four."), "prompt")
    routes = pd.read_csv(_read(target, "routes"))
    ok("SF16 expert labels are the register's EXP route", list(routes["label_route"]) == ["EXP", "CTR", "MAP"] and facts["expert_items"] == P.DEV_MIX["A"],
       "%d expert development items" % facts["expert_items"])

    # ---------------------------------------------------------------- bands: the golden clear of each edge
    def clear(v, b):
        return min(v - b[0], b[1] - v) / (b[1] - b[0])
    edges = {"trial": clear(g["trial"]["exp128k_map384k"], B["trial"]["exp128k_map384k"]), "map transfer": clear(g["costs"]["map_per10"], B["costs"]["map_per10"]),
             "contractor": clear(g["costs"]["ctr_per10"], B["costs"]["ctr_per10"]), "level": clear(g["level"], B["level"]),
             "rate": clear(g["rate"], B["rate"]), "range low": clear(g["range"]["low"], B["range"]["low"]), "range high": clear(g["range"]["high"], B["range"]["high"]),
             "range half": clear(RS.half_width(g["range"]), B["range"]["half"])}
    edges.update({"expected %s" % k: clear(g["expected"][k], B["expected"][k]) for k in "ABCD"})
    ok("the golden sits clear of every band edge", min(edges.values()) >= 0.15, {k: round(v, 2) for k, v in edges.items()})
    ru = G["rm_unweighted"]
    ok("an unweighted fit of the routes' costs moves them by 0.0005 a tenth or less, inside the bands",
       abs(ru["kC"] - G["rm"]["kC"]) / 10.0 <= 0.0005 and abs(ru["kB"] - G["rm"]["kB"]) / 10.0 <= 0.0005 and
       B["costs"]["map_per10"][0] <= ru["kC"] / 10.0 <= B["costs"]["map_per10"][1] and B["costs"]["ctr_per10"][0] <= ru["kB"] / 10.0 <= B["costs"]["ctr_per10"][1],
       "contractor %.4f against %.4f, map transfer %.4f against %.4f" % (ru["kB"] / 10.0, G["rm"]["kB"] / 10.0, ru["kC"] / 10.0, G["rm"]["kC"] / 10.0))
    st = G["same_total"]
    ok("pair by pair at 128,000 examples the map-transfer cost is the same at half and at three quarters of the set",
       abs(st[(64000, 0, 64000)] - st[(32000, 0, 96000)]) <= 0.0005 and all(B["costs"]["map_per10"][0] <= st[k] <= B["costs"]["map_per10"][1]
                                                                             for k in ((64000, 0, 64000), (32000, 0, 96000))),
       {"%dk+%dk" % ((k[0]) // 1000, (k[1] + k[2]) // 1000): round(v, 4) for k, v in st.items()})
    ok("the benchmark digest joins one store file each", joined["path"].notna().all() and joined["file_sha1_12"].nunique() == 30, "30 digests, 32 rows")

    # ---------------------------------------------------------------- input gates
    cats = {"spreadsheet": [f for f in files if f.endswith((".csv", ".xlsx"))], "text": [f for f in files if f.endswith((".md", ".yaml"))],
            "code": [f for f in files if f.endswith(".sh")]}
    ok("gate: ten or more usable files in two or more categories", len(files) >= 10 and sum(1 for v in cats.values() if v) >= 2 and
       all(os.path.getsize(os.path.join(target, f)) > 0 for f in files), "%d files, %s" % (len(files), {k: len(v) for k, v in cats.items()}))
    ok("gate: one CSV of 20,000 rows or more", len(m) >= 20000, "%d logged scalar rows" % len(m))
    ok("gate: a second large CSV of ten printed pages or more", len(ck) >= 500, "%d store rows" % len(ck))
    dnames = [pack.FILES[k] for k in pack.DISTRACTORS]
    src = inspect.getsource(load)
    ok("gate: two unused files that look relevant, read by nothing", all(n in files for n in dnames) and '"probe"' not in src and '"counts"' not in src,
       dnames)
    ok("gate: no file describes the pack", not [f for f in files if re.search(r"readme|dictionary|manifest|codebook|schema|field", f, re.I)], "none")
    ok("gate: no author noun in a file name", not [f for f in files if re.search(r"trap|golden|answer|clean_|_v\d|decoy|distract", f, re.I)], "none")

    # ---------------------------------------------------------------- realism sweep
    ok("realism: run ids are not a sequence", runs["run_id"].is_unique and sorted(runs["run_id"]) != list(runs["run_id"]), "134 hashed ids")
    jobs = pd.read_csv(_read(target, "jobs"))
    steps = np.diff(sorted(set(jobs["JobID"])))
    ok("realism: scheduler job ids rise unevenly", len(set(steps)) > 20, "%d distinct gaps" % len(set(steps)))
    sid = np.diff([int(s.split("-")[1]) for s in sub["submission_id"]])
    ok("realism: benchmark submission ids rise unevenly", len(set(sid)) > 10, "%d distinct gaps" % len(set(sid)))
    ok("realism: nothing is dated after its export", pd.to_datetime(runs["end_time"]).max() < pd.Timestamp("2026-11-02", tz="UTC") and
       m["timestamp_ms"].max() < pd.Timestamp("2026-11-02", tz="UTC").value // 10 ** 6 and
       pd.to_datetime(sub["received_utc"]).max() < pd.Timestamp("2026-10-24", tz="UTC"), "runs end before 2 November, uploads before 24 October")
    sd = [np.std([r["y"] for r in v]) for v in _cells(yr).values() if len(v) > 1]
    ok("realism: seeds differ", min(sd) > 0 and len(set(round(float(x), 6) for x in sd)) >= len(sd) - 3, "%d cells, spread %.4f to %.4f" % (len(sd), min(sd), max(sd)))
    ok("realism: no em dash in any text file", not any(chr(0x2014) in open(os.path.join(target, f), encoding="utf-8").read()
                                                       for f in files if f.endswith((".md", ".yaml", ".sh", ".csv")) and os.path.getsize(os.path.join(target, f)) < 2e6), "none")

    # ---------------------------------------------------------------- the truth runs (author side)
    T, clean = truth()
    if T is None:
        ok("truth runs on disk", False, "run `python3 run_sweeps.py truth` before the build")
    else:
        tv = {"A": T[("A", 3.5e-4)], "B": T[("B", 5e-4)], "C": T[("C", 1e-3)], "D": T[("D", 1e-3)]}
        ok("truth: every configuration really scores inside its band", all(B["expected"][k][0] <= tv[k] <= B["expected"][k][1] for k in tv),
           {k: round(v, 4) for k, v in tv.items()})
        ok("truth: B is really the lowest, by 0.02 or more", min(tv, key=tv.get) == "B" and sorted(tv.values())[1] - tv["B"] >= 0.02,
           "by %.4f" % (sorted(tv.values())[1] - tv["B"]))
        ok("truth: B's real score falls inside the stated range", g["range"]["low"] <= tv["B"] <= g["range"]["high"],
           "%.4f in %.4f to %.4f" % (tv["B"], g["range"]["low"], g["range"]["high"]))
        ok("truth: seed spread alone would have missed B's real score", not (sr["low"] <= tv["B"] <= sr["high"]), "%.4f outside %.4f to %.4f" % (tv["B"], sr["low"], sr["high"]))
        ok("truth: the careful pass's C is 0.03 or more below what C really scores", tv["C"] - c["expected"]["C"] >= 0.03, "%.4f against %.4f" % (c["expected"]["C"], tv["C"]))
        ok("truth: 512,000 clean labels really give the level's band", B["level"][0] <= clean["clean-w128-512k"] <= B["level"][1], "%.4f" % clean["clean-w128-512k"])
        ta = {k[1]: v for k, v in T.items() if k[0] == "A"}
        inside = [lr for lr in ta if B["rate"][0] <= lr <= B["rate"][1]]
        ok("truth: the learning rate's band holds the best of the rates run, and the golden's rate is within 0.002 of it",
           min(ta, key=ta.get) in inside and ta[2.74e-4] - min(ta.values()) <= 0.002 and ta[5e-4] - min(ta.values()) >= 0.006,
           {"%g" % k: round(v, 4) for k, v in sorted(ta.items())})
        ok("truth: A at the golden's rate really scores what the forecast says", abs(ta[2.74e-4] - g["expected"]["A"]) <= 0.004,
           "%.4f against %.4f" % (ta[2.74e-4], g["expected"]["A"]))
        ok("truth: A stays inside its band at every rate run, so the rate it is forecast at opens no fork",
           all(B["expected"]["A"][0] <= v <= B["expected"]["A"][1] for v in ta.values()), {"%g" % k: round(v, 4) for k, v in sorted(ta.items())})
        ok("truth: C and D really fall between the two bounds on what more examples return",
           all(G["bound_last"]["expected"][k] - 0.003 <= tv[k] <= G["bound_none"]["expected"][k] + 0.003 for k in "CD"),
           {k: (round(G["bound_last"]["expected"][k], 4), round(tv[k], 4), round(G["bound_none"]["expected"][k], 4)) for k in "CD"})
        tc = true_costs(clean)
        ok("truth: each route's real cost per tenth sits inside its band", tc is not None and
           all(B["costs"]["ctr_per10"][0] <= v <= B["costs"]["ctr_per10"][1] for v in tc["contractor"].values()) and
           all(B["costs"]["map_per10"][0] <= v <= B["costs"]["map_per10"][1] for v in tc["map"].values()),
           tc and {k: {a: round(b, 4) for a, b in v.items()} for k, v in tc.items()})
    return G, F, E


def _cells(yr):
    out = {}
    for r in yr:
        out.setdefault((r["stage"], r["width"], r["lr"], r["nA"], r["nB"], r["nC"]), []).append(r)
    return out


if __name__ == "__main__":
    import sys
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    run(os.path.join(task, "target"), here, os.path.join(task, "prompt.txt"))
    bad = [r for r in RESULTS if not r[1]]
    for name, good, d in RESULTS:
        if not good:
            print("FAIL  %s  %s" % (name, d))
    print("checks: %d of %d" % (len(RESULTS) - len(bad), len(RESULTS)))
    sys.exit(1 if bad else 0)
