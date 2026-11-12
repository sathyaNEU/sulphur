"""task22 analysis on the pack as a solver reads it: every result's golden computation and the hurried analyst's
routes, from the shipped frames only (golden.py loads the files into these frames; the generator's calibration
builds the same frames in memory). Nothing here reads the simulation.

The balance for a feeder and a period: the energy that entered at its breaker, plus what its customers' meters
received from their solar, is what their meters delivered, what the large power meters recorded, what the city's
unmetered lights used, what the lines and transformers lost, and what is left: the non-technical loss."""
import datetime as dt
import math
from collections import defaultdict, deque
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

TZ = ZoneInfo("America/Chicago")
UTC = dt.timezone.utc
CST = dt.timezone(dt.timedelta(hours=-6))
T0 = dt.datetime(2023, 9, 1, 6, 0, tzinfo=UTC)           # 2023-09-01 00:00 Central standard time
T1 = dt.datetime(2026, 11, 1, 5, 0, tzinfo=UTC)          # 2026-11-01 00:00 local, where the extracts end
H = int((T1 - T0).total_seconds() // 3600)
V_KV = 12.47
WIN26 = (dt.date(2025, 10, 1), dt.date(2026, 10, 1))
WIN24 = (dt.date(2023, 10, 1), dt.date(2024, 10, 1))
SUBS = {"North": "NTH", "Industrial Park": "IND", "Airport Road": "APT", "Cherry Hill": "CHL"}
DP_OF = {"DLM-NTH69": "NTH", "DLM-IND69": "IND", "DLM-APT69": "APT", "DLM-CHL69": "CHL"}
FEEDERS = ["NTH-1", "NTH-2", "NTH-3", "NTH-4", "IND-1", "IND-2", "IND-3", "APT-1", "APT-2", "APT-3", "APT-4",
           "CHL-1", "CHL-2", "CHL-3"]
SUB_FEEDERS = {s: [f for f in FEEDERS if f[:3] == s] for s in ("NTH", "IND", "APT", "CHL")}


class Grid:
    def __init__(self):
        self.utc = [T0 + dt.timedelta(hours=k) for k in range(H)]
        self.loc = [u.astimezone(TZ) for u in self.utc]
        self.date = [x.date() for x in self.loc]
        self.dord = np.array([d.toordinal() for d in self.date])
        self.d0 = self.date[0]
        self.day = self.dord - self.d0.toordinal()
        self.D = int(self.day.max()) + 1
        self.dates = [self.d0 + dt.timedelta(days=k) for k in range(self.D)]
        self.month = np.array([d.year * 100 + d.month for d in self.date])

    def mask(self, win):
        return (self.dord >= win[0].toordinal()) & (self.dord < win[1].toordinal())

    def dmask(self, win):
        return np.array([win[0] <= d < win[1] for d in self.dates])


G = Grid()


def hidx_utc(u):
    return int((u - T0).total_seconds() // 3600)


# ---------------------------------------------------------------------------------------------------------------
# R1: each feeder's energy in, the breaker metering's gaps filled from the delivery point balance
# ---------------------------------------------------------------------------------------------------------------

def parse_dp(F):
    dp = F["dp"]
    out = {s: np.full(H, np.nan) for s in SUB_FEEDERS}
    outq = {s: np.full(H, np.nan) for s in SUB_FEEDERS}
    for row in dp.itertuples(index=False):
        s = DP_OF[row.DeliveryPoint]
        d = dt.date.fromisoformat(row.Date) if isinstance(row.Date, str) else row.Date
        he = int(row.HourEnding)
        end = dt.datetime(d.year, d.month, d.day, tzinfo=CST) + dt.timedelta(hours=he)
        h = hidx_utc((end - dt.timedelta(hours=1)).astimezone(UTC))
        if 0 <= h < H:
            out[s][h] = row.kWh
            outq[s][h] = row.kVArh
    return out, outq


def parse_scada(F):
    sc = F["scada"].copy()
    sc["fold"] = sc.groupby(["Point", "Timestamp"]).cumcount()
    mw = {f: np.full(H, np.nan) for f in FEEDERS}
    mv = {f: np.full(H, np.nan) for f in FEEDERS}
    tagf = {"%s_F%s" % (f[:3], f[-1]): f for f in FEEDERS}
    cache = {}
    for row in sc.itertuples(index=False):
        key = (row.Timestamp, row.fold)
        if key not in cache:
            t = dt.datetime.strptime(row.Timestamp, "%Y-%m-%d %H:%M").replace(tzinfo=TZ, fold=row.fold)
            cache[key] = hidx_utc(t.astimezone(UTC))
        h = cache[key]
        if not (0 <= h < H):
            continue
        f = tagf[row.Point]
        if row.Quality == "GOOD" and row.MW == row.MW:
            mw[f][h] = row.MW * 1000.0
            mv[f][h] = row.MVAR * 1000.0
    # a value repeated to the kW for six hours or more is a stuck transducer: treat as missing
    for f in FEEDERS:
        x = mw[f]
        run = 1
        for h in range(1, H):
            # an open breaker reads zero for as long as it is open: zeros are readings, not a stuck transducer
            if x[h] == x[h] and x[h] == x[h - 1] and x[h] != 0.0:
                run += 1
                if run == 6:
                    x[h - 5:h + 1] = np.nan
                    mv[f][h - 5:h + 1] = np.nan
                elif run > 6:
                    x[h] = np.nan
                    mv[f][h] = np.nan
            else:
                run = 1
    return mw, mv


def station_service_hourly(F):
    ss = F["station_service"]
    out = {s: np.zeros(H) for s in SUB_FEEDERS}
    months = defaultdict(list)
    for h in range(H):
        months[G.month[h]].append(h)
    for row in ss.itertuples(index=False):
        s = SUBS[row.Substation]
        y, m = map(int, row.Month.split("-"))
        hs = months.get(y * 100 + m, [])
        if hs:
            out[s][hs] = row.kWh / len(hs)
    return out


def sub_transformer(F):
    t = F["subxf"]
    return {SUBS[r.Substation]: (r.NoLoad_kW, r.LoadLoss_kW, r.Rating_MVA) for r in t.itertuples(index=False)}


def energy_in(F, fill="balance"):
    """Hourly breaker energy per feeder (kWh) with each missing hour filled. fill: 'balance' (the golden: the
    delivery point less the substation transformer's losses, station service and the other feeders), 'mean' (the
    feeder's average for that hour of day over its valid hours in the month), 'interp' (linear across the gap),
    'drop' (missing hours count nothing)."""
    mw, mv = parse_scada(F)
    dp, dpq = parse_dp(F)
    ss = station_service_hourly(F)
    sx = sub_transformer(F)
    out, outq = {}, {}
    for s, fs in SUB_FEEDERS.items():
        nl, ll, mva = sx[s]
        P = np.vstack([mw[f] for f in fs])
        Q = np.vstack([mv[f] for f in fs])
        miss = np.isnan(P)
        if fill == "balance":
            # the substation's feeders together: delivery point less station service and the transformer's losses
            tot_q = dpq[s]
            S = np.sqrt(dp[s] ** 2 + tot_q ** 2)
            feeders_tot = dp[s] - ss[s] - (nl + ll * (S / (mva * 1000.0)) ** 2)
            known = np.where(miss, 0.0, P).sum(axis=0)
            nmiss = miss.sum(axis=0)
            resid = feeders_tot - known
            Pf = P.copy()
            Qf = Q.copy()
            # shares of each feeder in the same hour of the nearest days where all reported
            for h in np.nonzero(nmiss)[0]:
                js = np.nonzero(miss[:, h])[0]
                if len(js) == 1:
                    Pf[js[0], h] = resid[h]
                else:
                    sh = np.zeros(len(js))
                    for dd in (24, -24, 48, -48, 168, -168):
                        k = h + dd
                        if 0 <= k < H and not np.isnan(P[js, k]).any():
                            sh += P[js, k]
                    sh = sh / sh.sum() if sh.sum() > 0 else np.ones(len(js)) / len(js)
                    Pf[js, h] = resid[h] * sh
                for j in js:
                    # reactive power at the feeder's own power factor in the nearest valid hour
                    for dd in (1, -1, 2, -2, 24, -24):
                        k = h + dd
                        if 0 <= k < H and not np.isnan(P[j, k]) and P[j, k] > 0:
                            Qf[j, h] = Pf[j, h] * Q[j, k] / P[j, k]
                            break
                    else:
                        Qf[j, h] = 0.3 * Pf[j, h]
        else:
            Pf = P.copy()
            Qf = Q.copy()
            for j in range(len(fs)):
                x, q = Pf[j], Qf[j]
                bad = np.isnan(x)
                if fill == "drop":
                    x[bad] = 0.0
                    q[bad] = 0.0
                elif fill == "interp":
                    idx = np.arange(H)
                    x[bad] = np.interp(idx[bad], idx[~bad], x[~bad])
                    q[bad] = np.interp(idx[bad], idx[~bad], q[~bad])
                elif fill == "mean":
                    hod = np.array([u.hour for u in G.loc])
                    for mth in np.unique(G.month[bad]):
                        sel = G.month == mth
                        for hh in range(24):
                            cell = sel & (hod == hh)
                            ok = cell & ~bad
                            v = x[ok].mean() if ok.any() else np.nanmean(x[sel])
                            vq = q[ok].mean() if ok.any() else np.nanmean(q[sel])
                            x[cell & bad] = v
                            q[cell & bad] = vq
        for j, f in enumerate(fs):
            out[f] = Pf[j]
            outq[f] = Qf[j]
    return out, outq


# ---------------------------------------------------------------------------------------------------------------
# R2: the network, who each feeder served month by month, and what their meters recorded
# ---------------------------------------------------------------------------------------------------------------

def norm_tag(x):
    return str(x).strip().upper().replace(" ", "-")


class Network:
    def __init__(self, F, history=True):
        segs, sws = F["gis_segments"], F["gis_switches"]
        self.seg = {r.SegmentID: dict(a=r.FromNode, b=r.ToNode, ft=r.Length_ft, cond=r.Conductor, ph=r.Phasing)
                    for r in segs.itertuples(index=False)}
        self.sw = {r.SwitchID: dict(a=r.NodeA, b=r.NodeB, normal=r.NormalState, tag=norm_tag(r.PoleTag))
                   for r in sws.itertuples(index=False)}
        self.adj = defaultdict(list)
        for k, s in self.seg.items():
            self.adj[s["a"]].append(("seg", k))
            self.adj[s["b"]].append(("seg", k))
        for k, s in self.sw.items():
            self.adj[s["a"]].append(("sw", k))
            self.adj[s["b"]].append(("sw", k))
        self.breakers = {f: "BKR-" + f for f in FEEDERS}
        # switching history: the OMS's two naming schemes linked to the GIS switch ids
        xref = {norm_tag(r.OMS_Device): r.GIS_SwitchID for r in F["oms_xref"].itertuples(index=False)}
        by_tag = {s["tag"]: k for k, s in self.sw.items()}
        ops = []
        unmatched = 0
        for r in F["oms_log"].itertuples(index=False):
            t = dt.datetime.strptime(r.DateTime, "%m/%d/%Y %H:%M").replace(tzinfo=TZ)
            dev = str(r.Device).strip()
            sid = dev if dev in self.sw else (xref.get(norm_tag(dev)) or by_tag.get(norm_tag(dev)))
            if sid is None:
                unmatched += 1
                continue
            ops.append((t, sid, r.Operation == "CLOSE"))
        ops.sort()
        self.unmatched = unmatched
        today = {k: s["normal"] == "Closed" for k, s in self.sw.items()}
        if history:
            # the state before the first operation on each switch is the opposite of that operation
            start = dict(today)
            seen = set()
            for t, sid, close in ops:
                if sid not in seen:
                    start[sid] = not close
                    seen.add(sid)
            self.ops = ops
        else:
            start = dict(today)
            self.ops = []
        # epochs on the hour grid
        ev = defaultdict(list)
        for t, sid, close in self.ops:
            ev[max(0, hidx_utc(t.astimezone(UTC)))].append((sid, close))
        epochs = []
        cur = dict(start)
        h0 = 0
        for h in sorted(ev):
            if h > h0:
                epochs.append((h0, h, dict(cur)))
            for sid, close in ev[h]:
                cur[sid] = close
            h0 = h
        epochs.append((h0, H, dict(cur)))
        self.epochs = epochs
        self.trees = [self.bfs(closed) for (_, _, closed) in epochs]

    def bfs(self, closed):
        seen = {}
        out = {}
        for f in FEEDERS:
            root = self.breakers[f]
            q = deque([root])
            seen[root] = f
            order, pseg, pnode = [root], {root: None}, {root: None}
            while q:
                u = q.popleft()
                for kind, k in self.adj[u]:
                    if kind == "sw" and not closed[k]:
                        continue
                    s = self.seg[k] if kind == "seg" else self.sw[k]
                    v = s["b"] if s["a"] == u else s["a"]
                    if v in seen or str(v).startswith("BKR"):
                        continue
                    seen[v] = f
                    pseg[v] = (kind, k)
                    pnode[v] = u
                    order.append(v)
                    q.append(v)
            out[f] = (order, pseg, pnode)
        return out

    def node_feeder_hourly(self, nodes):
        """For each node, its feeder in every hour (index into FEEDERS, -1 when no breaker reaches it)."""
        fi = {f: i for i, f in enumerate(FEEDERS)}
        out = {n: np.full(H, -1, dtype=np.int8) for n in nodes}
        for (h0, h1, _), tr in zip(self.epochs, self.trees):
            for f, (order, _, _) in tr.items():
                for n in order:
                    if n in out:
                        out[n][h0:h1] = fi[f]
        return out


def calendarize(F, weights=None):
    """Each service point's delivered and received kWh day by day from its reads. An estimated read is folded into
    the actual read that trues it up, so its period and the next become one; a period's kWh is spread over its days
    evenly (weights None) or in proportion to weights[the service point's feeder] (a daily array)."""
    r = F["reads"].drop_duplicates().copy()
    r["d"] = pd.to_datetime(r["ReadDate"]).dt.date
    r["o"] = r["ReadType"].map({"F": 0, "I": 1}).fillna(2)
    r = r.sort_values(["ServicePointID", "d", "o"])
    D = G.D
    spf = F.get("_sp_home", {})
    idx, dels, rcvs = {}, [], []
    for sp, grp in r.groupby("ServicePointID", sort=True):
        wd = weights.get(spf.get(sp)) if weights else None
        dd = np.zeros(D)
        rr = np.zeros(D)
        pend_kwh = pend_rcv = 0.0
        pend_start = None
        prev = None
        for row in grp.itertuples(index=False):
            if row.ReadType == "I":
                prev = row.d
                pend_kwh = pend_rcv = 0.0
                pend_start = None
                continue
            if prev is None:
                prev = row.d
                continue
            k = row.kWh if row.kWh == row.kWh else 0.0
            kr = row.kWhRcv if row.kWhRcv == row.kWhRcv else 0.0
            if pend_start is None:
                pend_start = prev
            pend_kwh += k
            pend_rcv += kr
            if row.ReadType == "E":
                prev = row.d
                continue
            a = (pend_start - G.d0).days
            b = (row.d - G.d0).days
            if b > a:
                seg = np.ones(b - a)
                lo, hi = max(a, 0), min(b, D)
                if wd is not None and hi > lo:
                    seg[lo - a:hi - a] = wd[lo:hi]
                    if a < 0:
                        seg[:lo - a] = wd[lo]
                    if b > D:
                        seg[hi - a:] = wd[hi - 1]
                seg = seg / seg.sum()
                if hi > lo:
                    dd[lo:hi] += pend_kwh * seg[lo - a:hi - a]
                    rr[lo:hi] += pend_rcv * seg[lo - a:hi - a]
            pend_kwh = pend_rcv = 0.0
            pend_start = None
            prev = row.d
        idx[sp] = len(dels)
        dels.append(dd)
        rcvs.append(rr)
    return idx, np.array(dels), np.array(rcvs)


def billed_in(F, win):
    """kWh on customer bills issued in a window (the line loss summary's basis): billed accounts only, net of what
    net-metered customers' meters received, with the large power bills and the lights' deemed kWh."""
    r = F["reads"].drop_duplicates()
    bd = pd.to_datetime(r["BillDate"]).dt.date
    sel = (bd >= win[0]) & (bd < win[1]) & r["AccountNo"].astype(str).str.len().gt(0) & (r["AccountNo"].astype(str) != "nan")
    k = r.loc[sel, "kWh"].fillna(0).sum() - r.loc[sel, "kWhRcv"].fillna(0).sum()
    lb = F["lights_billing"]
    m = pd.to_datetime(lb["Month"]).dt.date
    lk = lb.loc[(m >= win[0]) & (m < win[1]), "DeemedkWh"].sum()
    return float(k), float(lk)


# ---------------------------------------------------------------------------------------------------------------
# where every load sits, and on which feeder each hour
# ---------------------------------------------------------------------------------------------------------------

def locations(F):
    """Service point -> transformer -> node; large power service points; each light's node; transformers by node."""
    sp = F["gis_sp"]
    xf = F["gis_xf"]
    xnode = dict(zip(xf["XfmrID"], xf["Node"]))
    reg = F["xfmr_register"]
    for r in reg.itertuples(index=False):
        xnode.setdefault(r.AssetID, r.Location)
    sp_node = {r.ServicePointID: xnode.get(r.XfmrID) for r in sp.itertuples(index=False)}
    sp_home = dict(zip(sp["ServicePointID"], sp["Feeder"]))
    lp_sp = set(sp.loc[sp["MeterType"] == "IDR", "ServicePointID"])
    return sp_node, sp_home, lp_sp


def day_fractions(nf_hourly):
    """(D x 14) share of each day's hours a node spent on each feeder."""
    out = np.zeros((G.D, len(FEEDERS)))
    for j in range(len(FEEDERS)):
        out[:, j] = np.bincount(G.day, weights=(nf_hourly == j).astype(float), minlength=G.D)
    tot = np.bincount(G.day, minlength=G.D).astype(float)
    return out / tot[:, None]


def lights_actual_daily(F):
    """Each light's kWh a day at its input watts (the lamp it carried that day) and the month's burning hours."""
    inv = F["lights_inventory"]
    bh = F["burn_hours"]
    burn = {int(r.Month): float(r.BurningHours) for r in bh.itertuples(index=False)}
    watts = {r.LampCode: float(r.Input_W) for r in F["lamp_watts"].itertuples(index=False)}
    days_in = defaultdict(int)
    for d in G.dates:
        days_in[(d.year, d.month)] += 1
    import calendar
    nodes, daily = [], []
    for r in inv.itertuples(index=False):
        x = np.zeros(G.D)
        ins = pd.to_datetime(r.InstallDate).date()
        led = pd.to_datetime(r.LEDConversion).date() if isinstance(r.LEDConversion, str) and r.LEDConversion else None
        for k, d in enumerate(G.dates):
            if d < ins:
                continue
            code = r.LEDLampCode if (led and d >= led) else r.LampCode
            nd = calendar.monthrange(d.year, d.month)[1]
            x[k] = watts[code] * burn[d.month] / nd / 1000.0
        nodes.append(r.PoleNode)
        daily.append(x)
    return nodes, np.array(daily)


_PARTS = {}


def _bid(F):
    return F.get("_bid") or id(F)


def _part(key, fn):
    if key not in _PARTS:
        _PARTS[key] = fn()
    return _PARTS[key]


def build_state(F, topology="history", fill="balance", calendar_by="breaker"):
    """Everything the balance needs, assembled once per route from parts shared across routes: hourly breaker
    energy (per fill), the network and each node's feeder by hour (per topology), the customers' daily use (per
    calendarisation), the lights."""
    bid = _bid(F)
    pert = F.get("_pert", "")
    st = {}
    sp_node, sp_home, lp_sp = _part((bid, "loc"), lambda: locations(F))
    F["_sp_home"] = sp_home
    sub_p = pert if "substation" in pert else ""
    st["P"], st["Q"] = _part((bid, "ein", fill, sub_p), lambda: energy_in(F, fill=fill))
    net = _part((bid, "net", topology), lambda: Network(F, history=(topology == "history")))
    st["net"] = net

    def cal():
        if calendar_by == "breaker":
            # a read period's kWh follows the substation's own daily energy at the delivery point (a feeder's
            # breaker can be open for days while its customers are fed from a neighbour)
            dp, _ = parse_dp(F)
            sub_day = {s: np.maximum(np.bincount(G.day, weights=np.nan_to_num(dp[s]), minlength=G.D), 1.0)
                       for s in SUB_FEEDERS}
            wts = {f: sub_day[f[:3]] for f in FEEDERS}
        else:
            wts = None
        return calendarize(F, wts)
    idx, dels, rcvs = _part((bid, "cal", calendar_by), cal)
    st["sp_idx"], st["dels"], st["rcvs"] = idx, dels, rcvs
    burn_p = pert if "burning" in pert else ""
    l_nodes, l_daily = _part((bid, "lights", burn_p), lambda: lights_actual_daily(F))
    reg = F["xfmr_register"]

    def nf():
        nodes = set(v for v in sp_node.values() if v) | set(l_nodes) | set(reg["Location"])
        h = net.node_feeder_hourly(nodes)
        if topology == "today":
            gis_today = {}
            for r in F["gis_segments"].itertuples(index=False):
                gis_today[r.ToNode] = r.Feeder
                gis_today.setdefault(r.FromNode, r.Feeder)
            fi = {f: i for i, f in enumerate(FEEDERS)}
            h = {n: np.full(H, fi.get(gis_today.get(n), h[n][-1]), dtype=np.int8) for n in nodes}
        return h
    st["nfh"] = _part((bid, "nfh", topology), nf)
    dayfrac = _part((bid, "dayfrac", topology), lambda: {})

    def frac(n):
        if n not in dayfrac:
            dayfrac[n] = day_fractions(st["nfh"][n])
        return dayfrac[n]
    st["frac"] = frac
    st["sp_node"], st["sp_home"], st["lp_sp"] = sp_node, sp_home, lp_sp
    st["l_nodes"], st["l_daily"] = l_nodes, l_daily
    return st


def by_feeder_daily(st):
    """(14 x D) matrices: delivered and received by customers (large power apart), large power, lights."""
    D = G.D
    out = {k: np.zeros((len(FEEDERS), D)) for k in ("del", "rcv", "lp", "lights")}
    node_del = defaultdict(lambda: np.zeros(D))
    node_rcv = defaultdict(lambda: np.zeros(D))
    node_lp = defaultdict(lambda: np.zeros(D))
    for sp, i in st["sp_idx"].items():
        n = st["sp_node"].get(sp)
        if n is None:
            continue
        if sp in st["lp_sp"]:
            node_lp[n] += st["dels"][i]
        else:
            node_del[n] += st["dels"][i]
            node_rcv[n] += st["rcvs"][i]
    node_l = defaultdict(lambda: np.zeros(D))
    for n, x in zip(st["l_nodes"], st["l_daily"]):
        node_l[n] += x
    for key, src in (("del", node_del), ("rcv", node_rcv), ("lp", node_lp), ("lights", node_l)):
        for n, x in src.items():
            fr = st["frac"](n)
            out[key] += (fr * x[:, None]).T
    st["node_del"], st["node_rcv"], st["node_lp"], st["node_l"] = node_del, node_rcv, node_lp, node_l
    return out


# ---------------------------------------------------------------------------------------------------------------
# R4: technical losses at each load's position on the network
# ---------------------------------------------------------------------------------------------------------------

def conductor_r(F):
    return {r.Conductor: float(r.R50_ohm_per_mile) for r in F["conductors"].itertuples(index=False)}


def xfmr_losses_table(F):
    t = F["xfmr_losses"]
    return {(float(r.kVA), r.Vintage): (float(r.NoLoad_W), float(r.LoadLoss_W)) for r in t.itertuples(index=False)}


def technical(F, st, alloc="kwh_month", reconductor=None, extra=None, months=None):
    """Hourly technical losses per feeder (kW): primary I2R through an equivalent resistance built from each
    month's load at its nodes on the tree that served them, transformer core and copper losses, and secondary
    losses at the 2019 study's 0.7 per cent of energy delivered to services. alloc: 'kwh_month' (golden),
    'kwh_year', 'kva'. reconductor: {segment id: conductor} from a date; extra: new loads for 2027."""
    net = st["net"]
    rc = conductor_r(F)
    xt = xfmr_losses_table(F)
    sp_node = st["sp_node"]
    D = G.D
    # monthly metered load at each node (net of received), large power and lights included
    node_load_daily = defaultdict(lambda: np.zeros(D))
    for n, x in st["node_del"].items():
        node_load_daily[n] += x
    for n, x in st["node_rcv"].items():
        node_load_daily[n] -= x
    for n, x in st["node_lp"].items():
        node_load_daily[n] += x
    for n, x in st["node_l"].items():
        node_load_daily[n] += x
    mon_days = defaultdict(list)
    for k, d in enumerate(G.dates):
        mon_days[d.year * 100 + d.month].append(k)
    node_month = {}
    for n, x in node_load_daily.items():
        node_month[n] = {m: max(x[ks].sum(), 0.0) for m, ks in mon_days.items()}
    node_year = {n: max(sum(v.values()), 0.0) for n, v in node_month.items()}
    kva_node = defaultdict(float)
    for r in F["gis_xf"].itertuples(index=False):
        kva_node[r.Node] += float(r.kVA)
    prim = {f: np.zeros(H) for f in FEEDERS}
    cache = {}
    for ei, ((h0, h1, _), tr) in enumerate(zip(net.epochs, net.trees)):
        months_here = np.unique(G.month[h0:h1])
        for f in FEEDERS:
            order, pseg, pnode = tr[f]
            if len(order) <= 1:
                continue
            for m in months_here:
                sel = np.nonzero(G.month[h0:h1] == m)[0] + h0
                if alloc == "kva":
                    load = {n: kva_node.get(n, 0.0) for n in order}
                elif alloc == "kwh_year":
                    load = {n: node_year.get(n, 0.0) for n in order}
                else:
                    load = {n: node_month.get(n, {}).get(m, 0.0) for n in order}
                tot = sum(load.values())
                if tot <= 0:
                    continue
                down = dict(load)
                for j in range(len(order) - 1, 0, -1):
                    n = order[j]
                    down[pnode[n]] += down[n]
                req = 0.0
                for j in range(1, len(order)):
                    n = order[j]
                    kind, k = pseg[n]
                    if kind != "seg":
                        continue
                    s = net.seg[k]
                    cond = s["cond"]
                    if reconductor and k in reconductor["segments"]:
                        cond = reconductor["new"]
                    R = s["ft"] / 5280.0 * rc[cond]
                    fac = 1.0 if s["ph"] == "ABC" else 6.0
                    req += fac * R * (down[n] / tot) ** 2
                Pp = np.nan_to_num(st["P"][f][sel])
                Qq = np.nan_to_num(st["Q"][f][sel])
                prim[f][sel] = req * (Pp ** 2 + Qq ** 2) / V_KV ** 2 / 1000.0
    # transformers: core losses while in service at the node's feeder, copper with the square of the load
    reg = F["xfmr_register"]
    nl = {f: np.zeros(H) for f in FEEDERS}
    ll = {f: np.zeros(H) for f in FEEDERS}
    fi = {f: i for i, f in enumerate(FEEDERS)}
    node_units = defaultdict(list)
    for r in reg.itertuples(index=False):
        ins = pd.to_datetime(r.InstallDate).date()
        rem = pd.to_datetime(r.RemovedDate).date() if isinstance(r.RemovedDate, str) and r.RemovedDate else None
        vint = "2010 and later" if int(r.MfgYear) >= 2010 else "before 2010"
        a, b = xt[(float(r.kVA), vint)]
        on = (G.dord >= ins.toordinal())
        if rem:
            on &= G.dord < rem.toordinal()
        nfh = st["nfh"].get(r.Location)
        if nfh is None:
            continue
        for j, f in enumerate(FEEDERS):
            sel = on & (nfh == j)
            if sel.any():
                nl[f][sel] += a / 1000.0
        node_units[r.Location].append((float(r.kVA), b, on))
    # copper: each node's units share its load in proportion to rating; the node's hourly load follows its
    # feeder's breaker profile within the month
    hourshare = {}
    for f in FEEDERS:
        Pp = np.nan_to_num(st["P"][f])
        Qq = np.nan_to_num(st["Q"][f])
        S = np.sqrt(Pp ** 2 + Qq ** 2)
        tot = np.zeros(H)
        for m, ks in mon_days.items():
            sel = G.month == m
            tot[sel] = Pp[sel].sum()
        hourshare[f] = np.where(tot > 0, S / np.maximum(tot, 1e-9), 0.0)
    for n, units in node_units.items():
        nfh = st["nfh"].get(n)
        if nfh is None or n not in node_month:
            continue
        kva_on = sum(u[0] for u in units if u[2][-1])
        if kva_on <= 0:
            continue
        llr = sum(u[1] for u in units if u[2][-1]) / 1000.0
        for j, f in enumerate(FEEDERS):
            sel = nfh == j
            if not sel.any():
                continue
            mk = np.array([node_month[n].get(m, 0.0) for m in G.month])
            s_node = mk * hourshare[f]
            ll[f][sel] += (llr * (s_node / kva_on) ** 2)[sel]
    sec = {f: np.zeros(H) for f in FEEDERS}
    deliv_month = defaultdict(float)
    return dict(prim=prim, nl=nl, ll=ll, node_month=node_month)


def window_sum(x, win):
    return float(np.nansum(x[G.mask(win)]))


def dwindow_sum(x, win):
    return float(np.nansum(x[G.dmask(win)]))


def balance(F, st, tech, win):
    """Each feeder's balance over a window (kWh): breaker energy in, received from customers, delivered to
    customers, large power, lights, technical (primary, core, copper, secondary) and the non-technical rest."""
    bf = st.get("_bf") or by_feeder_daily(st)
    st["_bf"] = bf
    out = {}
    for j, f in enumerate(FEEDERS):
        e_in = window_sum(st["P"][f], win)
        rcv = dwindow_sum(bf["rcv"][j], win)
        dlv = dwindow_sum(bf["del"][j], win)
        lp = dwindow_sum(bf["lp"][j], win)
        li = dwindow_sum(bf["lights"][j], win)
        pr = window_sum(tech["prim"][f], win)
        nl = window_sum(tech["nl"][f], win)
        cu = window_sum(tech["ll"][f], win)
        se = 0.007 * (dlv + lp)
        t = pr + nl + cu + se
        out[f] = dict(e_in=e_in, rcv=rcv, dlv=dlv, lp=lp, lights=li, prim=pr, nl=nl, cu=cu, sec=se, tech=t,
                      ntl=e_in + rcv - dlv - lp - li - t)
    return out


# ---------------------------------------------------------------------------------------------------------------
# the routes: the golden and the hurried analyst's shortcuts, each run end to end on the same frames
# ---------------------------------------------------------------------------------------------------------------

def study_table(F):
    t = F["study2019"]
    return {r.Feeder: dict(pct=float(r.Technical_pct), req=float(r.Req_ohm), nl=float(r.NoLoad_MWh),
                           ll=float(r.LoadLoss_MWh), energy=float(r.Energy_MWh), lsf=float(r.LossFactor),
                           peak=float(r.Peak_MW), prim=float(r.Primary_MWh)) for r in t.itertuples(index=False)}


_STATE = {}


def state(F, topology="history", fill="balance"):
    key = (_bid(F), F.get("_pert", ""), topology, fill)
    if key not in _STATE:
        st = build_state(F, topology=topology, fill=fill)
        st["_bf"] = by_feeder_daily(st)
        _STATE[key] = st
    return _STATE[key]


_TECH = {}


def tech_for(F, st, method="golden", key=None):
    k = (id(st), method, F.get("_pert", ""))
    if k not in _TECH:
        if method == "golden":
            _TECH[k] = technical(F, st)
        elif method in ("kva", "kwh_year"):
            _TECH[k] = technical(F, st, alloc=method)
        else:
            raise ValueError(method)
    return _TECH[k]


def ntl_route(F, win=WIN26, topology="history", fill="balance", tech="golden"):
    """Each feeder's non-technical loss over the window on one route: the topology replayed or today's GIS, the
    breaker gaps filled by the balance or carried, technical losses at the loads' positions or from the 2019
    study."""
    st = state(F, topology, fill)
    if tech in ("golden", "kva", "kwh_year"):
        t = tech_for(F, st, tech)
        b = balance(F, st, t, win)
        return {f: b[f]["ntl"] for f in FEEDERS}, b
    t = tech_for(F, st, "golden")
    b = balance(F, st, t, win)
    sd = study_table(F)
    out = {}
    for f in FEEDERS:
        x = b[f]
        if tech == "study_pct":
            tt = sd[f]["pct"] / 100.0 * x["e_in"]
        elif tech == "study_req":
            # the study's equivalent resistance on the window's hourly current, its core and copper losses scaled
            # to the window's energy, secondary at 0.7 per cent
            sel = G.mask(win)
            Pp = np.nan_to_num(st["P"][f][sel])
            Qq = np.nan_to_num(st["Q"][f][sel])
            prim = sd[f]["req"] * ((Pp ** 2 + Qq ** 2) / V_KV ** 2 / 1000.0).sum()
            tt = prim + sd[f]["nl"] * 1000.0 + sd[f]["ll"] * 1000.0 * (x["e_in"] / (sd[f]["energy"] * 1000.0)) ** 2 + \
                0.007 * (x["dlv"] + x["lp"])
        else:
            raise ValueError(tech)
        out[f] = x["e_in"] + x["rcv"] - x["dlv"] - x["lp"] - x["lights"] - tt
    return out, b


def top4(ntl):
    return sorted(ntl, key=lambda f: -ntl[f])[:4]


# ---------------------------------------------------------------------------------------------------------------
# R6: the line loss rise bridged; R7: the grows' demand; R8: 2027's technical losses
# ---------------------------------------------------------------------------------------------------------------

def purchases(F, win):
    dp, _ = parse_dp(F)
    return float(sum(np.nansum(dp[s][G.mask(win)]) for s in dp))


def deemed_lights(F, win):
    lb = F["lights_billing"]
    m = pd.to_datetime(lb["Month"]).dt.date
    return float(lb.loc[(m >= win[0]) & (m < win[1]), "DeemedkWh"].sum())


def bridge(F, st, tech, tech_method="golden", topology="history", fill="balance"):
    """The utility's line loss on its own basis (purchases less billed sales, over purchases) for the twelve months
    to September 2024 and to September 2026, each split into the substations, technical losses, non-technical losses,
    the lights (their real use less their deemed kWh) and billing (metered use not yet billed or never billed)."""
    out = {}
    for name, win in (("2024", WIN24), ("2026", WIN26)):
        b = balance(F, st, tech, win)
        if tech_method != "golden":
            n, _ = ntl_route(F, win=win, topology=topology, fill=fill, tech=tech_method)
        pur = purchases(F, win)
        billed_c, billed_l = billed_in(F, win)
        e_in = sum(x["e_in"] for x in b.values())
        rcv = sum(x["rcv"] for x in b.values())
        dlv = sum(x["dlv"] for x in b.values())
        lp = sum(x["lp"] for x in b.values())
        li = sum(x["lights"] for x in b.values())
        t = sum(x["tech"] for x in b.values())
        ntl = sum(x["ntl"] for x in b.values())
        if tech_method != "golden":
            ntl = sum(n.values())
            t = e_in + rcv - dlv - lp - li - ntl
        sub = pur - e_in
        loss = pur - billed_c - billed_l
        metered = dlv - rcv + lp
        parts = dict(substation=sub, technical=t, nontechnical=ntl, lights=li - billed_l, billing=metered - billed_c)
        out[name] = dict(purchases=pur, billed=billed_c + billed_l, loss=loss, pct=100.0 * loss / pur,
                         parts={k: 100.0 * v / pur for k, v in parts.items()}, kwh=parts)
    d = {k: out["2026"]["parts"][k] - out["2024"]["parts"][k] for k in out["2026"]["parts"]}
    out["change"] = d
    out["change_total"] = out["2026"]["pct"] - out["2024"]["pct"]
    return out


GROW_WORDS = ("cultivation", "cannabis", "growers", "botanicals", "gardens", "indoor farms", "harvest", "farms",
              "greenhouse")


def is_grow(name):
    n = str(name).lower()
    return any(k in n for k in GROW_WORDS)


def lp_hourly(F):
    li = F["lp_interval"]
    out = {}
    for sp, grp in li.groupby("ServicePointID"):
        x = np.full(H, np.nan)
        for r in grp.itertuples(index=False):
            end = dt.datetime.strptime(r.IntervalEnd, "%Y-%m-%d %H:%M").replace(tzinfo=CST)
            h = hidx_utc((end - dt.timedelta(hours=1)).astimezone(UTC))
            if 0 <= h < H:
                x[h] = r.kWh
        out[sp] = x
    return out


def demand_factors(F, how="aggregate"):
    """Each energized licensed grow's peak hourly demand in the base year over the connected load it applied for;
    the grows' factor (aggregate: their peaks over their connected loads; or the mean of their ratios); and the cold
    store's own."""
    ap = F["applications"]
    lp = lp_hourly(F)
    rows = []
    for r in ap.itertuples(index=False):
        if r.Status != "Energized" or not isinstance(r.ServicePointID, str) or r.ServicePointID not in lp:
            continue
        x = lp[r.ServicePointID]
        pk = float(np.nanmax(x))
        rows.append(dict(sp=r.ServicePointID, name=r.Applicant, conn=float(r.Connected_kW), peak=pk,
                         grow=is_grow(r.Applicant), ratio=pk / float(r.Connected_kW)))
    g = [x for x in rows if x["grow"]]
    if how == "aggregate":
        df = sum(x["peak"] for x in g) / sum(x["conn"] for x in g)
    else:
        df = float(np.mean([x["ratio"] for x in g]))
    cold = [x for x in rows if "cold storage" in x["name"].lower()]
    return dict(grow=df, cold=cold[0]["ratio"] if cold else None, rows=rows)


def profiles(F):
    """The base year's hourly shape of the existing grows (each normalised to its own peak, averaged, renormalised)
    and of the cold store, on the hour grid."""
    ap = F["applications"]
    lp = lp_hourly(F)
    gs = []
    cold = None
    for r in ap.itertuples(index=False):
        if r.Status != "Energized" or not isinstance(r.ServicePointID, str) or r.ServicePointID not in lp:
            continue
        x = lp[r.ServicePointID]
        if is_grow(r.Applicant):
            gs.append(x / np.nanmax(x))
        if "cold storage" in r.Applicant.lower():
            cold = x / np.nanmax(x)
    gp = np.nanmean(np.vstack(gs), axis=0)
    gp = gp / np.nanmax(gp)
    return np.nan_to_num(gp), np.nan_to_num(cold)


def node_hourly_base(F, st, hours, nm):
    """Each node's base-year load hour by hour: its share of the metered load on the tree that served it that month,
    times that feeder's breaker flow (so the node carries its part of the feeder's losses and unmetered load too)."""
    net = st["net"]
    hset = np.zeros(H, dtype=bool)
    hset[hours] = True
    LP = defaultdict(lambda: np.zeros(H))
    LQ = defaultdict(lambda: np.zeros(H))
    for (h0, h1, _), tr in zip(net.epochs, net.trees):
        sel_e = np.zeros(H, dtype=bool)
        sel_e[h0:h1] = True
        sel_e &= hset
        if not sel_e.any():
            continue
        for m in np.unique(G.month[sel_e]):
            sel = sel_e & (G.month == m)
            for g, (order, _, _) in tr.items():
                load = {n: nm.get(n, {}).get(m, 0.0) for n in order}
                tot = sum(load.values())
                if tot <= 0:
                    continue
                Pg = np.nan_to_num(st["P"][g])
                Qg = np.nan_to_num(st["Q"][g])
                for n, v in load.items():
                    if v > 0:
                        LP[n][sel] += v / tot * Pg[sel]
                        LQ[n][sel] += v / tot * Qg[sel]
    return LP, LQ


def tech_2027(F, st, df=None, flat_nameplate=False, ignore_reconductor=False, base_pct=None):
    """Each feeder's technical losses in 2027: the base year (the twelve months to September 2026) with each month
    standing for the same month of 2027, today's network, the approved connections from their service dates at the
    demand comparable members draw, and the APT-3 reconductor from its in-service date."""
    if df is None:
        df = demand_factors(F)
    gp, cp = profiles(F)
    net = st["net"]
    rc = conductor_r(F)
    xt = xfmr_losses_table(F)
    tr = net.trees[-1]
    win = WIN26
    selw = G.mask(win)
    hours = np.nonzero(selw)[0]
    d27 = np.array([dt.date(G.date[h].year + 1, G.date[h].month, min(G.date[h].day, 28 if G.date[h].month == 2 else 31))
                    for h in hours])
    if "_techfull" not in st:
        st["_techfull"] = technical(F, st)
    tb = st["_techfull"]
    nm = tb["node_month"]
    if "_nhb" not in st:
        st["_nhb"] = node_hourly_base(F, st, hours, nm)
    LP, LQ = st["_nhb"]
    new = []
    for r in F["applications"].itertuples(index=False):
        if r.Status != "Approved":
            continue
        node = str(r.XfmrID).split(" at ")[-1].rstrip(")")
        kva = float(str(r.XfmrID).split("(new ")[1].split(" kVA")[0])
        start = pd.to_datetime(r.ServiceDate).date()
        on = np.array([d >= start for d in d27])
        if "cold storage" in r.Applicant.lower():
            shape, fac, pf = cp[hours], df["cold"], 0.87
        else:
            shape, fac, pf = gp[hours], df["grow"], 0.94
        if flat_nameplate:
            p = float(r.Connected_kW) * np.ones(len(hours))
        else:
            p = float(r.Connected_kW) * fac * shape
        p = p * on
        new.append(dict(feeder=r.Feeder, node=node, p=p, q=p * math.tan(math.acos(pf)), kva=kva, on=on))
    rec = F.get("cwp")
    rec_from = pd.to_datetime(rec["in_service"]).date() if rec else None
    after = np.array([d >= rec_from for d in d27]) if rec else None
    b26 = balance(F, st, tb, win)
    out = {}
    for f in FEEDERS:
        order, pseg, pnode = tr[f]
        if len(order) <= 1:
            continue
        pos = {n: j for j, n in enumerate(order)}
        FP = [LP[n][hours].copy() if n in LP else np.zeros(len(hours)) for n in order]
        FQ = [LQ[n][hours].copy() if n in LQ else np.zeros(len(hours)) for n in order]
        e_new = 0.0
        for x in new:
            if x["feeder"] == f and x["node"] in pos:
                FP[pos[x["node"]]] += x["p"]
                FQ[pos[x["node"]]] += x["q"]
                e_new += float(x["p"].sum())
        prim = np.zeros(len(hours))
        for j in range(len(order) - 1, 0, -1):
            n = order[j]
            kind, k = pseg[n]
            if kind == "seg":
                s = net.seg[k]
                fac = 1.0 if s["ph"] == "ABC" else 6.0
                R = s["ft"] / 5280.0 * rc[s["cond"]]
                if rec and (not ignore_reconductor) and k in rec["segments"]:
                    R = np.where(after, s["ft"] / 5280.0 * rc[rec["new"]], R)
                prim += fac * R * (FP[j] ** 2 + FQ[j] ** 2) / V_KV ** 2 / 1000.0
            pj = pos[pnode[n]]
            FP[pj] += FP[j]
            FQ[pj] += FQ[j]
        nl = 0.0
        cu = 0.0
        # today's units on the feeder, all year; their copper scaled with the base year's own
        nl = float(tb["nl"][f][selw].sum())
        cu = float(tb["ll"][f][selw].sum())
        for x in new:
            if x["feeder"] == f:
                a_, bll = xt[(x["kva"], "2010 and later")]
                nl += a_ / 1000.0 * x["on"].sum()
                cu += float((bll / 1000.0 * ((np.sqrt(x["p"] ** 2 + x["q"] ** 2) / x["kva"]) ** 2)).sum())
        sec = 0.007 * (b26[f]["dlv"] + b26[f]["lp"] + e_new)
        tot_t = float(prim.sum()) + nl + cu + sec
        if base_pct is not None:
            tot_t = base_pct[f] / 100.0 * (b26[f]["e_in"] + e_new)
        out[f] = dict(prim=float(prim.sum()), nl=nl, cu=cu, sec=sec, tech=tot_t, e_new=e_new,
                      e_in=b26[f]["e_in"] + e_new)
    return out
