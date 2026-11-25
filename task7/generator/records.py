"""Member services' switch register, the cooperative's HVAC rebates, the county's mechanical permits, the switch test log,
the service work orders, and the two files the analysis has no use for (the monthly AMR reads and the winter water
heater schedule). The replaced-unit records are written from core's world: every switch core flags has a qualifying
rebate or permit dated after its install, no other switch has one, and records dated before an install, records for
other equipment and records at premises with no switch fill the files as they would."""
import datetime as dt

import numpy as np

import common as CM
import params as P

QUAL_REBATE = ("Central air conditioner", "Central heat pump (air source)")
OTHER_REBATE = ("Ductless mini-split", "Heat pump water heater", "Smart thermostat", "Attic insulation")
QUAL_PERMIT = ("REPLACE A/C CONDENSING UNIT", "REPLACE CONDENSING UNIT AND COIL", "HEAT PUMP CHANGE-OUT, SPLIT SYSTEM")
OTHER_PERMIT = ("FURNACE REPLACEMENT", "WATER HEATER", "GAS PIPING", "DUCTWORK ALTERATION", "MINI-SPLIT INSTALL",
                "BATH EXHAUST FAN", "BOILER REPAIR")
REBATE_START, PERMIT_START = dt.date(2012, 3, 1), dt.date(2010, 1, 4)
RECODE = dt.date(2021, 4, 1)             # the billing conversion: premise numbers re-keyed


def rdate(r, a, b):
    a, b = (a, b) if a <= b else (b, a)
    return a + dt.timedelta(int(r.integers(0, max((b - a).days, 1) + 1)))


def weekday(d):
    while d.weekday() >= 5:
        d -= dt.timedelta(1)
    return d


def install_dates(W, r):
    """A date for every switch inside its install year, in batch order: a paging group is a run of installs."""
    yr, grp = W["yr"], W["grp"]
    out = [None] * len(yr)
    for Y in range(2004, 2026):
        ids = np.flatnonzero(yr == Y)
        ids = ids[np.lexsort((W["order_u"][ids], grp[ids]))]
        n = len(ids)
        offs = np.sort(r.integers(3, 361, n))           # installs fall on working days through the year, in batch order
        for k, i in enumerate(ids):
            d = dt.date(Y, 1, 1) + dt.timedelta(int(offs[k]))
            wd_ = weekday(d)
            out[i] = wd_ if wd_.year == Y else d + dt.timedelta(7 - d.weekday())
    return out


def premises(W, r, study_xy):
    """The AC switches' premises, then the study homes', the water-heater-only and removed switches', and premises with
    no switch: numbers, old numbers, addresses."""
    n_s = W["n_s"]
    n_st = len(W["study"]["d"])
    n_wh_only, n_rem, n_out = 1130, 140, 9200
    # positions: the AC premises are core's; the rest are drawn around the feeders
    xs, ys, ds = list(W["x"]), list(W["y"]), list(W["dist"][W["sf"]])
    st_x, st_y = study_xy
    xs += list(st_x)
    ys += list(st_y)
    ds += [0] * n_st
    extra_f = r.integers(0, W["n_feed"], n_wh_only + n_rem + n_out)
    ex = W["cent"][extra_f] + r.normal(0, 2.2, (len(extra_f), 2))
    xs += list(ex[:, 0])
    ys += list(ex[:, 1])
    ds += list(W["dist"][extra_f])
    xs, ys, ds = np.array(xs), np.array(ys), np.array(ds)
    addr = CM.addresses(xs, ys, ds, r)
    nums = CM.premise_numbers(len(xs), r)
    est = []
    for i in range(len(xs)):
        est.append(int(r.integers(1958, 2021)) if r.random() < 0.9 else int(r.integers(2021, 2026)))
    olds, seen = [], set()
    for i in range(len(xs)):
        if est[i] >= 2021:
            olds.append("")
            continue
        while True:
            o = CM.old_number(ds[i], r)
            if o not in seen:
                seen.add(o)
                olds.append(o)
                break
    return dict(x=xs, y=ys, dist=ds, addr=addr, no=nums, old=olds, est=est, n_s=n_s, n_st=n_st,
                wh_only=np.arange(n_s + n_st, n_s + n_st + n_wh_only), removed=np.arange(n_s + n_st + n_wh_only, n_s + n_st + n_wh_only + n_rem),
                outside=np.arange(n_s + n_st + n_wh_only + n_rem, len(xs)), extra_feeder=extra_f)


