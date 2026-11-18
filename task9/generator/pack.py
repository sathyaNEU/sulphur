"""The data files of the pack, each written from the core's world the way its own system would export it: the edge
log's hourly sessions, the nightly conversion mart, the monitor's status rows, the jobs' own logs, the experiment
platform's database, the edge cache's daily record and the components' render record. The only randomness here is
texture (request counts, load times, run times, repeated rows) on its own stream: no array of the core is redrawn."""
import os
import sqlite3

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

import core as C
import world as WL

PSEED = 910401
F = WL.FILES
H, DAYS = C.H, C.DAYS
MK, DV = C.MARKETS, C.DEVICES
CELL_M = np.array([m for m, d in C.CELLS])
CELL_D = np.array([d for m, d in C.CELLS])
HOURS = np.array([WL.hour_utc(h) for h in range(H)])
DATES = np.array([WL.date_of(d).isoformat() for d in range(DAYS)])
VOCAB_DAY = 153                                    # 3 June: the scoring job's logging library upgraded
RESTATED = (138, 145)                              # 18 to 24 May: the monitor dropped probes and reloaded the week
ABORTED = dict(group="trend", k=4, days=(126, 128), held=0.004)


def daily(a):
    return a.reshape(a.shape[0], DAYS, 24).sum(axis=2)


def put(path, df, sep=",", crlf=False):
    df.to_csv(path, index=False, sep=sep, lineterminator="\r\n" if crlf else "\n")
    return len(df)


def sessions(W, target):
    df = pd.DataFrame({"hour_utc": np.repeat(HOURS, 12), "market": np.tile(np.array(MK)[CELL_M], H),
                       "device": np.tile(np.array(DV)[CELL_D], H),
                       "search_sessions": W["sess"].T.astype(int).ravel()})
    return put(os.path.join(target, F["sessions"]), df)


def mart(W, target):
    sp = W["split"]
    parts = []
    for r, (n, o) in enumerate(((sp["na"], sp["oa"]), (sp["nb"], sp["ob"]))):
        nd, od = daily(n), daily(o)
        parts.append(pd.DataFrame({"business_date_utc": np.tile(DATES, 12),
                                   "market_key": np.repeat([WL.MART_KEY[MK[m]] for m in CELL_M], DAYS),
                                   "platform": np.repeat([DV[d].upper() for d in CELL_D], DAYS),
                                   "serving_region": WL.REGIONS[r],
                                   "search_sessions": nd.ravel().astype(int),
                                   "attributed_orders": od.ravel().astype(int)}))
    df = pd.concat(parts).sort_values(["business_date_utc", "market_key", "platform", "serving_region"], kind="stable")
    return put(os.path.join(target, F["mart"]), df, crlf=True)


