"""Independent verifier. Reads only the shipped bundle (target/ and golden/) and generator/figures.json, imports no
module of the generator, and recomputes every graded figure on its own code path.

    python3 verify.py [task_dir]      exit 0 when every check holds

It also reads back every format the pack ships (csv, xlsx, md, yaml, sh) and both golden files.
"""
import json
import math
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []


def check(name, cond, detail=""):
    OUT.append((name, bool(cond), str(detail)))


def near(a, b, tol):
    return a is not None and b is not None and abs(a - b) <= tol


def read_pack(t):
    runs = pd.read_csv(os.path.join(t, "tracking_runs_export_2026-11-04.csv"), dtype={"shards_exp": str, "shards_ctr": str, "shards_map": str})
    met = pd.read_csv(os.path.join(t, "tracking_metrics_export_2026-11-04.csv"))
    items = pd.read_csv(os.path.join(t, "dev_item_loss_final_checkpoints.csv"))
    split = pd.read_csv(os.path.join(t, "dev_split_items.csv"))
    reg = pd.read_csv(os.path.join(t, "label_shard_register.csv"))
    sub = pd.read_csv(os.path.join(t, "nssmp_benchmark_submissions_mml.csv"), dtype={"file_sha1_12": str})
    store = pd.read_csv(os.path.join(t, "checkpoint_store_listing_2026-11-04.csv"))
    return runs, met, items, split, reg, sub, store


def assemble(t):
    runs, met, items, split, reg, sub, store = read_pack(t)
    # finished runs
    last = met.groupby("run_id")["step"].max()
    runs["last_step"] = runs["run_id"].map(last).fillna(0).astype(int)
    runs["done"] = (runs["status"] == "FINISHED") & (runs["last_step"] == runs["max_steps"])
    # examples by route, from the register (the superseded receipt left out)
    live = reg[reg["use"] != "superseded"].set_index("shard_id")["points"]

    def pts(spec, tag):
        if not isinstance(spec, str) or not spec:
            return 0
        a, b = spec.split("-")
        return int(sum(live["%s-%04d" % (tag, k)] for k in range(int(a), int(b) + 1)))
    runs["nE"] = [pts(s, "EXP") for s in runs["shards_exp"]]
    runs["nK"] = [pts(s, "CTR") for s in runs["shards_ctr"]]
    runs["nM"] = [pts(s, "MAP") for s in runs["shards_map"]]
    runs["total"] = runs["nE"] + runs["nK"] + runs["nM"]
    runs["stage"] = runs["run_name"].str.split("-").str[0]
    # benchmark scores of final checkpoints
    ck = store[store["path"].str.endswith(".pt")].copy()
    ck["d12"] = ck["sha1"].str[:12]
    ck["rid"] = ck["path"].str.split("/").str[-2]
    ck["is_final"] = ck["path"].str.endswith("ckpt_final.pt")
    j = sub.merge(ck[["d12", "rid", "is_final"]], left_on="file_sha1_12", right_on="d12", how="left")
    scored = j[j["status"] == "SCORED"]
    fin = scored[scored["is_final"]]
    bench = dict(zip(fin["rid"], fin["log_loss"].astype(float)))
    counts = dict(records=len(runs), finished=int(runs["done"].sum()), rows=len(sub), scored=len(scored), final=len(fin),
                  part_way=int((~scored["is_final"]).sum()), repeats=int((j["status"] != "SCORED").sum()))
    # expert-item loss of each final checkpoint
    route = split["shard_id"].map(reg.drop_duplicates("shard_id").set_index("shard_id")["label_route"])
    exp_rows = (route == "EXP").values
    counts["items"] = len(split); counts["expert_items"] = int(exp_rows.sum())
    cols = [c for c in items.columns if c != "item"]
    dev_e = items.loc[exp_rows, cols].mean(axis=0)
    # logged development loss at the final step (either vocabulary; the later row of a repeated step)
    d = met[met["key"].isin(["dev/loss", "val_loss"])].sort_values("timestamp_ms").groupby(["run_id", "step"]).tail(1)
    d = d.set_index(["run_id", "step"])["value"]
    R = runs[runs["done"] & runs["run_id"].isin(cols)].copy()
    R["devE"] = R["run_id"].map(dev_e)
    R["dev"] = [float(d.get((r, s), np.nan)) for r, s in zip(R["run_id"], R["max_steps"])]
    R["bench"] = R["run_id"].map(bench)
    counts["with_items"] = len(R)
    return R, counts


