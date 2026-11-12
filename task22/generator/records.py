"""task22: what each system records of the clean truth. The wholesale delivery point meters (hour-ending, standard
time all year), the feeder breakers' telemetry in the historian (hour-beginning local clock, its communication
failures and a stale transducer), the customer information system's reads (AMR routes on twenty business-day cycles
with estimated reads trued up later, AMI meters read at midnight on the first, meter exchanges, register rollovers
and CT multipliers, vacant premises read but not billed), the large power interval meters, the lights billed at
their lamp codes' deemed kWh, the GIS as it stands today, the asset register, the OMS switching log in its two naming
schemes, and the rest. Nothing here is placed to be caught: each record is what that system writes."""
import datetime as dt
import math
from collections import defaultdict

import numpy as np

import params as P
import world as WD

UTC = dt.timezone.utc
CST = dt.timezone(dt.timedelta(hours=-6))


def business_days(year, month):
    d = dt.date(year, month, 1)
    out = []
    while d.month == month:
        if d.weekday() < 5 and d not in P.HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def add_business(d, n):
    while n > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in P.HOLIDAYS:
            n -= 1
    return d


# ---------------------------------------------------------------------------------------------------------------
# customers' metered energy, day by day: outages, PV export, meter registration
# ---------------------------------------------------------------------------------------------------------------

def customer_metered(w):
    """Per customer and day: kWh consumed at the premises after outages (true), delivered and received through the
    meter (true), and what the meter registered (delivered and received, after a slow AMR meter or a tampered one)."""
    g = w.g
    D = g.D
    n = len(w.cust)
    share = {c: (w.u[c] / np.maximum(w.dayU[c][g.day], 1e-9)) for c in sorted(set(x["cls"] for x in w.cust))}
    cons = w.E.copy()
    node_cust = defaultdict(list)
    for i, c in enumerate(w.cust):
        node_cust[c["node"]].append(i)
    hours_out = defaultdict(list)            # customer -> list of (h0, h1): outages, the storm, maintenance
    for nd, spans in w.out_mask.items():
        for i in node_cust.get(nd, []):
            hours_out[i].extend(spans)
    for i, spans in hours_out.items():
        c = w.cust[i]
        u = share[c["cls"]]
        mask = np.zeros(g.H, dtype=bool)
        for h0, h1 in spans:
            mask[h0:h1] = True
        lost = np.bincount(g.day[mask], weights=u[mask], minlength=D)
        cons[i] -= w.E[i] * lost
    cons = np.maximum(cons, 0.0)
    deliv = cons.copy()
    recv = np.zeros((n, D))
    for i, gen in w.pv.items():
        c = w.cust[i]
        u = share[c["cls"]]
        load = w.E[i][g.day] * u
        # outage hours carry no load and no generation
        gen = gen.astype(np.float64).copy()
        for h0, h1 in hours_out.get(i, []):
            gen[h0:h1] = 0
            load[h0:h1] = 0
        cons[i] = np.bincount(g.day, weights=load, minlength=D)
        dh = np.maximum(load - gen, 0)
        rh = np.maximum(gen - load, 0)
        deliv[i] = np.bincount(g.day, weights=dh, minlength=D)
        recv[i] = np.bincount(g.day, weights=rh, minlength=D)
    # registration: an AMR meter runs slow until it is exchanged; a tampered commercial meter registers a share
    regd = deliv.copy()
    regr = recv.copy()
    for i, c in enumerate(w.cust):
        ex = (c["ami_date"] - g.d0).days if c["ami_date"] else D
        ex = max(0, min(D, ex))
        regd[i, :ex] *= c["slow"]
        regr[i, :ex] *= c["slow"]
        if c["tamper"]:
            a, b, k = c["tamper"]
            i0, i1 = max(0, (a - g.d0).days), max(0, min(D, (b - g.d0).days))
            regd[i, i0:i1] *= k
    w.cons, w.deliv, w.recv, w.regd, w.regr = cons, deliv, recv, regd, regr
    return w


# ---------------------------------------------------------------------------------------------------------------
# CIS meter reads
# ---------------------------------------------------------------------------------------------------------------

