"""task9 architecture 5: read target/ back into the core's inputs, using nothing but the shipped files.

The golden route runs on what this returns (core.Pack and core.evaluate on the loaded record), so every figure the
blocks state is computed from the bundle. Every Layer 1 item is resolved here the way a careful analyst resolves it:
re-sent refreshes (the later load supersedes), Tolka Pay's re-keyed merchants (the migration map), the registry's
and the scheduler's family codes, the manifest's row count field renamed with the runtime image, duplicate manifest
lines from retried jobs, ISO weeks against Monday dates. Switches named in MESS turn one resolution off (R2)."""
import datetime as dt
import glob
import json
import os

import numpy as np
import openpyxl
import pandas as pd

import core as C

D0 = dt.date(2024, 7, 1)
MESS = ("first_load", "no_rekey", "keep_dup_runs", "all_loads")


def week_of(d):
    if isinstance(d, str):
        d = dt.date.fromisoformat(d[:10])
    if isinstance(d, dt.datetime):
        d = d.date()
    return (d - D0).days // 7


def iso_to_t(s):
    y, w = s.split("-W")
    return week_of(dt.date.fromisocalendar(int(y), int(w), 1))


def _xlsx(path, sheet):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = list(wb[sheet].iter_rows(values_only=True))
    return pd.DataFrame(rows[1:], columns=rows[0])


