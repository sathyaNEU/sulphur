"""Read the pack back into the arrays the core's estimators take: nothing here knows the core's world, only the
shipped files. The hygiene every route does is done here (the monitor's reloaded rows, renamed shards, rows the
scoring writer wrote twice, the two status vocabularies, the aborted test, the mart's market keys, local times)."""
import os
import sqlite3

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import core as C
import world as WL

F = WL.FILES
H, DAYS = C.H, C.DAYS
T0 = pd.Timestamp("2026-01-01", tz="UTC")
CELL = {(C.MARKETS[m], C.DEVICES[d]): i for i, (m, d) in enumerate(C.CELLS)}
GOOD = {"OK": True, "scored": True, "FAIL": False, "failed": False}


def hours_of(col):
    """Hours from the start of 2026 (a float) of a column of timestamps, with or without an offset."""
    t = pd.to_datetime(col, utc=True)
    return ((t - T0).dt.total_seconds() / 3600.0).to_numpy(float)


def hour_index(col):
    return np.rint(hours_of(col)).astype(int)


def day_index(col):
    return np.rint((pd.to_datetime(col) - pd.Timestamp("2026-01-01")).dt.total_seconds() / 86400.0).to_numpy().astype(int)


def grid(df, value, hours=True):
    """A (12, hours or days) array from long rows carrying market, device and an index column `i`."""
    out = np.zeros((12, H if hours else DAYS))
    c = np.array([CELL[k] for k in zip(df["market"], df["device"])])
    np.add.at(out, (c, df["i"].to_numpy()), df[value].to_numpy(float))
    return out


def on_hour0(a):
    """Daily totals laid on the first hour of each day, so the core's hourly sums see the daily record."""
    out = np.zeros((a.shape[0], H))
    out[:, ::24] = a
    return out