def account_on(c, d):
    """The account billed for a read: the occupant's, or between occupants the property owner's account, which
    the city bills for a vacant premises."""
    for a, b, acct in c["accounts"]:
        if a <= d and (b is None or d < b):
            return acct
    return "5" + c["sp"]


def meter_reads(w, rng):
    """One row per read: AMR cycle reads (actual or estimated), meter exchanges (final and initial), AMI month-end
    reads, initial reads on new service points; registers cumulative with rollover, kWh the billed usage."""
    g = w.g
    rows = []
    first_month = (2023, 8)
    months = []
    y, m = first_month
    while (y, m) <= (2026, 10):
        months.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    # cumulative registered energy at the start of each day
    cumd = np.concatenate([np.zeros((len(w.cust), 1)), np.cumsum(w.regd, axis=1)], axis=1)
    cumr = np.concatenate([np.zeros((len(w.cust), 1)), np.cumsum(w.regr, axis=1)], axis=1)
    pre = 30   # August 2023 reads: the days before the simulation are carried at the first month's daily rate

    def at(cum, i, d):
        k = (d - g.d0).days
        if k < 0:
            return cum[i, 0] + k * (cum[i, 30] - cum[i, 0]) / 30.0
        return cum[i, min(k, g.D)]

    for i, c in enumerate(w.cust):
        mult = 1
        if c["cls"] == "SC" and c["a"] > 22:
            mult = int(rng.choice([40, 80]))
        meter_amr = "%s%07d" % ("E", int(rng.integers(1000000, 9999999)))
        meter_ami = "%s%08d" % ("A", int(rng.integers(10000000, 99999999)))
        off_d = float(rng.uniform(1000, 60000))
        off_r = float(rng.uniform(0, 3000)) if c["pv_kw"] > 0 else 0.0
        ex = c["ami_date"]
        start = c["start"]
        reads = []
        for (y, m) in months:
            if ex is None or dt.date(y, m, 1) <= ex:
                bd = business_days(y, m)
                d = bd[min(c["cycle"] - 1, len(bd) - 1)]
                if ex is not None and d >= ex:
                    continue
                if start and d <= start:
                    continue
                reads.append(("AMR", d))
            if ex is not None:
                d1 = dt.date(y, m, 1)
                if d1 > ex and (not start or d1 > start):
                    reads.append(("AMI", d1))
        events = []
        if start and start >= dt.date(2023, 8, 1):
            events.append((start, "I", "AMI" if (ex is not None and start >= ex) else "AMR"))
        if ex is not None and (not start or ex > start) and ex < dt.date(2026, 11, 1):
            events.append((ex, "F", "AMR"))
            events.append((ex, "I", "AMI"))
        for kind, d in reads:
            events.append((d, "A" if kind == "AMR" else "M", kind))
        events.sort(key=lambda e: (e[0], {"F": 0, "I": 1}.get(e[1], 2)))
        last = None        # (date, true register, billed register) on the current meter
        rural = P.FEEDERS[c["feeder"]]["kind"] == "rural"
        history = []
        for d, typ, kind in events:
            if d >= dt.date(2026, 11, 1):
                continue
            true_d = at(cumd, i, d)
            true_r = at(cumr, i, d)
            if typ == "I":
                base_d = 0.0 if kind == "AMI" else off_d
                last = dict(kind=kind, d=d, t0=true_d, t0r=true_r, base=base_d, baser=0.0 if kind == "AMI" else off_r,
                            reg=base_d, regr=0.0 if kind == "AMI" else off_r)
                rows.append(_row(w, c, i, d, "I", kind, meter_ami if kind == "AMI" else meter_amr, last["reg"],
                                 0.0, last["regr"], 0.0, mult, account_on(c, d)))
                continue
            if last is None:
                last = dict(kind=kind, d=d, t0=true_d, t0r=true_r, base=off_d, baser=off_r, reg=off_d, regr=off_r)
                if d < dt.date(2023, 9, 1):
                    rows.append(_row(w, c, i, d, "A", kind, meter_amr, last["reg"], None, last["regr"], None, mult,
                                     account_on(c, d)))
                    continue
            actual_reg = last["base"] + (true_d - last["t0"])
            actual_regr = last["baser"] + (true_r - last["t0r"])
            est = False
            if typ == "A" and kind == "AMR":
                p = (0.075 if d.month in (12, 1, 2) else 0.03) * (1.6 if rural else 1.0)
                est = rng.random() < p
            if est:
                days = (d - last["d"]).days
                ref = [h for h in history if (d - h[0]).days > 330 and (d - h[0]).days < 400]
                if ref:
                    use = ref[-1][1] * days / max(ref[-1][2], 1)
                else:
                    use = (history[-1][1] * days / max(history[-1][2], 1)) if history else 1.0 * days
                reg = last["reg"] + use
                regr = last["regr"]
                kwh = use
                kwr = 0.0
                rtype = "E"
            else:
                reg, regr = actual_reg, actual_regr
                kwh = reg - last["reg"]
                kwr = regr - last["regr"]
                rtype = typ
            days = (d - last["d"]).days
            meter = meter_ami if kind == "AMI" else meter_amr
            if kind == "AMI" and typ == "F":
                meter = meter_amr
            rows.append(_row(w, c, i, d, rtype, kind if typ != "F" else "AMR", meter, reg, kwh, regr, kwr, mult,
                             account_on(c, d)))
            history.append((d, kwh, max(days, 1)))
            last["reg"], last["regr"], last["d"] = reg, regr, d
    return rows


