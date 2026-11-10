"""Write the pack's data files from the pilot's jobs: what the tracking server, the scheduler, the checkpoint store,
the data-preparation scripts and the programme's benchmark server each hold about the five weeks.

Every loss, score and digest written here is read off a real training run (runner.load). The mess is the systems'
own: a tracking server that appends whatever a resumed job logs again, a logger that was renamed between weeks, a
store listing with the dumps that exist, a benchmark server that keeps a short digest and counts a re-upload.
"""
import csv
import datetime as dt
import io
import os

import numpy as np

import infra as I
import params as P
import runner as R
import sweep as S
import world as W

UTC = dt.timezone.utc
FILES = {
    "metrics": "tracking_metrics_export_2026-11-04.csv",
    "runs": "tracking_runs_export_2026-11-04.csv",
    "items": "dev_item_loss_final_checkpoints.csv",
    "devsplit": "dev_split_items.csv",
    "shards": "label_shard_register.csv",
    "routes": "label_routes.csv",
    "classes": "sediment_classes_folk.csv",
    "jobs": "slurm_accounting_mml-sedi_2026-09-21_2026-11-01.csv",
    "ckpt": "checkpoint_store_listing_2026-11-04.csv",
    "bench": "nssmp_benchmark_submissions_mml.csv",
    "notes": "mml_group_meeting_2026-11-05.md",
    "shortlist": "compute_call_2027_shortlist.xlsx",
    "defaults": "sedinet_train_defaults.yaml",
    "launch": "launch_vendor_trials.sh",
    "probe": "gpu_throughput_probe_2026-09.csv",
    "counts": "shard_class_counts.csv",
}
DISTRACTORS = ("probe", "counts")
STORE = "/cluster/projects/mml/sedinet/runs"
TEAM = "MML-TOS"
CODE_REV = {"ladder": "a41c9e2", "lrcheck": "7be03f5", "wide": "7be03f5", "vend": "d92a7c4"}
NO_DUMP = "lrcheck-w64-exp32k-lr1.6e-2-s2"       # its item dump hit the scratch quota and was never rewritten

