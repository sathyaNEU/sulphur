"""Every assertion of the build on the cut pack: the input gates, the never-filed list, the pack against the core's
arrays, the bar block (R1 to R7), every row of the fork table (SF1 to SF28), the pinning list read back from the
documents and configuration files, the second implementation, the goldens against figures.json and the realism sweep.

    python3 task9/generator/checks.py [target]
"""
import csv
import glob
import io
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
from contextlib import redirect_stdout

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core as C  # noqa: E402
import deliver  # noqa: E402
import load as L  # noqa: E402
import results as RS  # noqa: E402
import verify as V  # noqa: E402
import world as WL  # noqa: E402

ROWS = []
G = C.GROUPS
F = WL.FILES
TASK = os.path.dirname(HERE)
MONTHS = [n for n, _, _ in C.Q3_MONTHS]
NEVER = (r"dilut|understat|overstat|complian|treatment.received|\bexposure|\bexposed|fresh share|full effect|outliv|"
         r"persist|still (being )?served|\bstale|default[_ ]served|served[_ ](the |a )?default|at (a|the|its) default|"
         r"same sellers|repeat(ed|edly)? fail|second reader|other reader|downstream|second consumer|calibrat|validat|"
         r"natural experiment|share of the fall|correct(ion|ed)\b|intent.to.treat|\bITT\b|contaminat|spill|"
         r"shared (by|across) (arms|users)|cached page|held users? (is|are|get)|not in any (test|ablation)|\bbias|"
         r"confound|root cause|points of (search )?conversion lost|legacy")
CONTROL = {F["charter"]: "to every service that reads it", F["pipeline"]: "requests_without_overrides",
           F["store"]: "serve_group_default", F["incidents"]: "page cache lifetime raised"}
DATA = ("sessions", "mart", "status", "gaps", "batches", "lags", "scoring", "seller_traffic", "cache", "render")


def ok(label, cond, detail=""):
    ROWS.append((label, bool(cond), str(detail)))
    return bool(cond)


def texts(target):
    """every word a reader can find in the pack: file names, headers, small files whole, workbook cells, the PDF's text
    (through the verifier's own extractor), the configuration and text files, the database's schema and register"""
    out = {}
    for path in sorted(glob.glob(os.path.join(target, "*"))):
        name = os.path.basename(path)
        if name.endswith(".csv"):
            with open(path, newline="") as fh:
                out[name] = fh.readline()
                if os.path.getsize(path) < 600000:
                    out[name] += " " + fh.read()
        elif name.endswith(".xlsx"):
            wb = load_workbook(path, read_only=True, data_only=True)
            out[name] = " ".join(wb.sheetnames) + " " + " ".join(
                str(c) for ws in wb for r in ws.iter_rows(values_only=True) for c in r if c is not None)
        elif name.endswith(".pdf"):
            out[name] = V.pdf_text(path)
        elif name.endswith((".yaml", ".txt")):
            out[name] = open(path).read()
        elif name.endswith(".sqlite"):
            con = sqlite3.connect(path)
            out[name] = " ".join(r[0] or "" for r in con.execute("SELECT sql FROM sqlite_master")) + " " + " ".join(
                " ".join(str(x) for x in r) for r in con.execute("SELECT * FROM experiment"))
            con.close()
    return out


def header(target, key):
    with open(os.path.join(target, F[key]), newline="") as fh:
        return next(csv.reader(fh))


def cells_of(route):
    c = dict(route["cost"])
    c.update(route["month"])
    c[RS.ALL], c[RS.LISTED] = route["all"], route["listed_cost"]
    return c


def bands_of(fig):
    b = dict(fig["cost_band"])
    b.update(fig["month_band"])
    b[RS.ALL], b[RS.LISTED] = fig["all_band"], fig["listed_band"]
    return b