def _row(w, c, i, d, rtype, kind, meter, reg, kwh, regr, kwr, mult, acct):
    roll = 100000.0 if kind == "AMR" else 1000000.0
    disp = (reg / mult) % roll
    dispr = (regr / mult) % roll if c["pv_kw"] > 0 else None
    return dict(sp=c["sp"], account=acct, meter=meter, rate=c["rate"], cycle=c["cycle"] if kind == "AMR" else None,
                read_date=d, read_type=rtype, register=disp, kwh=kwh, register_rcv=dispr,
                kwh_rcv=kwr if c["pv_kw"] > 0 else None, mult=mult, meter_type=kind, cust=i)


def lp_actual(w, lp):
    x = w.lp_load[lp["key"]].astype(np.float64).copy()
    for h0, h1 in w.out_mask.get(lp["node"], []):
        x[h0:h1] = 0
    return x


def lp_reads(w, rng):
    """Large power accounts: interval meters read at midnight on the first, every month."""
    g = w.g
    rows = []
    for lp in w.lp:
        x = lp_actual(w, lp)
        daily = np.bincount(g.day, weights=x, minlength=g.D)
        cum = np.concatenate([[0.0], np.cumsum(daily)])
        base = float(rng.uniform(100000, 900000))
        mult = int(rng.choice([400, 600, 800, 1200]))
        prev = None
        d = dt.date(2023, 9, 1)
        while d <= dt.date(2026, 11, 1):
            k = (d - g.d0).days
            if lp["start"] and d < lp["start"]:
                pass
            else:
                # September 2023, before the simulated record, is carried at October's daily rate
                reg = base + (cum[min(k, g.D)] if k >= 0 else k * cum[30] / 30.0)
                kwh = None if prev is None else reg - prev
                rows.append(dict(sp=lp["sp"], account="9%07d" % (int(lp["key"][2:]) * 1311 % 9999991), meter=lp["meter"],
                                 rate="LP" if lp["cls"] not in ("WATER",) else "CITY-NB", cycle=None, read_date=d,
                                 read_type="M" if prev is not None else "I", register=(reg / mult) % 1000000.0,
                                 kwh=kwh, register_rcv=None, kwh_rcv=None, mult=mult, meter_type="IDR", cust=None,
                                 lp=lp["key"]))
                prev = reg
            d = (d.replace(day=28) + dt.timedelta(days=5)).replace(day=1)
    return rows


# ---------------------------------------------------------------------------------------------------------------
# substation and feeder metering
# ---------------------------------------------------------------------------------------------------------------

def delivery_points(w, rng):
    """BMPA's revenue meters at each substation's 69 kV side: kWh per hour ending, Central Standard Time all year."""
    g = w.g
    rows = []
    for s, spec in P.SUBSTATIONS.items():
        x = w.dp[s] * (1 + rng.normal(0, 0.0004, g.H))
        q = (sum(w.head_Q[f] for f in P.SUB_FEEDERS[s])) * (1 + rng.normal(0, 0.002, g.H))
        for h in range(g.H):
            he = (g.utc[h] + dt.timedelta(hours=1)).astimezone(CST)
            rows.append((spec["dp"], he.strftime("%Y-%m-%d"), he.hour if he.hour else 24, round(float(x[h]), 1),
                         round(float(q[h]), 1)))
    return rows