def yardstick(R):
    c = R[R["bench"].notna()]
    b, a = np.polyfit(c["devE"], c["bench"], 1)
    res = c["bench"] - (a + b * c["devE"])
    sd = float(np.sqrt((res ** 2).sum() / (len(c) - 2)))
    R = R.copy()
    R["y"] = np.where(R["bench"].notna(), R["bench"], a + b * R["devE"])
    return R, float(a), float(b), sd, len(c)


def cell(R, **kw):
    m = np.ones(len(R), bool)
    for k, v in kw.items():
        col = R[k].values
        m &= np.isclose(col.astype(float), float(v), rtol=1e-9) if isinstance(v, float) else (col == v)
    return R[m]


def expert(R, width, n, lr, col="y"):
    q = cell(R, model_width=width, nE=n, nK=0, nM=0, lr=float(lr))
    return float(q[col].mean()) if len(q) else None


TABLED = {64: 2e-3, 128: 1e-3, 256: 5e-4}
TUNED = {64: 8e-3, 128: 2e-3, 256: 1e-3, 512: 5e-4}
LADDER = (8000, 16000, 32000, 64000, 128000)


def expert_curve(R, width=128):
    cost = {n: expert(R, width, n, TABLED[width]) - expert(R, width, n, TUNED[width]) for n in (32000, 128000)}
    out = {}
    for n in LADDER:
        t = min(1.0, max(0.0, (math.log2(n) - math.log2(32000)) / 2.0))
        out[n] = expert(R, width, n, TABLED[width]) - (cost[32000] + t * (cost[128000] - cost[32000]))
    for n in (32000, 128000):
        out[n] = expert(R, width, n, TUNED[width])
    return out, cost


def trials(R, width):
    v = R[(R["stage"] == "vend") & (R["model_width"] == width)]
    g = v.groupby(["nE", "nK", "nM"])["y"].agg(["mean", "size"]).reset_index()
    return [(int(a), int(b), int(c), float(m), int(n)) for a, b, c, m, n in g.itertuples(index=False)]


def routes(R, hold_above=None):
    """Each width-128 trial's loss = a level of its own at its total + a cost per unit share of each route. The
    expert-label runs at the trials' own rate stand at their total as a mix with no vendor labels, so each cost
    rests on the contrasts between mixes at one total, width and rate; totals no trial ran keep the ladder's level."""
    f, cost = expert_curve(R)
    cells = [c for c in trials(R, 128) if hold_above is None or sum(c[:3]) <= hold_above]
    free = sorted({sum(c[:3]) for c in cells})
    for u in free:
        q = cell(R, model_width=128, nE=u, nK=0, nM=0, lr=float(TUNED[128]))
        if len(q):
            cells.append((u, 0, 0, float(q["y"].mean()), len(q)))
    X, y, w = [], [], []
    for a, b, c, m, n in cells:
        t = a + b + c
        X.append([b / t, c / t] + [1.0 if t == u else 0.0 for u in free])
        y.append(m); w.append(math.sqrt(n))
    X, y, w = np.array(X), np.array(y), np.array(w)
    sol = np.linalg.lstsq(X * w[:, None], y * w, rcond=None)[0]
    levels = dict(f)
    for u, v in zip(free, sol[2:]):
        levels[u] = float(v)
    return float(sol[0]), float(sol[1]), levels, cost


def floor_curve(levels):
    xs = sorted(levels)[-3:]
    ys = [levels[x] for x in xs]
    s1 = (ys[2] - ys[1]) / math.log2(xs[2] / xs[1]); s0 = (ys[1] - ys[0]) / math.log2(xs[1] / xs[0])
    ratio = min(0.97, max(0.2, s1 / s0))
    grid = sorted(levels)

    def f(n):
        k = math.log2(n / xs[2])
        if k <= 0:
            return float(np.interp(math.log2(n), [math.log2(g) for g in grid], [levels[g] for g in grid]))
        return ys[2] + s1 * math.sqrt(ratio) * (ratio ** k - 1.0) / math.log(ratio)
    return f, ratio


def width_levels(R, kB, kC, levels, hold_above=None):
    """What width 256 gains on width 128 at each total, and width 512 on 256 at the expert pool."""
    lv256 = {n: expert(R, 256, n, TUNED[256]) for n in (32000, 128000)}
    per = {}
    for a, b, c, m, n in trials(R, 256):
        t = a + b + c
        if hold_above is not None and t > hold_above:
            continue
        per.setdefault(t, []).append((m - kB * b / t - kC * c / t, n))
    for t, v in per.items():
        lv256[t] = sum(x * n for x, n in v) / sum(n for _, n in v)
    g256 = {t: levels[t] - lv256[t] for t in lv256 if t in levels}
    step512 = expert(R, 256, 128000, TUNED[256]) - expert(R, 512, 128000, TUNED[512])
    return g256, step512