def status(W, target, rng):
    L, S = W["logs"], W["S"]
    tot = W["sess"].sum(axis=0)
    blocks = []

    def timed(group, k, frac, days=None):
        hs = np.arange(H)
        shard = np.array([WL.shard_of(group, k, d) for d in range(DAYS)])[hs // 24]
        blocks.append(pd.DataFrame({"h": hs, "feature_group": group, "shard": shard, "basis": "seconds",
                                    "observed": 3600, "unhealthy": np.rint(frac * 3600).astype(int)}))

    for k in range(L["stock"]["unavail"].shape[0]):
        timed("stock", k, L["stock"]["unavail"][k])
    for k in range(L["price"]["st_src"].shape[0]):
        timed("price", k, L["price"]["st_src"][k])
    for k in range(L["trend"]["lag_s"].shape[0]):
        timed("trend", k, L["trend"]["lag_s"][k])
    for m in range(6):
        timed("match", m, S["match"][2 * m])
    for group, per in (("promise", 2.4), ("history", 5.1)):
        req = np.maximum(rng.poisson(tot * per * np.exp(rng.normal(0, 0.03, H))), 1)
        blocks.append(pd.DataFrame({"h": np.arange(H), "feature_group": group, "shard": WL.shard_of(group, 0),
                                    "basis": "requests", "observed": req,
                                    "unhealthy": rng.binomial(req, np.clip(S[group][0], 0, 1))}))
    sl = L["seller"]
    blocks.append(pd.DataFrame({"h": np.arange(DAYS) * 24, "feature_group": "seller", "shard": WL.shard_of("seller", 0),
                                "basis": "runs", "observed": sl["due"].astype(int), "unhealthy": sl["failed"].astype(int)}))
    df = pd.concat(blocks, ignore_index=True)
    n = len(df)
    load = df["h"].to_numpy() * 3600 + 3600 + 240 + rng.integers(0, 300, n)
    late = rng.random(n) < 0.003
    load = load + np.where(late, rng.integers(3 * 3600, 40 * 3600, n), 0)
    df["load_s"] = load
    # the week the monitor lost part of its probes: the rows it first loaded, and the reload nine days later
    a, b = RESTATED
    wk = df["feature_group"].isin(["trend", "match"]) & (df["h"] >= a * 24) & (df["h"] < b * 24)
    full = df[wk].copy()
    kept = rng.uniform(0.45, 0.8, H)[df.loc[wk, "h"].to_numpy()]
    obs = np.rint(3600 * kept).astype(int)
    df.loc[wk, "unhealthy"] = np.rint(df.loc[wk, "unhealthy"].to_numpy() * obs / 3600.0).astype(int)
    df.loc[wk, "observed"] = obs
    full["load_s"] = (b + 2) * 86400 + 9 * 3600 + 1260 + np.arange(len(full)) // 40
    df = pd.concat([df, full], ignore_index=True)
    df["hour_utc"] = HOURS[df["h"].to_numpy()]
    df["loaded_at_utc"] = (pd.Timestamp("2026-01-01") + pd.to_timedelta(df["load_s"], unit="s")).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    df = df.sort_values(["h", "feature_group", "shard", "load_s"], kind="stable")
    return put(os.path.join(target, F["status"]),
               df[["hour_utc", "feature_group", "shard", "basis", "observed", "unhealthy", "loaded_at_utc"]])


def gaps(W, target, rng):
    rows = []
    for k, s, e in sorted(W["logs"]["stock"]["gaps"], key=lambda g: (g[1], g[0])):
        how = "gateway_alarm" if (k in WL.MIGRATING and s >= WL.GATEWAY_DAY * 24 and rng.random() < 0.7) else \
            ("partner_notice" if rng.random() < 0.12 else "heartbeat")
        rows.append(("chn-%02d" % (k + 1), WL.stamp_local(s), WL.stamp_local(e), how))
    df = pd.DataFrame(rows, columns=["chain_id", "feed_stopped_at", "feed_resumed_at", "detected_by"])
    return put(os.path.join(target, F["gaps"]), df)


def batches(W, target, rng):
    ok = W["logs"]["price"]["ok"]
    rows = []
    size = (41000, 33500, 22800, 18900, 15200)
    for dd in range(DAYS):
        for s in range(ok.shape[0]):
            good = bool(ok[s, dd])
            start = dd * 24 + 4 + rng.uniform(0.002, 0.03)
            a = "loaded" if good else "failed"
            b = "not_replicated" if (good and dd in C.SPLIT["days"]) else a
            rows.append((DATES[dd], WL.SOURCES[s], WL.stamp_utc(start),
                         int(size[s] * (1 + 0.0006 * dd) * np.exp(rng.normal(0, 0.04))) if good else 0, a, b))
    df = pd.DataFrame(rows, columns=["batch_date_utc", "source", "started_at_utc", "prices_loaded",
                                     "status_%s" % WL.REGIONS[0], "status_%s" % WL.REGIONS[1]])
    return put(os.path.join(target, F["batches"]), df)


def lags(W, target, rng):
    rows = []
    for p, s, e in sorted(W["logs"]["trend"]["eps"], key=lambda g: (g[1], g[0])):
        rows.append(("p%02d" % p, WL.stamp_utc(s), WL.stamp_utc(e), int(round((e - s) * 60 * rng.uniform(0.55, 0.98)))))
    df = pd.DataFrame(rows, columns=["partition", "lag_started_utc", "caught_up_utc", "peak_lag_minutes"])
    return put(os.path.join(target, F["lags"]), df)


def seller_ids(rng):
    return np.array(["S%06d" % x for x in 100000 + rng.permutation(C.N_SELLERS * 3)[:C.N_SELLERS]])


def scoring(W, target, rng, sid):
    sl = W["logs"]["seller"]
    dd, ss = np.nonzero(sl["dirty"].T)
    failed = sl["fail"][ss, dd]
    old = dd < VOCAB_DAY
    st = np.where(failed, np.where(old, "FAIL", "failed"), np.where(old, "OK", "scored"))
    act = sl["dirty"].mean(axis=1)
    orders = 1 + rng.poisson(0.4 + 6.0 * act[ss] ** 2)
    slow = failed & sl["legacy"][ss] & (dd >= C.SELLER_WINDOW[0]) & (dd < C.SELLER_WINDOW[1])
    run = np.where(slow, 30000 + rng.integers(0, 40, len(dd)),
                   np.where(failed, rng.integers(900, 21000, len(dd)), np.rint(rng.lognormal(np.log(420), 0.5, len(dd)))))
    df = pd.DataFrame({"effective_date_utc": DATES[dd], "seller_id": sid[ss], "new_settled_orders": orders,
                       "status": st, "runtime_ms": run.astype(int)})
    rep = np.sort(rng.choice(len(df), int(0.0015 * len(df)), replace=False))      # rows the writer retried and wrote twice
    idx = np.sort(np.concatenate([np.arange(len(df)), rep]), kind="stable")
    return put(os.path.join(target, F["scoring"]), df.iloc[idx]), len(df)


def seller_traffic(W, target, sid):
    mw = W["logs"]["seller"]["mw"]
    sd = daily(W["sess"]).sum(axis=0)
    parts = []
    for k in range(9):
        total = 10.0 * sd[C.MONTH_START[k]:C.MONTH_START[k + 1]].sum()
        parts.append(pd.DataFrame({"month": "2026-%02d" % (k + 1), "seller_id": sid,
                                   "top10_result_impressions": np.rint(mw[k] * total).astype(np.int64)}))
    df = pd.concat(parts).sort_values(["month", "seller_id"], kind="stable")
    return put(os.path.join(target, F["seller_traffic"]), df)


def shares(W, target):
    L = W["logs"]
    wb = Workbook()
    ws = wb.active
    ws.title = "chain_feeds"
    ws.append(["chain_id", "chain", "status_shard", "status_shard_until_2026-07-05"] + ["share_%s" % m for m in MK])
    for k, name in enumerate(WL.CHAINS):
        ws.append(["chn-%02d" % (k + 1), name, WL.shard_of("stock", k, DAYS - 1),
                   WL.shard_of("stock", k, 0) if k in WL.MIGRATING else None]
                  + [round(float(L["stock"]["Wc"][m, k]), 6) or None for m in range(6)])
    ws2 = wb.create_sheet("price_sources")
    ws2.append(["source", "status_shard"] + ["share_%s" % m for m in MK])
    for s, name in enumerate(WL.SOURCES):
        ws2.append([name, WL.shard_of("price", s)] + [round(float(L["price"]["Ws"][m, s]), 6) for m in range(6)])
    ws3 = wb.create_sheet("clickstream_partitions")
    ws3.append(["partition", "status_shard", "share_of_search_sessions"])
    for p, x in enumerate(L["trend"]["wp"]):
        ws3.append(["p%02d" % p, WL.shard_of("trend", p), round(float(x), 6)])
    for sh, widths in ((ws, [10, 20, 16, 30] + [10] * 6), (ws2, [24, 30] + [10] * 6), (ws3, [12, 16, 26])):
        for c in sh[1]:
            c.font = Font(bold=True)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        for i, wd in enumerate(widths):
            sh.column_dimensions[chr(65 + i)].width = wd
        sh.freeze_panes = "A2"
    wb.save(os.path.join(target, F["shares"]))
    return 14 + 5 + 24


def experiments(W, target, rng):
    path = os.path.join(target, F["experiments"])
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("PRAGMA page_size = 4096")
    cur.execute("CREATE TABLE experiment (experiment_id TEXT PRIMARY KEY, kind TEXT NOT NULL, subject TEXT NOT NULL, "
                "start_date TEXT NOT NULL, end_date TEXT NOT NULL, status TEXT NOT NULL, held_pct REAL, control_pct REAL, "
                "owner TEXT)")
    cur.execute("CREATE TABLE experiment_daily (experiment_id TEXT NOT NULL REFERENCES experiment(experiment_id), "
                "date_utc TEXT NOT NULL, market TEXT NOT NULL, device TEXT NOT NULL, arm TEXT NOT NULL, "
                "sessions INTEGER NOT NULL, eligible_sessions INTEGER, orders INTEGER NOT NULL)")
    exps, rows = [], []
    sd, od = daily(W["sess"]), daily(W["orders"])

    def add(eid, d0, arm, n, o, el=None):
        for c in range(12):
            for i in range(n.shape[1]):
                rows.append((eid, DATES[d0 + i], MK[CELL_M[c]], DV[CELL_D[c]], arm, int(n[c, i]),
                             None if el is None else int(el[c, i]), int(o[c, i])))

    tests = sorted(W["tests"], key=lambda t: (t["d0"], t["group"]))
    seq = 2600
    order = []
    for t in tests:
        order.append(("abl", t))
    for j in C.READERS:
        order.append(("hold", j))
    order.sort(key=lambda x: x[1]["d0"] if x[0] == "abl" else C.READER_TEST[x[1]][0])
    for kind, t in order:
        if kind == "abl" and t["group"] == ABORTED["group"] and t["k"] == ABORTED["k"]:
            a0, a1 = ABORTED["days"]
            seq += int(rng.integers(1, 4))
            eid = "EXP-%d" % seq
            nh = rng.binomial(sd[:, a0:a1].astype(int), ABORTED["held"])
            nc = rng.binomial(sd[:, a0:a1].astype(int), C.HELD)
            rate = od[:, a0:a1] / sd[:, a0:a1]
            exps.append((eid, "feature_ablation", ABORTED["group"], DATES[a0], DATES[a1 - 1], "aborted",
                         100 * ABORTED["held"], 100 * C.HELD, WL.PEOPLE["experiments"]))
            add(eid, a0, "held", nh, rng.binomial(nh, rate))
            add(eid, a0, "control", nc, rng.binomial(nc, rate))
        seq += int(rng.integers(1, 4))
        eid = "EXP-%d" % seq
        if kind == "abl":
            exps.append((eid, "feature_ablation", t["group"], DATES[t["d0"]], DATES[t["d1"] - 1], "completed",
                         100 * C.HELD, 100 * C.HELD, WL.PEOPLE["experiments"]))
            add(eid, t["d0"], "held", t["nh"], t["oh"])
            add(eid, t["d0"], "control", t["nc"], t["oc"])
        else:
            d0, d1 = C.READER_TEST[t]
            r = W["rtest"][t]
            wts = sd[:, d0:d1] / sd[:, d0:d1].sum(axis=1, keepdims=True)
            split = lambda v: np.array([rng.multinomial(int(v[c]), wts[c]) for c in range(12)])   # noqa: E731
            nh, nc = split(r["nh"]), split(r["nc"])
            oh, oc, el = split(r["oh"]), split(r["oc"]), split(r["elig_c"])
            assert (oh <= nh).all() and (oc <= nc).all() and (el <= nc).all()
            exps.append((eid, "component_holdout", WL.COMPONENT[t], DATES[d0], DATES[d1 - 1], "completed",
                         100 * C.READER_HELD, 100 * C.READER_HELD, WL.PEOPLE["experiments"]))
            add(eid, d0, "held", nh, oh)
            add(eid, d0, "control", nc, oc, el)
    cur.executemany("INSERT INTO experiment VALUES (?,?,?,?,?,?,?,?,?)", exps)
    cur.executemany("INSERT INTO experiment_daily VALUES (?,?,?,?,?,?,?,?)", rows)
    cur.execute("CREATE INDEX experiment_daily_by_experiment ON experiment_daily (experiment_id, date_utc)")
    con.commit()
    cur.execute("VACUUM")
    con.commit()
    con.close()
    return len(rows)


def cache(W, target, rng):
    sd = daily(W["sess"])
    ppv = np.array([(2.55, 2.20)[d] + rng.uniform(-0.1, 0.1) for m, d in C.CELLS])
    views = np.rint(sd * ppv[:, None] * np.exp(rng.normal(0, 0.02, sd.shape))).astype(np.int64)
    fresh = np.rint(W["u"] * views).astype(np.int64)
    df = pd.DataFrame({"date_utc": np.tile(DATES, 12), "market": np.repeat(np.array(MK)[CELL_M], DAYS),
                       "device": np.repeat(np.array(DV)[CELL_D], DAYS), "result_page_views": views.ravel(),
                       "served_from_cache": (views - fresh).ravel(), "built_at_origin": fresh.ravel()})
    df = df.sort_values(["date_utc", "market", "device"], kind="stable")
    return put(os.path.join(target, F["cache"]), df)


def render(W, target):
    parts = []
    for j in C.READERS:
        r = W["render"][j]
        parts.append(pd.DataFrame({"h": np.repeat(np.arange(H), 12), "component": WL.COMPONENT[j],
                                   "market": np.tile(np.array(MK)[CELL_M], H), "device": np.tile(np.array(DV)[CELL_D], H),
                                   "eligible_sessions": r["eligible"].T.astype(int).ravel(),
                                   "rendered": (r["eligible"] - r["suppressed"]).T.astype(int).ravel(),
                                   "suppressed": r["suppressed"].T.astype(int).ravel()}))
    df = pd.concat(parts, ignore_index=True).sort_values(["h", "component"], kind="stable")
    df.insert(0, "hour_utc", HOURS[df["h"].to_numpy()])
    return put(os.path.join(target, F["render"]), df.drop(columns="h"))


def campaign(date, market, i):
    """The trading calendar's own name for a promotion day. The world's promotions are single days, so every name is a
    one-day event: the season's where the date falls in one, a standing one (payday, free delivery, members)
    otherwise. Names only; the days are the world's."""
    d = pd.Timestamp(str(date))
    md = (d.month, d.day)
    if (3, 23) <= md <= (4, 6):
        return "Easter Table"                                   # Easter Sunday 2026 is 5 April
    if market == "NL" and (4, 18) <= md <= (4, 27):
        return "King's Day Deals"
    if market in ("SE", "DK") and (6, 12) <= md <= (6, 21):
        return "Midsummer Deals"
    if (2, 1) <= md <= (2, 14):
        return "Valentine Picks"
    if (8, 10) <= md <= (9, 5):
        return ("Back to School", "Late Summer Deal Day")[i % 2]
    season = {1: "Winter Deal Day", 2: "Winter Deal Day", 3: "Spring Deal Day", 4: "Spring Deal Day", 5: "Garden Day",
              6: "Garden Day", 7: "Summer Deal Day", 8: "Summer Deal Day", 9: "Autumn Deal Day"}[d.month]
    pool = [season, "Member Day"]
    if d.dayofweek == 4:
        pool.append("Free Delivery Friday")
    if d.day >= 24 or d.day <= 2:
        pool.append("Payday Deals")
    return pool[(i + d.day) % len(pool)]


def lookups(W, target):
    reg = [("stock", WL.GROUP_NAME["stock"], WL.TEAMS["stock"], "store chain feed", 14, "stock-snapshot", "rerank", 2, "on feed sync", 15, ""),
           ("promise", WL.GROUP_NAME["promise"], WL.TEAMS["promise"], "delivery promise service", 1, "", "rerank", "", "request time", "", ""),
           ("price", WL.GROUP_NAME["price"], WL.TEAMS["price"], "competitor price source", 5, "price-batch", "rank", 36, "daily batch 04:00 UTC", "", ""),
           ("history", WL.GROUP_NAME["history"], WL.TEAMS["history"], "shopper profile store", 1, "", "rerank", "", "request time", "", ""),
           ("trend", WL.GROUP_NAME["trend"], WL.TEAMS["trend"], "click stream partition", 24, "trend-counters", "rank", 6, "streaming, hourly windows", "", 1),
           ("seller", WL.GROUP_NAME["seller"], WL.TEAMS["seller"], "seller", C.N_SELLERS, "seller-score", "rank", 120,
            "nightly run for sellers with newly settled orders, effective 00:00 UTC", "", ""),
           ("match", WL.GROUP_NAME["match"], WL.TEAMS["match"], "index replica", 6, "", "rank", "", "request time", "", "")]
    df = pd.DataFrame(reg, columns=["feature_group", "name", "owner_team", "entity", "entities", "store", "pipeline_stage",
                                    "validity_hours", "refresh", "sync_interval_minutes", "window_hours"])
    n = put(os.path.join(target, F["registry"]), df)
    mk = pd.DataFrame([(m, WL.MART_KEY[m], WL.COUNTRY[m], WL.SITE[m], WL.CURRENCY[m], WL.LAUNCHED[m]) for m in MK],
                      columns=["market", "mart_market_key", "country", "site", "currency", "launched"])
    put(os.path.join(target, F["markets"]), mk)
    rg = pd.DataFrame([(WL.REGIONS[0], "Amsterdam", "user_id_hash % 2 == 0", "pc-ams1", "2021-03-02"),
                       (WL.REGIONS[1], "Frankfurt", "user_id_hash % 2 == 1", "pc-fra2", "2023-09-19")],
                      columns=["serving_region", "site", "user_assignment", "page_cache_cluster", "in_service_since"])
    put(os.path.join(target, F["regions"]), rg)
    pr = []
    for m in range(6):
        for i, dd in enumerate(np.nonzero(W["promo"][m])[0]):
            pr.append((DATES[dd], MK[m], campaign(DATES[dd], MK[m], i)))
    pr = pd.DataFrame(sorted(pr), columns=["date_utc", "market", "campaign"])
    put(os.path.join(target, F["promo"]), pr)
    return n


def build(W, target):
    rng = np.random.default_rng(PSEED)
    sid = seller_ids(rng)
    counts = {}
    counts[F["sessions"]] = sessions(W, target)
    counts[F["mart"]] = mart(W, target)
    counts[F["status"]] = status(W, target, rng)
    counts[F["gaps"]] = gaps(W, target, rng)
    counts[F["batches"]] = batches(W, target, rng)
    counts[F["lags"]] = lags(W, target, rng)
    counts[F["scoring"]], counts["scoring_runs"] = scoring(W, target, rng, sid)
    counts[F["seller_traffic"]] = seller_traffic(W, target, sid)
    counts[F["shares"]] = shares(W, target)
    counts[F["experiments"]] = experiments(W, target, rng)
    counts[F["cache"]] = cache(W, target, rng)
    counts[F["render"]] = render(W, target)
    counts[F["registry"]] = lookups(W, target)
    return counts