def scada(w, rng):
    """The historian's hourly averages for each feeder breaker, labelled by the hour's start in local clock time:
    the November repeated hour appears twice, the March hour is skipped. Communication failures blank the value;
    a transducer that stuck in August 2025 repeats its last value with good quality."""
    g = w.g
    gaps = defaultdict(set)
    for f in P.FEEDER_ORDER:
        h = 0
        while h < g.H:
            h += int(rng.exponential(300))
            n = int(rng.integers(1, 6))
            for k in range(h, min(g.H, h + n)):
                gaps[f].add(k)
            h += n
    # the North RTU lost its link for an afternoon in June 2025
    a = WD.hour_index(w, dt.datetime(2025, 6, 11, 13, 0, tzinfo=P.TZ))
    for f in P.SUB_FEEDERS["NTH"]:
        gaps[f].update(range(a, a + 14))
    # Cherry Hill 3's relay lost communications through the ice storm
    s0 = WD.hour_index(w, P.STORM["gap_start"].replace(tzinfo=P.TZ))
    s1 = WD.hour_index(w, P.STORM["gap_end"].replace(tzinfo=P.TZ))
    gaps["CHL-3"].update(range(s0, s1))
    stale = set(range(WD.hour_index(w, dt.datetime(2025, 8, 18, 9, 0, tzinfo=P.TZ)),
                      WD.hour_index(w, dt.datetime(2025, 8, 20, 13, 0, tzinfo=P.TZ))))
    rows = []
    tag = {f: "%s_F%s" % (f[:3], f[-1]) for f in P.FEEDER_ORDER}
    for f in P.FEEDER_ORDER:
        mw = w.head_P[f] / 1000.0 * (1 + rng.normal(0, 0.0025, g.H))
        mvar = w.head_Q[f] / 1000.0 * (1 + rng.normal(0, 0.004, g.H))
        hold = None
        for h in range(g.H):
            lab = g.loc[h].strftime("%Y-%m-%d %H:00")
            if h in gaps[f]:
                rows.append((lab, tag[f], None, None, "COMM FAIL"))
                continue
            if f == "APT-2" and h in stale:
                if hold is None:
                    hold = (round(float(mw[h - 1]), 3), round(float(mvar[h - 1]), 3))
                rows.append((lab, tag[f], hold[0], hold[1], "GOOD"))
                continue
            rows.append((lab, tag[f], round(float(mw[h]), 3), round(float(mvar[h]), 3), "GOOD"))
    w.scada_gaps = gaps
    w.scada_stale = stale
    return rows


def lp_interval(w):
    """The large power meters' hourly kWh for October 2025 to September 2026, hour ending, local standard time."""
    g = w.g
    m = (g.dord >= P.WIN26[0].toordinal()) & (g.dord < P.WIN26[1].toordinal())
    rows = []
    for lp in w.lp:
        x = lp_actual(w, lp)
        for h in np.nonzero(m)[0]:
            he = (g.utc[h] + dt.timedelta(hours=1)).astimezone(CST)
            rows.append((lp["sp"], lp["meter"], he.strftime("%Y-%m-%d %H:%M"), round(float(x[h]), 2)))
    return rows


# ---------------------------------------------------------------------------------------------------------------
# lights, the GIS, the asset register, the OMS
# ---------------------------------------------------------------------------------------------------------------

def lamp_billed(L, d):
    """The lamp code the lighting bill carries in the month starting d."""
    if L["billed_led"] and d >= L["billed_led"].replace(day=1):
        return P.LED_FOR[L["lamp"]]
    return L["lamp"]


def light_accounts(w, rng):
    """Street lights billed to the city by district (one account per feeder area), area lights to the customers who
    rent them. Each light carries its account."""
    acct = {}
    for f in P.FEEDER_ORDER:
        acct[f] = "70%06d" % int(rng.integers(100000, 999999))
    area_accts = {}
    for L in w.lights:
        if L["kind"] == "Street":
            L["account"] = acct[L["feeder"]]
        else:
            # an area light is billed on the account of a customer near it
            if L["node"] not in area_accts:
                area_accts[L["node"]] = "%08d" % int(rng.integers(10000000, 99999999))
            L["account"] = area_accts[L["node"]]
    return acct