def landed(route, bands):
    c = cells_of(route)
    return [k for k in bands if bands[k][0] - 1e-9 <= c[k] <= bands[k][1] + 1e-9]


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    with redirect_stdout(io.StringIO()):
        X, fig_now, E, spec = RS.run(target)
    W, WC, info = X["W"], X["core"], X["info"]
    ok("figures.json is the pack's: recomputed from target/ it is identical",
       json.loads(json.dumps(fig_now, sort_keys=True, default=float)) == fig)
    bands = bands_of(fig)
    T = texts(target)
    files = sorted(os.listdir(target))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    D = V.documents(target)
    ch = D["charter"]

    # ---------------------------------------------------------------- the input gates
    ok("gate: ten or more usable files", len(files) >= 10 and all(os.path.getsize(os.path.join(target, f)) > 100 for f in files),
       len(files))
    ext = {os.path.splitext(f)[1] for f in files}
    ok("gate: two file categories or more (spreadsheets as csv and xlsx, a database, text as pdf and txt, configuration)",
       {".csv", ".xlsx", ".sqlite", ".pdf", ".yaml", ".txt"} <= ext, ext)
    k = fig["counts"]
    ok("gate: a CSV of 20,000 rows or more (the seller scoring log)", k["scoring_rows"] >= 20000, k["scoring_rows"])
    ok("gate: a second CSV that runs 20 printed pages or more (the status rows at 50 lines a page)",
       k["status_rows"] / 50.0 >= 20, k["status_rows"])
    sc_head = pd.read_csv(os.path.join(target, F["scoring"]), usecols=["status"])["status"].value_counts().to_dict()
    shards = set(pd.read_csv(os.path.join(target, F["status"]), usecols=["shard"])["shard"].unique())
    ok("gate: both large files carry mess to clean (scoring rows written twice and two status vocabularies; status hours "
       "loaded twice and renamed shards)",
       k["scoring_repeats"] > 500 and set(sc_head) == {"OK", "FAIL", "scored", "failed"} and k["status_rows_reloaded"] > 1000
       and {"gw2/chn-01", "feed/chn-01"} <= shards, (k["scoring_repeats"], sc_head, k["status_rows_reloaded"]))
    size = sum(os.path.getsize(os.path.join(target, f)) for f in files)
    ok("gate: the pack is 30 MB or more", size >= 30e6, "%.1f MB" % (size / 1e6))
    unused = [F[u] for u in WL.UNUSED]
    ok("gate: two or more files the analysis never reads, named only in metadata.json",
       len(unused) >= 2 and sorted(meta["distractor_files"]) == sorted(unused)
       and not any(re.search(r"unused|distract|decoy|ignore", f, re.I) for f in files), unused)
    ok("gate: metadata.json records every shipped file's source, date and licence", sorted(meta["files"]) == files,
       sorted(set(files) ^ set(meta["files"])))
    ok("gate: no file name names a judgment",
       not any(re.search(r"served_default|default_served|fresh|full_effect|correct|complian|reader|golden|answer|trap|clean|true",
                         f, re.I) for f in files), files)
    sheets = {f: load_workbook(os.path.join(target, f), read_only=True).sheetnames for f in files if f.endswith(".xlsx")}
    desc = re.compile(r"readme|dictionar|notes|manifest|schema|codebook|definition|guide|how.to", re.I)
    ok("gate: no file describes the data (no readme, dictionary, notes, manifest or schema, by name or by sheet)",
       not any(desc.search(f) for f in files) and not any(desc.search(s) for ss in sheets.values() for s in ss), sheets)
    cols = set()
    for key in DATA:
        cols |= set(header(target, key))
    cols -= {"market", "device", "month", "status", "source", "partition", "component", "name", "arm"}
    named = {n: sorted(c for c in cols if re.search(r"(?<![a-z_])%s(?![a-z_])" % re.escape(c), T[n]))
             for n in (F["charter"], F["releases"], F["pipeline"], F["store"])}
    ok("gate: no document or configuration file names four or more of the data files' columns",
       all(len(v) < 4 for v in named.values()), named)
    ok("gate: nothing by hour carries orders (the conversion record ships by business day only)",
       not any("order" in c for key in ("sessions", "status", "render") for c in header(target, key))
       and "business_date_utc" in header(target, "mart"))
    tmp = tempfile.mkdtemp()
    for f in files:
        if f not in unused:
            os.symlink(os.path.join(os.path.abspath(target), f), os.path.join(tmp, f))
    v_less = V.run(tmp)
    g_less = C.view(L.load(tmp)[0])
    shutil.rmtree(tmp)
    ok("gate: with the three unused files deleted both implementations file the same figures",
       all(abs(v_less["cost"][j] - fig["cost"][j]) < 0.00051 and abs(g_less["loss"][j] - fig["cost"][j]) < 0.00051 for j in G))

    # ---------------------------------------------------------------- never filed
    hits = [(n, m.group(0)) for n, t in T.items() for m in re.finditer(NEVER, t, re.I)]
    ok("never filed: no file, header, cell, key or document sentence carries the vocabulary of the three judgments", not hits, hits[:8])
    ok("never filed: the control phrases are found by the same search (the charter's estimand, the cache's write rule, the "
       "store's expiry rule, the cache lifetime change)", all(v in T[n] for n, v in CONTROL.items()),
       [n for n, v in CONTROL.items() if v not in T[n]])
    every = set()
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), newline="") as fh:
                every |= set(next(csv.reader(fh)))
    ok("never filed: no column named for a judgment or holding a result",
       not any(re.search(r"(?<![a-z])(default|fresh|held|arm|cost|loss|effect|lift|stale|expired|true|flag)(?![a-z])", c, re.I)
               for c in every), sorted(every))
    ok("never filed: the cache record carries page views only, with no arm, experiment or user column",
       header(target, "cache") == ["date_utc", "market", "device", "result_page_views", "served_from_cache", "built_at_origin"])
    money = re.compile(r"\b0\.\d{2,3}\b")
    figs = {"%.3f" % fig["cost"][j] for j in G} | {"%.3f" % fig["hurried"]["cost"][j] for j in G}
    docs_ = [F["charter"], F["releases"], F["incidents"], F["pipeline"], F["store"], F["replay"]]
    found = {n: sorted(set(money.findall(T[n])) & figs) for n in docs_}
    ok("never filed: no document, register or configuration file carries a figure for any group's cost",
       not any(found.values()), found)
    ok("never filed: the incident register gives dates, systems and what happened, and no conversion figure or tier",
       not re.search(r"conversion|tier one|points", T[F["incidents"]], re.I))

    # ---------------------------------------------------------------- the pinning list, read back
    ok("pinned: the charter files the line at 0.05 percentage points or more and the third quarter of 2026 by the mart's "
       "business days", D["line"] == C.LINE == fig["line"] and D["quarter"] == ("2026", "1", "July", "30", "September")
       and "by the business days of the search conversion mart" in ch, (D["line"], D["quarter"]))
    R = D["registry"].set_index("feature_group")
    ttl = {j: (0.0 if pd.isna(R.loc[j, "validity_hours"]) else float(R.loc[j, "validity_hours"])) for j in G}
    st_groups = D["store"]["groups"]
    ok("pinned: each group's validity is the registry's and the store configuration's, and the one the estimate uses",
       ttl == {j: C.G[j]["ttl"] for j in G} and all(float(st_groups[j]["validity_hours"]) == ttl[j] for j in st_groups)
       and sorted(st_groups) == sorted(j for j in G if ttl[j]), ttl)
    bt = pd.read_csv(os.path.join(target, F["batches"]))
    ok("pinned: the refresh rules (a 15-minute feed sync, a daily batch at 04:00 UTC, hourly windows, a nightly run "
       "effective 00:00 UTC) are in the registry and the store configuration, and the batch log starts its runs in the 04:00 hour",
       float(R.loc["stock", "sync_interval_minutes"]) == 15 and float(R.loc["trend", "window_hours"]) == 1
       and st_groups["price"]["refresh"]["at_utc"] == "04:00" and st_groups["seller"]["refresh"]["effective_at_utc"] == "00:00"
       and set(bt["started_at_utc"].str[11:13]) == {"04"}, set(bt["started_at_utc"].str[11:13]))
    ok("pinned: which groups are read before the page cache: the pipeline's first pass and the registry's stage column agree",
       sorted(D["first_pass"]) == sorted(j for j in G if C.G[j]["pre"]) == sorted(R.index[R["pipeline_stage"] == "rank"])
       and D["order"] == ["retrieve", "rank", "page_cache", "rerank", "render"], (D["first_pass"], D["order"]))
    ok("pinned: which groups a page component reads: the pipeline's render components and the render record agree",
       D["components"] == {v: kk for kk, v in WL.COMPONENT.items()}
       and sorted(pd.read_csv(os.path.join(target, F["render"]), usecols=["component"])["component"].unique()) == sorted(D["components"]),
       D["components"])
    ok("pinned: the status record's seller and price rows are the scoring and batch logs' own counts",
       info["status_matches_scoring_log"] and info["status_matches_batch_log"])
    ok("pinned: April's check is seven batches missed in fra2 alone and fourteen business days touched",
       fig["april"]["batches"] == 7 and fig["april"]["days"] == 14
       and set(bt.loc[bt["status_fra2"] != bt["status_ams1"], "status_fra2"]) == {"not_replicated"})

    # ---------------------------------------------------------------- the pack against the core's world
    same = lambda a, b, tol=0.0: float(np.abs(np.asarray(a, float) - np.asarray(b, float)).max()) <= tol   # noqa: E731
    ok("pack against core: search sessions by market, device and hour", same(W["sess"], WC["sess"]))
    ok("pack against core: the status shares (seconds and runs exact to a second; requests within sampling)",
       all(same(W["S"][j], WC["S"][j], 3e-4) for j in ("stock", "price", "trend", "match", "seller"))
       and all(abs(float(np.sum(C.q3w(W) * (W["S"][j] - WC["S"][j])[:, C.Q3[0] * 24:])) * 100) < 0.02 for j in ("promise", "history")))
    Lw, Lc = W["logs"], WC["logs"]
    ok("pack against core: each source's replayed state (snapshots, prices, counters to a second; seller scores exactly)",
       same(Lw["stock"]["default_c"], Lc["stock"]["default_c"], 1e-3) and same(Lw["price"]["df_src"], Lc["price"]["df_src"])
       and same(Lw["trend"]["lag_d"], Lc["trend"]["lag_d"], 1e-3) and np.array_equal(Lw["seller"]["d_act"].sum(axis=0), Lc["seller"]["d_act"].sum(axis=0))
       and np.array_equal(Lw["seller"]["d_cf"].sum(axis=0), Lc["seller"]["d_cf"].sum(axis=0)))
    tw, tc = W["tests"], WC["tests"]
    ok("pack against core: the 63 ablation tests, arm by arm and day by day",
       len(tw) == len(tc) == 63 and all(a["group"] == b["group"] and a["d0"] == b["d0"] and all(same(a[x], b[x]) for x in ("nh", "oh", "nc", "oc"))
                                        for a, b in zip(sorted(tw, key=lambda t: (t["group"], t["d0"])), sorted(tc, key=lambda t: (t["group"], t["d0"])))))
    ok("pack against core: the cache record's share built at origin, the holdouts, the render record",
       same(W["u"], WC["u"], 2e-3) and all(same(W["rtest"][j][x], WC["rtest"][j][x]) for j in C.READERS for x in ("nh", "oh", "nc", "oc", "elig_c"))
       and all(same(W["render"][j][x], WC["render"][j][x]) for j in C.READERS for x in ("eligible", "suppressed")))
    day = lambda a: a.reshape(12, C.DAYS, 24).sum(axis=2)   # noqa: E731
    ok("pack against core: the mart by serving region and day, and the promotion calendar",
       all(same(day(W["split"][x]), day(WC["split"][x])) for x in ("na", "oa", "nb", "ob")) and same(day(W["orders"]), day(WC["orders"]))
       and np.array_equal(W["promo"], WC["promo"]) and info["mart_sessions_match"])
    gc = fig["core_world_golden"]
    ok("pack against core: the estimate on the pack is the core's on its own arrays to 0.001 point and files the same list",
       all(abs(gc[j] - X["x"]["g"]["loss"][j]) < 0.001 for j in G), {j: round(gc[j] - X["x"]["g"]["loss"][j], 5) for j in G})
    ok("the world's own values sit inside every group's stated range, on the estimate's side of the line",
       fig["truth_call"] == fig["call"] and all(fig["cost_band"][j][0] <= round(fig["truth"][j], 3) <= fig["cost_band"][j][1] for j in G),
       fig["truth"])
    rb = fig["rubric"]
    ok("the core on the cut pack: level 5, one judgment lost earns 50 or under, the reflex route 30 or under, the rigorous "
       "standard route 50 or under", rb["level"] == 5 and not rb["fails"] and max(rb["one_lost"].values()) <= 50
       and rb["reflex"] <= 30 and rb["rigorous"] <= 50, rb)

    # ---------------------------------------------------------------- the bar block
    ok("R1 the raw material ships: sessions by hour, the mart by day and region, every test by day and arm, every scoring "
       "run, every gap, batch and lag episode, the cache by day, the renders by hour",
       k["session_rows"] == 12 * C.H and k["mart_rows"] == 24 * C.DAYS and k["ablation_tests"] == 63 and k["scoring_runs"] > 800000
       and k["gaps"] > 1000 and k["render_rows"] == 36 * C.H, k)
    W_rep, _ = L.load(target, keep_repeats=True)
    v_rep = C.view(W_rep)
    bs = {b["name"]: b for b in fig["beside"]}
    slips = {"the scoring rows written twice counted twice": (RS.call_of(v_rep["loss"]) == fig["call"]
                                                               and all(abs(v_rep["loss"][j] - X["x"]["g"]["loss"][j]) < 1e-9 for j in G)),
             "the monitor's first load of each hour kept": bs["the monitor's first load of each hour kept"]["call_holds"]
             and not bs["the monitor's first load of each hour kept"]["outside"],
             "the aborted test read with the completed ones": bs["the aborted test read with the completed ones"]["call_holds"]
             and not bs["the aborted test read with the completed ones"]["outside"],
             "the quarter cut on local calendar days": bs[RS.LOCAL_DAYS]["call_holds"] and not bs[RS.LOCAL_DAYS]["outside"]}
    for label, held in slips.items():
        ok("R2 a hygiene slip costs nothing: %s (same list, every figure inside its range)" % label, held)
    ok("R2 the mess resolves exactly: every status shard maps to a source, every mart key to a market, every seller in the "
       "scoring log has traffic rows", k["status_rows_kept"] + k["status_rows_reloaded"] == k["status_rows"]
       and k["scoring_runs"] + k["scoring_repeats"] == k["scoring_rows"] and info["mart_sessions_match"])
    routes = fig["routes"]
    got = {key: landed(routes[key], bands) for key in routes}
    ok("R3 the careful but hurried pass lands none of the twelve ask figures and none of the four components",
       not got[RS.REFLEX] and not got["rigorous"], (got[RS.REFLEX], got["rigorous"]))
    ok("R3 each judgment lost alone leaves eight or more of the twelve ask figures outside their ranges",
       all(len(got[s]) <= 4 for s in C.SIDS), {s: got[s] for s in C.SIDS})
    la = fig["lost_alone"]
    inb = lambda v, b: b[0] - 1e-9 <= v <= b[1] + 1e-9   # noqa: E731
    cb = {"c1": fig["c1_band"], "c2": fig["c2_band"], "c3": fig["c3_band"], "c4": fig["c4_band"]}
    own = {"S1": "c1", "S2": "c2", "S3": "c3"}
    ok("R3 each judgment lost alone moves its own component and April's call, and leaves the other two components",
       all(not inb(la[s][own[s]], cb[own[s]]) and not inb(la[s]["c4"], cb["c4"])
           and all(inb(la[s][c], cb[c]) for c in ("c1", "c2", "c3") if c != own[s]) for s in C.SIDS), la)
    calls = {key: tuple(routes[key]["call"]) for key in RS.KEYS}
    ok("R3 no shortcut files the estimate's list, the three single losses land on three different wrong lists and the "
       "seven shortcuts on seven", all(c != tuple(fig["call"]) for c in calls.values()) and len(set(calls.values())) == 7
       and len({calls[s] for s in C.SIDS}) == 3, calls)
    ok("R3 the direct and the rigorous standard routes file wrong lists",
       routes["direct"]["list"] != fig["list"] and routes["rigorous"]["list"] != fig["list"],
       (routes["direct"]["list"], routes["rigorous"]["list"]))
    ok("R4 no plant: no memo, draft, note or review ships, and the two files that score the groups on something else "
       "(offline replay, feature importance) are the unused ones",
       not any(re.search(r"memo|draft|note|review|analysis|estimate", f, re.I) for f in files)
       and {F["replay"], F["importance"]} <= set(unused))
    u = W["u"]
    sd = W["sess"].reshape(12, C.DAYS, 24).sum(axis=2)
    um = (u * sd).sum(axis=1) / sd.sum(axis=1)
    rh = fig["reported_effect_halves"]
    first = [j for j in G if C.G[j]["pre"]]
    second = [j for j in G if not C.G[j]["pre"]]
    ok("R5 the cache sits in front of every first-pass group in every market and device: the share built at origin is "
       "under 0.7 in all twelve cells, and all four groups' reported effects fall from the January to May tests to the "
       "July to September ones while the three second-pass groups' move by under a tenth",
       um.max() < 0.7 and all(rh[j]["jul_sep"] < 0.85 * rh[j]["jan_may"] for j in first)
       and all(abs(rh[j]["jul_sep"] / rh[j]["jan_may"] - 1) < 0.1 for j in second), (um.round(2), rh))
    exp = C.exposure(W, {})
    h1 = slice(10 * 24, 181 * 24)
    w1 = W["sess"][:, h1] / W["sess"][:, h1].sum()
    part = {j: (100 * float(np.sum(w1 * exp[j]["tot"][:, h1])), 100 * float(np.sum(w1 * W["S"][j][:, h1]))) for j in ("stock", "price", "trend", "seller")}
    ok("R5 a value outlasting its source is in all four stored groups, each at its own ratio, in the first half as in the "
       "third quarter", all(abs(a / b - 1) > 0.1 for a, b in part.values())
       and all(abs(fig["served_default_pct"][j] / fig["status_unhealthy_pct"][j] - 1) > 0.05 for j in ("stock", "price", "trend", "seller"))
       and len({round(fig["served_default_pct"][j] / fig["status_unhealthy_pct"][j], 1) for j in ("stock", "price", "trend", "seller")}) == 4, part)
    rf = fig["render_failed_pct"]
    ok("R5 all three components fail with their group, the whole year: each failed more of its eligible sessions in the "
       "third quarter than in the second", all(rf[j]["q3"] > rf[j]["q2"] + 1.0 for j in C.READERS), rf)
    side = lambda key, j: routes[key]["cost"][j] >= fig["line"]   # noqa: E731
    ok("R5 where they decide nothing: stock carries the replay, match the cache and history a component, and each sits on "
       "its side of the line on every shortcut; price carries all three and is listed on all seven",
       all(side(key, "stock") and side(key, "price") and not side(key, "match") and not side(key, "history") for key in RS.KEYS)
       and abs(fig["served_default_pct"]["stock"] / fig["status_unhealthy_pct"]["stock"] - 1) > 0.3
       and fig["full_effect"]["match"] > 1.5 * fig["measured_effect"]["match"] and fig["reader_cost"]["history"] > 0.003)
    ok("R5 and R6 no one thing: each judgment fixed alone on the hurried pass rescues two results or fewer of the six it "
       "lost, and still files a wrong list",
       all(len(h["rescues"]) <= 2 for h in E["hints"]) and all(routes[RS.ALONE[s]]["list"] != fig["list"] for s in C.SIDS),
       [h["rescues"] for h in E["hints"]])
    nv = fig["nearest_variant"]
    ok("R7 the battery: every variant files the estimate's list, twelve or more of them, the nearest 0.01 points or more "
       "from the line", fig["family_calls_all_golden"] and fig["variants"] >= 12 and nv["distance"] >= 0.01, (fig["variants"], nv))
    ok("R7 each fitted input moved one spread either way, alone and all three together, files the same list",
       len(fig["perturbations"]) == 14 and all(p["call_holds"] for p in fig["perturbations"]),
       min(p["nearest"] for p in fig["perturbations"]))
    a = fig["april"]
    ok("R7 April rules between routes: the estimate within one standard error of the mart's difference, every shortcut "
       "six or more away", a["off"] <= a["record_se"] and all(r["off"] >= 6 * a["record_se"] for r in a["rivals"].values()),
       (a["off"], a["record_se"], {n: r["off"] for n, r in a["rivals"].items()}))
    ok("R7 the readings beside the battery keep the list with every figure inside its stated range",
       all(b["call_holds"] and not b["outside"] for b in fig["beside"]), [(b["name"], b["outside"]) for b in fig["beside"] if b["outside"]])

    # ---------------------------------------------------------------- the fork table
    names = fig["variant_names"]
    has = lambda *ws: all(any(w in n for n in names) for w in ws)   # noqa: E731
    mart_cols = header(target, "mart")
    ok("SF1 search conversion is attributed orders over search sessions, in per cent (charter 3.1), and the mart carries "
       "those two measures only", "orders attributed to search sessions divided by the search sessions" in ch
       and mart_cols[-2:] == ["search_sessions", "attributed_orders"] and len(mart_cols) == 6, mart_cols)
    ok("SF2 a group's cost is against normal service to every service that reads it (charter 3.3)",
       "in normal service to every service that reads it, less the search conversion as served" in ch)
    un = fig["rival_seller_not_netted"]
    ok("SF3 normal service is each source refreshing on its schedule and the services answering (charter 3.2); seller's "
       "default charged in full stays on the same side of the line",
       "when each of its sources refreshes on its schedule and the services it is read from answer" in ch and un["call_holds"]
       and un["cost"] < fig["line"], un)
    ok("SF4 the window is the mart's business days (charter 2.1), which the mart dates in UTC; cut on local calendar days "
       "the list holds with every figure inside its range", "business_date_utc" in mart_cols and bs[RS.LOCAL_DAYS]["call_holds"]
       and not bs[RS.LOCAL_DAYS]["outside"])
    ok("SF5 the line is 0.05 percentage points or more (charter 4.1), and no variant or reading comes within 0.013 of it",
       "0.05 percentage points or more goes on the tier one list" in ch and nv["distance"] >= 0.013
       and fig["nearest_beside"]["distance"] >= 0.013, (nv["distance"], fig["nearest_beside"]["distance"]))
    ok("SF6 a cost is taken over all search sessions of the quarter (charter 3.3)",
       "each taken over all search sessions of the quarter in the six markets" in ch)
    ok("SF7 the grain of the share built at origin: averaged over each test is in the battery",
       has("the fresh share averaged over each test"))
    ok("SF8 how tests are pooled: over every market and device, cell by cell, by precision, before July and from April are "
       "in the battery", has("pooled over every market and device", "cell by cell", "precision", "before July", "from April"))
    ok("SF9 the default served on a test's own days: not netted is in the battery", has("not netted for the default served"))
    ok("SF10 a snapshot's age when its feed stops: fresh to the minute and a quarter of an hour old are in the battery, and "
       "the registry gives the 15-minute sync", has("fresh the minute its feed stops", "a quarter of an hour old")
       and float(R.loc["stock", "sync_interval_minutes"]) == 15)
    ok("SF11 when a counter is back: the hour of catch-up and two hours after are in the battery, and the registry gives "
       "the one-hour window", has("back the hour their partition catches up", "back two hours after"))
    ok("SF12 a seller's traffic: the quarter's in place of the month's is in the battery", has("weighted by the quarter's traffic"))
    ok("SF13 what normal service leaves at the default for sellers: the second quarter's, June's and the first half's "
       "levels are in the battery", has("default share from the second quarter", "default share from June", "default share from the first half"))
    con = sqlite3.connect(os.path.join(target, F["experiments"]))
    el = dict(con.execute("SELECT arm, SUM(eligible_sessions IS NOT NULL) FROM experiment_daily d JOIN experiment e USING "
                          "(experiment_id) WHERE e.kind = 'component_holdout' GROUP BY arm").fetchall())
    statuses = dict(con.execute("SELECT status, COUNT(*) FROM experiment GROUP BY status").fetchall())
    con.close()
    per_sess = bs["a component's loss per session of its own test, eligible or not, at its group's default share"]
    ok("SF14 a component's loss is per eligible session: the holdouts report eligible sessions on the control arm, and "
       "read per session of the test the list holds inside every range",
       el.get("control", 0) > 0 and not el.get("held", 0) and per_sess["call_holds"] and not per_sess["outside"], el)
    ok("SF15 a component's lost sessions: its failed renders over the rate at which it fails with the value present, and "
       "over its second-quarter, first-half and June rates, are in the battery",
       has("fails with its group's value present", "second-quarter rate", "first-half rate", "June rate"))
    cpd = fig["rival_compounding"]
    ok("SF16 two groups at their defaults in one session: the costs add (charter 3.4); compounded, the list holds with "
       "every group inside its range", "is the sum of their costs" in ch and cpd["call_holds"] and not cpd["outside"], cpd)
    ab = fig["april_batch_days"]
    ok("SF17 April's days: on the fourteen days touched and on the seven batch days alike the estimate is the nearest to "
       "the mart, every shortcut seven times further off or more",
       all(r["off"] >= 7 * a["off"] for r in a["rivals"].values()) and all(r["off"] >= 7 * ab["off"] for r in ab["rivals"].values()),
       (a["off"], ab["off"], {n: r["off"] for n, r in ab["rivals"].items()}))
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    ok("SF18 the listed groups together are the sum of their costs (charter 3.4; the prompt asks for the groups on the list "
       "together)", "for the groups on the list together" in prompt
       and abs(sum(X["x"]["g"]["loss"][j] for j in fig["list"]) - X["x"]["g"]["tier"]) < 1e-9)
    ok("SF19 a month's cost is taken over that month's search sessions (charter 3.4)",
       "A month's cost is the same quantity taken over that month's search sessions" in ch)
    sc = pd.read_csv(os.path.join(target, F["scoring"]))
    ok("SF20 a retried scoring run is one run: every repeated seller and night is a row repeated whole",
       int(sc.duplicated(["effective_date_utc", "seller_id"]).sum()) == int(sc.duplicated().sum()) == k["scoring_repeats"],
       (int(sc.duplicated(["effective_date_utc", "seller_id"]).sum()), int(sc.duplicated().sum())))
    us = fig["rival_usual_level"]
    ok("SF21 normal service read as the second quarter's level of service is refused by the charter's 3.2, and files the "
       "same list", not us["wrong"] and us["list"] == fig["list"], us["cost"])
    first_load = bs["the monitor's first load of each hour kept"]
    ok("SF22 an hour the monitor loaded twice: the later load stands; with the first kept the list holds inside every range",
       first_load["call_holds"] and not first_load["outside"] and k["status_rows_reloaded"] > 0)
    abort = bs["the aborted test read with the completed ones"]
    ok("SF23 the aborted run of a test is left out (the export's status column); read with the completed tests the list "
       "holds inside every range", statuses.get("aborted") == 1 and abort["call_holds"] and not abort["outside"], statuses)
    ratio = bs["each group's full effect as the mean of its tests' own ratios"]
    daily = bs["every default share taken day by day before it meets the sessions"]
    cell = bs["a component's loss per eligible session market by market"]
    ok("SF24 how a group's tests are combined and at what grain a default share meets the sessions: the mean of the tests' "
       "own ratios, a component's loss market by market, and default shares by day all hold the list inside every range",
       all(b["call_holds"] and not b["outside"] for b in (ratio, daily, cell)))
    subs, ta = fig["rival_test_subsets"], fig["test_agreement"]
    q3s, jun, lat1 = subs["the quarter's own tests"], subs["the four tests from June"], subs["the latest test alone"]
    ok("SF25 which tests carry a group's effect: on the quarter's own three or the four from June the list holds, also "
       "stacked with two other choices; only trend, price and components 1 and 4 leave their ranges; and the nine tests "
       "agree (Cochran's Q under the five per cent point on eight degrees of freedom) at under half the standard error",
       q3s["call_holds"] and jun["call_holds"] and fig["rival_test_subsets_stacked"]["call_holds"]
       and set(q3s["outside"]) == set(jun["outside"]) == {"trend", "price"}
       and q3s["c_outside"] == jun["c_outside"] == ["1", "4"]
       and all(ta[j]["q"] < 15.51 and ta[j]["df"] == 8 and ta[j]["se_quarter"] > 2 * ta[j]["se_all"] for j in ("trend", "price")),
       (q3s["cost"], jun["cost"], ta["trend"], ta["price"]))
    ok("SF26 the latest test alone leaves trend off the list and is refused by its own precision: the line is inside one "
       "standard error of trend's cost on it, where the nine tests put trend over five standard errors above the line",
       lat1["list"] != fig["list"] and "trend" not in lat1["list"]
       and abs(lat1["cost"]["trend"] - C.LINE) < ta["trend"]["cost_se_latest"] and ta["trend"]["from_line_all"] > 5,
       (lat1["cost"], ta["trend"]))
    rr, arms, sp_ = fig["rival_replayed_regression"], fig["trend_arms"], fig["trend_share_spread"]
    ok("SF27 the daily record regressed on the replayed shares cannot place promise or seller, and its trend figure is "
       "refused by trend's randomised tests (over twice their effect a session, more than twenty of their standard "
       "errors away) and by the held arm of those tests, which loses as much as the control arm on trend's default "
       "share; that share is one figure a day across markets and devices",
       {"promise", "seller"} <= set(rr["unplaced"]) and {"promise", "seller"} <= set(fig["rival_daily_regression_unplaced"])
       and rr["per_session"]["trend"] > 2 * fig["c1"]
       and (rr["per_session"]["trend"] - fig["c1"]) / ta["trend"]["se_all"] > 20
       and arms["held"] > 2 * arms["held_expected"] and abs(arms["held"] - arms["control"]) < arms["held_se"]
       and sp_["within_day"] < 0.001 and sp_["across_days"] > 0.05, (rr, arms, sp_))
    short = fig["rival_stock_short_gaps"]
    ok("SF28 a feed gap that ends before the snapshot's validity runs out never reaches the default (the blocks say so); "
       "counted from the validity's end to the next sync, stock stays inside its range and the list holds",
       short["inside"] and short["call_holds"] and short["served_pct"] >= fig["served_default_pct"]["stock"], short)
    h_ = fig["hurried"]
    ok("the hurried products rebuild from the factors the blocks state beside them: each group's effect netted for the "
       "status share times that share, and seller's on the status share alone",
       all(abs(h_["effect"][j] * fig["status_unhealthy_pct"][j] / 100.0 - h_["cost"][j]) < 0.0025 for j in G)
       and abs(fig["routes"]["S2"]["effect"]["seller"] * fig["status_unhealthy_pct"]["seller"] / 100.0
               - fig["routes"]["S2"]["cost"]["seller"]) < 0.0025,
       {j: (h_["effect"][j], fig["status_unhealthy_pct"][j], h_["cost"][j]) for j in G})
    sub = open(os.path.join(TASK, "submission.md")).read()
    ok("stated precision: every group's cost to 0.001 point with its range in the answer blocks, and the prompt dictates no "
       "rounding", all(("%s %.3f (%.3f to %.3f)" % (j, fig["cost"][j], *fig["cost_band"][j])) in sub for j in G)
       and not re.search(r"round|decimal|nearest", prompt, re.I))

    # ---------------------------------------------------------------- the second implementation
    with redirect_stdout(io.StringIO()):
        v = V.run(target)
        vr = {key: V.run(target, lost=tuple(key.split("+"))) for key in ("S1", "S2", "S3", RS.REFLEX)}
    rows = V.compare(v, fig, vr)
    bad = [r for r in rows if not r[3]]
    ok("verify: the second implementation, from the shipped files alone, agrees on every figure it shares with figures.json "
       "(the estimate, the three single shortcuts, the hurried route, April)", not bad and len(rows) > 100, bad[:5])

    # ---------------------------------------------------------------- the goldens and the blocks
    gold = os.path.join(TASK, "golden")
    ok("golden: exactly the two files the prompt asks for", sorted(os.listdir(gold)) == sorted(deliver.FILES.values()), os.listdir(gold))
    wb = load_workbook(os.path.join(gold, deliver.FILES["wb"]), data_only=True)
    ws = wb.worksheets[0]
    first_rows = {r[0]: r for r in ws.iter_rows(min_row=5, max_row=13, values_only=True) if r[0]}
    ok("golden: the first sheet states the list and holds each group's cost, range and tier from figures.json",
       ws.title == "Tier one list" and str(ws["A1"].value).startswith("Tier one for 2027")
       and all(abs(first_rows[WL.GROUP_NAME[j]][2] - fig["cost"][j]) < 1e-9
               and first_rows[WL.GROUP_NAME[j]][4] == ("Tier one" if j in fig["list"] else "Present tier") for j in G)
       and abs(first_rows["All feature groups together"][2] - fig["all"]) < 1e-9
       and abs(first_rows["Tier one groups together"][2] - fig["listed_cost"]) < 1e-9 and len(ws._charts) == 1, list(first_rows))
    ok("golden: the workbook's sheets are named for what they hold and none is a default",
       wb.sheetnames == ["Tier one list", "Cost by month", "Inputs", "April check", "Sensitivity", "Routes", "Basis"], wb.sheetnames)
    gcsv = pd.read_csv(os.path.join(gold, deliver.FILES["csv"]))
    msum = gcsv.groupby("month")["cost_points"].sum()
    ok("golden: the CSV holds one row per group and month, its months sum to the workbook's monthly figures, and each row is "
       "the second implementation's to 0.0001",
       len(gcsv) == 21 == fig["csv_rows"] and list(gcsv.columns) == ["feature_group", "month", "cost_points"]
       and all(round(float(msum[deliver.MONTH_KEY[n]]), 2) == fig["month"][n] for n in MONTHS)
       and all(abs(r.cost_points - v["group_month"][r.feature_group][{"2026-07": "July", "2026-08": "August", "2026-09": "September"}[r.month]]) < 0.0001
               for r in gcsv.itertuples()), msum.round(4).to_dict())
    ok("the answer blocks carry no em dash and no design word",
       "—" not in sub and not re.search(r"stump|rung|reflex|lattice|golden|decoy|\btrap|solver|rubric|shortcut family", sub, re.I))
    ok("the answer blocks state each refused route with its figure",
       all(("%.3f" % routes[s]["cost"][m]) in sub for s, m in (("S1", "trend"), ("S2", "seller"), ("S3", "promise")))
       and ("%.3f" % a["rivals"]["every stump lost"]["value"]) in sub)
    blocks = sub.split("## Step-by-Step")[0]
    ok("the graded blocks state no count or base every route reaches (rows, runs, tests, sessions sit in the Step-by-Step)",
       not any(format(k[x], ",") in blocks for x in ("status_rows", "scoring_rows", "scoring_runs", "gaps"))
       and ("%.2f" % fig["conversion"]["q3"]) not in blocks and ("%.3f" % a["record"]) not in blocks)

    # ---------------------------------------------------------------- realism
    gp = pd.read_csv(os.path.join(target, F["gaps"]))
    dur = (pd.to_datetime(gp["feed_resumed_at"], utc=True) - pd.to_datetime(gp["feed_stopped_at"], utc=True)).dt.total_seconds()
    ok("realism: feed gaps start and end at uneven times (under a tenth on a whole minute) and run from minutes to hours",
       float((dur % 60 == 0).mean()) < 0.1 and dur.min() < 1800 and dur.max() > 4 * 3600, (round(float((dur % 60 == 0).mean()), 3), dur.min(), dur.max()))
    shares = pd.read_excel(os.path.join(target, F["shares"]), sheet_name="chain_feeds")
    spread = {m: round(float(shares["share_%s" % m].max() / shares["share_%s" % m].min()), 2) for m in C.MARKETS}
    ok("realism: no two chains carry the same share of a market and traffic is uneven across them (the largest chain "
       "1.4 times the smallest or more in every market, four times or more in three)",
       all(shares["share_%s" % m].dropna().nunique() == shares["share_%s" % m].dropna().size for m in C.MARKETS)
       and min(spread.values()) >= 1.4 and sum(v >= 4 for v in spread.values()) >= 3, spread)
    last = pd.read_csv(os.path.join(target, F["sessions"]), usecols=["search_sessions"])["search_sessions"] % 10
    freq = last.value_counts(normalize=True)
    ok("realism: session counts do not heap on a last digit (none holds more than 12 per cent)", float(freq.max()) < 0.12, freq.round(3).to_dict())
    ratios = {j: round(fig["served_default_pct"][j] / fig["status_unhealthy_pct"][j], 2) for j in ("stock", "price", "trend", "seller")}
    ok("realism: each job fails its own way (the four stored groups' served and unhealthy shares stand in four different "
       "ratios, and no group's full effect equals another's)", len(set(ratios.values())) == 4 and len({fig["full_effect"][j] for j in G}) == 7, ratios)
    stamps = {f: os.path.getmtime(os.path.join(target, f)) for f in files}
    asof_end = pd.Timestamp(str(WL.ASOF) + " 23:59:59", tz="UTC").timestamp()
    ok("realism: no two files share a save time and none is saved after the as-of date",
       len(set(stamps.values())) == len(stamps) and max(stamps.values()) <= asof_end)
    reg = pd.read_excel(os.path.join(target, F["incidents"]))
    ok("realism: the register's tickets are opened on uneven minutes, none after the as-of date, and its text carries no "
       "figure of the estimate", pd.to_datetime(reg["opened"]).max() <= pd.Timestamp(str(WL.ASOF) + " 23:59:59")
       and pd.to_datetime(reg["opened"]).dt.minute.nunique() >= 8, pd.to_datetime(reg["opened"]).dt.minute.nunique())
    late = pd.read_csv(os.path.join(target, F["status"]), usecols=["hour_utc", "loaded_at_utc"])
    lag_h = (pd.to_datetime(late["loaded_at_utc"], utc=True) - pd.to_datetime(late["hour_utc"], utc=True)).dt.total_seconds() / 3600
    ok("realism: the monitor loads most hours within two hours and a few late", 0.001 < float((lag_h > 3).mean()) < 0.05,
       round(float((lag_h > 3).mean()), 4))
    mtxt = json.dumps(meta)
    ok("metadata.json names the decision, the deliverables and the provenance and no method, figure or mechanism",
       not re.search(NEVER + r"|stump|mechanism|easy route|rung|decisive", mtxt, re.I)
       and not any(("%.3f" % fig["cost"][j]) in mtxt for j in G) and meta["as_of"] == str(WL.ASOF))

    bad = [r for r in ROWS if not r[1]]
    for label, _, detail in bad:
        print("FAIL  %s  %s" % (label, detail[:400]))
    print("checks: %d assertions, %d failed" % (len(ROWS), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
