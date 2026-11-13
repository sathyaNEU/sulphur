"""Read the cut pack back into the arrays the estimators use, from the shipped files alone: the golden figures are
computed on this read-back, so what a solver can recompute from the pack is what the golden used."""
import csv
import datetime as dt
import os

import numpy as np
from openpyxl import load_workbook

import params as P
import pack as PK
import docs as D


class Pack:
    pass


def _q(s):
    t = dt.datetime.strptime(s[:16], "%Y-%m-%d %H:%M")
    return int((t - P.T0).total_seconds() // 900)


def _rows(target, key):
    with open(os.path.join(target, PK.FILES[key]), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def read_pack(target):
    O = Pack()
    O.target = target
    wb = load_workbook(os.path.join(target, PK.FILES["reg_x"]), read_only=True)
    reg = [r for r in wb["Feeders"].iter_rows(min_row=2, values_only=True) if r[0]]
    ids = [r[0] for r in reg]
    O.ids = ids
    idx = {f: i for i, f in enumerate(ids)}
    cls = {"Residential": "res", "Commercial": "com", "Rural": "rural"}
    O.sub = [r[1] for r in reg]
    O.kind = [cls[r[2]] for r in reg]
    O.cust = [int(r[3]) for r in reg]
    O.L = [float(r[4]) for r in reg]
    O.r = [float(r[6]) for r in reg]
    O.midreg = [r[7] == "Yes" for r in reg]
    O.headmetered = [i for i, r in enumerate(reg) if r[8] == "Yes"]
    wb = load_workbook(os.path.join(target, PK.FILES["plan_x"]), read_only=True)
    cost = {r[0]: float(r[2]) for r in wb["2027 estimates"].iter_rows(min_row=2, values_only=True) if r[0]}
    O.cost = [cost[f] for f in ids]
    # customer meters: the re-sent rows dropped
    O.ami = [np.zeros(P.NQ) for _ in ids]
    seen = set()
    for r in _rows(target, "ami"):
        k = (r["feeder_id"], r["interval_start_cst"])
        if k in seen:
            continue
        seen.add(k)
        O.ami[idx[r["feeder_id"]]][_q(r["interval_start_cst"])] = float(r["kwh"]) / 1000.0
    O.head = {i: np.zeros(P.NQ) for i in O.headmetered}
    for r in _rows(target, "head"):
        O.head[idx[r["feeder_id"]]][_q(r["interval_start_cst"])] = float(r["kwh_delivered"]) / 1000.0
    # bus SCADA, a lost scan filled from its neighbours
    O.vbus = {}
    by = {s: np.full(P.NQ, np.nan) for s in P.SUBSTATIONS}
    for r in _rows(target, "bus"):
        if r["bus_volts_120v_base"]:
            by[r["substation"]][_q(r["interval_start_cst"])] = float(r["bus_volts_120v_base"])
    for s, v in by.items():
        ok = ~np.isnan(v)
        O.vbus[s] = np.interp(np.arange(P.NQ), np.where(ok)[0], v[ok])
    O.tap_q = {s: [] for s in P.SUBSTATIONS}
    for r in _rows(target, "ltc"):
        t = dt.datetime.strptime(r["operated_at_cst"], "%Y-%m-%d %H:%M:%S")
        O.tap_q[r["substation"]].append((int((t - P.T0).total_seconds() // 900), 1 if r["command"] == "RAISE" else -1))
    # far end: the lowest of the bellwethers each hour
    O.vmin_h = [np.full(P.ND * 24, np.inf) for _ in ids]
    for r in _rows(target, "bell"):
        t = dt.datetime.strptime(r["hour_start_cst"], "%Y-%m-%d %H:%M")
        h = int((t - P.T0).total_seconds() // 3600)
        i = idx[r["feeder_id"]]
        O.vmin_h[i][h] = min(O.vmin_h[i][h], float(r["min_volts"]))
    # weather, a missing report filled from its neighbours
    T = np.full(P.ND * 24, np.nan)
    for r in _rows(target, "wx"):
        if r["tmpf"] != "M":
            t = dt.datetime.strptime(r["observed_cst"], "%Y-%m-%d %H:%M")
            T[int((t - P.T0).total_seconds() // 3600)] = float(r["tmpf"])
    ok = ~np.isnan(T)
    O.T = np.interp(np.arange(P.ND * 24), np.where(ok)[0], T[ok])
    # the trial
    O.assign, trial, days = {}, [], set()
    for r in _rows(target, "sched"):
        i = idx[r["feeder_id"]]
        if i not in O.assign:
            O.assign[i] = np.zeros(P.ND, dtype=int)
            trial.append(i)
        d = (dt.datetime.strptime(r["trial_day"], "%Y-%m-%d") - P.T0).days
        days.add(d)
        O.assign[i][d] = 1 if r["assignment"] == "ON" else 0
    O.trial = sorted(trial)
    O.trial_days = np.array(sorted(days))
    O.dose_q = {i: np.zeros(P.NQ) for i in O.trial}
    O.vhead_reg = {i: None for i in O.trial}
    for r in _rows(target, "reg"):
        i = idx[r["feeder_id"]]
        q = _q(r["interval_start_cst"])
        O.dose_q[i][q] = max(0.0, O.vbus[O.sub[i]][q] - float(r["output_volts_120v_base"]))
    for i in O.trial:
        O.dose_q[i][O.dose_q[i] < 0.05] = 0.0
    O.dose_daily = {i: O.dose_q[i].reshape(P.ND, P.Q).mean(axis=1) for i in O.trial}
    O.vmin_h_head = [O.vbus[O.sub[i]] - (O.dose_q[i] if i in O.trial else 0.0) for i in range(len(ids))]
    # the survey's holdings by feeder
    cnt = {i: dict(n=0, res=0, hp=0, ewh=0, ac=0) for i in range(len(ids))}
    for r in _rows(target, "survey"):
        c = cnt[idx[r["feeder_id"]]]
        c["n"] += 1
        c["res"] += r["primary_heating"].startswith("Electric resistance")
        c["hp"] += r["primary_heating"].startswith("Heat pump")
        c["ewh"] += r["water_heater_fuel"] == "Electric"
        c["ac"] += r["central_air"] == "Yes"
    O.survey = {i: dict(n=c["n"], sat_res_heat=c["res"] / c["n"], sat_hp=c["hp"] / c["n"], sat_ewh=c["ewh"] / c["n"],
                        sat_ac=c["ac"] / c["n"]) for i, c in cnt.items()}
    # the annual report's load research (kWh a year per home with the end use)
    import re, subprocess
    txt = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", os.path.join(target, D.FILES["ar"]), "-"],
                                             capture_output=True, text=True).stdout)
    def kwh(label):
        return float(re.search(re.escape(label) + r" ([\d,]+) kWh", txt).group(1).replace(",", ""))
    O.lr = dict(ewh=kwh("Electric water heater"), res_heat=kwh("Electric resistance space heating"),
                hp=kwh("Heat pump space heating"), ac=kwh("Central air conditioning"))
    return O