def lights_billing(w):
    """Monthly unmetered lighting charges: account, month, lamp code, lamps billed and deemed kWh."""
    rows = []
    d = dt.date(2023, 9, 1)
    while d < dt.date(2026, 11, 1):
        agg = defaultdict(int)
        for L in w.lights:
            if L["install"] <= d:
                agg[(L["account"], L["kind"], lamp_billed(L, d))] += 1
        for (acct, kind, code), n in sorted(agg.items()):
            rows.append(dict(account=acct, month=d, kind=kind, lamp=code, lamps=n, kwh=n * P.DEEMED_KWH[code]))
        d = (d.replace(day=28) + dt.timedelta(days=5)).replace(day=1)
    return rows


def gis_feeder_today(w):
    """The GIS feeder attribute: each node's feeder in the network as it stands at the extract (last epoch)."""
    tr = w.ep_trees[-1]
    out = {}
    for f, (order, _, _) in tr.items():
        for n in order:
            out[n] = f
    return out


def gis_export(w, rng):
    """The GIS as it stands at the extract: segments, switches with today's normal state, transformers in service
    and service points, each carrying the feeder the network gives it today."""
    today = gis_feeder_today(w)
    net = w.net
    segs = []
    for s in net.seg:
        f = today.get(s["b"]) or today.get(s["a"]) or s["feeder"]
        segs.append(dict(SegmentID=s["id"], Feeder=f, FromNode=s["a"], ToNode=s["b"],
                         Length_ft=int(round(s["mi"] * 5280)), Conductor=s["cond"], Phasing=s["phasing"],
                         InstallYear=s["year"]))
    sws = []
    for k, s in enumerate(net.sw):
        f = today.get(s["a"]) or today.get(s["b"]) or s["feeder"]
        sws.append(dict(SwitchID=s["id"], DeviceType=s["kind"], NodeA=s["a"], NodeB=s["b"], NormalState=s["normal"],
                        PoleTag=s["pole_tag"], Feeder=f))
    xfs = []
    for x in w.xfmrs:
        if x["removed"]:
            continue
        xfs.append(dict(XfmrID=x["id"], Node=x["node"], kVA=x["kva"], Mount=x["kind"], MfgYear=x["mfg"],
                        InService=x["install"], Feeder=today.get(x["node"], x["feeder"])))
    sps = []
    for c in w.cust:
        xf = w.xfmrs[c["xf"]]
        sps.append(dict(ServicePointID=c["sp"], XfmrID=xf["id"], Feeder=today.get(c["node"], c["feeder"]),
                        RateCode=c["rate"], MeterType="AMI" if c["ami_date"] else "AMR"))
    for lp in w.lp:
        xf = w.xfmrs[lp["xf"]]
        sps.append(dict(ServicePointID=lp["sp"], XfmrID=xf["id"], Feeder=today.get(lp["node"], lp["feeder"]),
                        RateCode="LP" if lp["cls"] != "WATER" else "CITY-NB", MeterType="IDR"))
    return segs, sws, xfs, sps


def xfmr_register(w):
    """The asset register: every distribution transformer in service since 2019, with its removal date."""
    rows = []
    for x in w.xfmrs:
        if x["removed"] and x["removed"] < dt.date(2019, 1, 1):
            continue
        rows.append(dict(AssetID=x["id"], kVA=x["kva"], MfgYear=x["mfg"], InstallDate=x["install"],
                         RemovedDate=x["removed"], Location=x["node"], Mount=x["kind"]))
    return rows


def legacy_name(tag):
    a, b = tag.split("-")
    return "%s %s" % (a, b)