def serial(yr, vhf, r, used):
    while True:
        s = "%s%02d-%06d" % ("CV" if vhf else "FX", yr % 100, int(r.integers(100000, 999999)))
        if s not in used:
            used.add(s)
            return s


def register(W, PR, inst, codes, r):
    rows, used = [], set()
    ser = [None] * W["n_s"]
    for i in range(W["n_s"]):
        ser[i] = serial(int(W["yr"][i]), bool(W["vhf"][i]), r, used)
        f = int(W["sf"][i])
        rows.append((ser[i], "Central air conditioner", PR["no"][i], PR["old"][i], PR["addr"][i][0], PR["addr"][i][1],
                     P.DISTRICTS[int(W["dist"][f])], codes[f], "%.3f" % W["x"][i], "%.3f" % W["y"][i],
                     P.VHF_FREQ if W["vhf"][i] else P.FLEX_FREQ, "AC-%02d" % (int(W["grp"][i]) + 1), CM.fmt_date(inst[i]),
                     "Active", ""))
    # removed A/C switches: the member left the programme or the house was vacated; batches from their install years
    gyr = [(int(W["yr"][W["grp"] == g].min()), int(W["yr"][W["grp"] == g].max())) for g in range(16)]
    for j in PR["removed"]:
        Y = int(r.integers(2004, 2019))
        g = max(k for k in range(16) if gyr[k][0] <= Y)
        f = int(PR["extra_feeder"][j - (PR["n_s"] + PR["n_st"])])
        d0 = weekday(dt.date(Y, 1, 2) + dt.timedelta(int(r.integers(0, 360))))
        dr = weekday(rdate(r, dt.date(2020, 1, 10), dt.date(2026, 5, 29)))
        rows.append((serial(Y, Y <= 2015, r, used), "Central air conditioner", PR["no"][j], PR["old"][j], PR["addr"][j][0],
                     PR["addr"][j][1], P.DISTRICTS[int(PR["dist"][j])], codes[f], "%.3f" % PR["x"][j], "%.3f" % PR["y"][j],
                     P.VHF_FREQ if Y <= 2015 else P.FLEX_FREQ, "AC-%02d" % (g + 1), CM.fmt_date(d0), "Removed", CM.fmt_date(dr)))
    # water heater switches: at two in five A/C premises and at premises with no A/C switch
    wh_at = list(r.choice(W["n_s"], 760, replace=False)) + list(PR["wh_only"])
    for j in wh_at:
        Y = int(r.integers(2008, 2025))
        if j < W["n_s"]:
            f = int(W["sf"][j])
            x, y = W["x"][j], W["y"][j]
        else:
            f = int(PR["extra_feeder"][j - (PR["n_s"] + PR["n_st"])])
            x, y = PR["x"][j], PR["y"][j]
        d0 = weekday(dt.date(Y, 1, 2) + dt.timedelta(int(r.integers(0, 360))))
        rows.append((serial(Y, Y <= 2015, r, used), "Electric water heater", PR["no"][j], PR["old"][j],
                     PR["addr"][j][0], PR["addr"][j][1], P.DISTRICTS[int(W["dist"][f])], codes[f], "%.3f" % x, "%.3f" % y,
                     P.VHF_FREQ if Y <= 2015 else P.FLEX_FREQ, "WH-%d" % (1 + int(r.integers(0, 4))), CM.fmt_date(d0),
                     "Active", ""))
    rows.sort(key=lambda t: (t[2], t[1]))
    return rows, ser


