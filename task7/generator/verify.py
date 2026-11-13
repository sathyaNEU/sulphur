"""task7 architecture 11: the pack read back as an analyst assembles it, from the shipped files only (no world object).

Meters are tied to service points through the GIS and the exchange log, service points to transformers through the GIS and
the work orders it has not caught up with, transformers to their nameplate through the register and the change-outs it has
not caught up with; the roster is de-duplicated and each member's charger followed through a swap to one identity; the
session log is put on local time with the re-sent batch and the empty plug-ins dropped."""
import csv
import datetime as dt
import os
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook

MDT = dt.timezone(dt.timedelta(hours=-6))
JUL1 = dt.date(2026, 7, 1)
NDAY = 62
Q = 96
QUOTE_DAY = dt.date(2026, 11, 1)


def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).astimezone(MDT)


class Pack:
    def __init__(self, target):
        self.t = target
        self.load_network()
        self.load_roster()
        self.load_sessions()
        self.load_ami()
        self.load_monitors()

    def p(self, name):
        return os.path.join(self.t, name)

    # ---- the network ------------------------------------------------------------------------------------------------
    def load_network(self):
        gis = rows(self.p("gis_service_points_2026-10-30.csv"))
        self.sp_tx = {r["service_point"]: r["transformer_location"] for r in gis}
        self.meter_sp = {r["meter_no"]: r["service_point"] for r in gis}
        for r in rows(self.p("ami_meter_exchanges_2026.csv")):
            self.meter_sp[r["old_meter_no"]] = r["service_point"]
        reg = rows(self.p("transformer_register_2026.csv"))
        self.kva = {r["transformer_location"]: float(r["kva"]) for r in reg}
        self.area = {r["transformer_location"]: r["substation"] for r in reg}
        wb = load_workbook(self.p("distribution_work_orders_2025_2026.xlsx"), read_only=True)
        ws = wb.worksheets[0]
        it = ws.iter_rows(values_only=True)
        hdr = next(it)
        self.transfers, self.changeouts = [], []
        for r in it:
            r = dict(zip(hdr, r))
            if r["type"] == "Service transfer":
                self.sp_tx[str(r["service_point"])] = r["transformer_location"]
                self.transfers.append(r)
            elif r["type"] == "Transformer change-out":
                new = float(r["detail"].split(" with ")[1].split(" kVA")[0])
                self.kva[r["transformer_location"]] = new
                self.changeouts.append(r)
        self.tx_sps = defaultdict(list)
        for sp, t in self.sp_tx.items():
            self.tx_sps[t].append(sp)

    # ---- the roster and the pilot halves -----------------------------------------------------------------------------
    def load_roster(self):
        seen, ro = set(), []
        for r in rows(self.p("ev_overnight_roster_2026-11-02.csv")):
            key = (r["service_point"], r["charger_serial"], r["enrolled_on"])
            if key in seen:
                continue
            seen.add(key)
            ro.append(r)
        # one identity per member charger: a replacement serial points back to the serial it replaced
        root = {}
        for r in ro:
            root[r["charger_serial"]] = r["replaces_serial"] or r["charger_serial"]
        for s in list(root):
            k = s
            while root[k] != k:
                k = root[k]
            root[s] = k
        self.root = root
        self.ch = {}
        for r in ro:
            c = self.ch.setdefault(root[r["charger_serial"]], dict(sp=r["service_point"], kw=float(r["rated_kw"]),
                                                                    enrolled=dt.date.fromisoformat(r["enrolled_on"]),
                                                                    closed=None, serials=[], declared=r["usual_charging_at_enrolment"]))
            c["serials"].append(r["charger_serial"])
            c["enrolled"] = min(c["enrolled"], dt.date.fromisoformat(r["enrolled_on"]))
            if r["status"] == "Closed":
                c["closed"] = dt.date.fromisoformat(r["status_date"])
        self.half = {}
        for r in rows(self.p("pilot_assignment_2025.csv")):
            self.half[root.get(r["charger_serial"], r["charger_serial"])] = "managed" if r["pilot_half"] == "Stagger" else "own"
        self.enrolled = sorted(k for k, c in self.ch.items()
                               if c["enrolled"] <= QUOTE_DAY and (c["closed"] is None or c["closed"] > QUOTE_DAY))

    # ---- sessions ------------------------------------------------------------------------------------------------------
    def load_sessions(self):
        seen = set()
        self.sess = defaultdict(list)
        for r in rows(self.p("quillpoint_sessions_2024-06_2026-09.csv")):
            if r["session_id"] in seen:
                continue
            seen.add(r["session_id"])
            if float(r["energy_kwh"]) <= 0 or not r["charge_start_utc"]:
                continue
            pin, st, en, un = (utc(r[k]) for k in ("plugged_in_utc", "charge_start_utc", "charge_end_utc", "unplugged_utc"))
            night = (pin - dt.timedelta(hours=6)).date()           # the evening the car came home
            self.sess[self.root.get(r["charger_serial"], r["charger_serial"])].append(
                dict(night=night, plug=pin, start=st, end=en, unplug=un, kwh=float(r["energy_kwh"]), peak=float(r["peak_kw"]),
                     mode=r["control_mode"], ready=r["ready_by_local"]))

    # ---- hourly reads -------------------------------------------------------------------------------------------------
    def load_ami(self):
        files = sorted(f for f in os.listdir(self.t) if f.startswith("mdm_hourly_"))
        self.ami = defaultdict(lambda: np.zeros(NDAY * 24))
        self.ami_seen = set()
        self.est_hours = 0
        for f in files:
            for r in rows(self.p(f)):
                key = (r["meter_no"], r["read_date"])
                if key in self.ami_seen:
                    continue
                self.ami_seen.add(key)
                sp = self.meter_sp[r["meter_no"]]
                d = (dt.date.fromisoformat(r["read_date"]) - JUL1).days
                vals = [float(r["he%02d" % k]) if r["he%02d" % k] != "" else 0.0 for k in range(1, 25)]
                self.ami[sp][d * 24:(d + 1) * 24] += np.array(vals)
                self.est_hours += int(r["estimated_hours"])

    # ---- the monitored transformers --------------------------------------------------------------------------------------
    def load_monitors(self):
        self.mon = {}
        for r in rows(self.p("transformer_monitors_15min_2026-07_08.csv")):
            if r["quantity"] != "kW":
                continue
            arr = self.mon.setdefault(r["transformer_location"], np.full(NDAY * Q, np.nan))
            d = (dt.date.fromisoformat(r["date"]) - JUL1).days
            vals = [r[k] for k in list(r.keys())[3:]]
            arr[d * Q:(d + 1) * Q] = [float(v) if v != "" else np.nan for v in vals]