def oms_log(w, rng):
    """Switching orders from the OMS: before the July 2024 upgrade the OMS names a device by its pole tag in the old
    style; from the upgrade on by its GIS switch id."""
    rows = []
    crews = ["Line 2", "Line 4", "Line 5", "Line 7", "Serv 1", "Serv 3", "Sub 1"]
    seq = defaultdict(int)
    # the OMS numbers every order (switching, tags, holds, restorations) in one sequence a year, so the switching
    # orders in this extract skip the numbers the other order types took
    gaps = np.random.default_rng(P.SEED + 61)
    for o in w.ops:
        s = w.net.sw[o["sw"]]
        dev = legacy_name(s["pole_tag"]) if o["t"] < P.OMS_CUTOVER else s["id"]
        yr = o["t"].year
        seq[yr] += int(gaps.integers(1, 16))
        rows.append(dict(OrderNo="SO-%02d-%04d" % (yr % 100, seq[yr]), Device=dev, Operation=o["op"],
                         DateTime=o["t"].strftime("%m/%d/%Y %H:%M"), Reason=o["reason"],
                         Crew=crews[int(rng.integers(0, len(crews)))]))
    return rows


def oms_xref(w, rng):
    """The device crosswalk built at the OMS upgrade: the old OMS name for each switch then in service and its GIS
    id, keyed by hand at the upgrade, about one switch in eight missed."""
    rows = []
    for s in w.net.sw:
        if rng.random() < 0.12:
            continue
        rows.append(dict(OMS_Device=legacy_name(s["pole_tag"]), GIS_SwitchID=s["id"], Mapped="2024-07-12"))
    return rows


def station_service(w):
    g = w.g
    rows = []
    for s in P.SUBSTATIONS:
        ss = w.dp[s + "_ss"]
        d = dt.date(2023, 9, 1)
        while d < dt.date(2026, 11, 1):
            n = (d.replace(day=28) + dt.timedelta(days=5)).replace(day=1)
            m = (g.dord >= d.toordinal()) & (g.dord < n.toordinal())
            rows.append(dict(Substation=P.SUBSTATIONS[s]["name"], Month=d.strftime("%Y-%m"),
                             kWh=int(round(float(ss[m].sum())))))
            d = n
    return rows


def applications(w, rng):
    """Large load service applications 2019 to 2027: connected load as applied, by component, and status."""
    rows = []
    roads = ["E 360 Rd", "S 4320 Rd", "N 4410 Rd", "E 250 Rd", "S 4200 Rd", "W 290 Rd", "N 4380 Rd", "E 330 Rd"]
    for lp in w.lp:
        if lp["key"] in P.LP_BEFORE_2019:
            continue
        light = round(lp["conn_kw"] * float(rng.uniform(0.52, 0.62)), 0) if lp["cls"] == "GROW" else round(
            lp["conn_kw"] * 0.08)
        hvac = round(lp["conn_kw"] * float(rng.uniform(0.28, 0.36)), 0) if lp["cls"] == "GROW" else round(
            lp["conn_kw"] * 0.55)
        proc = lp["conn_kw"] - light - hvac
        n = int(rng.integers(10, 990))
        addr = "%d %s" % (int(rng.integers(10000, 49999)), roads[int(rng.integers(0, len(roads)))])
        req = lp["energized"] - dt.timedelta(days=int(rng.integers(60, 200)))
        # an application is numbered in the year it was received
        rows.append(dict(AppNo="LL-%d-%03d" % (req.year, n), Applicant=lp["name"], ServiceAddress=addr,
                         Feeder=lp["feeder"], XfmrID=w.xfmrs[lp["xf"]]["id"], RateClass="LP",
                         Lighting_kW=light, HVAC_kW=hvac, Process_kW=proc, Connected_kW=lp["conn_kw"],
                         Requested=req, Status="Energized", ServiceDate=lp["energized"], ServicePointID=lp["sp"]))
    # the 2026 applications approved for 2027, numbered in the order received
    ar = np.random.default_rng(P.SEED + 69)
    nums = sorted(int(x) for x in ar.choice(np.arange(20, 990), len(P.NEW_2027), replace=False))
    new = []
    for key, f, name, cls, kw, pos, en, kva in P.NEW_2027:
        light = round(kw * 0.58) if cls == "GROW" else round(kw * 0.06)
        hvac = round(kw * 0.32) if cls == "GROW" else round(kw * 0.60)
        node = w.net.trunk[f][min(len(w.net.trunk[f]) - 1, int(round(pos * (len(w.net.trunk[f]) - 1))))]
        new.append(dict(AppNo="", Applicant=name, ServiceAddress="%d %s" % (
            int(rng.integers(10000, 49999)), roads[int(rng.integers(0, len(roads)))]), Feeder=f,
            XfmrID="(new %d kVA at %s)" % (kva, node), RateClass="LP", Lighting_kW=light, HVAC_kW=hvac,
            Process_kW=kw - light - hvac, Connected_kW=kw,
            Requested=dt.date(2026, int(rng.integers(3, 9)), int(ar.integers(2, 28))),
            Status="Approved", ServiceDate=dt.date(*en), ServicePointID=""))
    for r, n in zip(sorted(new, key=lambda r: r["Requested"]), nums):
        r["AppNo"] = "LL-2026-%03d" % n
    rows += new
    # two withdrawn applications
    for k in range(2):
        f = ["IND-3", "NTH-4"][k]
        rows.append(dict(AppNo="LL-2025-%03d" % int(rng.integers(10, 990)), Applicant=["Prairie Sky Gardens LLC",
                                                                                         "Grand Lake Harvest"][k],
                         ServiceAddress="%d %s" % (int(rng.integers(10000, 49999)), roads[k]), Feeder=f, XfmrID="",
                         RateClass="LP", Lighting_kW=[310, 260][k], HVAC_kW=[170, 140][k], Process_kW=[40, 30][k],
                         Connected_kW=[520, 430][k], Requested=dt.date(2025, [3, 8][k], 2), Status="Withdrawn",
                         ServiceDate=None, ServicePointID=""))
    # each year's numbers run in the order the applications were received
    by_year = defaultdict(list)
    for r in rows:
        by_year[r["AppNo"][3:7]].append(r)
    for yr, rs in by_year.items():
        nums = sorted(r["AppNo"][8:] for r in rs)
        for r, n in zip(sorted(rs, key=lambda r: r["Requested"]), nums):
            r["AppNo"] = "LL-%s-%s" % (yr, n)
    rows.sort(key=lambda r: r["AppNo"])
    return rows