def level_fn(f128, g256, step512):
    big = float(np.mean([v for t, v in g256.items() if t >= 128000]))

    def level(width, n):
        v = f128(n)
        if width >= 256:
            v -= big if n >= 128000 else float(np.interp(math.log2(n), [math.log2(t) for t in sorted(g256)], [g256[t] for t in sorted(g256)]))
        if width >= 512:
            v -= step512
        if width >= 1024:
            v -= step512
        return v
    return level


def lr_best(R, width):
    q = R[(R["model_width"] == width) & (R["nE"] == 32000) & (R["nK"] == 0) & (R["nM"] == 0)]
    g = q.groupby("lr")["y"].mean().sort_index()
    x = np.log10(g.index.values.astype(float)); y = g.values
    i = int(np.argmin(y)); lo, hi = max(0, i - 1), min(len(x), i + 2)
    if hi - lo < 3:
        lo, hi = (0, 3) if i == 0 else (len(x) - 3, len(x))
    c2, c1, c0 = np.polyfit(x[lo:hi], y[lo:hi], 2)
    if c2 <= 0:
        return float(10 ** x[i])
    return float(10 ** min(max(-c1 / (2 * c2), x[lo:hi].min()), x[lo:hi].max()))


def read_shortlist(t):
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(t, "compute_call_2027_shortlist.xlsx"), data_only=True)["Shortlist"]
    rows = list(ws.iter_rows(values_only=True))
    h = list(rows[0])
    out = {}
    for r in rows[1:]:
        if r[0]:
            out[r[0]] = dict(width=int(r[h.index("Width")]), nE=int(r[h.index("Expert points")]),
                             nK=int(r[h.index("Contractor points")]), nM=int(r[h.index("Map-transfer points")]),
                             lr=r[h.index("Learning rate")])
    return out