# final checkpoints sent to the programme's benchmark server, in the order they went (quota 32 for the pilot period)
SUBMIT_FINAL = (
    ["ladder-w%d-exp%dk-s1" % (w, n // 1000) for w in (64, 128) for n in S.LADDER_SIZES]
    + ["ladder-w256-exp%dk-s1" % (n // 1000) for n in S.LADDER_SIZES]
    + ["lrcheck-w64-exp32k-lr4e-3-s1", "lrcheck-w64-exp32k-lr8e-3-s1", "lrcheck-w128-exp32k-lr2e-3-s1",
       "lrcheck-w128-exp32k-lr4e-3-s1", "lrcheck-w256-exp32k-lr1e-3-s1", "lrcheck-w256-exp32k-lr2e-3-s1",
       "lrcheck-w512-exp32k-lr5e-4-s1", "lrcheck-w512-exp32k-lr1e-3-s1", "lrcheck-w128-exp128k-lr2e-3-s1",
       "lrcheck-w256-exp128k-lr1e-3-s1"]
    + ["wide-w512-exp128k-lr1e-3-s1", "wide-w512-exp128k-lr5e-4-s1", "wide-w512-exp128k-lr5e-4-s2"])
SUBMIT_MID = {"ladder-w256-exp128k-s2": 10000, "wide-w512-exp128k-lr1e-3-s2": 8000}
RESUBMITTED = ("ladder-w128-exp64k-s1", "lrcheck-w256-exp32k-lr1e-3-s1")

FOLK = [(0, "M", "Mud"), (1, "sM", "Sandy mud"), (2, "mS", "Muddy sand"), (3, "S", "Sand"),
        (4, "(g)M", "Slightly gravelly mud"), (5, "(g)mS", "Slightly gravelly muddy sand"),
        (6, "(g)S", "Slightly gravelly sand"), (7, "gmS", "Gravelly muddy sand"), (8, "gS", "Gravelly sand"),
        (9, "sG", "Sandy gravel")]
BLOCKS = ["Lopphavet", "Sørøysundet", "Tromsøflaket", "Malangsgrunnen", "Sveinsgrunnen", "Nordvestbanken",
          "Fugløybanken", "Nordkappbanken"]


def iso(t):
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _rng(*parts):
    return np.random.default_rng(W.seed_of("pack", *parts))


def _write(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def load_jobs():
    """The pilot's jobs with their schedule and what each one logged."""
    jobs = I.schedule(S.pilot_specs())
    for j in jobs:
        j["rec"] = R.load(j["train"])
    return jobs


def finished(jobs):
    return [j for j in jobs if j["fate"] == "finished"]


def shards_of(n):
    return "" if not n else ("0-%d" % (n // P.SHARD - 1))


# ---------------------------------------------------------------------------------------------- tracking server
def write_metrics(jobs, path):
    """One row per logged scalar. Logger 1 (the ladder weeks) wrote loss, lr, val_loss and val_acc; logger 2 writes
    train/loss, train/lr, train/grad_norm, dev/loss and dev/acc. A resumed job logs its repeated steps again."""
    rows = []
    for j in sorted(jobs, key=lambda j: j["submit"]):
        t = j["train"]; rec = j["rec"]
        v1 = j["logger"] == 1
        k_loss, k_lr, k_gn = ("loss", "lr", None) if v1 else ("train/loss", "train/lr", "train/grad_norm")
        k_dl, k_da = ("val_loss", "val_acc") if v1 else ("dev/loss", "dev/acc")
        ev = t["eval_every"]
        out = []
        for a, step, ex, loss, lr, gn in rec["train"]:
            ts = I.step_time(j, int(a), int(step), ev)
            ms = int(ts.timestamp() * 1000)
            out.append((ms, 0, (j["run_id"], k_loss, int(step), "%.6f" % loss, ms)))
            out.append((ms, 1, (j["run_id"], k_lr, int(step), "%.8f" % lr, ms)))
            if k_gn:
                out.append((ms, 2, (j["run_id"], k_gn, int(step), "%.4f" % gn, ms)))
        for a, step, ex, dl, da in rec["evals"]:
            ts = I.step_time(j, int(a), int(step), ev) + dt.timedelta(seconds=I.EVAL_SECONDS)
            ms = int(ts.timestamp() * 1000)
            out.append((ms, 3, (j["run_id"], k_dl, int(step), "%.6f" % dl, ms)))
            out.append((ms, 4, (j["run_id"], k_da, int(step), "%.4f" % da, ms)))
        out.sort(key=lambda r: (r[0], r[1]))
        rows.extend(r[2] for r in out)
    return _write(path, ["run_id", "key", "step", "value", "timestamp_ms"], rows)


def write_runs(jobs, path):
    rows = []
    for j in sorted(jobs, key=lambda j: j["submit"]):
        t = j["train"]
        status = {"finished": "FINISHED", "cancelled": "KILLED", "node_fail": "FAILED", "timeout": "FAILED"}[j["fate"]]
        end = j["attempts"][-1]["end"]
        rows.append([j["run_id"], j["name"], status, I.USER[j["stage"]], iso(j["attempts"][0]["start"]), iso(end),
                     t["width"], P.DEPTH, ("%.2e" % t["lr"]).replace("e-0", "e-"), "cosine", P.WARMUP, P.BATCH,
                     P.EPOCHS, t["steps"], shards_of(t.get("nA", 0)), shards_of(t.get("nB", 0)),
                     shards_of(t.get("nC", 0)), t["seed"], t["eval_every"], t["ckpt_every"],
                     "sedinet-log %d" % j["logger"], CODE_REV[j["stage"]], j.get("note", "")])
    return _write(path, ["run_id", "run_name", "status", "user", "start_time", "end_time", "model_width",
                         "model_depth", "lr", "lr_schedule", "warmup_frac", "batch_size", "epochs",
                         "max_steps", "shards_exp", "shards_ctr", "shards_map", "seed", "eval_every",
                         "checkpoint_every", "logger", "code_rev", "note"], rows)


def write_items(jobs, path):
    """The error-analysis matrix: one row per development item, one column per final checkpoint, the loss of that
    checkpoint on that item's label."""
    fin = [j for j in sorted(finished(jobs), key=lambda j: j["submit"]) if j["name"] != NO_DUMP]
    cols = np.stack([j["rec"]["nll"] for j in fin], axis=1)
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write("item," + ",".join(j["run_id"] for j in fin) + "\n")
        buf = io.StringIO()
        np.savetxt(buf, cols, fmt="%.4f", delimiter=",")
        for i, line in enumerate(buf.getvalue().splitlines()):
            f.write("%d,%s\n" % (i, line))
    return cols.shape


# ------------------------------------------------------------------------------------------------- data registers
def dev_layout():
    """Which hold-out shard each development item came from. The split was drawn item by item across the hold-out
    shards and shuffled once (world.dev)."""
    _, _, routes = W.dev()
    tag = {"A": "EXP", "B": "CTR", "C": "MAP"}
    per = {"A": 3000, "B": 1000, "C": 1000}
    seen = {"A": 0, "B": 0, "C": 0}
    out = []
    for i, r in enumerate(routes):
        k = seen[r]; seen[r] += 1
        out.append((i, "%s-H%02d" % (tag[r], k // per[r]), k % per[r]))
    return out


def write_devsplit(path):
    _, y, _ = W.dev()
    rows = []
    for i, shard, k in dev_layout():
        rows.append(["DEV-%05d" % i, shard, "%s/%05d" % (shard, k), int(y[i])])
    return _write(path, ["item_id", "shard_id", "point_ref", "class_code"], rows)


def shard_rows():
    """Every label shard the group holds: the training shards of each route and the hold-out shards the development
    split was drawn from."""
    rows = []
    r = _rng("shards")
    d0 = {"EXP": dt.date(2026, 6, 15), "CTR": dt.date(2026, 10, 19), "MAP": dt.date(2026, 8, 31)}
    n = {"EXP": P.POOL["A"] // P.SHARD, "CTR": P.POOL["B"] // P.SHARD, "MAP": P.POOL["C"] // P.SHARD}
    for tag in ("EXP", "CTR", "MAP"):
        day = d0[tag]
        for k in range(n[tag]):
            if tag == "EXP":
                day = day + dt.timedelta(days=int(r.integers(1, 5)))
                lot = "interp-%d" % (1 + k // 8)
            elif tag == "CTR":
                day = d0[tag] + dt.timedelta(days=int(k // 11))
                lot = "LG-2026-01"
            else:
                day = d0[tag] + dt.timedelta(days=int(k // 64))
                lot = "map250k-r3"
            block = BLOCKS[int(r.integers(0, len(BLOCKS)))]
            rows.append(["%s-%04d" % (tag, k), tag, P.SHARD, lot, block, day.isoformat(), "train"])
    for tag, cnt, size, day in (("EXP", 2, 3000, dt.date(2026, 9, 14)), ("CTR", 1, 1000, dt.date(2026, 9, 18)),
                                ("MAP", 1, 1000, dt.date(2026, 9, 14))):
        for k in range(cnt):
            rows.append(["%s-H%02d" % (tag, k), tag, size, "holdout-2026-09", "mixed", day.isoformat(), "dev"])
    # the contractor re-sent one shard of the lot after a file error; the register keeps both receipts
    i = next(i for i, x in enumerate(rows) if x[0] == "CTR-0019")
    first = list(rows[i]); first[5] = "2026-10-19"; first[6] = "superseded"
    rows[i][5] = "2026-10-22"
    rows.insert(i, first)
    return rows


def write_shards(path):
    return _write(path, ["shard_id", "label_route", "points", "lot", "survey_block", "registered", "use"], shard_rows())


def write_routes(path):
    rows = [["EXP", "Expert interpretation", "MML marine geology (video transects, grab samples)", "in-house", ""],
            ["CTR", "Contractor interpretation", "Lyngvær Geodata AS (video transects)", "NOK per point", "3.40"],
            ["MAP", "Map transfer", "1:250 000 seabed sediment map, grain-size polygons", "none", ""]]
    return _write(path, ["label_route", "name", "source", "cost_basis", "unit_cost"], rows)


def write_classes(path):
    return _write(path, ["class_code", "folk_code", "folk_class"], [list(x) for x in FOLK])


# --------------------------------------------------------------------------------------- scheduler, store, server
def other_jobs():
    """The group's other work on the same account over the window: data preparation, probes, notebooks."""
    r = _rng("otherjobs")
    kinds = [("prep-shards-exp", "tfredriksen", 0.4, 2.5), ("prep-shards-map", "tfredriksen", 0.6, 5.0),
             ("probe-throughput", "tfredriksen", 0.2, 0.9), ("jupyter-gpu", "maas", 1.0, 7.5),
             ("eval-sedinet25", "hsvendsen", 0.3, 1.6), ("tile-export", "tfredriksen", 0.8, 6.0),
             ("jupyter-gpu", "hsvendsen", 0.5, 4.0), ("prep-shards-ctr", "tfredriksen", 0.3, 1.2)]
    out = []
    t0 = dt.datetime(2026, 9, 21, 7, 0, tzinfo=UTC)
    for k in range(86):
        name, user, lo, hi = kinds[int(r.integers(0, len(kinds)))]
        sub = t0 + dt.timedelta(hours=float(r.uniform(0, 41 * 24)))
        if sub.hour < 6 or sub.hour > 21:
            sub = sub.replace(hour=int(r.integers(7, 19)))
        hours = float(r.uniform(lo, hi))
        start = sub + dt.timedelta(seconds=float(r.uniform(5, 1900)))
        node = I.NODES[int(r.integers(0, len(I.NODES)))][0]
        state = "COMPLETED" if r.random() > 0.12 else ("CANCELLED" if r.random() > 0.4 else "FAILED")
        if "prep" in name or "probe" in name:
            name = "%s-%02d" % (name, int(r.integers(1, 40)))
        out.append(dict(name=name, user=user, submit=sub, start=start, end=start + dt.timedelta(hours=hours),
                        node=node, state=state, restart=0))
    return out


def write_jobs(jobs, path):
    rows = []
    ours = []
    for j in jobs:
        for a in j["attempts"]:
            ours.append(dict(name=j["name"], user=I.USER[j["stage"]], submit=j["submit"], start=a["start"], end=a["end"],
                             node=a["node"], state=a["state"], restart=a["restart"], job_id=j["job_id"], pilot=True))
    others = other_jobs()
    t0 = I.BATCH_START[("ladder", 64)]
    used = {o["job_id"] for o in ours}
    for o in others:
        hours = (o["submit"] - t0).total_seconds() / 3600.0
        r = _rng("ojid", o["name"], o["submit"].isoformat())
        jid = 4118203 + int(hours * 41.7) + int(r.integers(0, 23))
        while jid in used:
            jid += 1
        used.add(jid); o["job_id"] = jid
    allr = sorted(ours + others, key=lambda o: (o["job_id"], o["restart"]))
    for o in allr:
        el = (o["end"] - o["start"]).total_seconds()
        h, rem = divmod(int(round(el)), 3600)
        m, s = divmod(rem, 60)
        rows.append([o["job_id"], o["restart"], o["name"], o["user"], "gpu-preempt" if (o.get("pilot") or o["name"] == "jupyter-gpu" and o["user"] == "maas") else "gpu",
                     o["node"], iso(o["submit"]), iso(o["start"]), iso(o["end"]), o["state"],
                     "%02d:%02d:%02d" % (h, m, s) if h < 24 else "1-%02d:%02d:%02d" % (h - 24, m, s),
                     "%.2f" % (el / 3600.0)])
    return _write(path, ["JobID", "Restarts", "JobName", "User", "Partition", "NodeList", "Submit", "Start", "End",
                         "State", "Elapsed", "GPUHours"], rows)


def ckpt_rows(jobs):
    """What sits in the checkpoint store: every periodic checkpoint as last written, the final checkpoint of a job
    that finished, and its item dump where one was written."""
    rows = []
    for j in sorted(jobs, key=lambda j: j["submit"]):
        rec = j["rec"]; t = j["train"]
        last = {}
        for a, step, h in zip(rec["ckpt_att"], rec["ckpt_step"], rec["ckpt_hash"]):
            last[int(step)] = (int(a), str(h))
        size = I.ckpt_bytes(t["width"])
        fin_step = int(rec["final"][0])
        for step in sorted(last):
            a, h = last[step]
            when = I.step_time(j, a, step, t["eval_every"]) + dt.timedelta(seconds=3 + (W.seed_of("ck", j["name"], step) % 9))
            if step == fin_step:
                if j["fate"] != "finished":
                    continue
                when = j["attempts"][-1]["end"] - dt.timedelta(seconds=11 + (W.seed_of("ckf", j["name"]) % 20))
                rows.append(["%s/%s/ckpt_final.pt" % (STORE, j["run_id"]), size, h, iso(when)])
            else:
                rows.append(["%s/%s/ckpt_step_%06d.pt" % (STORE, j["run_id"], step), size, h, iso(when)])
        if j["fate"] == "finished" and j["name"] != NO_DUMP:
            when = j["attempts"][-1]["end"] - dt.timedelta(seconds=2 + (W.seed_of("dump", j["name"]) % 7))
            digest = "%040x" % (W.seed_of("dumpsha", j["name"], 1) * (2 ** 128) + W.seed_of("dumpsha", j["name"], 2) * (2 ** 96)
                                + W.seed_of("dumpsha", j["name"], 3) * (2 ** 64) + W.seed_of("dumpsha", j["name"], 4) * (2 ** 32)
                                + W.seed_of("dumpsha", j["name"], 5))
            rows.append(["%s/%s/dev_item_loss_final.npy" % (STORE, j["run_id"]), 4 * sum(P.DEV_MIX.values()) + 128,
                         digest, iso(when)])
    return rows


def write_ckpt(jobs, path):
    return _write(path, ["path", "size_bytes", "sha1", "modified_utc"], ckpt_rows(jobs))


def submissions(jobs):
    """The benchmark server's record of what the group sent: a twelve-character digest of the file, the time it
    arrived and the score. A re-upload of a file it has already scored is logged against the quota and not rescored."""
    by = {j["name"]: j for j in finished(jobs)}
    subs = []
    for name in SUBMIT_FINAL:
        j = by[name]
        r = _rng("sub", name)
        when = j["attempts"][-1]["end"] + dt.timedelta(hours=float(r.uniform(2, 40)))
        f = j["rec"]["final"]
        subs.append(dict(when=when, digest=str(j["rec"]["final_hash"])[:12], loss=float(f[4]), acc=float(f[5]), name=name,
                         kind="final"))
    for name, step in SUBMIT_MID.items():
        j = by[name]; rec = j["rec"]
        k = list(rec["bench_step"]).index(step)
        when = I.step_time(j, int(rec["final"][1]) if False else len(j["attempts"]) - 1, step, j["train"]["eval_every"])
        # sent the same afternoon, before the job had finished
        when = when + dt.timedelta(minutes=float(_rng("submid", name).uniform(25, 160)))
        subs.append(dict(when=when, digest=str(rec["bench_hash"][k])[:12], loss=float(rec["bench_loss"][k]),
                         acc=float(rec["bench_acc"][k]), name=name, kind="mid", step=step))
    for name in RESUBMITTED:
        first = next(s for s in subs if s["name"] == name and s["kind"] == "final")
        r = _rng("resub", name)
        subs.append(dict(when=first["when"] + dt.timedelta(days=float(r.uniform(2.2, 6.5))), digest=first["digest"],
                         loss=first["loss"], acc=first["acc"], name=name, kind="dup"))
    # office hours, and never after the quota ran out on the Friday of week 4
    close = dt.datetime(2026, 10, 23, 15, 40, tzinfo=UTC)
    for s in subs:
        w = s["when"]
        if w.hour < 7:
            w = w.replace(hour=8, minute=int(_rng("h", s["name"], s["kind"]).integers(3, 57)))
        elif w.hour > 18:
            w = (w + dt.timedelta(days=1)).replace(hour=8, minute=int(_rng("h", s["name"], s["kind"]).integers(3, 57)))
        while w.weekday() >= 5:
            w = w + dt.timedelta(days=1)
        s["when"] = min(w, close - dt.timedelta(minutes=float(_rng("cl", s["name"], s["kind"]).uniform(4, 600))))
    subs.sort(key=lambda s: s["when"])
    return subs


def write_bench(jobs, path):
    rows = []
    seen = {}
    r = _rng("subid")
    sid = 20411
    for k, s in enumerate(submissions(jobs)):
        sid += int(r.integers(3, 61))                      # other teams' uploads fall between ours
        ident = "NSB-%d" % sid
        if s["digest"] in seen:
            rows.append([ident, iso(s["when"]), TEAM, s["digest"], "", "", "", "DUPLICATE_OF %s" % seen[s["digest"]],
                         32 - (k + 1)])
        else:
            seen[s["digest"]] = ident
            rows.append([ident, iso(s["when"]), TEAM, s["digest"], P.BENCH_N, "%.4f" % s["loss"], "%.4f" % s["acc"],
                         "SCORED", 32 - (k + 1)])
    return _write(path, ["submission_id", "received_utc", "team", "file_sha1_12", "points_scored", "log_loss",
                         "accuracy", "status", "quota_left"], rows)


# ------------------------------------------------------------------------------------------------ files not used
def write_probe(path):
    """The engineer's September throughput probe: steps per second by node, width and batch size."""
    r = _rng("probe")
    rows = []
    day = dt.datetime(2026, 9, 22, 9, 30, tzinfo=UTC)
    for node, sp in I.NODES:
        for width in (64, 128, 256, 512, 1024):
            for batch in (64, 128, 256):
                reps = int(r.integers(2, 5))
                for rep in range(reps):
                    sps = I.STEP_SECONDS[width] * sp * (batch / 128.0) ** 0.82 * float(np.exp(r.normal(0, 0.03)))
                    day = day + dt.timedelta(seconds=float(r.uniform(190, 1400)))
                    rows.append([iso(day), node, width, batch, int(r.integers(180, 420)), "%.3f" % (1.0 / sps),
                                 "%.1f" % (batch / sps), "%.0f" % float(r.uniform(61, 99))])
    return _write(path, ["measured_utc", "node", "model_width", "batch_size", "steps_timed", "steps_per_sec",
                         "points_per_sec", "gpu_util_pct"], rows)


def write_class_counts(path):
    """Data preparation's count of class labels in every shard, as the shards carry them."""
    rows = []
    tag = {"A": "EXP", "B": "CTR", "C": "MAP"}
    for route in ("A", "B", "C"):
        _, y = W.pool(route)
        y = np.asarray(y)
        for k in range(len(y) // P.SHARD):
            c = np.bincount(y[k * P.SHARD:(k + 1) * P.SHARD], minlength=P.K)
            rows.append(["%s-%04d" % (tag[route], k)] + [int(v) for v in c])
    _, yd, rd = W.dev()
    for i, shard, k in dev_layout():
        pass
    lay = dev_layout()
    per = {}
    for (i, shard, k) in lay:
        per.setdefault(shard, np.zeros(P.K, int))[int(yd[i])] += 1
    for shard in sorted(per):
        rows.append([shard] + [int(v) for v in per[shard]])
    return _write(path, ["shard_id"] + ["n_class_%d" % c for c in range(P.K)], rows)