def load(target, keep_first_status=False, keep_aborted=False, keep_repeats=False):
    p = lambda k: os.path.join(target, F[k])   # noqa: E731
    info = {}
    hod, day = np.arange(H) % 24, np.arange(H) // 24
    W = dict(hod=hod, day=day, dow=(day + 3) % 7)

    # ---- sessions by hour (the edge log) and the nightly mart by business day and serving region
    s = pd.read_csv(p("sessions"))
    s["i"] = hour_index(s["hour_utc"])
    W["sess"] = grid(s, "search_sessions")
    mk = pd.read_csv(p("markets"))
    key = dict(zip(mk["mart_market_key"], mk["market"]))
    m = pd.read_csv(p("mart"))
    m["market"] = m["market_key"].map(key)
    m["device"] = m["platform"].str.lower()
    m["i"] = day_index(m["business_date_utc"])
    reg = {}
    for r in WL.REGIONS:
        k = m[m["serving_region"] == r]
        reg[r] = (grid(k, "search_sessions", False), grid(k, "attributed_orders", False))
    W["orders"] = on_hour0(reg[WL.REGIONS[0]][1] + reg[WL.REGIONS[1]][1])
    info["mart_sessions_match"] = bool(np.array_equal(reg[WL.REGIONS[0]][0] + reg[WL.REGIONS[1]][0],
                                                     W["sess"].reshape(12, DAYS, 24).sum(axis=2)))
    pr = pd.read_csv(p("promo"))
    promo = np.zeros((6, DAYS), bool)
    promo[[C.MARKETS.index(x) for x in pr["market"]], day_index(pr["date_utc"])] = True
    W["promo"] = promo

    # ---- the traffic each source carries
    wb = load_workbook(p("shares"), read_only=True, data_only=True)
    rows = list(wb["chain_feeds"].iter_rows(values_only=True))
    chains = [r[0] for r in rows[1:]]
    Wc = np.array([[float(r[4 + mi] or 0.0) for r in rows[1:]] for mi in range(6)])
    shard_chain = {}
    for ki, r in enumerate(rows[1:]):
        shard_chain[r[2]] = ki
        if r[3]:
            shard_chain[r[3]] = ki
    rows = list(wb["price_sources"].iter_rows(values_only=True))
    sources = [r[0] for r in rows[1:]]
    Ws = np.array([[float(r[2 + mi]) for r in rows[1:]] for mi in range(6)])
    shard_source = {r[1]: i for i, r in enumerate(rows[1:])}
    rows = list(wb["clickstream_partitions"].iter_rows(values_only=True))
    parts = [r[0] for r in rows[1:]]
    wp = np.array([float(r[2]) for r in rows[1:]])
    shard_part = {r[1]: i for i, r in enumerate(rows[1:])}

    # ---- the monitor's status rows: the later load of an hour stands
    st = pd.read_csv(p("status"))
    info["status_rows"] = len(st)
    st = st.sort_values("loaded_at_utc", kind="stable")
    st = st.drop_duplicates(["hour_utc", "feature_group", "shard"], keep="first" if keep_first_status else "last")
    info["status_rows_kept"] = len(st)
    st["i"] = hour_index(st["hour_utc"])
    st["rate"] = st["unhealthy"] / st["observed"].clip(lower=1)
    S = {}

    def shards(group, index, n):
        k = st[st["feature_group"] == group]
        out = np.zeros((n, H))
        out[k["shard"].map(index).to_numpy(), k["i"].to_numpy()] = k["rate"].to_numpy()
        return out
    unavail = shards("stock", shard_chain, len(chains))
    st_src = shards("price", shard_source, len(sources))
    lag_s = shards("trend", shard_part, len(parts))
    em = shards("match", {WL.shard_of("match", mi): mi for mi in range(6)}, 6)
    S["stock"] = np.array([Wc[mi] @ unavail for mi, d in C.CELLS])
    S["price"] = np.array([Ws[mi] @ st_src for mi, d in C.CELLS])
    S["trend"] = np.tile(wp @ lag_s, (12, 1))
    S["match"] = np.array([em[mi] for mi, d in C.CELLS])
    for g in ("promise", "history"):
        k = st[st["feature_group"] == g]
        v = np.zeros(H)
        v[k["i"].to_numpy()] = k["rate"].to_numpy()
        S[g] = np.tile(v, (12, 1))
    k = st[st["feature_group"] == "seller"]
    due, failed = np.zeros(DAYS), np.zeros(DAYS)
    due[k["i"].to_numpy() // 24] = k["observed"].to_numpy()
    failed[k["i"].to_numpy() // 24] = k["unhealthy"].to_numpy()
    S["seller"] = np.tile(np.repeat(failed / np.maximum(due, 1), 24), (12, 1))
    W["S"] = S
    logs = {}

    # ---- stock: the feed gap log (wall clock with its offset) and the two-hour snapshot
    g = pd.read_csv(p("gaps"))
    gs, ge = hours_of(g["feed_stopped_at"]), hours_of(g["feed_resumed_at"])
    gk = g["chain_id"].map({c: i for i, c in enumerate(chains)}).to_numpy()
    gaps = list(zip(gk.tolist(), gs.tolist(), ge.tolist()))
    ttl = 2.0
    default_c = np.array([C.cover([(a + ttl - 0.125, b + 0.125) for kk, a, b in gaps if kk == ki and b - a > ttl - 0.125])
                          for ki in range(len(chains))])
    logs["stock"] = dict(Wc=Wc, gaps=gaps, unavail=unavail, default_c=default_c)
    info["gaps"] = len(gaps)

    # ---- price: the batch log by serving region, a price served 36 hours after its batch
    b = pd.read_csv(p("batches"))
    bd = day_index(b["batch_date_utc"])
    bs = b["source"].map({c: i for i, c in enumerate(sources)}).to_numpy()

    def state(col):
        ok = np.ones((len(sources), DAYS), bool)
        ok[bs, bd] = (b[col] == "loaded").to_numpy()
        stt, dft = np.zeros((len(sources), H)), np.zeros((len(sources), H))
        for si in range(len(sources)):
            last = 4.0
            for h in range(H):
                dd, hh = divmod(h, 24)
                d0 = dd if hh >= 4 else dd - 1
                if d0 >= 0 and ok[si, d0]:
                    last = d0 * 24 + 4.0
                stt[si, h] = 0.0 if (d0 < 0 or ok[si, d0]) else 1.0
                dft[si, h] = 1.0 if h + 0.5 - last > 36.0 else 0.0
        return ok, stt, dft
    ok_a, st_a, df_a = state("status_%s" % WL.REGIONS[0])
    ok_b, st_b, df_b = state("status_%s" % WL.REGIONS[1])
    logs["price"] = dict(Ws=Ws, ok=ok_a, df_src=df_a, st_src=st_src, st_log=st_a)
    info["status_matches_batch_log"] = bool(np.array_equal(st_src, st_a))
    sp_def, sp_stat = (df_b - df_a).mean(axis=0), (st_b - st_a).mean(axis=0)
    days_hit = np.unique(np.nonzero((sp_def != 0) | (sp_stat != 0))[0] // 24)
    win = np.zeros(H, bool)
    for dd in days_hit:
        win[dd * 24:(dd + 1) * 24] = True
    A, B = WL.REGIONS
    W["split"] = dict(window=win, default=sp_def, status=sp_stat, na=on_hour0(reg[A][0]), oa=on_hour0(reg[A][1]),
                      nb=on_hour0(reg[B][0]), ob=on_hour0(reg[B][1]))
    info["split_days"] = [int(x) for x in days_hit]
    info["split_batches"] = int((~ok_b & ok_a).any(axis=0).sum())

    # ---- trend: the lag episodes, a counter served six hours and back one window after catch-up
    lg = pd.read_csv(p("lags"))
    ls, le = hours_of(lg["lag_started_utc"]), hours_of(lg["caught_up_utc"])
    lp = lg["partition"].map({c: i for i, c in enumerate(parts)}).to_numpy()
    eps = list(zip(lp.tolist(), ls.tolist(), le.tolist()))
    lag_d = np.array([C.cover([(a + 6.0, e + 1.0) for pp, a, e in eps if pp == pi and e - a > 6.0]) for pi in range(len(parts))])
    logs["trend"] = dict(wp=wp, eps=eps, lag_d=lag_d, lag_s=lag_s)
    info["lag_episodes"] = len(eps)

    # ---- seller: the scoring log replayed seller by seller; a score is served five days
    sc = pd.read_csv(p("scoring"))
    info["scoring_rows"] = len(sc)
    if not keep_repeats:
        sc = sc.drop_duplicates()
    info["scoring_runs"] = len(sc)
    tr = pd.read_csv(p("seller_traffic"))
    ids = np.sort(tr["seller_id"].unique())
    pos = {x: i for i, x in enumerate(ids)}
    n = len(ids)
    si, di = sc["seller_id"].map(pos).to_numpy(), day_index(sc["effective_date_utc"])
    good = sc["status"].map(GOOD).to_numpy(bool)
    dirty, fail = np.zeros((n, DAYS), bool), np.zeros((n, DAYS), bool)
    dirty[si, di] = True
    fail[si[~good], di[~good]] = True

    def served_default(scored):
        idx = np.where(scored, np.arange(DAYS)[None, :], -10 ** 6)
        last = np.maximum.accumulate(idx, axis=1)
        return (np.arange(DAYS)[None, :] - last) > 4
    mw = np.zeros((9, n))
    mi_ = tr["month"].str[5:7].astype(int).to_numpy() - 1
    mw[mi_, tr["seller_id"].map(pos).to_numpy()] = tr["top10_result_impressions"].to_numpy(float)
    mw = mw / mw.sum(axis=1, keepdims=True)
    logs["seller"] = dict(mw=mw, dirty=dirty, fail=fail, d_act=served_default(dirty & ~fail), d_cf=served_default(dirty),
                          due=dirty.sum(axis=0), failed=(dirty & fail).sum(axis=0), ids=ids)
    info["status_matches_scoring_log"] = bool(np.array_equal(logs["seller"]["due"], due) and
                                              np.array_equal(logs["seller"]["failed"], failed))
    info["sellers"] = n
    W["logs"] = logs

    # ---- the edge cache: the share of result page views built at origin
    cc = pd.read_csv(p("cache"))
    cc["i"] = day_index(cc["date_utc"])
    W["u"] = grid(cc, "built_at_origin", False) / grid(cc, "result_page_views", False)

    # ---- the experiment platform: completed ablation tests day by day, and the component holdouts
    con = sqlite3.connect(p("experiments"))
    ex = pd.read_sql_query("SELECT * FROM experiment", con)
    dy = pd.read_sql_query("SELECT * FROM experiment_daily", con)
    con.close()
    info["experiments"] = len(ex)
    info["aborted"] = int((ex["status"] != "completed").sum())
    dy["d"] = day_index(dy["date_utc"])
    tests, count = [], {}
    use = ex if keep_aborted else ex[ex["status"] == "completed"]
    for _, e in use[use["kind"] == "feature_ablation"].sort_values("start_date").iterrows():
        k = dy[dy["experiment_id"] == e["experiment_id"]]
        d0, d1 = int(k["d"].min()), int(k["d"].max()) + 1
        arr = {}
        for arm, a, o in (("held", "nh", "oh"), ("control", "nc", "oc")):
            q = k[k["arm"] == arm].assign(i=lambda z: z["d"] - d0)
            ns, os_ = np.zeros((12, d1 - d0)), np.zeros((12, d1 - d0))
            c = np.array([CELL[x] for x in zip(q["market"], q["device"])])
            ns[c, q["i"].to_numpy()] = q["sessions"].to_numpy()
            os_[c, q["i"].to_numpy()] = q["orders"].to_numpy()
            arr[a], arr[o] = ns, os_
        g_ = e["subject"]
        count[g_] = count.get(g_, 0) + 1
        tests.append(dict(group=g_, k=count[g_] - 1, d0=d0, d1=d1, id=e["experiment_id"], **arr))
    W["tests"] = tests
    info["ablation_tests"] = len(tests)
    comp = {v: k for k, v in WL.COMPONENT.items()}
    rtest = {}
    for _, e in ex[ex["kind"] == "component_holdout"].iterrows():
        k = dy[dy["experiment_id"] == e["experiment_id"]]
        out = {}
        for arm, a, o in (("held", "nh", "oh"), ("control", "nc", "oc")):
            q = k[k["arm"] == arm]
            c = np.array([CELL[x] for x in zip(q["market"], q["device"])])
            ns, os_, el = np.zeros(12), np.zeros(12), np.zeros(12)
            np.add.at(ns, c, q["sessions"].to_numpy(float))
            np.add.at(os_, c, q["orders"].to_numpy(float))
            out[a], out[o] = ns, os_
            if arm == "control":
                np.add.at(el, c, q["eligible_sessions"].to_numpy(float))
                out["elig_c"] = el
        rtest[comp[e["subject"]]] = out
    W["rtest"] = rtest

    # ---- the components' render record
    rr = pd.read_csv(p("render"))
    rr["i"] = hour_index(rr["hour_utc"])
    render = {}
    for name, g_ in comp.items():
        k = rr[rr["component"] == name]
        render[g_] = dict(eligible=grid(k, "eligible_sessions"), suppressed=grid(k, "suppressed"))
    W["render"] = render
    info["render_rows"] = len(rr)

    # ---- the registry
    rg = pd.read_csv(p("registry"))
    info["registry"] = {r["feature_group"]: dict(stage=r["pipeline_stage"],
                                                 validity=None if pd.isna(r["validity_hours"]) else float(r["validity_hours"]))
                        for _, r in rg.iterrows()}
    info["session_rows"], info["mart_rows"] = len(s), len(m)
    return W, info


if __name__ == "__main__":
    import sys
    W, info = load(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target"))
    print({k: v for k, v in info.items() if k != "registry"})
    v = C.view(W)
    print({j: round(x, 4) for j, x in v["loss"].items()}, round(v["total"], 4), round(v["tier"], 4))
    print("months", {k: round(x, 3) for k, x in v["month"].items()}, "c1", v["c1"], "c2", v["c2"], "c3", v["c3"],
          "april", v["split"], C.split_measured(W))