def replacements(W, inst, r):
    """When each replaced air conditioner went in (core's repl), and which records show it (core's flag: a rebate, a
    permit or both, dated after the switch's install)."""
    out = {}
    for i in np.flatnonzero(W["repl"]):
        lo = max(inst[i] + dt.timedelta(60), PERMIT_START + dt.timedelta(70))
        hi = dt.date(2026, 9, 12)
        D = weekday(rdate(r, lo, hi))
        kind = None
        if W["flag"][i]:
            if D < REBATE_START + dt.timedelta(30):
                kind = "permit"
            else:
                u = r.random()
                kind = "rebate" if u < 0.37 else ("permit" if u < 0.64 else "both")
        out[int(i)] = (D, kind)
    return out


def rebates_permits(W, PR, inst, REP, r):
    reb, per = [], []
    rno = [int(r.integers(1200, 1500))]
    pseq = {}

    def pnum(d):
        pseq[d.year] = pseq.get(d.year, int(r.integers(40, 160))) + int(r.integers(1, 4))
        return "M%02d-%05d" % (d.year % 100, pseq[d.year])

    def add_rebate(i, d, unit):
        no = PR["no"][i] if (d >= RECODE or not PR["old"][i]) else PR["old"][i]
        if d < dt.date(2021, 6, 15) and d >= RECODE and PR["old"][i] and r.random() < 0.18:
            no = PR["old"][i]                     # the first weeks after the conversion still took the old number
        paid = d + dt.timedelta(int(r.integers(18, 75)))
        amt = {"Central air conditioner": [250, 350, 450], "Central heat pump (air source)": [400, 550, 650],
               "Ductless mini-split": [300, 400], "Heat pump water heater": [300], "Smart thermostat": [50, 75],
               "Attic insulation": [150, 250]}[unit]
        seer = "%.1f" % (14 + 0.5 * int(r.integers(0, 9))) if unit in QUAL_REBATE else ""
        reb.append(["R%06d" % rno[0], str(no), unit, CM.fmt_date(d), CM.fmt_date(paid) if paid <= P.REGISTER_AT else "",
                    str(amt[int(r.integers(len(amt)))]), seer, P.CONTRACTORS[int(r.integers(len(P.CONTRACTORS)))]])
        rno[0] += int(r.integers(1, 6))

    def add_permit(i, d, work):
        a, city = PR["addr"][i]
        val = int(round(float(r.uniform(3200, 11800) if work in QUAL_PERMIT else r.uniform(400, 7800)), -1))
        status = "FINALED" if d < dt.date(2026, 7, 1) else ("ISSUED" if r.random() < 0.7 else "FINALED")
        per.append([pnum(d), CM.fmt_date(d), CM.county_style(a, r), city.upper(), work, str(val),
                    P.CONTRACTORS[int(r.integers(len(P.CONTRACTORS)))].upper(), status])

    n_s = W["n_s"]
    for i in range(n_s):
        D, kind = REP.get(i, (None, None))
        if kind in ("rebate", "both"):
            add_rebate(i, D, QUAL_REBATE[1] if r.random() < 0.16 else QUAL_REBATE[0])
        if kind in ("permit", "both"):
            pd_ = max(D - dt.timedelta(int(r.integers(1, 11))), inst[i] + dt.timedelta(35))
            add_permit(i, pd_, QUAL_PERMIT[2] if r.random() < 0.15 else QUAL_PERMIT[int(r.integers(0, 2))])
        # an air conditioner replaced before the switch went in (the switch was wired to the new unit)
        if r.random() < 0.13 and inst[i] > dt.date(2011, 9, 1):
            d = rdate(r, PERMIT_START + dt.timedelta(5), inst[i] - dt.timedelta(40))
            if d >= REBATE_START and r.random() < 0.6:
                add_rebate(i, d, QUAL_REBATE[0])
            else:
                add_permit(i, d, QUAL_PERMIT[0])
        # other equipment, any time
        if r.random() < 0.22:
            d = rdate(r, PERMIT_START, dt.date(2026, 9, 25))
            if d >= REBATE_START and r.random() < 0.5:
                add_rebate(i, d, OTHER_REBATE[int(r.integers(len(OTHER_REBATE)))])
            else:
                add_permit(i, d, OTHER_PERMIT[int(r.integers(len(OTHER_PERMIT)))])
    # the study homes rebated their new units before their switches went in; removed and water-heater-only premises and
    # premises with no switch take rebates and permits like anyone else
    for j in list(PR["wh_only"]) + list(PR["removed"]) + list(PR["outside"]):
        u = r.random()
        if u < 0.42:
            d = rdate(r, PERMIT_START, dt.date(2026, 9, 25))
            if d >= REBATE_START and r.random() < 0.45:
                add_rebate(j, d, (QUAL_REBATE + OTHER_REBATE)[int(r.integers(6))])
            else:
                add_permit(j, d, (QUAL_PERMIT + OTHER_PERMIT)[int(r.integers(10))])
        if u < 0.08:
            d = rdate(r, PERMIT_START, dt.date(2026, 9, 25))
            add_permit(j, d, OTHER_PERMIT[int(r.integers(len(OTHER_PERMIT)))])
    reb.sort(key=lambda t: (t[3], t[0]))
    per.sort(key=lambda t: (t[1], t[0]))
    # the county numbers its permits in issue order within each year (building and electrical permits share the series)
    seq = {}
    for row in per:
        yr_ = int(row[1][:4])
        seq[yr_] = seq.get(yr_, int(r.integers(30, 120))) + 1 + int(r.poisson(1.8))
        row[0] = "M%02d-%05d" % (yr_ % 100, seq[yr_])
    # renumber the rebates in date order, the way the rebate system issues them (numbers voided at the counter leave gaps)
    no = 3104
    for row in reb:
        row[0] = "R%06d" % no
        no += 1 + int(r.poisson(0.45))
    return reb, per


