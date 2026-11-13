"""The data files the district's systems export (the documents are docs.py): every file carries the mess its own system
makes, and nothing in any file names a method."""
import csv
import datetime as dt
import os

import numpy as np

import params as P
import world as W

FILES = {
    "ami": "mdm_feeder_interval_kwh_2026.csv",
    "head": "substation_revenue_meters_15min_2026.csv",
    "bus": "scada_bus_voltage_15min_2026.csv",
    "ltc": "ltc_operations_log_2026.csv",
    "bell": "ami_bellwether_voltage_hourly_2026.csv",
    "reg": "vo_pilot_regulator_log_2026.csv",
    "sched": "vo_trial_day_assignments_2026.csv",
    "wx": "asos_kgri_hourly_2026.csv",
    "survey": "residential_appliance_survey_2025.csv",
    "reg_x": "feeder_register_2026-11.xlsx",
    "plan_x": "vo_capital_plan_2027_estimates.xlsx",
    "out": "oms_outage_events_2026.csv",
    "der": "der_interconnection_queue_2026-10.csv",
}
FEEDER = None


def feeder_ids(w):
    """feeder names in the district's own form: substation code and circuit number"""
    codes = {"Ashgrove": "ASH", "Cedar Bluff": "CDB", "Elm Creek": "ELC", "Fairview": "FRV", "Gibbon Road": "GBR",
             "Hollister": "HOL"}
    n = {}
    out = []
    for f in w.F:
        c = codes[f["sub"]]
        n[c] = n.get(c, 0) + 1
        out.append("%s-%d%02d" % (c, 1 + (n[c] - 1) // 2, 10 + 3 * n[c]))
    return out


def ts(q):
    return (P.T0 + dt.timedelta(minutes=15 * int(q))).strftime("%Y-%m-%d %H:%M")


def _w(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)
    return len(rows)


def write_ami(w, O, ids, target, rng):
    """the meter data management system's feeder sums: interval kWh of every meter on the feeder, how many reported,
    and estimated intervals where too few did (filled by the system's own linear estimate)"""
    rows = []
    for i in range(P.NF):
        k = O.ami[i]
        n = w.F[i]["customers"]
        rep = np.full(P.NQ, n)
        drop = rng.random(P.NQ) < 0.004
        rep[drop] = (n * rng.uniform(0.6, 0.95, drop.sum())).astype(int)
        est = rep < 0.85 * n
        for q in range(P.NQ):
            rows.append([ids[i], ts(q), "%.3f" % k[q], int(rep[q]), "E" if est[q] else "A"])
    # a re-sent batch: one feeder-week delivered twice in the October export
    j = [r for r in rows if r[1].startswith("2026-10-1") and r[0] == ids[3]][:672]
    rows += [list(r) for r in j]
    rows.sort(key=lambda r: (r[1], r[0]))
    return _w(os.path.join(target, FILES["ami"]), ["feeder_id", "interval_start_cst", "kwh", "meters_reporting", "quality"], rows)


def write_head(w, O, ids, target):
    rows = []
    for i in O.headmetered:
        for q in range(P.NQ):
            rows.append([ids[i], ts(q), "%.3f" % O.head[i][q]])
    return _w(os.path.join(target, FILES["head"]), ["feeder_id", "interval_start_cst", "kwh_delivered"], rows)


def write_bus(w, O, target, rng):
    rows = []
    for s in P.SUBSTATIONS:
        v = O.vbus[s]
        for q in range(P.NQ):
            if rng.random() < 0.0015:
                rows.append([s, ts(q), ""])                          # a scan the historian lost
            else:
                rows.append([s, ts(q), "%.2f" % v[q]])
    return _w(os.path.join(target, FILES["bus"]), ["substation", "interval_start_cst", "bus_volts_120v_base"], rows)


def write_ltc(w, target):
    rows = []
    for (s, minute, step, tap) in w.taplog:
        t = (P.T0 + dt.timedelta(minutes=int(minute))).strftime("%Y-%m-%d %H:%M:00")
        rows.append([s, t, "RAISE" if step > 0 else "LOWER", tap - step, tap])
    rows.sort(key=lambda r: (r[1], r[0]))
    return _w(os.path.join(target, FILES["ltc"]), ["substation", "operated_at_cst", "command", "tap_from", "tap_to"], rows)


def write_bell(w, O, ids, target, rng):
    """three bellwether meters near each feeder's far end, the lowest voltage each recorded in the hour"""
    rows = []
    for i, f in enumerate(w.F):
        base = O.vmin_h[i]
        for b, extra in enumerate((0.0, 0.4, 0.9)):
            mid = "%s-BW%d" % (ids[i], b + 1)
            v = base + extra + rng.normal(0, 0.1, P.ND * 24)
            for h in range(P.ND * 24):
                t = (P.T0 + dt.timedelta(hours=h)).strftime("%Y-%m-%d %H:00")
                rows.append([mid, ids[i], t, "%.1f" % v[h]])
    return _w(os.path.join(target, FILES["bell"]), ["meter_id", "feeder_id", "hour_start_cst", "min_volts"], rows)


def write_reg(w, O, ids, target, rng):
    """the pilot regulators' log on the trial feeders through the trial windows: mode and output voltage each quarter"""
    rows = []
    days = set(int(d) for d in w.trial_days)
    for f in w.trial:
        out = w.Vhead[f]
        for q in range(P.NQ):
            if q // P.Q not in days:
                continue
            mode = "VO" if w.dose[f][q] > 0.05 else ("local" if rng.random() < 0.03 else "LOCAL")
            rows.append([ids[f], ts(q), mode, "%.2f" % out[q]])
    return _w(os.path.join(target, FILES["reg"]), ["feeder_id", "interval_start_cst", "mode", "output_volts_120v_base"], rows)


def write_sched(w, ids, target):
    rows = []
    for f in w.trial:
        for d in w.trial_days:
            day = (P.T0 + dt.timedelta(days=int(d))).strftime("%Y-%m-%d")
            rows.append([ids[f], day, "ON" if w.assign[f][d] else "OFF"])
    return _w(os.path.join(target, FILES["sched"]), ["feeder_id", "trial_day", "assignment"], rows)


def write_wx(w, target, rng):
    rows = []
    for h in range(P.ND * 24):
        t = (P.T0 + dt.timedelta(hours=h)).strftime("%Y-%m-%d %H:53")
        if rng.random() < 0.003:
            rows.append(["KGRI", t, "M"])
        else:
            rows.append(["KGRI", t, "%.0f" % w.T[h]])
    return _w(os.path.join(target, FILES["wx"]), ["station", "observed_cst", "tmpf"], rows)


def write_survey(w, O, ids, target, rng):
    """the 2025 residential appliance saturation survey: one row a responding household"""
    rows = []
    rid = 51000
    for i, f in enumerate(w.F):
        sv = O.survey[i]
        n = sv["n"]
        res = int(round(sv["sat_res_heat"] * n))
        hp = int(round(sv["sat_hp"] * n))
        ewh = int(round(sv["sat_ewh"] * n))
        ac = int(round(sv["sat_ac"] * n))
        heat = (["Electric resistance (baseboard or furnace)"] * res + ["Heat pump (air source)"] * hp +
                ["Natural gas furnace"] * max(n - res - hp, 0))[:n]
        rng.shuffle(heat)
        wh = ["Electric"] * ewh + ["Natural gas"] * max(n - ewh, 0)
        rng.shuffle(wh)
        acl = ["Yes"] * ac + ["No"] * max(n - ac, 0)
        rng.shuffle(acl)
        for k in range(n):
            rid += int(rng.integers(1, 4))
            rows.append([rid, ids[i], heat[k], wh[k], acl[k], int(rng.integers(1940, 2024))])
    return _w(os.path.join(target, FILES["survey"]), ["respondent_id", "feeder_id", "primary_heating", "water_heater_fuel",
                                                     "central_air", "year_built"], rows)


def write_distractors(w, ids, target, rng):
    rows = []
    oid = 26000
    for d in range(P.ND):
        for _ in range(int(rng.poisson(1.6))):
            i = int(rng.integers(P.NF))
            oid += 1
            t0 = P.T0 + dt.timedelta(days=d, minutes=int(rng.integers(0, 1440)))
            dur = int(rng.lognormal(4.2, 0.8))
            rows.append(["OE%d" % oid, ids[i], t0.strftime("%Y-%m-%d %H:%M"), (t0 + dt.timedelta(minutes=dur)).strftime("%Y-%m-%d %H:%M"),
                         int(rng.integers(1, 400)), str(rng.choice(["Tree", "Animal", "Equipment", "Weather", "Unknown", "Vehicle"]))])
    n1 = _w(os.path.join(target, FILES["out"]), ["event_id", "feeder_id", "start_cst", "restored_cst", "customers_out", "cause"], rows)
    rows = []
    qid = 4100
    for i in range(P.NF):
        for _ in range(int(rng.integers(2, 14))):
            qid += 1
            rows.append(["Q%d" % qid, ids[i], "%.1f" % rng.uniform(3.8, 14.0), str(rng.choice(["Rooftop solar", "Rooftop solar", "Rooftop solar + battery"])),
                         str(rng.choice(["Applied", "Approved", "In service"])), (P.T0 + dt.timedelta(days=int(rng.integers(0, 300)))).strftime("%Y-%m-%d")])
    n2 = _w(os.path.join(target, FILES["der"]), ["queue_id", "feeder_id", "kw_ac", "type", "status", "received"], rows)
    return n1, n2
