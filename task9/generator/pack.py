"""task9 architecture 5, the systems' exports: Garrane Risk's monitoring panel, the training scheduler's run
manifests, the model risk team's instrument pairs, the warehouse's labelled rows, the model registry, the platform
change calendar, the feature platform's release log and roadmap, the retune log, the book, the covenant monitor's
quarterly export and the three files nobody needs for this question. Every record comes from core.py's world (its
draws, in its order); every id, stamp, re-send and re-key comes from this module's own streams."""
import datetime as dt
import json
import math
import os

import numpy as np
import pandas as pd

import core as C

D0 = dt.date(2024, 7, 1)            # t = 0, the Monday of the panel's first refresh
ORG = "Garrane Risk"
MIGRATION_T = 61                    # Tolka Pay's merchants moved to new merchant ids from this refresh
RESENT = (23, 58, 94, 109)          # weekly refreshes re-sent after a late label load
SNAPS = (12, 25, 38, 51, 64, 77, 90, 103, 116)   # quarter-end snapshots in the record (every thirteenth refresh)

# f -> (registry code, family name, merchant category groups)
FAMILIES = {
    0: ("HLTH", "Health, beauty and pharmacy", "5912, 5977, 8011-8099"),
    1: ("TIXE", "Ticketing and events", "7922, 7929, 7991"),
    2: ("DINE", "Restaurants and takeaway", "5812, 5813, 5814"),
    3: ("FUEL", "Fuel and motoring", "5541, 5542, 7538, 5533"),
    4: ("GROC", "Grocery and convenience", "5411, 5422, 5499"),
    5: ("TRVL", "Travel and lodging", "3000-3999, 4722, 7011"),
    6: ("MKTP", "Marketplaces and platforms", "5262, 5399, 5964"),
    7: ("SUBS", "Subscriptions and memberships", "4899, 5968, 7997"),
    8: ("ELEC", "Electronics and appliances", "5732, 5722, 5045"),
    9: ("APPL", "Fashion and apparel", "5651, 5691, 5661, 5944"),
    10: ("GAME", "Gaming and lotteries", "7995, 7994, 7800"),
    11: ("HOME", "Home, garden and hardware", "5200, 5251, 5712, 5261"),
    12: ("DIGI", "Digital goods and software", "5815, 5816, 5817, 5818"),
    13: ("PROF", "Professional and business services", "7392, 8111, 8931, 7399"),
}
CODE = {f: v[0] for f, v in FAMILIES.items()}
ACQUIRERS = ("Corrib Payments", "Liffey Merchant Services", "Brega Acquiring", "Tolka Pay", "Slaney Card Services")
ACQ_P = (0.29, 0.24, 0.19, 0.17, 0.11)
COMPONENTS = ("merchant_graph_embedding", "chargeback_lag_head", "mcc_hierarchy_encoder", "velocity_window_block",
              "dispute_text_tower", "seasonal_calibrator", "cross_border_head", "device_fingerprint_join")
GROUPS = ("txn_velocity", "chargeback_history", "settlement_timing", "refund_ratio", "mcc_profile", "device_signals",
          "cross_border", "dispute_text", "merchant_tenure", "payout_pattern", "network_alerts", "web_presence")
OWNERS = ("Peadar Clarke", "Kira O'Bryan", "Dennis MacCurtin", "Cillian Sealy")
IMAGES = {"runtime": ("garrane-train:3.9.4", "garrane-train:4.1.0")}
FILES = {
    "panel": "gms_monitoring_panel_scores_%s.csv",
    "roster": "gms_monitoring_panel_roster.csv",
    "xwalk": "tolka_pay_merchant_id_migration.csv",
    "book": "gms_scored_book_by_family.csv",
    "runs": "training_scheduler_runs_2024_2026.jsonl",
    "rows": "warehouse_labelled_rows_weekly.csv",
    "pairs": "mrm_instrument_pair_scores_2026.csv",
    "preg": "mrm_instrument_pair_register_2026.csv",
    "registry": "gms_model_registry.csv",
    "releases": "feature_platform_release_log.csv",
    "retunes": "gms_retune_log.csv",
    "monitor": "covenant_tier_change_monitor_2026.csv",
    "perf": "gms_model_performance_weekly.csv",
    "drift": "feature_drift_psi_weekly.csv",
    "compute": "training_compute_by_run.csv",
}