def test_log(W, PR, inst, ser, r):
    """The bench-signal test: at install, at a sample of premises each spring, and at service visits. A switch that fails
    is replaced on the spot (its serial leaves the register and the replacement's install test follows)."""
    rows = []
    n_s = W["n_s"]
    recent = [i for i in range(n_s) if inst[i] >= dt.date(2019, 1, 1)]
    swap = set(int(v) for v in r.choice(recent, int(0.094 * len(recent)), replace=False))
    used = set(ser)
    for i in recent:
        if i in swap:
            Y = int(r.integers(2004, 2016))
            old = serial(Y, Y <= 2015, r, used)
            rows.append([CM.fmt_date(inst[i]), old, str(PR["no"][i]), "Service visit", "FAIL", "replaced"])
        rows.append([CM.fmt_date(inst[i]), ser[i], str(PR["no"][i]), "Install", "PASS", ""])
    for Y in range(2019, 2027):
        cand = [i for i in range(n_s) if inst[i] < dt.date(Y, 3, 1)]
        for i in r.choice(cand, int(r.integers(330, 420)), replace=False):
            d = weekday(rdate(r, dt.date(Y, 3, 2), dt.date(Y, 5, 22)))
            rows.append([CM.fmt_date(d), ser[i], str(PR["no"][i]), "Annual sample", "PASS", ""])
    rows.sort(key=lambda t: (t[0], t[1]))
    return rows


