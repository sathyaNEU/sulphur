"""task22 verify: an independent recompute from the bundle alone (target/ and generator/figures.json), on its own
code path: pandas time handling, its own network replay and its own balance, with read periods spread evenly over
their days (a golden-family variant). It imports nothing from the generator.

    python3 task22/generator/verify.py
"""
import calendar
import datetime as dt
import json
import os
import re
import subprocess
import sys
from collections import defaultdict, deque
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
TZ = ZoneInfo("America/Chicago")
FEEDERS = ["NTH-1", "NTH-2", "NTH-3", "NTH-4", "IND-1", "IND-2", "IND-3", "APT-1", "APT-2", "APT-3", "APT-4",
           "CHL-1", "CHL-2", "CHL-3"]
SUB = {"DLM-NTH69": "North", "DLM-IND69": "Industrial Park", "DLM-APT69": "Airport Road", "DLM-CHL69": "Cherry Hill"}
CODE = {"North": "NTH", "Industrial Park": "IND", "Airport Road": "APT", "Cherry Hill": "CHL"}
FAILS = []


def say(label, ok, detail=""):
    print("%s  %-70s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILS.append(label)


def f_(name):
    for n in os.listdir(T):
        if n.startswith(name):
            return os.path.join(T, n)
    raise FileNotFoundError(name)


def hours_utc():
    idx = pd.date_range("2023-09-01 06:00", "2026-11-01 04:00", freq="h", tz="UTC")
    return idx


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    H = hours_utc()
    pos = {t: i for i, t in enumerate(H)}
    # delivery points: hour ending, standard time all year
    dp = pd.read_csv(f_("bmpa_delivery_point"), dtype={"Date": str})
    start = pd.to_datetime(dp["Date"]) + pd.to_timedelta(dp["HourEnding"] - 1, unit="h")
    dp["t"] = (start + pd.Timedelta(hours=6)).dt.tz_localize("UTC")
    DP = {CODE[SUB[k]]: g.set_index("t")["kWh"].reindex(H).values for k, g in dp.groupby("DeliveryPoint")}
    DQ = {CODE[SUB[k]]: g.set_index("t")["kVArh"].reindex(H).values for k, g in dp.groupby("DeliveryPoint")}
    # historian: hour beginning, local clock (the repeated November hour in file order)
    sc = pd.read_csv(f_("historian_feeder"))
    sc["n"] = sc.groupby(["Point", "Timestamp"]).cumcount()
    loc = pd.to_datetime(sc["Timestamp"])
    utc = []
    cache = {}
    for ts, n in zip(loc, sc["n"]):
        k = (ts, n)
        if k not in cache:
            cache[k] = pd.Timestamp(ts.to_pydatetime().replace(tzinfo=TZ, fold=int(n))).tz_convert("UTC")
        utc.append(cache[k])
    sc["t"] = utc
    good = sc["Quality"].eq("GOOD")
    MW, MV = {}, {}
    for p, g in sc[good].groupby("Point"):
        fdr = "%s-%s" % (p[:3], p[-1])
        x = g.set_index("t")["MW"].reindex(H).values * 1000.0
        q = g.set_index("t")["MVAR"].reindex(H).values * 1000.0
        # a reading repeated exactly for six hours or more (not zero) is a stuck transducer
        s = pd.Series(x)
        grp = (s != s.shift()).cumsum()
        run = s.groupby(grp).transform("size")
        stuck = (run >= 6) & (s != 0) & s.notna()
        x[stuck.values] = np.nan
        q[stuck.values] = np.nan
        MW[fdr], MV[fdr] = x, q
    subx = pd.read_excel(f_("substations_and"), sheet_name=None, header=2)
    tx = {CODE[r.Substation]: (r.NoLoad_kW, r.LoadLoss_kW, r.Rating_MVA) for r in subx["Power transformers"].itertuples()}
    ssm = subx["Station service"]
    month_of = pd.Series(H.tz_convert(TZ).strftime("%Y-%m"))
    hours_in = month_of.value_counts()
    SS = {}
    for s in tx:
        m = dict(zip(ssm[ssm["Substation"].map(CODE) == s]["Month"].astype(str), ssm[ssm["Substation"].map(CODE) == s]["kWh"]))
        SS[s] = month_of.map(lambda k: m.get(k, 0.0) / hours_in[k]).values
    # fill each substation's missing breaker hours from the delivery point
    EIN = {}
    for s in tx:
        fs = [f for f in FEEDERS if f[:3] == s]
        nl, ll, mva = tx[s]
        S = np.sqrt(DP[s] ** 2 + DQ[s] ** 2)
        resid = DP[s] - SS[s] - nl - ll * (S / (mva * 1000.0)) ** 2
        M = np.vstack([MW[f] for f in fs])
        miss = np.isnan(M)
        known = np.nansum(M, axis=0)
        out = M.copy()
        for h in np.nonzero(miss.any(axis=0))[0]:
            js = np.nonzero(miss[:, h])[0]
            if len(js) == 1:
                out[js[0], h] = resid[h] - known[h]
            else:
                w = np.zeros(len(js))
                for d in (24, -24, 48, -48, 168, -168):
                    k = h + d
                    if 0 <= k < len(H) and not np.isnan(M[js, k]).any():
                        w += M[js, k]
                w = w / w.sum() if w.sum() > 0 else np.full(len(js), 1 / len(js))
                out[js, h] = (resid[h] - known[h]) * w
        for j, f in enumerate(fs):
            EIN[f] = out[j]
    t_loc = H.tz_convert(TZ)
    in26 = (t_loc >= pd.Timestamp("2025-10-01", tz=TZ)) & (t_loc < pd.Timestamp("2026-10-01", tz=TZ))
    jan = (t_loc >= pd.Timestamp("2026-01-01", tz=TZ)) & (t_loc < pd.Timestamp("2026-02-01", tz=TZ))
    chl3_26 = EIN["CHL-3"][in26].sum() / 1000.0
    chl3_jan = EIN["CHL-3"][jan].sum() / 1000.0
    g1 = figs["R1_energy_in"]
    say("R1 CHL-3 energy in, twelve months", abs(chl3_26 / g1["CHL-3, twelve months to September 2026"] - 1) < 0.006,
        "%.1f vs %.1f" % (chl3_26, g1["CHL-3, twelve months to September 2026"]))
    say("R1 CHL-3 energy in, January 2026", abs(chl3_jan / g1["CHL-3, January 2026"] - 1) < 0.03,
        "%.1f vs %.1f" % (chl3_jan, g1["CHL-3, January 2026"]))
    sys26 = sum(EIN[f][in26].sum() for f in FEEDERS) / 1000.0
    say("R1 fourteen feeders' energy in", abs(sys26 / g1["fourteen feeders, twelve months to September 2026"] - 1) < 0.0012,
        "%.1f" % sys26)
    # ---------------------------------------------------------------- the network replayed
    gis = pd.read_excel(f_("gis_electric"), sheet_name=None, dtype={"ServicePointID": str})
    seg, sw = gis["Primary segments"], gis["Switches"]
    adj = defaultdict(list)
    for r in seg.itertuples():
        adj[r.FromNode].append(("g", r.SegmentID, r.ToNode))
        adj[r.ToNode].append(("g", r.SegmentID, r.FromNode))
    for r in sw.itertuples():
        adj[r.NodeA].append(("s", r.SwitchID, r.NodeB))
        adj[r.NodeB].append(("s", r.SwitchID, r.NodeA))
    xr = pd.read_excel(f_("oms_gis_device"))
    tagmap = {str(a).replace(" ", "-"): b for a, b in zip(xr["OMS_Device"], xr["GIS_SwitchID"])}
    tagmap.update({str(t): i for t, i in zip(sw["PoleTag"], sw["SwitchID"])})
    log = pd.read_csv(f_("oms_switching"))
    log["t"] = pd.to_datetime(log["DateTime"], format="%m/%d/%Y %H:%M").dt.tz_localize(TZ, ambiguous=True).dt.tz_convert("UTC")
    log["sw"] = [d if d in set(sw["SwitchID"]) else tagmap.get(str(d).replace(" ", "-")) for d in log["Device"]]
    log = log.sort_values("t")
    state = {r.SwitchID: r.NormalState == "Closed" for r in sw.itertuples()}
    first = {}
    for r in log.itertuples():
        first.setdefault(r.sw, r.Operation == "CLOSE")
    for k, v in first.items():
        state[k] = not v

    def trees(st_):
        seen = set()
        out = {}
        for fdr in FEEDERS:
            root = "BKR-" + fdr
            q = deque([root])
            seen.add(root)
            par = {root: None}
            order = [root]
            while q:
                u = q.popleft()
                for kind, ident, v in adj[u]:
                    if kind == "s" and not st_[ident]:
                        continue
                    if v in seen or str(v).startswith("BKR"):
                        continue
                    seen.add(v)
                    par[v] = (u, kind, ident)
                    order.append(v)
                    q.append(v)
            out[fdr] = (order, par)
        return out
    # epochs: hour of each operation
    epochs = []
    cur = dict(state)
    h0 = 0
    for t_, grp in log.groupby(log["t"].dt.floor("h"), sort=True):
        h = pos.get(t_, None)
        if h is None:
            continue
        if h > h0:
            epochs.append((h0, h, dict(cur)))
        for r in grp.itertuples():
            cur[r.sw] = r.Operation == "CLOSE"
        h0 = h
    epochs.append((h0, len(H), dict(cur)))
    ET = [trees(e[2]) for e in epochs]
    node_f = defaultdict(lambda: np.full(len(H), -1, dtype=np.int8))
    for (a, b, _), tr in zip(epochs, ET):
        for j, fdr in enumerate(FEEDERS):
            for n in tr[fdr][0]:
                node_f[n][a:b] = j
    xf = gis["Transformers"]
    reg = pd.read_excel(f_("transformer_asset"), dtype={"InstallDate": str, "RemovedDate": str})
    xnode = dict(zip(xf["XfmrID"], xf["Node"]))
    xnode.update({a: l for a, l in zip(reg["AssetID"], reg["Location"]) if a not in xnode})
    spt = gis["Service points"]
    sp_node = {s: xnode.get(x) for s, x in zip(spt["ServicePointID"], spt["XfmrID"])}
    lp_sp = set(spt.loc[spt["MeterType"] == "IDR", "ServicePointID"])
    reads = pd.read_csv(f_("cis_meter_reads"), dtype={"ServicePointID": str, "AccountNo": str}).drop_duplicates()
    first_read = reads.groupby("ServicePointID")["ReadDate"].min()

    def cust_at(y, m, fdr):
        nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
        h = pos[pd.Timestamp(dt.datetime(nxt.year, nxt.month, 1, tzinfo=TZ)).tz_convert("UTC")] - 1
        j = FEEDERS.index(fdr)
        n = 0
        last_day = (nxt - dt.timedelta(days=1)).isoformat()
        for s, d0 in first_read.items():
            if s in lp_sp or d0 > last_day:
                continue
            nd = sp_node.get(s)
            if nd is not None and node_f[nd][h] == j:
                n += 1
        return n
    r2 = figs["R2_membership"]
    c3, c5 = cust_at(2026, 3, "NTH-4"), cust_at(2026, 5, "NTH-4")
    say("R2 NTH-4 customers at the end of March 2026", abs(c3 - r2["NTH-4 customers, 31 March 2026"]) <= 3,
        "%d vs %d" % (c3, r2["NTH-4 customers, 31 March 2026"]))
    say("R2 NTH-4 customers at the end of May 2026", abs(c5 - r2["NTH-4 customers, 31 May 2026"]) <= 3,
        "%d vs %d" % (c5, r2["NTH-4 customers, 31 May 2026"]))
    # ---------------------------------------------------------------- daily use, evenly over each read period
    d0 = dt.date(2023, 9, 1)
    D = (dt.date(2026, 11, 1) - d0).days
    reads["d"] = pd.to_datetime(reads["ReadDate"]).dt.date
    reads["o"] = reads["ReadType"].map({"F": 0, "I": 1}).fillna(2)
    reads = reads.sort_values(["ServicePointID", "d", "o"])
    node_del = defaultdict(lambda: np.zeros(D))
    node_rcv = defaultdict(lambda: np.zeros(D))
    node_lp = defaultdict(lambda: np.zeros(D))
    for s, g in reads.groupby("ServicePointID"):
        nd = sp_node.get(s)
        if nd is None:
            continue
        prev = None
        pk = pr = 0.0
        ps = None
        for r in g.itertuples():
            if r.ReadType == "I":
                prev, pk, pr, ps = r.d, 0.0, 0.0, None
                continue
            if prev is None:
                prev = r.d
                continue
            ps = ps or prev
            pk += 0.0 if pd.isna(r.kWh) else r.kWh
            pr += 0.0 if pd.isna(r.kWhRcv) else r.kWhRcv
            if r.ReadType == "E":
                prev = r.d
                continue
            a, b = (ps - d0).days, (r.d - d0).days
            if b > a:
                lo, hi = max(a, 0), min(b, D)
                if hi > lo:
                    tgt = node_lp if s in lp_sp else node_del
                    tgt[nd][lo:hi] += pk / (b - a)
                    if s not in lp_sp:
                        node_rcv[nd][lo:hi] += pr / (b - a)
            prev, pk, pr, ps = r.d, 0.0, 0.0, None
    # lights at input watts and burning hours
    eng = pd.read_excel(f_("distribution_engineering"), sheet_name=None, header=2)
    watts = dict(zip(eng["Lamp input watts"]["LampCode"], eng["Lamp input watts"]["Input_W"]))
    burn = dict(zip(eng["Burning hours"]["Month"].astype(int), eng["Burning hours"]["BurningHours"]))
    inv = pd.read_excel(f_("street_area_lighting"), dtype={"InstallDate": str, "LEDConversion": str})
    days = [d0 + dt.timedelta(days=k) for k in range(D)]
    per_day = np.array([burn[d.month] / calendar.monthrange(d.year, d.month)[1] for d in days])
    node_l = defaultdict(lambda: np.zeros(D))
    ins_idx = lambda s: max(0, (dt.date.fromisoformat(s) - d0).days)
    for r in inv.itertuples():
        x = np.zeros(D)
        i0 = ins_idx(r.InstallDate)
        if isinstance(r.LEDConversion, str) and r.LEDConversion:
            i1 = max(0, (dt.date.fromisoformat(r.LEDConversion) - d0).days)
            x[i0:] = watts[r.LampCode] / 1000.0
            x[max(i0, i1):] = watts[r.LEDLampCode] / 1000.0
        else:
            x[i0:] = watts[r.LampCode] / 1000.0
        node_l[r.PoleNode] += x * per_day
    dd = np.array([d0 <= dt.date(2025, 10, 1) for d0_ in [0]])  # noqa
    d26 = np.array([(dt.date(2025, 10, 1) <= d < dt.date(2026, 10, 1)) for d in days])
    li26 = sum(v[d26].sum() for v in node_l.values()) / 1000.0
    say("R3 the lights' real use", abs(li26 / figs["R3_lights"]["real use"] - 1) < 0.04,
        "%.1f vs %.1f" % (li26, figs["R3_lights"]["real use"]))
    lb = pd.read_csv(f_("unmetered_lighting"), dtype={"Month": str})
    deemed = lb[(lb["Month"] >= "2025-10-01") & (lb["Month"] < "2026-10-01")]["DeemedkWh"].sum() / 1000.0
    say("R3 the lights' deemed kWh", abs(deemed / figs["R3_lights"]["deemed kWh billed"] - 1) < 0.003, "%.1f" % deemed)
    # ---------------------------------------------------------------- each feeder's share of each day
    hday = np.array((H.tz_convert(TZ).normalize().tz_localize(None) - pd.Timestamp(d0)).days)

    def frac(nd):
        nf = node_f.get(nd)
        out = np.zeros((D, 14))
        if nf is None:
            return out
        for j in range(14):
            out[:, j] = np.bincount(hday, weights=(nf == j), minlength=D)[:D]
        tot = np.bincount(hday, minlength=D)[:D]
        return out / tot[:, None]
    FR = {}
    agg = {k: np.zeros((14, D)) for k in ("del", "rcv", "lp", "l")}
    for key, src in (("del", node_del), ("rcv", node_rcv), ("lp", node_lp), ("l", node_l)):
        for nd, x in src.items():
            if nd not in FR:
                FR[nd] = frac(nd)
            agg[key] += (FR[nd] * x[:, None]).T
    # ---------------------------------------------------------------- technical losses
    cond = dict(zip(eng["Conductors"]["Conductor"], eng["Conductors"]["R50_ohm_per_mile"]))
    seginfo = {r.SegmentID: (r.Length_ft / 5280.0 * cond[r.Conductor], 1.0 if r.Phasing == "ABC" else 6.0)
               for r in seg.itertuples()}
    load_nd = defaultdict(lambda: np.zeros(D))
    for src, sgn in ((node_del, 1), (node_rcv, -1), (node_lp, 1), (node_l, 1)):
        for nd, x in src.items():
            load_nd[nd] += sgn * x
    mon_day = np.array([d.year * 100 + d.month for d in days])
    mon_h = np.array([t.year * 100 + t.month for t in H.tz_convert(TZ)])
    prim = {fdr: np.zeros(len(H)) for fdr in FEEDERS}
    for (a, b, _), tr in zip(epochs, ET):
        for fdr in FEEDERS:
            order, par = tr[fdr]
            if len(order) < 2:
                continue
            for m in np.unique(mon_h[a:b]):
                hs = np.nonzero(mon_h[a:b] == m)[0] + a
                ld = {n: max(load_nd[n][mon_day == m].sum(), 0.0) if n in load_nd else 0.0 for n in order}
                tot = sum(ld.values())
                if tot <= 0:
                    continue
                down = dict(ld)
                for n in reversed(order[1:]):
                    down[par[n][0]] += down[n]
                req = sum(seginfo[par[n][2]][1] * seginfo[par[n][2]][0] * (down[n] / tot) ** 2
                          for n in order[1:] if par[n][1] == "g")
                P_ = np.nan_to_num(EIN[fdr][hs])
                Q_ = np.nan_to_num(MV[fdr][hs]) if fdr in MV else 0.0
                # reactive power at the breaker; missing hours at the hour's neighbours' power factor
                Qh = MV[fdr][hs]
                badq = np.isnan(Qh)
                if badq.any():
                    pf = np.nanmedian(MV[fdr][a:b] / np.where(MW[fdr][a:b] > 0, MW[fdr][a:b], np.nan))
                    Qh = np.where(badq, P_ * (pf if pf == pf else 0.3), Qh)
                prim[fdr][hs] = req * (P_ ** 2 + Qh ** 2) / 12.47 ** 2 / 1000.0
    # transformers
    xl = eng["Transformer losses"]
    xt = {(float(r.kVA), r.Vintage): (r.NoLoad_W, r.LoadLoss_W) for r in xl.itertuples()}
    nl = {fdr: 0.0 for fdr in FEEDERS}
    hloc_date = np.array([d.toordinal() for d in H.tz_convert(TZ).date])
    for r in reg.itertuples():
        v = "2010 and later" if int(r.MfgYear) >= 2010 else "before 2010"
        a_, b_ = xt[(float(r.kVA), v)]
        on = hloc_date >= dt.date.fromisoformat(r.InstallDate).toordinal()
        if isinstance(r.RemovedDate, str) and r.RemovedDate:
            on &= hloc_date < dt.date.fromisoformat(r.RemovedDate).toordinal()
        nf = node_f.get(r.Location)
        if nf is None:
            continue
        for j, fdr in enumerate(FEEDERS):
            nl[fdr] += a_ / 1000.0 * (on & (nf == j) & in26).sum()
    # copper losses: each node's units at their rating's share of the node's monthly energy, on the hourly profile of
    # the feeder that served it, with the square of the loading
    cu = {fdr: 0.0 for fdr in FEEDERS}
    units = defaultdict(lambda: [0.0, 0.0])
    for r in reg.itertuples():
        if isinstance(r.RemovedDate, str) and r.RemovedDate:
            continue
        v = "2010 and later" if int(r.MfgYear) >= 2010 else "before 2010"
        units[r.Location][0] += float(r.kVA)
        units[r.Location][1] += xt[(float(r.kVA), v)][1] / 1000.0
    Sh = {fdr: np.sqrt(np.nan_to_num(EIN[fdr]) ** 2 + np.nan_to_num(MV[fdr]) ** 2) for fdr in FEEDERS}
    msum = {fdr: pd.Series(np.nan_to_num(EIN[fdr])).groupby(mon_h).transform("sum").values for fdr in FEEDERS}
    for nd, (kva, llr) in units.items():
        nf = node_f.get(nd)
        if nf is None or nd not in load_nd or kva <= 0:
            continue
        mk = pd.Series(load_nd[nd]).groupby(mon_day).sum()
        mkh = np.array([max(mk.get(m, 0.0), 0.0) for m in mon_h])
        for j, fdr in enumerate(FEEDERS):
            sel = (nf == j) & in26
            if sel.any():
                s_node = mkh[sel] * Sh[fdr][sel] / np.maximum(msum[fdr][sel], 1e-9)
                cu[fdr] += float((llr * (s_node / kva) ** 2).sum()) / 1000.0
    tech = {}
    for j, fdr in enumerate(FEEDERS):
        dlv = agg["del"][j][d26].sum()
        lpx = agg["lp"][j][d26].sum()
        tech[fdr] = prim[fdr][in26].sum() + nl[fdr] + cu[fdr] * 1000.0 + 0.007 * (dlv + lpx)
    r4 = figs["R4_technical"]
    say("R4 APT-3 technical losses", abs(tech["APT-3"] / 1000.0 / r4["APT-3"] - 1) < 0.07,
        "%.1f vs %.1f" % (tech["APT-3"] / 1000.0, r4["APT-3"]))
    say("R4 APT-4 technical losses", abs(tech["APT-4"] / 1000.0 / r4["APT-4"] - 1) < 0.07,
        "%.1f vs %.1f" % (tech["APT-4"] / 1000.0, r4["APT-4"]))
    st_ = sum(tech.values()) / 1000.0
    say("R4 fourteen feeders' technical losses", abs(st_ / r4["fourteen feeders"] - 1) < 0.04, "%.1f" % st_)
    ntl = {}
    for j, fdr in enumerate(FEEDERS):
        ntl[fdr] = (EIN[fdr][in26].sum() + agg["rcv"][j][d26].sum() - agg["del"][j][d26].sum() -
                    agg["lp"][j][d26].sum() - agg["l"][j][d26].sum() - tech[fdr]) / 1000.0
    for fdr, v in figs["R5_ntl"].items():
        say("R5 %s non-technical loss" % fdr, abs(ntl[fdr] - v) <= max(75.0, 0.09 * v), "%.1f vs %.1f" % (ntl[fdr], v))
    four = sorted(sorted(ntl, key=lambda x: -ntl[x])[:4])
    say("R9 the four", four == sorted(figs["R9_sweep"]), four)
    # ---------------------------------------------------------------- R6 the utility's line loss
    reads["bd"] = pd.to_datetime(reads["BillDate"]).dt.date
    for lab, a, b, key in (("2024", dt.date(2023, 10, 1), dt.date(2024, 10, 1), "line loss, twelve months to September 2024"),
                           ("2026", dt.date(2025, 10, 1), dt.date(2026, 10, 1), "line loss, twelve months to September 2026")):
        tl = H.tz_convert(TZ)
        sel = (tl >= pd.Timestamp(a, tz=TZ)) & (tl < pd.Timestamp(b, tz=TZ))
        pur = sum(np.nansum(DP[s][sel]) for s in DP)
        rs = reads[(reads["bd"] >= a) & (reads["bd"] < b) & reads["AccountNo"].fillna("").str.len().gt(0)]
        billed = rs["kWh"].fillna(0).sum() - rs["kWhRcv"].fillna(0).sum()
        lbm = lb[(lb["Month"] >= a.isoformat()) & (lb["Month"] < b.isoformat())]["DeemedkWh"].sum()
        pct = 100.0 * (pur - billed - lbm) / pur
        say("R6 line loss, twelve months to September %s" % lab, abs(pct - figs["R6_bridge"][key]) < 0.05,
            "%.2f vs %.2f" % (pct, figs["R6_bridge"][key]))
    # ---------------------------------------------------------------- R7 the connections' demand
    ap = pd.read_excel(f_("large_load_service"), dtype={"ServicePointID": str})
    li = pd.read_csv(f_("idr_large_power"), dtype={"ServicePointID": str})
    pk = li.groupby("ServicePointID")["kWh"].max()
    words = ("cultivation", "cannabis", "growers", "botanicals", "gardens", "indoor farms", "harvest", "farms",
             "greenhouse")
    en = ap[ap["Status"] == "Energized"]
    grows = en[en["Applicant"].str.lower().apply(lambda n: any(w in n for w in words))]
    dfg = sum(pk[s] for s in grows["ServicePointID"]) / grows["Connected_kW"].sum()
    cs = en[en["Applicant"].str.contains("Cold Storage")]
    dfc = pk[cs["ServicePointID"].iloc[0]] / cs["Connected_kW"].iloc[0]
    for r in ap[ap["Status"] == "Approved"].itertuples():
        k = dfc if "Cold Storage" in r.Applicant else dfg
        v = r.Connected_kW * k
        g7 = figs["R7_new_peaks"][r.AppNo]
        say("R7 %s peak hourly demand" % r.AppNo, abs(v / g7 - 1) < 0.05, "%.1f vs %.1f" % (v, g7))
    # ---------------------------------------------------------------- R8 2027 on today's network
    hrs = np.nonzero(in26)[0]
    lastf = ET[-1]
    # each node's base-year hourly load: its monthly share of the tree that served it, times that breaker's flow
    LPn = defaultdict(lambda: np.zeros(len(H)))
    LQn = defaultdict(lambda: np.zeros(len(H)))
    for (a, b, _), tr in zip(epochs, ET):
        for fdr in FEEDERS:
            order, par = tr[fdr]
            for m in np.unique(mon_h[a:b]):
                hs = np.nonzero((mon_h[a:b] == m) & in26[a:b])[0] + a
                if not len(hs):
                    continue
                ld = {n: max(load_nd[n][mon_day == m].sum(), 0.0) if n in load_nd else 0.0 for n in order}
                tot = sum(ld.values())
                if tot <= 0:
                    continue
                Qh = MV[fdr][hs]
                Qh = np.where(np.isnan(Qh), 0.3 * np.nan_to_num(EIN[fdr][hs]), Qh)
                for n, v in ld.items():
                    if v > 0:
                        LPn[n][hs] += v / tot * np.nan_to_num(EIN[fdr][hs])
                        LQn[n][hs] += v / tot * Qh
    gs = []
    for sp_ in grows["ServicePointID"]:
        x = li[li["ServicePointID"] == sp_]["kWh"].values
        gs.append(x / x.max())
    gp = np.mean(np.vstack(gs), axis=0)
    gp = gp / gp.max()
    xs = li[li["ServicePointID"] == cs["ServicePointID"].iloc[0]]["kWh"].values
    cp = xs / xs.max()
    cwp = subprocess.run(["pdftotext", "-layout", f_("cwp_2027"), "-"], capture_output=True, text=True).stdout
    rec_segs = set(re.findall(r"OH-\d{6}", cwp))
    d27 = [d + dt.timedelta(days=365) for d in H[hrs].tz_convert(TZ).date]
    after = np.array([d >= dt.date(2027, 3, 15) for d in d27])
    t27 = {}
    for fdr in ("APT-4", "APT-3"):
        order, par = lastf[fdr]
        FPn = {n: LPn[n][hrs].copy() for n in order}
        FQn = {n: LQn[n][hrs].copy() for n in order}
        e_new = 0.0
        newx = []
        for r in ap[(ap["Status"] == "Approved") & (ap["Feeder"] == fdr)].itertuples():
            node = str(r.XfmrID).split(" at ")[-1].rstrip(")")
            kva = float(str(r.XfmrID).split("(new ")[1].split(" kVA")[0])
            on = np.array([d >= dt.date.fromisoformat(str(r.ServiceDate)[:10]) for d in d27])
            if "Cold Storage" in r.Applicant:
                p = r.Connected_kW * dfc * cp * on
                q = p * np.tan(np.arccos(0.87))
            else:
                p = r.Connected_kW * dfg * gp * on
                q = p * np.tan(np.arccos(0.94))
            FPn[node] = FPn.get(node, np.zeros(len(hrs))) + p
            FQn[node] = FQn.get(node, np.zeros(len(hrs))) + q
            e_new += p.sum()
            newx.append((kva, p, q, on))
        loss = np.zeros(len(hrs))
        for n in reversed(order[1:]):
            u, kind, ident = par[n]
            if kind == "g":
                R, k = seginfo[ident]
                if ident in rec_segs:
                    R = np.where(after, R / cond["4/0 ACSR"] * cond["336.4 ACSR"], R)
                loss += k * R * (FPn[n] ** 2 + FQn[n] ** 2) / 12.47 ** 2 / 1000.0
            FPn[u] = FPn.get(u, 0) + FPn[n]
            FQn[u] = FQn.get(u, 0) + FQn[n]
        extra = 0.0
        for kva, p, q, on in newx:
            a_, b_ = xt[(kva, "2010 and later")]
            extra += a_ / 1000.0 * on.sum() + (b_ / 1000.0 * ((np.sqrt(p ** 2 + q ** 2) / kva) ** 2)).sum()
        j = FEEDERS.index(fdr)
        base_nl_cu = nl[fdr] + cu[fdr]
        dlv = agg["del"][j][d26].sum() + agg["lp"][j][d26].sum()
        t27[fdr] = (loss.sum() + base_nl_cu + extra + 0.007 * (dlv + e_new)) / 1000.0
    r8 = figs["R8_tech2027"]
    for fdr in ("APT-4", "APT-3"):
        say("R8 %s 2027 technical losses" % fdr, abs(t27[fdr] / r8[fdr] - 1) < 0.07, "%.1f vs %.1f" % (t27[fdr], r8[fdr]))
    print("\n%s: %d failed" % ("VERIFY PASS" if not FAILS else "VERIFY FAIL", len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