def outage_log(w, rng):
    """The OMS outage record (customers interrupted, start and restore), unplanned and planned."""
    rows = []
    cust_at = defaultdict(int)
    for c in w.cust:
        cust_at[c["node"]] += 1
    for o in w.outages:
        n = cust_at.get(o["node"], 0)
        if n == 0:
            continue
        rows.append(dict(EventID="OE%07d" % int(rng.integers(1000000, 9999999)), Feeder=w.net.node_feeder[o["node"]],
                         Start=o["start"].strftime("%Y-%m-%d %H:%M"), Restored=o["end"].strftime("%Y-%m-%d %H:%M"),
                         Customers=n, Cause=o["cause"], Planned="N"))
    for nd, spans in w.deen.items():
        n = cust_at.get(nd, 0)
        if n == 0:
            continue
        for h0, h1 in spans:
            rows.append(dict(EventID="OE%07d" % int(rng.integers(1000000, 9999999)), Feeder=w.net.node_feeder[nd],
                             Start=w.g.loc[h0].strftime("%Y-%m-%d %H:%M"),
                             Restored=w.g.loc[min(h1, w.g.H - 1)].strftime("%Y-%m-%d %H:%M"), Customers=n,
                             Cause="Planned maintenance", Planned="Y"))
    # merge planned spans per event start so a feeder section shows as one event
    rows.sort(key=lambda r: (r["Start"], r["Feeder"]))
    merged = []
    for r in rows:
        if merged and r["Planned"] == "Y" and merged[-1]["Planned"] == "Y" and merged[-1]["Start"] == r["Start"] and (
                merged[-1]["Feeder"] == r["Feeder"]):
            merged[-1]["Customers"] += r["Customers"]
            continue
        merged.append(dict(r))
    return merged


def weather_daily(w):
    g = w.g
    rows = []
    for k, d in enumerate(g.dates):
        m = g.day == k
        rows.append(dict(DATE=d.isoformat(), TMAX=round(float(w.T[m].max() * 9 / 5 + 32)),
                         TMIN=round(float(w.T[m].min() * 9 / 5 + 32)),
                         PRCP=round(float(max(0.0, (0.5 - w.clear[k]) * 1.4)), 2) if w.clear[k] < 0.5 else 0.0))
    return rows