def orders(W, PR, inst, REP, r):
    """Service visits made for other reasons. The technician notes whether an A/C switch is on site, whether the
    air conditioner has been replaced since it went in, and the switch's state if anything was seen."""
    reasons = ["Meter exchange", "High bill investigation", "Outage call", "Service upgrade", "Tree clearance",
               "Disconnect for non-payment", "Reconnect", "Voltage complaint", "Pole inspection follow-up"]
    n_s = W["n_s"]
    rows = []
    vis = []
    for _ in range(6300):
        i = int(r.integers(0, n_s))
        d = weekday(rdate(r, dt.date(2019, 1, 7), dt.date(2026, 9, 25)))
        if d < inst[i]:
            continue
        D = REP.get(i, (None, None))[0]
        rep = D is not None and d > D
        vis.append((i, d, rep))
    # the share found unwired among visits that recorded a replaced unit is what the technicians happened to see
    ys = [k for k, (i, d, rep) in enumerate(vis) if rep]
    marked_y = set(k for k in ys if r.random() < 0.86)
    can = [k for k in marked_y if W["disc"][vis[k][0]]]
    n_found = int(round(0.09 * len(marked_y)))
    found = set(int(v) for v in r.choice(can, min(n_found, len(can)), replace=False))
    no = 190311
    for k, (i, d, rep) in enumerate(vis):
        if k in marked_y:
            yn = "Y"
            fnd = "Found unwired" if k in found else ("OK" if r.random() < 0.7 else "Not checked")
        elif rep:
            yn, fnd = "", ("OK" if r.random() < 0.6 else "Not checked")
        else:
            yn = "N" if r.random() < 0.8 else ""
            fnd = "OK" if r.random() < 0.66 else "Not checked"
        rows.append(["WO-%d" % no, CM.fmt_date(d), str(PR["no"][i]), reasons[int(r.integers(len(reasons)))], "Y", yn, fnd,
                     P.TECHS[int(r.integers(len(P.TECHS)))]])
        no += int(r.integers(1, 9))
    for j in r.choice(PR["outside"], 2100, replace=False):
        d = weekday(rdate(r, dt.date(2019, 1, 7), dt.date(2026, 9, 25)))
        rows.append(["WO-%d" % no, CM.fmt_date(d), str(PR["no"][j]), reasons[int(r.integers(len(reasons)))], "N", "", "",
                     P.TECHS[int(r.integers(len(P.TECHS)))]])
        no += int(r.integers(1, 9))
    rows.sort(key=lambda t: (t[1], t[0]))
    # work order numbers run in date order; the system issues numbers to other work types in between
    no = 190311
    for row in rows:
        row[0] = "WO-%d" % no
        no += 1 + int(r.poisson(2.6))
    return rows, len(marked_y), len(found)


def amr(W, PR, r):
    """Monthly drive-by reads for the A/C switch premises, January 2024 to September 2026, on each route's cycle."""
    rows = []
    n_s = W["n_s"]
    month_f = [1.10, 0.92, 0.80, 0.70, 0.78, 1.05, 1.42, 1.48, 1.10, 0.76, 0.82, 1.02]
    size = np.exp(r.normal(np.log(1050), 0.33, n_s))
    cyc = r.integers(3, 27, n_s)
    meters = ["%08d" % int(v) for v in r.integers(30000000, 39999999, n_s)]
    for i in range(n_s):
        m = 0
        for Y in (2024, 2025, 2026):
            for mo in range(1, 13):
                if Y == 2026 and mo > 9:
                    break
                d = dt.date(Y, mo, int(cyc[i]))
                kwh = size[i] * month_f[mo - 1] * (1 + 0.12 * r.normal()) * (1.06 if (Y == 2026 and mo in (7, 8)) else 1.0)
                tp = "E" if r.random() < 0.028 else "A"
                rows.append((str(PR["no"][i]), meters[i], CM.fmt_date(d), "%d" % max(int(round(kwh)), 0), tp))
                m += 1
    rows.sort(key=lambda t: (t[2], t[0]))
    return rows


def wh_schedule(r):
    rows = []
    d = dt.date(2025, 11, 17)
    while d <= dt.date(2026, 3, 13):
        if d.weekday() < 5 and r.random() < 0.31:
            for g in range(1, 5):
                st = dt.datetime(d.year, d.month, d.day, 6, 30, tzinfo=P.CST) + dt.timedelta(minutes=5 * (g - 1))
                en = st + dt.timedelta(minutes=int(r.choice([150, 180, 210])))
                ev = dt.datetime(d.year, d.month, d.day, 17, 0, tzinfo=P.CST) + dt.timedelta(minutes=5 * (g - 1))
                rows.append((CM.fmt_date(d), "WH-%d" % g, st.strftime("%H:%M"), en.strftime("%H:%M"),
                             ev.strftime("%H:%M"), (ev + dt.timedelta(minutes=180)).strftime("%H:%M"),
                             "Supplier winter peak alert" if r.random() < 0.7 else "Cold weather forecast"))
        d += dt.timedelta(1)
    return rows