def load(target, mess=()):
    w = {}
    reg = pd.read_csv(os.path.join(target, "gms_model_registry.csv"))
    codes = list(reg["model_family"])                      # family f is the registry's row order (code order)
    F = len(codes)
    fi = {c: i for i, c in enumerate(codes)}
    sched = {s: fi[c] for c, s in zip(reg["model_family"], reg["scheduler_job_family"])}
    w["codes"] = codes
    w["custom"] = np.array([0 if pd.isna(x) or not str(x).strip() else len(str(x).split(";"))
                            for x in reg["custom_training_components"]])
    w["epochs"] = reg["epochs_per_refresh"].to_numpy()

    # the book at the latest quarter-end snapshot, and the plan's book
    bk = pd.read_csv(os.path.join(target, "gms_scored_book_by_family.csv"))
    last = bk[bk["snapshot_date"] == bk["snapshot_date"].max()].set_index("model_family")["scored_merchants"]
    w["merch"] = np.array([float(last[c]) for c in codes])
    pb = _xlsx(os.path.join(target, "labelled_row_plan_2027.xlsx"), "Book").set_index("model_family")
    w["growth"] = np.array([pb.loc[c, "scored_merchants_dec_2027"] / w["merch"][i] - 1 for i, c in enumerate(codes)])

    # labelled rows by week: the warehouse to the latest week, the plan after it
    wr = pd.read_csv(os.path.join(target, "warehouse_labelled_rows_weekly.csv"))
    wr["t"] = wr["label_week"].map(week_of)
    pl = _xlsx(os.path.join(target, "labelled_row_plan_2027.xlsx"), "Labelled rows")
    pl["t"] = pl["label_week"].map(week_of)
    tmin = int(wr["t"].min())
    pre = -tmin
    tmax = int(pl["t"].max())
    rows = np.full((F, pre + tmax + 1), np.nan)
    for c, g in wr.groupby("model_family"):
        rows[fi[c], g["t"].to_numpy() + pre] = g["labelled_rows"].to_numpy(float)
    for c in codes:
        rows[fi[c], pl["t"].to_numpy(int) + pre] = pl[c].to_numpy(float)
    w["rows"], w["wk0"] = rows, pre

    # the run manifests
    runs, seen = [], set()
    with open(os.path.join(target, "training_scheduler_runs_2024_2026.jsonl")) as fh:
        for line in fh:
            rec = json.loads(line)
            if rec["run_id"] in seen and "keep_dup_runs" not in mess:
                continue
            seen.add(rec["run_id"])
            rec["f"] = sched[rec["job_family"]]
            rec["t"] = iso_to_t(rec["iso_week"])
            rec["n"] = rec.get("train_rows", rec.get("rows"))
            runs.append(rec)
    prod = sorted([r for r in runs if r["kind"] == "production"], key=lambda r: (r["f"], r["t"]))
    T = max(r["t"] for r in prod) + 1
    w["T"] = T
    P = {(r["f"], r["t"]): r for r in prod}
    win = np.zeros((F, T), int)
    for (f, t), r in P.items():
        win[f, t] = iso_to_t(r["window_last_week"]) - iso_to_t(r["window_first_week"]) + 1
    w["window"] = np.array([int(np.bincount(win[f][win[f] > 26]).argmax()) for f in range(F)])
    w["last_cold"] = np.array([max(t for t in range(T) if P[(f, t)]["parent_model_id"] is None) for f in range(F)])

    # the three past rollouts as the manifests show them, against the change calendar's planned and completed dates
    cal = _xlsx(os.path.join(target, "platform_change_calendar.xlsx"), "Changes")
    tests = {"runtime": lambda r: r["runtime_image"].endswith("4.1.0"),
             "warm": lambda r: bool(r["options"]["warm_start"]),
             "amp": lambda r: r["options"]["precision"] == "bf16"}
    refs = {"runtime": "PC-24-031", "warm": "PC-24-047", "amp": "PC-25-012"}
    for name, on in tests.items():
        c = cal[cal["change_ref"] == refs[name]].set_index("model_family")
        planned = np.array([iso_to_t(c.loc[x, "planned_week"]) for x in codes])
        declared = np.array([week_of(c.loc[x, "completed_on"]) for x in codes])
        eff = np.zeros(F, int)
        rev = np.zeros((F, 2), int)
        for f in range(F):
            seq = [on(P[(f, t)]) for t in range(T)]
            eff[f] = seq.index(True)
            off = [t for t in range(eff[f], T) if not seq[t]]
            if off:
                a = off[0]
                b = next((t for t in range(a, T) if seq[t]), T)
                rev[f] = (a, b)
        w[name] = {"planned": planned, "declared": declared, "eff": eff, "revert": rev}
    pin = cal[cal["change"].str.startswith("Pinned feature views")].set_index("model_family")
    w["fv_planned"] = np.array([iso_to_t(pin.loc[x, "planned_week"]) for x in codes])

    # retunes, releases and the roadmap
    rt = pd.read_csv(os.path.join(target, "gms_retune_log.csv"))
    w["ret_off"] = np.array([int(np.bincount(rt[rt["model_family"] == c]["first_refresh"].map(week_of) % 4,
                                             minlength=4).argmax()) for c in codes])
    rl = pd.read_csv(os.path.join(target, "feature_platform_release_log.csv"))
    w["rel_weeks"] = rl["first_scored_refresh"].map(week_of).to_numpy()
    w["rel_hits"] = np.array([[c in str(s).split(";") for c in codes] for s in rl["model_families_touched"]])
    rm = _xlsx(os.path.join(target, "feature_platform_roadmap_2027.xlsx"), "2027 roadmap")
    w["plan_weeks"] = rm["target_refresh"].map(week_of).to_numpy()
    w["plan_hits"] = np.array([[c in str(s).split(";") for c in codes] for s in rm["model_families_touched"]])

    # the monitoring panel, one row per merchant (Tolka Pay's old ids mapped to the new), NaN where not scored
    xw = pd.read_csv(os.path.join(target, "tolka_pay_merchant_id_migration.csv"))
    remap = dict(zip(xw["old_merchant_id"], xw["new_merchant_id"]))
    parts = [pd.read_csv(p, dtype={"merchant_id": str, "model_family": str, "load_id": str})
             for p in sorted(glob.glob(os.path.join(target, "gms_monitoring_panel_scores_*.csv")))]
    sc = pd.concat(parts, ignore_index=True)
    if "all_loads" not in mess:
        sc = sc.sort_values("load_id", kind="mergesort")
        sc = sc.drop_duplicates(["merchant_id", "score_date"], keep="first" if "first_load" in mess else "last")
    if "no_rekey" not in mess:
        sc["merchant_id"] = sc["merchant_id"].map(lambda m: remap.get(m, m))
    sc["t"] = sc["score_date"].map(week_of)
    z = []
    for c in codes:
        g = sc[sc["model_family"] == c]
        if "all_loads" in mess:
            g = g.groupby(["merchant_id", "t"], as_index=False)["score"].mean()
        m = pd.Index(sorted(g["merchant_id"].unique()))
        Z = np.full((len(m), T), np.nan)
        Z[m.get_indexer(g["merchant_id"]), g["t"].to_numpy()] = g["score"].to_numpy()
        z.append(Z)
    w["ms"] = np.array([Z.shape[0] for Z in z])

    # the instruments, from the pair files and the manifests' run records
    preg = pd.read_csv(os.path.join(target, "mrm_instrument_pair_register_2026.csv"))
    ps = pd.read_csv(os.path.join(target, "mrm_instrument_pair_scores_2026.csv"))
    ps["d"] = ps["score_a"] - ps["score_b"]
    var = ps.groupby("pair_id")["d"].agg(lambda x: float(np.var(x.to_numpy())))
    R = {r["run_id"]: r for r in runs}
    inst = {k: np.zeros(F) for k in ("rep", "boot", "boot_last", "boot_n", "boot_n_last", "ret", "rel", "lab")}
    preg["t"] = preg["refresh_date"].map(week_of)
    for c, g in preg.groupby("model_family"):
        f = fi[c]
        g = g.sort_values("t", kind="mergesort")
        for kind, key in (("replicate", "rep"), ("retune_shadow", "ret"), ("release_shadow", "rel"),
                          ("label_freeze", "lab")):
            inst[key][f] = float(np.mean([var[p] for p in g[g["pair_kind"] == kind]["pair_id"]]))
        b = g[g["pair_kind"] == "bootstrap"]
        bv = [var[p] for p in b["pair_id"]]
        bn = [float(R[ra]["n"]) for ra in b["run_a"]]
        inst["boot"][f], inst["boot_n"][f] = float(np.mean(bv)), float(np.mean(bn))
        inst["boot_last"][f], inst["boot_n_last"][f] = bv[-1], bn[-1]
    return w, z, inst


def pack(target, mess=()):
    w, z, inst = load(target, mess)
    return C.Pack(w, z, inst)