def main(task_dir):
    t = os.path.join(task_dir, "target")
    gdir = os.path.join(task_dir, "golden")
    F = json.load(open(os.path.join(task_dir, "generator", "figures.json")))
    R, n = assemble(t)
    check("run records, finished, with item scores", (n["records"], n["finished"], n["with_items"]) ==
          (F["run_records"], F["runs_finished"], F["runs_with_item_scores"]), n)
    check("benchmark rows, scored, final, part-way, repeats", (n["rows"], n["scored"], n["final"], n["part_way"], n["repeats"]) ==
          (F["bench_rows"], F["bench_scored"], F["bench_final"], F["bench_part_way"], F["bench_repeats"]), n)
    check("the development split: items and expert items", (n["items"], n["expert_items"]) == (F["dev_items"], F["dev_expert_items"]), n)
    R, a, b, sd, nc = yardstick(R)
    check("the yardstick's line and residual", near(a, F["cal_intercept"], 6e-5) and near(b, F["cal_slope"], 6e-4) and
          near(sd, F["cal_sd"], 6e-5) and nc == F["cal_n"], "%.4f + %.4f x, residual %.4f, n %d" % (a, b, sd, nc))
    trial = float(cell(R[R["stage"] == "vend"], model_width=128, nE=128000, nK=0, nM=384000)["y"].mean())
    check("the map trial on the benchmark's scale", near(trial, F["trial_map384"], 6e-4), "%.4f" % trial)
    kB, kC, levels, cost = routes(R)
    check("the routes' costs per tenth", near(kB / 10, F["cost_ctr"], 6e-5) and near(kC / 10, F["cost_map"], 6e-5),
          "contractor %.4f, map transfer %.4f" % (kB / 10, kC / 10))
    check("the level at 512,000 expert labels", near(levels[512000], F["level_512k"], 6e-4) and near(levels[256000], F["level_256k"], 6e-4),
          "256,000: %.4f; 512,000: %.4f" % (levels[256000], levels[512000]))
    check("the tabled rate's cost at width 128", near(float(np.mean(list(cost.values()))), F["hurried"]["lr_cost_128"], 6e-4), cost)
    f128, ratio = floor_curve(levels)
    check("the curve's ratio", near(ratio, F["curve_ratio"], 6e-3), "%.3f" % ratio)
    g256, step512 = width_levels(R, kB, kC, levels)
    level = level_fn(f128, g256, step512)
    SL = read_shortlist(t)
    exp = {k: level(o["width"], o["nE"] + o["nK"] + o["nM"]) + kB * o["nK"] / (o["nE"] + o["nK"] + o["nM"]) +
           kC * o["nM"] / (o["nE"] + o["nK"] + o["nM"]) for k, o in SL.items()}
    check("each configuration's expected loss", all(near(exp[k], F["expected"][k], 6e-4) for k in exp),
          {k: round(v, 4) for k, v in exp.items()})
    order = sorted(exp, key=exp.get)
    check("the configuration to name and its lead", order[0] == F["call"] and near(exp[order[1]] - exp[order[0]], F["margin"], 6e-4),
          "%s by %.4f over %s" % (order[0], exp[order[1]] - exp[order[0]], order[1]))
    # the check on the runs held back
    kB2, kC2, lev2, _ = routes(R, hold_above=256000)
    f2, _ = floor_curve(lev2)
    g2, s2 = width_levels(R, kB2, kC2, lev2, hold_above=256000)
    lvl2 = level_fn(f2, g2, s2)
    held = R[(R["stage"] == "vend") & (R["total"] > 256000)]
    gaps = []
    for (w, e, k, m), grp in held.groupby(["model_width", "nE", "nK", "nM"]):
        tot = e + k + m
        gaps.append(lvl2(int(w), int(tot)) + kB2 * k / tot + kC2 * m / tot - float(grp["y"].mean()))
    gap = float(np.mean(np.abs(gaps)))
    check("the gap on the configurations held back", len(gaps) == 3 and near(gap, F["gap"], 6e-5), "%.4f over %d configurations" % (gap, len(gaps)))
    # the learning rate
    best = {w: lr_best(R, w) for w in (64, 128, 256, 512)}
    sl, ic = np.polyfit(np.log2(list(best)), np.log10(list(best.values())), 1)
    lr1024 = float(10 ** (ic + sl * 10))
    check("the learning rate for 1,024 wide", near(lr1024, F["lr_1024"], 6e-6), "%.2e (power %.2f)" % (lr1024, sl / math.log10(2)))
    # the range
    grp = R.groupby(["stage", "model_width", "lr", "nE", "nK", "nM"])["y"]
    ss = float(((R["y"] - grp.transform("mean")) ** 2).sum()); dof = int((grp.transform("size") > 1).sum() - (grp.size() > 1).sum())
    s_run = math.sqrt(ss / dof); s_fore = math.sqrt(float(np.mean(np.square(gaps))))
    tot_sd = math.sqrt(s_run ** 2 + s_fore ** 2 + sd ** 2)
    lo, hi = exp[order[0]] - 1.2816 * tot_sd, exp[order[0]] + 1.2816 * tot_sd
    check("the range and its three parts", near(lo, F["range_low"], 6e-4) and near(hi, F["range_high"], 6e-4) and
          near(s_run, F["range_parts"]["run"], 6e-5) and near(s_fore, F["range_parts"]["forecast"], 6e-5),
          "%.4f to %.4f (run %.4f, forecast %.4f, yardstick %.4f)" % (lo, hi, s_run, s_fore, sd))
    # the shallow read, for the step that rejects it
    c = R[R["bench"].notna()]
    bq, aq = np.polyfit(c["dev"], c["bench"], 1)
    lg = float((aq + bq * cell(R[R["stage"] == "vend"], model_width=128, nE=128000, nK=0, nM=384000)["dev"]).mean())
    check("the logged loss carried to the benchmark puts the map trial far lower", near(lg, F["hurried"]["quick_trial"], 6e-4), "%.4f" % lg)

    # every format the pack ships, read back
    notes = open(os.path.join(t, "mml_group_meeting_2026-11-05.md"), encoding="utf-8").read()
    flat = re.sub(r"\s+", " ", notes)
    check("notes: the outcome, one run, the range and the ranking rule are filed",
          all(s in flat for s in ("scores the final checkpoint on the verified benchmark: mean log loss over the 20,000 grab-sample points",
                                  "It is trained once, with the recipe the proposal states", "fall in four times out of five",
                                  "Teams are ranked on the expected value")), "four sentences found")
    check("notes: the shortlist table agrees with the workbook", all(("| %s | %d |" % (k, o["width"])) in notes for k, o in SL.items()), sorted(SL))
    yml = open(os.path.join(t, "sedinet_train_defaults.yaml"), encoding="utf-8").read()
    check("defaults: recipe as the notes state it", "batch_size: 128" in yml and "epochs: 12" in yml and "schedule: cosine" in yml, "batch, epochs, schedule")
    sh = open(os.path.join(t, "launch_vendor_trials.sh"), encoding="utf-8").read()
    launched = len(re.findall(r"^submit vend-", sh, re.M))
    check("launch script: one line for each width-128 vendor trial", launched == int(((R["stage"] == "vend") & (R["model_width"] == 128)).sum()), "%d submit lines" % launched)
    routes_csv = pd.read_csv(os.path.join(t, "label_routes.csv"))
    check("routes file: three routes", list(routes_csv["label_route"]) == ["EXP", "CTR", "MAP"], list(routes_csv["name"]))
    jobs = pd.read_csv(os.path.join(t, "slurm_accounting_mml-sedi_2026-09-21_2026-11-01.csv"))
    check("scheduler rows cover every run's attempts", jobs["JobName"].isin(pd.read_csv(os.path.join(t, "tracking_runs_export_2026-11-04.csv"))["run_name"]).sum() >= n["records"], len(jobs))
    check("ten or more files, a CSV past 20,000 rows", len(os.listdir(t)) >= 10 and sum(1 for _ in open(os.path.join(t, "tracking_metrics_export_2026-11-04.csv"))) > 20000, len(os.listdir(t)))

    # the golden files, read back
    import openpyxl
    from docx import Document
    wb = openpyxl.load_workbook(os.path.join(gdir, "scale_up_forecast.xlsx"), data_only=True)
    rk = list(wb["Ranking"].iter_rows(min_row=5, max_row=8, values_only=True))
    got = {r[1]: r[7] for r in rk}
    check("workbook: the ranking sheet carries the four forecasts", [r[1] for r in rk][0] == F["call"] and
          all(near(got[k], exp[k], 5e-4) for k in exp), {k: round(v, 3) for k, v in got.items()})
    check("workbook: the named row carries the range and option A its rate", near(rk[0][8], lo, 5e-4) and near(rk[0][9], hi, 5e-4) and
          near({r[1]: r[6] for r in rk}["A"], F["lr_1024"], 1e-9), "%.3f to %.3f" % (rk[0][8], rk[0][9]))
    un = {r[0]: r[7] for r in wb["Ranking"].iter_rows(min_row=13, max_row=16, values_only=True) if r[0]}
    check("workbook: the three figures underneath the ranking", len(un) == 4 and
          near(un["Benchmark loss matching the width-128 trial on 128,000 expert plus 384,000 map-transfer labels"], trial, 5e-4) and
          near(un["Added to the benchmark loss by each tenth of a training set moved from expert to contractor labels"], kB / 10, 5e-5) and
          near(un["Added by each tenth moved from expert to map-transfer labels"], kC / 10, 5e-5) and
          near(un["Benchmark loss 512,000 expert labels would give at width 128 and learning rate 0.002"], levels[512000], 5e-4),
          {k[:34]: round(v, 4) for k, v in un.items()})
    dv = {r[0]: r[1] for r in wb["Drivers"].iter_rows(min_row=4, values_only=True) if r[0]}
    check("workbook: the drivers sheet", dv["Runs that finished their schedule"] == n["finished"] and dv["Final checkpoints the benchmark scored"] == n["final"]
          and near(dv["Benchmark loss 512,000 expert labels would give at width 128, learning rate 0.002"], levels[512000], 5e-4)
          and near(dv["Mean absolute gap to the pilot configurations above 256,000 examples, forecast built without them"], gap, 5e-5), "counts, level and gap")
    check("workbook: sheets", wb.sheetnames == ["Ranking", "Drivers", "Levels", "Trials", "Held back", "Learning rate", "Routes", "Runs", "Notes"], wb.sheetnames)
    doc = Document(os.path.join(gdir, "proposal_evidence_note.docx"))
    text = " ".join(p.text for p in doc.paragraphs)
    check("note: opens with the call and its figures", text.startswith("Name option %s" % F["call"]) and ("%.3f" % F["expected"][F["call"]]) in text and
          ("%.3f and %.3f" % (F["range_low"], F["range_high"])) in text, text[:110])
    check("note: one chart and one table", len(doc.inline_shapes) == 1 and len(doc.tables) == 1, "%d picture, %d table" % (len(doc.inline_shapes), len(doc.tables)))
    check("the golden folder holds exactly the two requested files", sorted(os.listdir(gdir)) == ["proposal_evidence_note.docx", "scale_up_forecast.xlsx"], sorted(os.listdir(gdir)))
    bad = [o for o in OUT if not o[1]]
    for name, okk, d in OUT:
        print("%s  %s  %s" % ("ok  " if okk else "FAIL", name, d if not okk else str(d)[:90]))
    print("verify: %d of %d" % (len(OUT) - len(bad), len(OUT)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)))