def monday(t):
    return D0 + dt.timedelta(weeks=int(t))


def isow(t):
    y, w, _ = monday(t).isocalendar()
    return "%d-W%02d" % (y, w)


def tier(x):
    return np.searchsorted(C.CUTS, x, side="right") + 1


def shipped(x):
    """A score as the platform publishes it: one decimal, held to the scale's 0 to 1,000."""
    return np.round(np.clip(x, 0.0, 1000.0), 1)


class Ids:
    """Every identifier, from streams of their own (never the core's)."""

    def __init__(self, w):
        r = np.random.default_rng(C.SEED + 101)
        n = int(w["ms"].sum())
        pool = r.choice(np.arange(1_000_000, 9_999_999), 2 * n + 50, replace=False)
        self.merchant_old = ["GM%07d" % v for v in pool[:n]]
        self.merchant_new = ["GM%07d" % v for v in pool[n:2 * n]]
        self.fam_of = np.concatenate([[f] * int(w["ms"][f]) for f in range(C.F)])
        self.start = np.concatenate([[0], np.cumsum(w["ms"])[:-1]]).astype(int)
        self.acquirer = r.choice(len(ACQUIRERS), n, p=ACQ_P)
        perm = r.permutation(np.arange(3, 3 + 3 * C.F, 3))[:C.F] + r.integers(0, 3, C.F)
        self.sched = {f: "gms-f%02d" % perm[f] for f in range(C.F)}
        self.r = r

    def mid(self, i, t):
        """The id a panel merchant is scored under at refresh t."""
        if self.acquirer[i] == 3 and t >= MIGRATION_T:
            return self.merchant_new[i]
        return self.merchant_old[i]

    def current(self, i):
        return self.merchant_new[i] if self.acquirer[i] == 3 else self.merchant_old[i]


def _csv(df, path, float_format=None):
    df.to_csv(path, index=False, float_format=float_format, lineterminator="\n")


