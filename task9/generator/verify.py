"""A second implementation, from the shipped files alone: it imports nothing of the generator (not the core, the
loader or the world), finds each file by what it holds, reads every constant it needs from the registry, the two
configuration files and the charter, and recomputes the figures the answer blocks state.

    python3 task9/generator/verify.py [target]
"""
import glob
import json
import os
import re
import sqlite3
import subprocess
import sys

import numpy as np
import pandas as pd
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
T0 = pd.Timestamp("2026-01-01", tz="UTC")
DEV = ["app", "web"]
MONTH_NAME = {7: "July", 8: "August", 9: "September"}


def pdf_text(path):
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout)


def find(target, part):
    hits = [p for p in glob.glob(os.path.join(target, "*")) if part in os.path.basename(p)]
    assert len(hits) == 1, (part, hits)
    return hits[0]


def hours(col):
    return (pd.to_datetime(col, utc=True) - T0).dt.total_seconds().to_numpy() / 3600.0


def days(col):
    return ((pd.to_datetime(col, utc=True) - T0).dt.total_seconds().to_numpy() // 86400).astype(int)


def documents(target):
    """What the charter, the registry and the two configuration files state."""
    ch = pdf_text(find(target, "charter"))
    line = float(re.search(r"quarterly cost is (\d\.\d+) percentage points or more", ch).group(1))
    q = re.search(r"third quarter of (\d{4}), (\d+) (\w+) to (\d+) (\w+) \d{4}", ch)
    reg = pd.read_csv(find(target, "feature_registry"))
    pipe = yaml.safe_load(open(find(target, "search_pipeline")))
    store = yaml.safe_load(open(find(target, "feature_store")))
    stages = {s["name"]: s for s in pipe["stages"]}
    comp = {c["name"]: c["feature_groups"][0] for c in stages["render"]["components"] if c.get("feature_groups")}
    return dict(charter=ch, line=line, quarter=q.groups() if q else None, registry=reg, pipeline=pipe, store=store,
                first_pass=list(stages["rank"]["feature_groups"]), second_pass=list(stages["rerank"]["feature_groups"]),
                components=comp, order=[s["name"] for s in pipe["stages"]])


def painted(starts, ends, n_hours):
    """Hour by hour, the fraction of the hour inside any of the intervals (hours from the start of the year), on a
    grid of seconds."""
    diff = np.zeros(n_hours * 3600 + 1, np.int32)
    for s, e in zip(starts, ends):
        a, b = int(round(max(s, 0.0) * 3600)), int(round(min(e, float(n_hours)) * 3600))
        if b > a:
            diff[a] += 1
            diff[b] -= 1
    return (np.cumsum(diff[:-1]) > 0).reshape(n_hours, 3600).mean(axis=1)


def read(target, first_load=False):
    D = documents(target)
    mk = pd.read_csv(find(target, "markets.csv"))
    MK = list(mk["market"])
    key = dict(zip(mk["mart_market_key"], mk["market"]))
    s = pd.read_csv(find(target, "edge_search_sessions"))
    s["h"] = np.rint(hours(s["hour_utc"])).astype(int)
    H = int(s["h"].max()) + 1
    ND = H // 24
    mi = {m: i for i, m in enumerate(MK)}
    di = {d: i for i, d in enumerate(DEV)}

    def cube(df, col, t="h", n=H):
        out = np.zeros((len(MK), 2, n))
        np.add.at(out, (df["market"].map(mi).to_numpy(), df["device"].map(di).to_numpy(), df[t].to_numpy()),
                  df[col].to_numpy(float))
        return out
    sess = cube(s, "search_sessions")
    R = D["registry"].set_index("feature_group")
    groups = list(R.index)

    # the traffic each source carries
    book = find(target, "feature_source_traffic")
    cf = pd.read_excel(book, sheet_name="chain_feeds")
    ps = pd.read_excel(book, sheet_name="price_sources")
    cp = pd.read_excel(book, sheet_name="clickstream_partitions")
    Wc = np.array([cf["share_%s" % m].fillna(0.0).to_numpy(float) for m in MK])
    Ws = np.array([ps["share_%s" % m].fillna(0.0).to_numpy(float) for m in MK])
    wp = cp["share_of_search_sessions"].to_numpy(float)
    former = [c for c in cf.columns if c.startswith("status_shard_until")][0]
    chain_of = {}
    for i, r in cf.iterrows():
        chain_of[r["status_shard"]] = i
        if isinstance(r[former], str):
            chain_of[r[former]] = i
    source_of = {r["status_shard"]: i for i, r in ps.iterrows()}
    part_of = {r["status_shard"]: i for i, r in cp.iterrows()}

    # the status record, the later load of an hour standing
    st = pd.read_csv(find(target, "feature_status"))
    n_status = len(st)
    st = st.sort_values("loaded_at_utc", kind="stable").drop_duplicates(
        ["hour_utc", "feature_group", "shard"], keep="first" if first_load else "last")
    st["h"] = np.rint(hours(st["hour_utc"])).astype(int)
    st["rate"] = st["unhealthy"] / st["observed"].clip(lower=1)

    def rates(group, index, n):
        k = st[st["feature_group"] == group]
        out = np.zeros((n, H))
        out[k["shard"].map(index).to_numpy(), k["h"].to_numpy()] = k["rate"].to_numpy()
        return out
    status = {}
    r_stock, r_price, r_trend = rates("stock", chain_of, len(cf)), rates("price", source_of, len(ps)), rates("trend", part_of, len(cp))
    status["stock"] = np.repeat((Wc @ r_stock)[:, None, :], 2, axis=1)
    status["price"] = np.repeat((Ws @ r_price)[:, None, :], 2, axis=1)
    status["trend"] = np.broadcast_to(wp @ r_trend, (len(MK), 2, H)).copy()
    rm = rates("match", {"index/replica-%s" % m.lower(): i for i, m in enumerate(MK)}, len(MK))
    status["match"] = np.repeat(rm[:, None, :], 2, axis=1)
    for g in ("promise", "history"):
        k = st[st["feature_group"] == g]
        v = np.zeros(H)
        v[k["h"].to_numpy()] = k["rate"].to_numpy()
        status[g] = np.broadcast_to(v, (len(MK), 2, H)).copy()
    k = st[st["feature_group"] == "seller"]
    v = np.zeros(ND)
    v[k["h"].to_numpy() // 24] = (k["unhealthy"] / k["observed"].clip(lower=1)).to_numpy()
    status["seller"] = np.broadcast_to(np.repeat(v, 24), (len(MK), 2, H)).copy()

    # each source's served state, replayed from its own log
    served, usual = {}, {}
    ttl = {g: float(R.loc[g, "validity_hours"]) for g in groups if not pd.isna(R.loc[g, "validity_hours"])}
    half = float(R.loc["stock", "sync_interval_minutes"]) / 120.0
    window = float(R.loc["trend", "window_hours"])
    gp = pd.read_csv(find(target, "chain_feed_gaps"))
    gs, ge = hours(gp["feed_stopped_at"]), hours(gp["feed_resumed_at"])
    ci = gp["chain_id"].map({c: i for i, c in enumerate(cf["chain_id"])}).to_numpy()
    dc = np.zeros((len(cf), H))
    for c in range(len(cf)):
        m = (ci == c) & (ge - gs > ttl["stock"] - half)
        dc[c] = painted(gs[m] + ttl["stock"] - half, ge[m] + half, H)
    served["stock"] = np.repeat((Wc @ dc)[:, None, :], 2, axis=1)
    bt = pd.read_csv(find(target, "competitor_price_batch"))
    bt["d"] = days(bt["batch_date_utc"])
    region_cols = [c for c in bt.columns if c.startswith("status_")]

    def price_default(col):
        out = np.zeros((len(ps), H))
        hrs = np.arange(H)
        for i, src in enumerate(ps["source"]):
            k = bt[bt["source"] == src]
            loaded = np.full(H, -1.0)
            okd = k.loc[k[col] == "loaded", "d"].to_numpy()
            missing = np.setdiff1d(np.arange(ND), k["d"].to_numpy())          # a day with no row is taken as loaded
            for d in np.concatenate([okd, missing]):
                if d * 24 + 4 < H:
                    loaded[d * 24 + 4] = d * 24 + 4.0
            last = np.maximum(np.maximum.accumulate(loaded), 4.0)
            out[i] = (hrs + 0.5 - last > ttl["price"]).astype(float)
        return out

    def price_failed(col):
        out = np.zeros((len(ps), H))
        for i, src in enumerate(ps["source"]):
            k = bt[(bt["source"] == src) & (bt[col] != "loaded")]
            for d in k["d"].to_numpy():
                out[i, d * 24 + 4:min((d + 1) * 24 + 4, H)] = 1.0
        return out
    dfa = price_default(region_cols[0])
    served["price"] = np.repeat((Ws @ dfa)[:, None, :], 2, axis=1)
    lg = pd.read_csv(find(target, "clickstream_lag"))
    ls, le = hours(lg["lag_started_utc"]), hours(lg["caught_up_utc"])
    pi = lg["partition"].map({c: i for i, c in enumerate(cp["partition"])}).to_numpy()
    ld = np.zeros((len(cp), H))
    for p in range(len(cp)):
        m = (pi == p) & (le - ls > ttl["trend"])
        ld[p] = painted(ls[m] + ttl["trend"], le[m] + window, H)
    served["trend"] = np.broadcast_to(wp @ ld, (len(MK), 2, H)).copy()
    sc = pd.read_csv(find(target, "seller_score_runs"))
    n_scoring = len(sc)
    sc = sc.drop_duplicates()
    tr = pd.read_csv(find(target, "seller_search_traffic"))
    ids = {x: i for i, x in enumerate(sorted(tr["seller_id"].unique()))}
    N = len(ids)
    si, dd = sc["seller_id"].map(ids).to_numpy(), days(sc["effective_date_utc"])
    good = sc["status"].isin(["OK", "scored"]).to_numpy()
    keep_days = int(round(ttl["seller"] / 24.0))

    def stale(rows):
        diff = np.zeros((N, ND + keep_days + 1), np.int32)
        np.add.at(diff, (si[rows], dd[rows]), 1)
        np.add.at(diff, (si[rows], dd[rows] + keep_days), -1)
        return ~(np.cumsum(diff, axis=1)[:, :ND] > 0)
    w = np.zeros((12, N))
    w[tr["month"].str[5:7].astype(int).to_numpy() - 1, tr["seller_id"].map(ids).to_numpy()] = tr["top10_result_impressions"].to_numpy(float)
    w = w / np.maximum(w.sum(axis=1, keepdims=True), 1)
    month_of_day = (T0 + pd.to_timedelta(np.arange(ND), unit="D")).month.to_numpy() - 1
    wd = w[month_of_day].T
    s_act = (wd * stale(good)).sum(axis=0)
    s_all = (wd * stale(np.ones(len(sc), bool))).sum(axis=0)
    served["seller"] = np.broadcast_to(np.repeat(s_act, 24), (len(MK), 2, H)).copy()
    usual["seller"] = np.broadcast_to(np.repeat(s_all, 24), (len(MK), 2, H)).copy()
    for g in ("promise", "history", "match"):
        served[g] = status[g]

    # the cache record, the experiments, the render record, the mart
    cc = pd.read_csv(find(target, "edge_page_cache"))
    cc["d"] = days(cc["date_utc"])
    origin = cube(cc, "built_at_origin", "d", ND) / cube(cc, "result_page_views", "d", ND)
    con = sqlite3.connect(find(target, "experiment_platform"))
    ex = pd.read_sql_query("SELECT * FROM experiment", con)
    dy = pd.read_sql_query("SELECT * FROM experiment_daily", con)
    con.close()
    dy["d"] = days(dy["date_utc"])
    rr = pd.read_csv(find(target, "component_render"))
    rr["h"] = np.rint(hours(rr["hour_utc"])).astype(int)
    eligible = {D["components"][c]: cube(rr[rr["component"] == c], "eligible_sessions") for c in D["components"]}
    failed = {D["components"][c]: cube(rr[rr["component"] == c], "suppressed") for c in D["components"]}
    mart = pd.read_csv(find(target, "mart_search_conversion"))
    mart["market"] = mart["market_key"].map(key)
    mart["device"] = mart["platform"].str.lower()
    mart["d"] = days(mart["business_date_utc"])
    return dict(D=D, MK=MK, H=H, ND=ND, sess=sess, groups=groups, status=status, served=served, usual=usual,
                origin=origin, ex=ex, dy=dy, eligible=eligible, failed=failed, mart=mart, cube=cube, ttl=ttl,
                price_default=price_default, price_failed=price_failed, region_cols=region_cols, Ws=Ws,
                counts=dict(status_rows=n_status, status_rows_kept=len(st), scoring_rows=n_scoring, scoring_runs=len(sc),
                            gaps=len(gp), lag_episodes=len(lg), sellers=N, experiments=len(ex),
                            ablation_tests=int(((ex["kind"] == "feature_ablation") & (ex["status"] == "completed")).sum()),
                            aborted=int((ex["status"] != "completed").sum())))


def run(target, lost=(), first_load=False):
    B = read(target, first_load=first_load)
    D, MK, H, ND, sess = B["D"], B["MK"], B["H"], B["ND"], B["sess"]
    s1, s2, s3 = "S1" in lost, "S2" in lost, "S3" in lost
    q = D["quarter"]
    q0 = int((pd.Timestamp("%s %s %s" % (q[1], q[2], q[0]), tz="UTC") - T0).days)
    q1 = int((pd.Timestamp("%s %s %s" % (q[3], q[4], q[0]), tz="UTC") - T0).days) + 1
    assert q1 * 24 == H, (q1, H)
    # the default share charged to degraded service, and all of it
    tot = {g: (B["status"][g] if s2 else B["served"][g]) for g in B["groups"]}
    exc = dict(tot)
    if not s2:
        exc["seller"] = tot["seller"] - B["usual"]["seller"]
    sd = sess.reshape(len(MK), 2, ND, 24)
    # each group's effect a session at its default, by device
    eff = {}
    done = B["ex"][(B["ex"]["kind"] == "feature_ablation") & (B["ex"]["status"] == "completed")]
    for g in B["groups"]:
        num, den = np.zeros(2), np.zeros(2)
        for eid in done.loc[done["subject"] == g, "experiment_id"]:
            k = B["dy"][B["dy"]["experiment_id"] == eid]
            a = {arm: (B["cube"](k[k["arm"] == arm], "sessions", "d", ND), B["cube"](k[k["arm"] == arm], "orders", "d", ND))
                 for arm in ("held", "control")}
            on = a["held"][0] > 0
            itt = np.zeros_like(a["held"][0])
            itt[on] = 100.0 * (a["control"][1][on] / a["control"][0][on] - a["held"][1][on] / a["held"][0][on])
            dfl = (tot[g].reshape(len(MK), 2, ND, 24) * sd).sum(axis=3) / np.maximum(sd.sum(axis=3), 1)
            share = (B["origin"] if (g in D["first_pass"] and not s1) else 1.0) * (1.0 - np.clip(dfl, 0, 0.9))
            num += (itt * a["held"][0]).sum(axis=(0, 2))
            den += (share * a["held"][0] * on).sum(axis=(0, 2))
        eff[g] = num / den
    # each component: its loss an eligible session by device, and its eligible share in its own test
    per, es = {}, {}
    hold = B["ex"][B["ex"]["kind"] == "component_holdout"]
    for _, e in hold.iterrows():
        g = D["components"][e["subject"]]
        k = B["dy"][B["dy"]["experiment_id"] == e["experiment_id"]]
        tot_arm = {arm: (B["cube"](k[k["arm"] == arm], "sessions", "d", ND).sum(axis=2),
                         B["cube"](k[k["arm"] == arm], "orders", "d", ND).sum(axis=2)) for arm in ("held", "control")}
        el = B["cube"](k[k["arm"] == "control"], "eligible_sessions", "d", ND).sum(axis=2) / tot_arm["control"][0]
        d = 100.0 * (tot_arm["control"][1] / tot_arm["control"][0] - tot_arm["held"][1] / tot_arm["held"][0])
        per[g] = (d * tot_arm["held"][0]).sum(axis=0) / (el * tot_arm["held"][0]).sum(axis=0)
        es[g] = el
    # each group's cost by market, device and hour
    hourly, rank, comp = {}, {}, {}
    for g in B["groups"]:
        rank[g] = eff[g][None, :, None] * exc[g]
        comp[g] = np.zeros_like(rank[g])
        if g in per and not s3:
            comp[g] = per[g][None, :, None] * B["eligible"][g] / np.maximum(sess, 1) * exc[g]
        hourly[g] = rank[g] + comp[g]

    def over(x, d0, d1):
        sl = slice(d0 * 24, d1 * 24)
        return float((x[:, :, sl] * sess[:, :, sl]).sum() / sess[:, :, sl].sum())
    out = dict(counts=B["counts"], line=D["line"], groups=B["groups"])
    out["cost"] = {g: over(hourly[g], q0, q1) for g in B["groups"]}
    out["component_cost"] = {g: over(comp[g], q0, q1) for g in per}
    out["served_pct"] = {g: 100.0 * over(exc[g], q0, q1) for g in B["groups"]}
    out["status_pct"] = {g: 100.0 * over(B["status"][g], q0, q1) for g in B["groups"]}
    dev_w = sess[:, :, q0 * 24:q1 * 24].sum(axis=(0, 2)) / sess[:, :, q0 * 24:q1 * 24].sum()
    out["effect"] = {g: float(eff[g] @ dev_w) for g in B["groups"]}
    months, gm = {}, {g: {} for g in B["groups"]}
    for mth in (7, 8, 9):
        d0 = int((pd.Timestamp(2026, mth, 1, tz="UTC") - T0).days)
        d1 = int((pd.Timestamp(2026, mth + 1, 1, tz="UTC") - T0).days)
        months[MONTH_NAME[mth]] = sum(over(hourly[g], d0, d1) for g in B["groups"])
        for g in B["groups"]:
            gm[g][MONTH_NAME[mth]] = over(hourly[g], d0, d1)
    out["month"], out["group_month"] = months, gm
    out["all"] = sum(out["cost"].values())
    out["list"] = [g for g in B["groups"] if out["cost"][g] >= D["line"]]
    out["listed"] = sum(out["cost"][g] for g in out["list"])
    # April: the region that missed its batches against the other, over the business days touched
    a, b = B["region_cols"]
    gap = (B["price_default"](b) - B["price_default"](a)).mean(axis=0)
    fgap = (B["price_failed"](b) - B["price_failed"](a)).mean(axis=0)
    touched = np.unique(np.nonzero((gap != 0) | (fgap != 0))[0] // 24)
    win = np.zeros(H, bool)
    for d in touched:
        win[d * 24:(d + 1) * 24] = True
    what = eff["price"][None, :] + (0.0 if s3 else per["price"][None, :] * es["price"])
    n = sess[:, :, win]
    out["april_called"] = float((n * what[:, :, None] * (fgap if s2 else gap)[win][None, None, :]).sum() / n.sum())
    m = B["mart"][B["mart"]["d"].isin(touched)]
    conv = m.groupby("serving_region")[["attributed_orders", "search_sessions"]].sum()
    ra, rb = a.replace("status_", ""), b.replace("status_", "")
    out["april_record"] = 100.0 * float(conv.loc[ra, "attributed_orders"] / conv.loc[ra, "search_sessions"] -
                                        conv.loc[rb, "attributed_orders"] / conv.loc[rb, "search_sessions"])
    out["april_days"] = int(len(touched))
    return out


def compare(v, fig, routes=None):
    """Every figure the verifier shares with figures.json: (label, verifier, figures.json, agrees)."""
    out = []

    def add(lab, a, c, tol):
        out.append((lab, round(float(a), 5), c, abs(float(a) - float(c)) <= tol))
    for g in v["groups"]:
        add("cost %s" % g, v["cost"][g], fig["cost"][g], 0.00051)
        add("effect %s" % g, v["effect"][g], fig["full_effect"][g], 0.0051)
        add("served %s" % g, v["served_pct"][g], fig["served_default_pct"][g], 0.0051)
        add("status %s" % g, v["status_pct"][g], fig["status_unhealthy_pct"][g], 0.0051)
        for mth, x in v["group_month"][g].items():
            add("cost %s %s" % (g, mth), x, fig["group_month"][g][mth], 0.000051)
    for g, x in v["component_cost"].items():
        add("component cost %s" % g, x, fig["reader_cost"][g], 0.00051)
    for mth, x in v["month"].items():
        add("month %s" % mth, x, fig["month"][mth], 0.0051)
    add("all groups", v["all"], fig["all"], 0.0051)
    add("listed groups", v["listed"], fig["listed_cost"], 0.0051)
    add("C1", v["effect"]["trend"], fig["c1"], 0.0051)
    add("C2", v["served_pct"]["seller"], fig["c2"], 0.0051)
    add("C3", v["component_cost"]["promise"], fig["c3"], 0.00051)
    add("C4", v["april_called"], fig["c4"], 0.00051)
    add("April in the mart", v["april_record"], fig["april"]["record"], 0.00051)
    add("April's days", v["april_days"], fig["april"]["days"], 0)
    out.append(("the list", v["list"], fig["list"], v["list"] == fig["list"]))
    for key_, c in v["counts"].items():
        add("count %s" % key_, c, fig["counts"][key_], 0)
    for name, r in (routes or {}).items():
        for g in r["groups"]:
            add("%s lost: cost %s" % (name, g), r["cost"][g], fig["routes"][name]["cost"][g], 0.00051)
        out.append(("%s lost: the list" % name, r["list"], fig["routes"][name]["list"], r["list"] == fig["routes"][name]["list"]))
        add("%s lost: April" % name, r["april_called"],
            fig["april"]["rivals"]["every stump lost" if name == "S1+S2+S3" else "%s lost" % name]["value"], 0.00051)
    return out


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    v = run(tgt)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    routes = {k: run(tgt, lost=tuple(k.split("+"))) for k in ("S1", "S2", "S3", "S1+S2+S3")}
    rows = compare(v, fig, routes)
    bad = [r for r in rows if not r[3]]
    for lab, a, c, same in bad:
        print("FAIL  %s: verifier %s, figures.json %s" % (lab, a, c))
    print("verify: %d figures compared, %d disagree; the list %s" % (len(rows), len(bad), ", ".join(v["list"])))
    sys.exit(1 if bad else 0)
