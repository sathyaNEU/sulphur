"""Every figure the build owes, computed from the pack alone (target/), never from the clean truth.

The golden: each run's road sections and district access times fitted on the observed legs of the stop log; each
district's door time and the drive between its own stops measured directly; 2027 stops from the volume plan at each
district's own stops per parcel; each road section driven on a 2027 delivery day with the probability that any
district beyond it has a stop that day (Poisson on the month's mean); a set of districts handed over is the run time
the runs would no longer take, at the 2027 rate, less Owenduff's charges; on each run the set that saves most."""
import csv
import datetime as dt
import itertools
import math
import os
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook

FILES = {
    "stops": "delivery_stops_2025-2026.csv", "rundays": "van_run_log_2025-2026.csv",
    "register": "district_register_2026.xlsx", "plan": "volume_plan_2027.xlsx", "rates": "fleet_rate_card_2027.xlsx",
    "calendar": "delivery_calendar_2027.csv",
}
PRICE = 13.40        # read from the offer letter's price table (asserted in checks against the PDF text)


def h(s):
    a, b, c = s.split(":")
    return int(a) + int(b) / 60 + int(c) / 3600


def hm(s):
    a, b = s.split(":")
    return int(a) + int(b) / 60


class Pack:
    def __init__(self, target):
        self.t = target
        p = lambda k: os.path.join(target, FILES[k])
        wb = load_workbook(p("register"), read_only=True)
        regs = list(wb["Districts"].iter_rows(values_only=True))[1:]
        self.reg = {r[0]: {"name": r[1], "lat": r[3], "lon": r[4], "run": r[5]} for r in regs}
        crow = list(wb["Code changes"].iter_rows(values_only=True))[1:]
        self.newcode = {r[2]: r[0] for r in crow}          # CBN -> CBR
        wb = load_workbook(p("plan"), read_only=True)
        rows = list(wb["Parcels by district"].iter_rows(values_only=True))[1:]
        self.plan = defaultdict(lambda: [0] * 12)
        for r in rows:
            code = self.newcode.get(r[0], r[0])
            for k in range(12):
                self.plan[code][k] += r[2 + k]
        wb = load_workbook(p("rates"), read_only=True)
        rr = list(wb["Van-hour rate 2027"].iter_rows(values_only=True))
        self.rate = [r[1] for r in rr if r[0] and str(r[0]).startswith("All-in")][0]
        self.days27 = [0] * 12
        with open(p("calendar"), encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if r["delivery_day"] == "Y":
                    self.days27[int(r["date"][5:7]) - 1] += 1
        # run-day log
        self.runlog = {}
        with open(p("rundays"), encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                self.runlog[(r["run_date"], r["run_code"])] = (hm(r["depot_out"]), hm(r["depot_in"]))
        # stop log, the handheld's re-synced copies dropped (same stop, same times; only the sync time differs)
        seen = set()
        byrd = defaultdict(list)
        with open(p("stops"), encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                key = tuple(r[k] for k in ("run_date", "run_code", "stop_seq", "stop_type", "customer_ref", "arrived_local"))
                if key in seen:
                    continue
                seen.add(key)
                byrd[(r["run_date"], r["run_code"])].append(r)
        self.rundays = {}
        for k, lst in byrd.items():
            lst.sort(key=lambda r: int(r["stop_seq"]))
            for r in lst:
                r["district_code"] = self.newcode.get(r["district_code"], r["district_code"])
            self.rundays[k] = lst
        self.runs = sorted({k[1] for k in self.rundays})
        self.chain = {}
        for run in self.runs:
            ds = sorted({self.newcode.get(c, c) for c, v in self.reg.items() if v["run"] == run})
            # road order outward from the depot: the order the runs visit them in
            pos = defaultdict(list)
            for (d, r), lst in self.rundays.items():
                if r != run:
                    continue
                order = []
                for x in lst:
                    c = x["district_code"]
                    if c and (not order or order[-1] != c):
                        order.append(c)
                for i, c in enumerate(order):
                    pos[c].append(i / max(1, len(order) - 1) if len(order) > 1 else 0)
            first = defaultdict(lambda: 0.0)
            for (d, r), lst in self.rundays.items():
                if r == run:
                    seq = []
                    for x in lst:
                        c = x["district_code"]
                        if c and c not in seq:
                            seq.append(c)
                    for i, c in enumerate(seq):
                        first[c] += i
            n = defaultdict(int)
            for (d, r), lst in self.rundays.items():
                if r == run:
                    for c in {x["district_code"] for x in lst if x["district_code"]}:
                        n[c] += 1
            self.chain[run] = sorted(ds, key=lambda c: (self._rank(run, c)))

    def _rank(self, run, c):
        # a district's place in the road order: in how many run-days some other district came after it
        after = before = 0
        for (d, r), lst in self.rundays.items():
            if r != run:
                continue
            seq = []
            for x in lst:
                cc = x["district_code"]
                if cc and cc not in seq:
                    seq.append(cc)
            if c in seq:
                i = seq.index(c)
                before += i
                after += len(seq) - 1 - i
        return before - after


def legs(pk, years=(2025, 2026), months=None):
    """every observed drive: (run, from, to, hours) with from/to a district or 'DEPOT', and every door time and
    within-district drive per district"""
    out = []
    door = defaultdict(list)
    local = defaultdict(list)
    stops_n = defaultdict(int)
    parcels_n = defaultdict(int)
    for (d, run), lst in pk.rundays.items():
        if int(d[:4]) not in years:
            continue
        if months and int(d[5:7]) not in months:
            continue
        t_out, t_in = pk.runlog[(d, run)]
        prev_c, prev_t = "DEPOT", t_out
        for x in lst:
            if x["stop_type"] == "BREAK":
                prev_t = h(x["departed_local"]) if prev_t is not None else None
                continue
            c = x["district_code"]
            a = h(x["arrived_local"])
            if prev_t is not None:
                if c == prev_c:
                    local[c].append(a - prev_t)
                else:
                    out.append((run, prev_c, c, a - prev_t))
            if x["departed_local"]:
                dp = h(x["departed_local"])
                door[c].append(dp - a)
                prev_t = dp
            else:
                prev_t = None
            prev_c = c
            stops_n[c] += 1
            parcels_n[c] += int(x["parcels_delivered"])
        if prev_t is not None:
            out.append((run, prev_c, "DEPOT", t_in - prev_t))
    return out, door, local, stops_n, parcels_n


def fit(pk, years=(2025, 2026), stat=None):
    """road sections e_k (from the district before) and access a_k per district, least squares on the mean drive of
    each from-to pair, weighted by its count"""
    L, door, local, sn, pn = legs(pk, years)
    # the driver's break, taken once on every run-day whatever the run serves (depot out to depot in counts it)
    bt = [h(x["departed_local"]) - h(x["arrived_local"]) for (d, r), lst in pk.rundays.items() if int(d[:4]) in years
          for x in lst if x["stop_type"] == "BREAK"]
    brk = float(np.mean(bt))
    model = {}
    for run in pk.runs:
        ch = pk.chain[run]
        n = len(ch)
        idx = {c: i for i, c in enumerate(ch)}
        pairs = defaultdict(list)
        for r, a, b, t in L:
            if r == run:
                pairs[(a, b)].append(t)
        A, y, wts = [], [], []
        for (a, b), ts in pairs.items():
            row = np.zeros(2 * n)
            if a == "DEPOT":
                j = idx[b]
                row[:j + 1] = 1
                row[n + j] = 0.5
            elif b == "DEPOT":
                j = idx[a]
                row[:j + 1] = 1
                row[n + j] = 0.5
            else:
                i, j = idx[a], idx[b]
                if j < i:
                    continue
                row[i + 1:j + 1] = 1
                row[n + i] += 0.5
                row[n + j] += 0.5
            A.append(row)
            y.append(float((stat or np.mean)(ts)))
            wts.append(math.sqrt(len(ts)))
        A, y, wts = np.array(A), np.array(y), np.array(wts)
        sol = np.linalg.lstsq(A * wts[:, None], y * wts, rcond=None)[0]
        e, acc = sol[:n], sol[n:]
        model[run] = {"chain": ch, "e": dict(zip(ch, e)), "a": dict(zip(ch, acc)), "break": brk}
    per = {}
    for c in sn:
        per[c] = {"door": float(np.mean(door[c])), "local": float(np.mean(local[c])) if local[c] else 0.0,
                  "stops_per_parcel": sn[c] / max(1, pn[c])}
    return model, per


def mu27(pk, per, c):
    """2027 mean stops a delivery day, month by month"""
    return [pk.plan[c][k] * per[c]["stops_per_parcel"] / pk.days27[k] for k in range(12)]


def run_hours(model, per, run, mus, removed=(), months=12):
    """expected van-hours on the run over the year, months of mean stops mus[c][k] and delivery days days[k]"""
    m = model[run]
    ch = m["chain"]
    tot = 0.0
    for k in range(months):
        lam = {c: (0.0 if c in removed else mus[c][k]) for c in ch}
        day = 0.0
        for i, c in enumerate(ch):
            beyond = sum(lam[x] for x in ch[i:])
            day += 2 * m["e"][c] * (1 - math.exp(-beyond))
            pv = 1 - math.exp(-lam[c])
            day += m["a"][c] * pv + lam[c] * per[c]["door"] + (lam[c] - pv) * per[c]["local"]
        day += m.get("break", 0.0)
        tot += day * mus["__days__"][k]
    return tot


def golden(pk, years=(2025, 2026), stat=None, annual=False):
    model, per = fit(pk, years, stat)
    mus = {c: mu27(pk, per, c) for c in per}
    if annual:
        mus = {c: [sum(pk.plan[c]) * per[c]["stops_per_parcel"] / sum(pk.days27)] * 12 for c in per}
    mus["__days__"] = pk.days27
    offer = offered(pk)
    res = {"runs": {}, "set": [], "saving": 0.0}
    for run in pk.runs:
        cand = [c for c in model[run]["chain"] if c in offer]
        base = run_hours(model, per, run, mus)
        best = ((), 0.0, 0.0, 0.0)
        table = {}
        for k in range(len(cand) + 1):
            for S in itertools.combinations(cand, k):
                hrs = base - run_hours(model, per, run, mus, S)
                charge = sum(sum(pk.plan[c]) for c in S) * PRICE
                v = hrs * pk.rate - charge
                table[S] = (hrs, charge, v)
                if v > best[1] + 1e-9:
                    best = (S, v, hrs, charge)
        res["runs"][run] = {"base_h": base, "set": best[0], "hours": best[2], "charge": best[3], "net": best[1],
                            "after_h": base - best[2], "table": table, "cand": cand}
        res["set"] += list(best[0])
        res["saving"] += best[1]
    res["model"], res["per"], res["mus"] = model, per, mus
    return res


def offered(pk):
    """the districts named in Owenduff's offer (read from the letter's district table; asserted in checks)"""
    return ["MUL", "ACH", "BAN", "BLM", "LOU", "LEE", "LET", "CLI", "BCA", "CON", "CHA"]


# ---------------------------------------------------------------- the rungs a competent solver stops at

def base_year(pk):
    """the last twelve months on file, November 2025 to October 2026"""
    return lambda d: d >= "2025-11-01"


def time_in_district(pk, inclusive_exit=False):
    """the field's cost-to-serve build: each district's drive in from the stop before, the drives between its stops
    and its door time, summed over the base year, carried to 2027 by the plan's parcels"""
    keep = base_year(pk)
    tid = defaultdict(float)
    parcels = defaultdict(int)
    for (d, run), lst in pk.rundays.items():
        if not keep(d):
            continue
        t_out, t_in = pk.runlog[(d, run)]
        prev_c, prev_t = "DEPOT", t_out
        for x in lst:
            if x["stop_type"] == "BREAK":
                prev_t = h(x["departed_local"])
                continue
            c = x["district_code"]
            a = h(x["arrived_local"])
            dp = h(x["departed_local"]) if x["departed_local"] else a + 4 / 60
            if prev_t is not None:
                tid[c] += dp - prev_t
            prev_t, prev_c = dp, c
            parcels[c] += int(x["parcels_delivered"])
        if inclusive_exit:
            tid[prev_c] += t_in - prev_t
    out = {}
    for c in tid:
        if c in pk.plan and parcels[c]:
            hrs = tid[c] * sum(pk.plan[c]) / parcels[c]
            out[c] = (hrs, hrs * pk.rate, sum(pk.plan[c]) * PRICE)
    return out


def removal_one(pk, res):
    """each district priced on its own, every other district kept"""
    out = {}
    for run, rr in res["runs"].items():
        for c in rr["cand"]:
            out[c] = rr["table"][(c,)]
    return out


def proportional_carry(pk, res):
    """the golden set's van-hours measured on the base year's stops and scaled to 2027 by parcels"""
    model, per = res["model"], res["per"]
    keep = base_year(pk)
    # base-year mean stops by month from the stop log
    cnt = defaultdict(lambda: [0] * 12)
    days = [0] * 12
    seen = set()
    for (d, run), lst in pk.rundays.items():
        if not keep(d):
            continue
        if d not in seen:
            seen.add(d)
            days[int(d[5:7]) - 1] += 1
        for x in lst:
            if x["stop_type"] != "BREAK":
                cnt[x["district_code"]][int(d[5:7]) - 1] += 1
    mus = {c: [cnt[c][k] / days[k] for k in range(12)] for c in cnt}
    mus["__days__"] = days
    tot = 0.0
    for run, rr in res["runs"].items():
        S = rr["set"]
        if not S:
            continue
        hrs = run_hours(model, per, run, mus) - run_hours(model, per, run, mus, S)
        p_base = sum(int(x["parcels_delivered"]) for (d, r), lst in pk.rundays.items() if keep(d) and r == run
                     for x in lst if x["district_code"] in S)
        scale = sum(sum(pk.plan[c]) for c in S) / p_base
        tot += hrs * scale * pk.rate - sum(sum(pk.plan[c]) for c in S) * PRICE
    return tot


def allocation_by_stops(pk):
    keep = base_year(pk)
    al = defaultdict(float)
    parcels = defaultdict(int)
    for (d, run), lst in pk.rundays.items():
        if not keep(d):
            continue
        t_out, t_in = pk.runlog[(d, run)]
        st = [x for x in lst if x["stop_type"] != "BREAK"]
        for x in st:
            al[x["district_code"]] += (t_in - t_out) / len(st)
            parcels[x["district_code"]] += int(x["parcels_delivered"])
    return {c: (al[c] * sum(pk.plan[c]) / parcels[c] * pk.rate, sum(pk.plan[c]) * PRICE)
            for c in al if c in pk.plan and parcels[c]}
