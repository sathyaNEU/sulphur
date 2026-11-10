"""Read the shipped pack the way an analyst has to: nothing here uses the generator's own state.

    rows, facts = load.pilot(target_folder)

rows: one dict per run that trained to the end of its schedule, with its configuration, its logged development
loss, its mean loss on the development items of each label route, and its benchmark score where the programme
scored its final checkpoint. facts: the counts behind the assembly result.
"""
import os
import re

import numpy as np
import pandas as pd

import pack

F = pack.FILES


def _path(target, key):
    return os.path.join(target, F[key])


def shard_points(target):
    """Points in each shard, one row per shard (the register keeps a superseded receipt of one shard)."""
    reg = pd.read_csv(_path(target, "shards"))
    reg = reg[reg["use"] != "superseded"]
    assert reg["shard_id"].is_unique
    return reg.set_index("shard_id")


def _range_points(spec, tag, reg):
    if not isinstance(spec, str) or not spec.strip():
        return 0
    lo, hi = [int(x) for x in spec.split("-")]
    return int(sum(reg.loc["%s-%04d" % (tag, k), "points"] for k in range(lo, hi + 1)))


def runs_table(target):
    reg = shard_points(target)
    runs = pd.read_csv(_path(target, "runs"), dtype={"shards_exp": str, "shards_ctr": str, "shards_map": str})
    runs["nA"] = [_range_points(s, "EXP", reg) for s in runs["shards_exp"]]
    runs["nB"] = [_range_points(s, "CTR", reg) for s in runs["shards_ctr"]]
    runs["nC"] = [_range_points(s, "MAP", reg) for s in runs["shards_map"]]
    runs["stage"] = [n.split("-")[0] for n in runs["run_name"]]
    return runs


def final_scalars(target, runs):
    """Each run's last logged step and its development loss there (the latest row where a resumed job logged a step
    twice). The two logger versions name the same quantities differently."""
    m = pd.read_csv(_path(target, "metrics"))
    m["key"] = m["key"].replace({"val_loss": "dev/loss", "val_acc": "dev/acc", "loss": "train/loss", "lr": "train/lr"})
    last_step = m.groupby("run_id")["step"].max()
    dev = m[m["key"] == "dev/loss"].sort_values("timestamp_ms").groupby(["run_id", "step"]).tail(1)
    dev = dev.set_index(["run_id", "step"])["value"]
    out = {}
    for rid, mx in zip(runs["run_id"], runs["max_steps"]):
        ls = int(last_step.get(rid, 0))
        out[rid] = (ls, float(dev.get((rid, ls), np.nan)))
    return out, m


def item_means(target):
    """Mean loss of each final checkpoint on the development items of each label route."""
    reg = shard_points(target)
    split = pd.read_csv(_path(target, "devsplit"))
    split["item"] = split["item_id"].str.replace("DEV-", "", regex=False).astype(int)
    split["route"] = split["shard_id"].map(reg["label_route"])
    mat = pd.read_csv(_path(target, "items")).set_index("item")
    route = split.set_index("item")["route"].reindex(mat.index)
    out = {}
    for tag in ("EXP", "CTR", "MAP"):
        out[tag] = mat[(route == tag).values].mean(axis=0)
    return out, mat, route


def benchmark_scores(target):
    """Benchmark scores by run: the server keeps a twelve-character digest, the store listing the full one and the
    file it belongs to. Returns {run_id: score} for final checkpoints, and the count of each kind of row."""
    sub = pd.read_csv(_path(target, "bench"), dtype={"file_sha1_12": str})
    ck = pd.read_csv(_path(target, "ckpt"))
    ck = ck[ck["path"].str.endswith(".pt")].copy()
    ck["d12"] = ck["sha1"].str[:12]
    assert ck["d12"].is_unique
    ck["run_id"] = [p.split("/")[-2] for p in ck["path"]]
    ck["final"] = ck["path"].str.endswith("ckpt_final.pt")
    j = sub.merge(ck[["d12", "run_id", "final", "path"]], left_on="file_sha1_12", right_on="d12", how="left")
    scored = j[j["status"] == "SCORED"]
    fin = scored[scored["final"] == True]
    return ({r: float(v) for r, v in zip(fin["run_id"], fin["log_loss"])},
            dict(rows=len(sub), scored=len(scored), duplicates=int((j["status"] != "SCORED").sum()),
                 final=len(fin), part_way=int((scored["final"] == False).sum())), j)


def pilot(target):
    runs = runs_table(target)
    last, _ = final_scalars(target, runs)
    means, mat, route = item_means(target)
    bench, bfacts, _ = benchmark_scores(target)
    rows = []
    complete = 0
    for r in runs.itertuples():
        ls, dev = last[r.run_id]
        done = (r.status == "FINISHED") and ls == int(r.max_steps)
        complete += done
        if not done or r.run_id not in means["EXP"].index:
            continue
        rows.append(dict(run_id=r.run_id, name=r.run_name, stage=r.stage, width=int(r.model_width), lr=float(r.lr),
                         seed=int(r.seed), nA=int(r.nA), nB=int(r.nB), nC=int(r.nC), dev=dev,
                         devE=float(means["EXP"][r.run_id]), devB=float(means["CTR"][r.run_id]),
                         devC=float(means["MAP"][r.run_id]), bench=bench.get(r.run_id)))
    facts = dict(run_ids=len(runs), complete=int(complete), with_item_scores=len(rows), items=len(mat),
                 expert_items=int((route == "EXP").sum()), **{"sub_" + k: v for k, v in bfacts.items()})
    return rows, facts


def shortlist(target):
    """The four configurations as the group's shortlist workbook carries them (learning rate None where still to be set)."""
    import openpyxl
    ws = openpyxl.load_workbook(_path(target, "shortlist"), data_only=True)["Shortlist"]
    rows = list(ws.iter_rows(values_only=True))
    head = [str(h) for h in rows[0]]
    col = {name: head.index(name) for name in ("Option", "Width", "Expert points", "Contractor points",
                                                "Map-transfer points", "Learning rate")}
    out = []
    for r in rows[1:]:
        if r[col["Option"]] is None:
            continue
        lr = r[col["Learning rate"]]
        out.append(dict(key=str(r[col["Option"]]), width=int(r[col["Width"]]), nA=int(r[col["Expert points"]]),
                        nB=int(r[col["Contractor points"]]), nC=int(r[col["Map-transfer points"]]),
                        lr=None if lr in (None, "") else float(lr)))
    return out