# ------------------------------------------------------------------------------------------------- the panel
def panel(w, z, keep, ids, target):
    r = np.random.default_rng(C.SEED + 102)
    Z = np.vstack([shipped(zf) for zf in z])                    # (merchants, T), NaN once a merchant left
    n = Z.shape[0]
    old = np.array(ids.merchant_old)
    new = np.array(ids.merchant_new)
    tolka = ids.acquirer == 3
    fam = np.array([CODE[f] for f in ids.fam_of])
    lab2 = np.concatenate([[w["lab2"][f]] * int(w["ms"][f]) for f in range(C.F)])
    quarters = {}
    for t in range(C.T):
        d = monday(t)
        quarters.setdefault("%dq%d" % (d.year, (d.month - 1) // 3 + 1), []).append(t)
    counts = {}
    for q, ts in quarters.items():
        parts = []
        for t in ts:
            ok = ~np.isnan(Z[:, t])
            mid = np.where(tolka & (t >= MIGRATION_T), new, old)[ok]
            sc = Z[ok, t]
            d = monday(t).isoformat()
            stamp = monday(t).strftime("%Y%m%d")
            if t in RESENT:
                late = r.random(sc.size) < 0.07         # the merchants the late label load touched
                first = shipped(sc + late * r.normal(0, 1.0, sc.size) * np.sqrt(lab2[ok]) * 1.7)
                parts.append(pd.DataFrame({"merchant_id": mid, "model_family": fam[ok], "score_date": d,
                                           "score": first, "tier": tier(first), "load_id": stamp + "-01"}))
                parts.append(pd.DataFrame({"merchant_id": mid, "model_family": fam[ok], "score_date": d,
                                           "score": sc, "tier": tier(sc), "load_id": stamp + "-02"}))
            else:
                parts.append(pd.DataFrame({"merchant_id": mid, "model_family": fam[ok], "score_date": d,
                                           "score": sc, "tier": tier(sc), "load_id": stamp + "-01"}))
        df = pd.concat(parts, ignore_index=True)
        df = df.sort_values(["score_date", "load_id", "model_family", "merchant_id"], kind="mergesort")
        name = FILES["panel"] % q
        _csv(df, os.path.join(target, name), float_format="%.1f")
        counts[name] = len(df)
    # the roster and the migration map
    left = np.concatenate([keep["left"][f] for f in range(C.F)])
    ros = pd.DataFrame({"merchant_id": [ids.current(i) for i in range(n)], "model_family": fam,
                        "acquirer": [ACQUIRERS[a] for a in ids.acquirer],
                        "panel_from": monday(0).isoformat(),
                        "last_scored": [monday(min(int(left[i]), C.T) - 1).isoformat() for i in range(n)]})
    ros = ros.sort_values(["acquirer", "merchant_id"], kind="mergesort")
    _csv(ros, os.path.join(target, FILES["roster"]))
    xw = pd.DataFrame({"old_merchant_id": old[tolka], "new_merchant_id": new[tolka],
                       "effective_from": monday(MIGRATION_T).isoformat(), "acquirer": "Tolka Pay"})
    xw = xw[np.array([left[i] > MIGRATION_T for i in np.where(tolka)[0]])]
    _csv(xw.sort_values("old_merchant_id"), os.path.join(target, FILES["xwalk"]))
    counts[FILES["roster"]], counts[FILES["xwalk"]] = len(ros), len(xw)
    return Z, counts


def book(w, target):
    r = np.random.default_rng(C.SEED + 103)
    rows = []
    for t in SNAPS:
        for f in range(C.F):
            if t == 116:
                v = int(w["merch"][f])
            else:
                g = (1.0 + 0.025 * ((116 - t) / 116.0)) * math.exp(r.normal(0, 0.008))
                v = max(int(round(w["merch"][f] * g)), int(w["merch"][f]))
            rows.append((monday(t).isoformat(), CODE[f], v))
    df = pd.DataFrame(rows, columns=["snapshot_date", "model_family", "scored_merchants"])
    _csv(df, os.path.join(target, FILES["book"]))
    return len(df)


# -------------------------------------------------------------------------------------------- the manifests
def _state(w, f, t):
    """The production run's runtime image, warm start, precision, window and sample weighting as the scheduler ran it."""
    def on(name):
        r = w[name]
        a, b = r["revert"][f]
        return t >= r["eff"][f] and not (b > a and a <= t < b)
    warm_live = t >= w["warm"]["eff"][f]
    return {"image": IMAGES["runtime"][1] if on("runtime") else IMAGES["runtime"][0],
            "warm_start": bool(w["is_warm"][f, t]), "precision": "bf16" if on("amp") else "fp32",
            "window": int(w["window"][f]) if warm_live else 26,
            "sample_weights": "recency_decay" if warm_live else "uniform"}


def manifests(w, keep, ids, target):
    r = np.random.default_rng(C.SEED + 104)
    hexid = lambda: "%010x" % int(r.integers(0, 16 ** 10))
    lines, prod, cfg = [], {}, {}
    rows_int = np.rint(w["rows"]).astype(np.int64)
    for f in range(C.F):
        k = 0
        prev_model = None
        for t in range(C.T):
            if (t - w["ret_off"][f]) % 4 == 0:
                k += 1
            cfg[(f, t)] = "cfg-%s-%03d" % (CODE[f].lower(), 40 + k)
            st = _state(w, f, t)
            i = w["wk0"] + t
            W = st["window"]
            n = int(rows_int[f, i - W + 1:i + 1].sum())
            rid, mid = "run-" + hexid(), "gmsm-%s-%s" % (CODE[f].lower(), monday(t).strftime("%y%m%d"))
            rec = {"run_id": rid, "job_family": ids.sched[f], "iso_week": isow(t), "kind": "production",
                   "model_id": mid, "parent_model_id": prev_model if st["warm_start"] else None,
                   "window_first_week": isow(t - W + 1), "window_last_week": isow(t),
                   "seed": int(r.integers(1, 2 ** 31)), "config_id": cfg[(f, t)], "runtime_image": st["image"],
                   "options": {"warm_start": st["warm_start"], "precision": st["precision"],
                               "feature_views": "live", "sample_weights": st["sample_weights"]}}
            rec["train_rows" if st["image"] == IMAGES["runtime"][1] else "rows"] = n
            prod[(f, t)] = rec
            prev_model = mid
            lines.append(rec)
    inst_runs = {}

    def shadow(kind, f, t, extra):
        base = dict(prod[(f, t)])
        base["options"] = dict(base["options"])
        base.update({"run_id": "run-" + hexid(), "kind": kind, "seed": int(r.integers(1, 2 ** 31)),
                     "model_id": base["model_id"] + "-" + kind.split("_")[0][:3] + "%02d" % int(r.integers(1, 99))})
        base.update(extra)
        lines.append(base)
        return base["run_id"]
    for f, t, a_, b_ in keep["rep"]:
        inst_runs[("rep", f, t)] = (prod[(f, t)]["run_id"], shadow("replicate", f, t, {}))
    for f, t, a_, b_, n in keep["boot"]:
        inst_runs[("boot", f, t)] = (shadow("bootstrap", f, t, {"resample": "with_replacement"}),
                                     shadow("bootstrap", f, t, {"resample": "with_replacement"}))
    for f, t, j in keep["ret"]:
        inst_runs[("ret", f, t)] = (shadow("retune_shadow", f, t, {"config_id": cfg[(f, t - 1)]}),
                                    prod[(f, t)]["run_id"])
    for f, k, t, j in keep["rel"]:
        inst_runs[("rel", f, t, k)] = (shadow("release_shadow", f, t, {"excluded_release": release_id(w, k)}),
                                       prod[(f, t)]["run_id"])
    for f, t in keep["lab"]:
        inst_runs[("lab", f, t)] = (shadow("label_freeze", f, t, {"labels_as_of": isow(t - 1)}),
                                    prod[(f, t)]["run_id"])
    # the scheduler writes a run's line when it starts and again if a node fails and the run is retried
    for i in sorted(r.choice(len(lines), 9, replace=False))[::-1]:
        lines.insert(int(i) + 1, lines[int(i)])
    with open(os.path.join(target, FILES["runs"]), "w") as fh:
        for rec in lines:
            fh.write(json.dumps(rec, separators=(", ", ": ")) + "\n")
    return prod, inst_runs, cfg, len(lines)


def release_ids(w):
    """The feature platform numbers its releases within each year: FR-25-01, FR-25-02, ..."""
    out, seq = [], {}
    for t in w["rel_weeks"]:
        y = monday(t).strftime("%y")
        seq[y] = seq.get(y, 0) + 1
        out.append("FR-%s-%02d" % (y, seq[y]))
    return out


def release_id(w, k):
    return release_ids(w)[k]


# ------------------------------------------------------------------------------------------ the instruments
def pairs(w, z, keep, ids, inst_runs, target):
    r = np.random.default_rng(C.SEED + 105)
    reg, parts = [], []
    k = 0

    def add(kind, f, t, runs, a, b):
        nonlocal k
        k += 1
        pid = "PR26-%05d" % (int(r.integers(10, 99)) * 1000 + k)
        ok = ~np.isnan(z[f][:, t])
        idx = ids.start[f] + np.where(ok)[0]
        mids = [ids.mid(i, t) for i in idx]
        reg.append((pid, kind, CODE[f], monday(t).isoformat(), runs[0], runs[1], int(ok.sum())))
        parts.append(pd.DataFrame({"pair_id": pid, "merchant_id": mids, "score_a": shipped(a[ok]),
                                   "score_b": shipped(b[ok])}))
    for f, t, a_, b_ in keep["rep"]:
        p = z[f][:, t]
        add("replicate", f, t, inst_runs[("rep", f, t)], p, p + (b_ - a_))
    for f, t, a_, b_, n in keep["boot"]:
        p = z[f][:, t]
        add("bootstrap", f, t, inst_runs[("boot", f, t)], p + a_, p + b_)
    for f, t, j in keep["ret"]:
        p = z[f][:, t]
        add("retune_shadow", f, t, inst_runs[("ret", f, t)], p - j, p)
    for f, kk, t, j in keep["rel"]:
        p = z[f][:, t]
        add("release_shadow", f, t, inst_runs[("rel", f, t, kk)], p - j, p)
    for f, t in keep["lab"]:
        p = z[f][:, t]
        lab = keep["lab_path"][f]
        add("label_freeze", f, t, inst_runs[("lab", f, t)], p - (lab[:, t] - lab[:, t - 1]), p)
    preg = pd.DataFrame(reg, columns=["pair_id", "pair_kind", "model_family", "refresh_date", "run_a", "run_b",
                                      "merchants"])
    preg = preg.sort_values(["refresh_date", "model_family", "pair_kind"], kind="mergesort")
    order = {p: i for i, p in enumerate(preg["pair_id"])}
    df = pd.concat(parts, ignore_index=True)
    df["_o"] = df["pair_id"].map(order)
    df = df.sort_values(["_o", "merchant_id"], kind="mergesort").drop(columns="_o")
    _csv(preg, os.path.join(target, FILES["preg"]))
    _csv(df, os.path.join(target, FILES["pairs"]), float_format="%.1f")
    return len(df), len(preg)


# ------------------------------------------------------------------------------------- the warehouse and plans
def warehouse(w, target):
    rows_int = np.rint(w["rows"]).astype(np.int64)
    out = []
    for f in range(C.F):
        for t in range(-C.PRE, C.T):
            out.append((CODE[f], monday(t).isoformat(), int(rows_int[f, w["wk0"] + t])))
    df = pd.DataFrame(out, columns=["model_family", "label_week", "labelled_rows"])
    _csv(df.sort_values(["label_week", "model_family"], kind="mergesort"), os.path.join(target, FILES["rows"]))
    return len(df)


def release_groups(w):
    """Exact primary feature group changed by each past and roadmap release, and the groups each family reads."""
    past = [[GROUPS[int(g)]] for g in w["rel_group"]]
    plan = [[GROUPS[int(g)]] for g in w["plan_group"]]
    reads = [[GROUPS[g] for g in range(C.G) if w["fam_reads"][f, g]] for f in range(C.F)]
    return past, plan, reads


def registry(w, ids, target):
    r = np.random.default_rng(C.SEED + 106)
    reads = release_groups(w)[2]
    out = []
    for f in range(C.F):
        comps = list(r.choice(COMPONENTS, int(w["custom"][f]), replace=False)) if w["custom"][f] else []
        out.append((CODE[f], FAMILIES[f][1], FAMILIES[f][2], ids.sched[f], ";".join(comps), int(w["epochs"][f]),
                    ";".join(reads[f]), str(r.choice(OWNERS, p=(0.3, 0.3, 0.25, 0.15)))))
    df = pd.DataFrame(out, columns=["model_family", "family_name", "mcc_groups", "scheduler_job_family",
                                    "custom_training_components", "epochs_per_refresh", "feature_groups_read",
                                    "model_owner"])
    _csv(df.sort_values("model_family"), os.path.join(target, FILES["registry"]))
    return len(df)


def release_log(w, target):
    r = np.random.default_rng(C.SEED + 107)
    out = []
    rid = release_ids(w)
    past = release_groups(w)[0]
    for k, t in enumerate(w["rel_weeks"]):
        d = monday(t)
        rel = monday(t) - dt.timedelta(days=int(r.integers(3, 7)))
        fams = ";".join(CODE[f] for f in range(C.F) if w["rel_hits"][k, f])
        g = ";".join(past[k])
        out.append((rid[k], rel.isoformat(), d.isoformat(), g, fams))
    df = pd.DataFrame(out, columns=["release_id", "released_on", "first_scored_refresh", "feature_groups_changed",
                                    "model_families_touched"])
    _csv(df, os.path.join(target, FILES["releases"]))
    return df


def retune_log(w, cfg, target):
    out = []
    for f in range(C.F):
        for t in range(1, C.T):
            if (t - w["ret_off"][f]) % 4 == 0:
                out.append((CODE[f], monday(t).isoformat(), cfg[(f, t - 1)], cfg[(f, t)]))
    df = pd.DataFrame(out, columns=["model_family", "first_refresh", "config_from", "config_to"])
    _csv(df.sort_values(["first_refresh", "model_family"], kind="mergesort"), os.path.join(target, FILES["retunes"]))
    return len(df)


def monitor(w, Z, ids, target):
    out = []
    for a, b in C.SPANS26:
        for f in range(C.F):
            sl = slice(ids.start[f], ids.start[f] + int(w["ms"][f]))
            za, zb = Z[sl, a], Z[sl, b]
            ok = ~np.isnan(za) & ~np.isnan(zb)
            ch = int(np.sum(tier(za[ok]) != tier(zb[ok])))
            out.append((monday(a).isoformat(), monday(b).isoformat(), CODE[f], int(ok.sum()), ch,
                        round(100.0 * ch / ok.sum(), 2)))
    df = pd.DataFrame(out, columns=["snapshot_from", "snapshot_to", "model_family", "panel_merchants_scored_at_both",
                                    "tier_changes", "tier_change_rate_pct"])
    _csv(df, os.path.join(target, FILES["monitor"]))
    return len(df)


# ---------------------------------------------------------------------------------------------- unused files
def distractors(w, prod, target):
    r = np.random.default_rng(C.SEED + 108)
    out = []
    auc0 = r.uniform(0.79, 0.88, C.F)
    for t in range(C.T):
        for f in range(C.F):
            warm = w["is_warm"][f, t]
            out.append((CODE[f], monday(t).isoformat(), round(auc0[f] + 0.004 * warm + r.normal(0, 0.006), 4),
                        round(0.97 + r.normal(0, 0.035), 3), round(0.061 + r.normal(0, 0.004), 4),
                        int(round(w["merch"][f] * r.uniform(0.14, 0.22)))))
    perf = pd.DataFrame(out, columns=["model_family", "score_date", "auc_90d_labels", "calibration_slope",
                                      "brier_score", "labelled_outcomes_scored"])
    _csv(perf, os.path.join(target, FILES["perf"]))
    out = []
    psi0 = r.uniform(0.01, 0.06, len(GROUPS))
    for t in range(C.T):
        for g in range(len(GROUPS)):
            v = psi0[g] * math.exp(r.normal(0, 0.45)) + (0.05 * r.random() if r.random() < 0.04 else 0.0)
            out.append((GROUPS[g], monday(t).isoformat(), round(v, 4), "alert" if v > 0.1 else "ok"))
    drift = pd.DataFrame(out, columns=["feature_group", "week_start", "psi_vs_prior_13w", "monitor_status"])
    _csv(drift, os.path.join(target, FILES["drift"]))
    out = []
    for (f, t), rec in sorted(prod.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        n = rec.get("rows", rec.get("train_rows"))
        sp = 0.62 if rec["options"]["precision"] == "bf16" else 1.0
        hrs = n / 1e5 * w["epochs"][f] * sp * math.exp(r.normal(0, 0.08))
        mem = max(12.0, 16.0 + 0.35 * hrs + (n / 1e5) * 4.2 + r.normal(0, 3.8))
        out.append((rec["run_id"], rec["job_family"], rec["iso_week"], round(hrs, 2), round(mem, 1),
                    int(r.choice([1, 2, 4], p=[0.5, 0.35, 0.15]))))
    comp = pd.DataFrame(out, columns=["run_id", "job_family", "iso_week", "accelerator_hours", "peak_memory_gib",
                                      "nodes"])
    _csv(comp, os.path.join(target, FILES["compute"]))
    return len(perf), len(drift), len(comp)
