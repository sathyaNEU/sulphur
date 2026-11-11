"""task9: the pack under target/, written from the simulated world the way Halden's systems export it.

  drive_inventory.csv                 every serial the inventory system has seen since telemetry began
  drive_quarter_stats.csv             the telemetry warehouse's drive-by-quarter rollup
  removal_tickets.csv                 the data-centre technicians' tickets
  vault_events.csv                    vault life events (commissioning, migration, reviews, decommissioning, incidents)
  brightstore_handover.xlsx           Brightstore's handover workbook (rack manifest, purchase batches, failure summary)
  kestrel_fe118_serial_numbers_and_firmware.pdf   the vendor's field guide
  ops_policy_wiki.md                  the operations wiki page on replacements, health pulls and decommissioning
  capacity_plan_2027.xlsx             installs scheduled for the year ahead
  procurement_and_costs.yaml          spares on hand, lead time and costs
  fleet_reliability_q3_2026.png       the quarter's close-out page (replacement rates by data centre)
  dc_environment_daily.csv, vendor_datasheets.pdf, ssd_boot_drive_stats.csv   on file, unused
"""
import collections
import csv
import datetime as dt
import io
import math
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import docs as DC
import officepdf as O
import params as P
import postprocess as PP
import world as WD

UTC = dt.timezone.utc
CT = dt.timezone(dt.timedelta(hours=-5))
F = {
    "inventory": "drive_inventory.csv", "quarters": "drive_quarter_stats.csv", "tickets": "removal_tickets.csv",
    "events": "vault_events.csv", "handover": "brightstore_handover.xlsx", "kestrel": "kestrel_fe118_serial_numbers_and_firmware.pdf",
    "wiki": "ops_policy_wiki.md", "capacity": "capacity_plan_2027.xlsx", "costs": "procurement_and_costs.yaml",
    "closeout": "fleet_reliability_q3_2026.png", "env": "dc_environment_daily.csv", "datasheets": "vendor_datasheets.pdf",
    "ssd": "ssd_boot_drive_stats.csv",
}
DISTRACTORS = [F["env"], F["datasheets"], F["ssd"]]
ALIASES = {"KESTREL KS10T0A": ["KS10T0A ", "Kestrel_KS10T0A"], "KESTREL HX18T8A": ["HX18T8A", "Kestrel HX18T8A"],
           "MERIDIAN MD8000NM": ["MD8000NM", "Meridian MD8000NM "], "BOREALIS VB12000": ["VB12000", "Borealis-VB12000"],
           "MERIDIAN MD14TNM": ["MD14TNM"], "MERIDIAN MD16TNM": ["MD16TNM"], "TAMSIN TS20000E": ["TS20000E"],
           "TAMSIN TS22000E": ["TS22000E"]}


def dstr(d, rng, mixed=True):
    """The inventory system's date, written three ways after its 2023 upgrade left older rows in their old forms."""
    if d is None:
        return ""
    if not mixed:
        return d.isoformat()
    u = rng.random()
    if u < 0.85:
        return d.isoformat()
    if u < 0.95:
        return "%02d/%02d/%04d" % (d.month, d.day, d.year)
    return d.isoformat() + "T00:00:00"


def quarter_of(d):
    return "%dQ%d" % (d.year, (d.month - 1) // 3 + 1)


def quarter_bounds(q):
    y, k = int(q[:4]), int(q[-1])
    a = dt.date(y, 3 * (k - 1) + 1, 1)
    b = dt.date(y + (k == 4), 1 if k == 4 else 3 * k + 1, 1)
    return a, b


def quarters_between(a, b):
    out = []
    q = quarter_of(a)
    while True:
        out.append(q)
        lo, hi = quarter_bounds(q)
        if hi > b:
            break
        q = quarter_of(hi)
    return out


class Pack:
    def __init__(self, W, seed=P.SEED + 7):
        self.W = W
        self.rng = np.random.default_rng(seed)
        self.vault = {v["vid"]: v for v in W.vaults}
        self._serials()

    # ---- serial numbers in each vendor's format
    def _serials(self):
        rng = self.rng
        seq = collections.Counter()
        used = set()
        for d in self.W.drives:
            fam = d["family"]
            vendor = P.FAMILY[fam]["vendor"]
            md = WD.to_date(d["manuf"])
            if vendor == "Kestrel":
                iso = md.isocalendar()
                plant = "TH" if rng.random() < 0.7 else "MY"
                key = (plant, iso[0] % 100, iso[1])
                seq[key] += int(rng.integers(1, 9))
                s = "KS%s%02d%02d%05d" % (plant, iso[0] % 100, iso[1], seq[key] % 100000)
            elif vendor == "Meridian":
                s = "MD%s%07d" % ("".join(rng.choice(list("ABCDEFGHJKLMNPRSTVWXYZ"), 2)), rng.integers(0, 10 ** 7))
            elif vendor == "Tamsin":
                s = "T%s" % "".join(rng.choice(list("0123456789ABCDEFGHJKLMNPRSTVWXYZ"), 9))
            else:
                s = "BV%010d" % rng.integers(0, 10 ** 10)
            while s in used:
                s = s[:-1] + str(rng.integers(0, 10))
            used.add(s)
            d["serial"] = s
            d["firmware"] = WD.firmware_for(fam, md)

    # ---- the record window each drive is seen in
    def seen(self, d):
        start = P.MIGRATION if d["dc"] == "DC-3" else P.REC_START
        inst = WD.to_date(d["install"])
        end = WD.to_date(d["exit"]) if d["exit"] is not None else P.END
        if end < start:
            return None
        return max(inst, start), end

    def write(self, tgt):
        os.makedirs(tgt, exist_ok=True)
        info = {}
        self._rma()
        info["inventory_rows"] = self.inventory(os.path.join(tgt, F["inventory"]))
        info["quarter_rows"] = self.quarters(os.path.join(tgt, F["quarters"]))
        info["ticket_rows"] = self.tickets(os.path.join(tgt, F["tickets"]))
        info["event_rows"] = self.events(os.path.join(tgt, F["events"]))
        self.handover(os.path.join(tgt, F["handover"]))
        self.kestrel(os.path.join(tgt, F["kestrel"]))
        open(os.path.join(tgt, F["wiki"]), "w").write(DC.WIKI)
        self.capacity(os.path.join(tgt, F["capacity"]))
        self.costs(os.path.join(tgt, F["costs"]))
        self.closeout(os.path.join(tgt, F["closeout"]))
        self.environment(os.path.join(tgt, F["env"]))
        self.datasheets(os.path.join(tgt, F["datasheets"]))
        info["ssd_rows"] = self.ssd(os.path.join(tgt, F["ssd"]))
        return info

    # ---- false removals that came back to service (reseats, cable faults)
    def _rma(self):
        rng = self.rng
        self.rma = {}
        cands = [d for d in self.W.drives if self.seen(d) and (d["exit"] is None or d["exit"] - d["install"] > 120)]
        n_fail = sum(1 for d in self.W.drives if d["kind"] == "FAIL" and self.seen(d))
        pick = rng.choice(len(cands), size=int(P.RMA_SHARE * n_fail), replace=False)
        for i in pick:
            d = cands[int(i)]
            a, b = self.seen(d)
            span = (b - a).days
            if span < 60:
                continue
            out = a + dt.timedelta(days=int(rng.integers(20, span - 35)))
            back = out + dt.timedelta(days=int(rng.integers(3, 29)))
            self.rma[d["serial"]] = (out, back)

    # ---- drive_inventory.csv
    def inventory(self, path):
        rng = self.rng
        rows = []
        po = {}
        for d in self.W.drives:
            s = self.seen(d)
            if s is None:
                continue
            fam = d["family"]
            f = P.FAMILY[fam]
            v = self.vault[d["vid"]]
            first, last = s
            inst = WD.to_date(d["install"])
            if d["dc"] == "DC-3" and inst < P.MIGRATION:
                inst_shown = P.MIGRATION
            else:
                inst_shown = inst
            model = f["model"]
            if model in ALIASES and rng.random() < 0.18:
                model = ALIASES[model][int(rng.integers(0, len(ALIASES[model])))]
            kind = d["kind"]
            reason = {"FAIL": "FAIL", "PULL": "PULL", "SPUR": "PULL", "DECOM": "DECOM"}.get(kind, "")
            removed = WD.to_date(d["exit"]) if d["exit"] is not None else None
            if reason in ("FAIL", "PULL") and rng.random() < 0.15:
                reason = ""
            bkey = (fam, d["batch"][1], d["batch"][2])
            if bkey not in po:
                po[bkey] = "PO-%d-%04d" % (WD.to_date(d["manuf"]).year, rng.integers(1000, 9999))
            base = dict(serial=d["serial"], model_string=model, vendor=f["vendor"], capacity_bytes=int(f["tb"] * 10 ** 12),
                        dc=d["dc"], vault_id=d["vid"], chassis_id="%s-C%02d" % (d["vid"], d["slot"] // P.SLOTS_PER_CHASSIS + 1),
                        slot=d["slot"] % P.SLOTS_PER_CHASSIS + 1, firmware=d["firmware"], po_number=po[bkey])
            if d["serial"] in self.rma:
                out, back = self.rma[d["serial"]]
                rows.append(dict(base, install_date=dstr(inst_shown, rng), first_seen=dstr(first, rng),
                                 last_seen=dstr(out, rng), status="REMOVED", removal_date=dstr(out, rng), removal_reason="FAIL"))
                rows.append(dict(base, serial=d["serial"] + "-R", install_date=dstr(back, rng), first_seen=dstr(back, rng),
                                 last_seen=dstr(last, rng), status="ACTIVE" if removed is None else "REMOVED",
                                 removal_date=dstr(removed, rng), removal_reason=reason))
            else:
                rows.append(dict(base, install_date=dstr(inst_shown, rng), first_seen=dstr(first, rng),
                                 last_seen=dstr(last, rng), status="ACTIVE" if removed is None else "REMOVED",
                                 removal_date=dstr(removed, rng), removal_reason=reason))
        # boot SSDs and the QA burn-in vault sit in the same inventory
        for i in range(3120):
            dc = ["DC-1", "DC-2", "DC-3"][i % 3]
            inst = P.REC_START + dt.timedelta(days=int(rng.integers(-900, 1500)))
            rows.append(dict(serial="SB%09d" % rng.integers(0, 10 ** 9), model_string="BOOTSSD 480G", vendor="Tamsin",
                             capacity_bytes=480 * 10 ** 9, dc=dc, vault_id="", chassis_id="", slot="", firmware="SB4.1",
                             po_number="PO-%d-%04d" % (inst.year, rng.integers(1000, 9999)), install_date=dstr(inst, rng),
                             first_seen=dstr(max(inst, P.REC_START), rng), last_seen=dstr(P.END, rng), status="ACTIVE",
                             removal_date="", removal_reason=""))
        for i in range(60):
            inst = dt.date(2026, 8, 3) + dt.timedelta(days=int(rng.integers(0, 20)))
            rows.append(dict(serial="T%s" % "".join(rng.choice(list("0123456789ABCDEFGHJKLMNPRSTVWXYZ"), 9)),
                             model_string="TAMSIN TS24000E", vendor="Tamsin", capacity_bytes=24 * 10 ** 12, dc="DC-2",
                             vault_id="QA-01", chassis_id="QA-01-C01", slot=i + 1, firmware="TS24.0.1", po_number="PO-2026-0412",
                             install_date=dstr(inst, rng), first_seen=dstr(inst, rng), last_seen=dstr(P.END, rng),
                             status="ACTIVE", removal_date="", removal_reason=""))
        order = rng.permutation(len(rows))
        cols = ["serial", "model_string", "vendor", "capacity_bytes", "dc", "vault_id", "chassis_id", "slot", "install_date",
                "first_seen", "last_seen", "status", "removal_date", "removal_reason", "firmware", "po_number"]
        with open(path, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            for i in order:
                w.writerow(rows[i])
        return len(rows)

    # ---- drive_quarter_stats.csv
    def quarters(self, path):
        rng = self.rng
        cols = ["serial", "quarter", "vault_id", "days_observed", "replaced_in_qtr", "smart_5_max", "smart_187_max",
                "smart_197_max", "smart_198_max", "smart_9_hours_end", "avg_temp_c", "firmware"]
        n = 0
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(cols)
            for d in self.W.drives:
                s = self.seen(d)
                if s is None:
                    continue
                first, last = s
                fam = d["family"]
                inst = WD.to_date(d["install"])
                fail = WD.to_date(d["fail"]) if d["fail"] is not None else None
                pre = WD.to_date(d["fail"] - d["precursor"]) if (d["precursor"] and d["fail"] is not None) else None
                s187 = WD.to_date(d["s187"]) if d["s187"] is not None else None
                rma = self.rma.get(d["serial"])
                base_t = 28.0 + {"DC-1": 0.0, "DC-2": 1.2, "DC-3": 2.1}[d["dc"]] + rng.normal(0, 1.5)
                exit_k = d["kind"]
                for q in quarters_between(first, last):
                    a, b = quarter_bounds(q)
                    lo, hi = max(a, first), min(b - dt.timedelta(days=1), last)
                    days = (hi - lo).days + 1
                    if days <= 0:
                        continue
                    serial = d["serial"]
                    if rma and hi >= rma[1]:
                        serial = d["serial"] + "-R"
                    if rma and lo <= rma[0] < b:
                        days -= (min(rma[1], b) - rma[0]).days
                    if rng.random() < P.OUTAGE_SHARE * 18:
                        days -= int(rng.integers(1, 6))
                    days = max(days, 1)
                    replaced = int(exit_k in ("FAIL", "PULL", "SPUR") and d["exit"] is not None and a <= WD.to_date(d["exit"]) < b)
                    s5 = s187 = s197 = s198 = 0
                    if rng.random() < 0.012:
                        s5 = int(rng.integers(1, 9))
                    if pre is not None and fail is not None and hi >= pre:
                        x = min(1.0, ((hi - pre).days + 1) / max(1, (fail - pre).days))
                        s5 = max(s5, int(x * rng.integers(30, 600)))
                        s197 = int(x * rng.integers(8, 240))
                        s198 = int(x * rng.integers(0, 120))
                        s187 = int(x * rng.integers(0, 40))
                    if s187 == 0 and s187_on(d, hi):
                        s187 = int(rng.integers(1, 6))
                    poh = "" if fam == "KS-10" else int(((hi - inst).days + 1) * 24 - rng.integers(0, 30))
                    temp = round(base_t + 2.0 * math.sin(2 * math.pi * (a.month - 4) / 12) + rng.normal(0, 0.6), 1)
                    row = [serial, q, d["vid"], days, replaced, s5, s187, s197, s198, poh, temp, d["firmware"]]
                    w.writerow(row)
                    n += 1
                    if rng.random() < P.DUP_SHARE:
                        w.writerow(row)
                        n += 1
        return n

    # ---- removal_tickets.csv
    def tickets(self, path):
        rng = self.rng
        rows = []
        k = 0
        for d in self.W.drives:
            s = self.seen(d)
            if s is None:
                continue
            events = []
            if d["kind"] in ("FAIL", "PULL", "SPUR") and d["exit"] is not None:
                events.append((WD.to_date(d["exit"]), d["kind"]))
            if d["serial"] in self.rma:
                out, back = self.rma[d["serial"]]
                events.append((out, "RMA_OUT"))
                events.append((back, "RMA_BACK"))
            for when, kind in events:
                k += 1
                cat = {"FAIL": "DRIVE_FAILURE", "PULL": "HEALTH_PULL", "SPUR": "HEALTH_PULL", "RMA_OUT": "DRIVE_FAILURE",
                       "RMA_BACK": "RETURN_TO_SERVICE"}[kind]
                note = self._note(kind, d)
                serial = d["serial"]
                u = rng.random()
                if u < 0.03:
                    serial = ""
                elif u < 0.05:
                    i = int(rng.integers(2, len(serial)))
                    serial = serial[:i] + str(rng.integers(0, 10)) + serial[i + 1:]
                op = dt.datetime.combine(when, dt.time(int(rng.integers(7, 19)), int(rng.integers(0, 60))))
                cl = op + dt.timedelta(minutes=int(rng.integers(25, 600)))
                rows.append(dict(ticket_id="T%07d" % (4100000 + k), serial=serial, vault_id=d["vid"],
                                 chassis_id="%s-C%02d" % (d["vid"], d["slot"] // P.SLOTS_PER_CHASSIS + 1),
                                 slot=d["slot"] % P.SLOTS_PER_CHASSIS + 1, opened_ts=op.strftime("%Y-%m-%d %H:%M"),
                                 closed_ts=cl.strftime("%Y-%m-%d %H:%M"), category=cat, tech_note=note,
                                 tech=P.TECHS[int(rng.integers(0, len(P.TECHS)))]))
        rows.sort(key=lambda r: r["opened_ts"])
        cols = ["ticket_id", "serial", "vault_id", "chassis_id", "slot", "opened_ts", "closed_ts", "category", "tech_note", "tech"]
        with open(path, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        return len(rows)

    def _note(self, kind, d):
        rng = self.rng
        if kind == "FAIL":
            return ["drive dropped from array, replaced", "no response on bus, swapped", "failed read-back, replaced from spares",
                    "array rebuild after drive fault; drive out", "hard fail, replaced"][int(rng.integers(0, 5))]
        if kind == "PULL":
            return ["pulled per health policy: realloc %d, pending %d" % (rng.integers(25, 400), rng.integers(9, 120)),
                    "health pull, SMART 197 high", "proactive pull, reallocated sectors climbing"][int(rng.integers(0, 3))]
        if kind == "SPUR":
            return ["pulled per P2, SMART 187 = %d" % rng.integers(1, 5), "health pull (187>0), no other errors",
                    "P2 pull: uncorrectable count nonzero"][int(rng.integers(0, 3))]
        if kind == "RMA_OUT":
            return ["drive offline, pulled for test", "dropped from array, removed"][int(rng.integers(0, 2))]
        return ["reseated after bench test, back in slot", "cable fault found, drive returned to slot"][int(rng.integers(0, 2))]

    # ---- vault_events.csv
    def events(self, path):
        rng = self.rng
        rows = []
        for v in self.W.vaults:
            c = WD.to_date(v["commission"])
            if v["dc"] != "DC-3":
                rows.append((c, v["vid"], v["dc"], "COMMISSION", "", "%s vault commissioned, 1200 x %s" % (v["vid"], P.FAMILY[v["family"]]["model"])))
            else:
                rows.append((P.MIGRATION, v["vid"], v["dc"], "MIGRATION_IN", "", "Brightstore rack moved into Halden inventory as %s" % v["vid"]))
            if v["decom"]:
                s, e = WD.to_date(v["decom"][0]), WD.to_date(v["decom"][1])
                rows.append((s, v["vid"], v["dc"], "DECOM_START", "", "data migrated off; drive removal begins"))
                rows.append((e, v["vid"], v["dc"], "DECOM_DONE", "", "vault empty"))
        for fam, dates in P.DECOM_FAMILIES.items():
            for R in dates:
                for dc in sorted({v["dc"] for v in self.W.vaults if v["family"] == fam}):
                    rows.append((R, "", dc, "DECOM_REVIEW", "", "ops review of %s vaults (%s)" % (fam, P.PEOPLE["reliability"])))
        for R in P.REVIEWS:
            for dc in ("DC-1", "DC-2", "DC-3"):
                if not any(r[0] == R and r[2] == dc for r in rows):
                    rows.append((R, "", dc, "DECOM_REVIEW", "", "ops review: no vault scheduled"))
        for s in self.W.shocks:
            when = WD.to_date(s["start"])
            start = P.MIGRATION if s["dc"] == "DC-3" else P.REC_START
            if when < start or not s["logged"]:
                continue
            note = {"CHASSIS_POWER_EVENT": ["PDU trip on chassis", "PSU failover, chassis brownout", "power event, chassis rebooted"],
                    "COOLING_EXCURSION": ["CRAH fault, inlet temps high", "cooling excursion in aisle", "fan wall fault"]}[s["kind"]]
            ch = "%s-C%02d" % (s["vid"], s["chassis"] + 1) if s["kind"] == "CHASSIS_POWER_EVENT" else ""
            rows.append((when, s["vid"], s["dc"], s["kind"], ch, note[int(rng.integers(0, 3))]))
        rows.sort(key=lambda r: (r[0], r[1]))
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["vault_id", "dc", "event_date", "event_type", "chassis_id", "notes"])
            for r in rows:
                w.writerow([r[1], r[2], r[0].isoformat(), r[3], r[4], r[5]])
        return len(rows)

    # ---- brightstore_handover.xlsx
    def handover(self, path):
        rng = self.rng
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "rack_manifest"
        ws.append(["Brightstore Inc. - storage handover to Halden Vault - rack manifest at cut-over (2024-02-29)"])
        ws.append(["serial", "model", "deploy_date", "rack", "chassis", "position"])
        rack_of = {}
        for v in self.W.vaults:
            if v["dc"] == "DC-3":
                rack_of[v["vid"]] = "BS-R%02d" % (int(v["vid"][1:]) + 6)
        mig = WD.day(P.MIGRATION)
        for d in sorted(self.W.drives, key=lambda d: (d["vid"], d["slot"])):
            if d["dc"] != "DC-3" or d["install"] >= mig or (d["exit"] is not None and d["exit"] < mig):
                continue
            s = d["serial"]
            dashed = ("%s-%s-%s-%s" % (s[:2], s[2:4], s[4:8], s[8:])) if s.startswith("KS") else ("%s-%s-%s" % (s[:2], s[2:6], s[6:]))
            dep = ""
            if d["family"] == "KS-10" and rng.random() < 0.40:
                dep = WD.to_date(d["install"]).isoformat()
            ws.append([dashed, P.FAMILY[d["family"]]["model"].split(" ")[1], dep, rack_of[d["vid"]],
                       d["slot"] // P.SLOTS_PER_CHASSIS + 1, d["slot"] % P.SLOTS_PER_CHASSIS + 1])
        ws2 = wb.create_sheet("purchase_batches")
        ws2.append(["Brightstore purchase orders, drives"])
        ws2.append(["po", "model", "qty", "ship_date"])
        seen = collections.Counter()
        first = {}
        for d in self.W.drives:
            if d["dc"] == "DC-3":
                k = (d["family"], d["batch"][1], d["batch"][2])
                seen[k] += 1
                first[k] = min(first.get(k, d["manuf"]), d["manuf"])
        for k in sorted(seen):
            if WD.to_date(first[k]) > P.MIGRATION:
                continue
            ws2.append(["BS-PO-%05d" % rng.integers(10000, 99999), P.FAMILY[k[0]]["model"].split(" ")[1], seen[k],
                        (WD.to_date(first[k]) + dt.timedelta(days=int(rng.integers(12, 30)))).isoformat()])
        ws3 = wb.create_sheet("legacy_failure_summary")
        ws3.append(["Drive failures and replacements by rack and year, as Brightstore's NOC logged them (no serials)"])
        ws3.append(["rack", "model", "year", "drives_installed", "failures_replaced"])
        for v in self.W.vaults:
            if v["dc"] != "DC-3":
                continue
            for y in range(2019, 2024):
                a, b = WD.day(dt.date(y, 1, 1)), WD.day(dt.date(y + 1, 1, 1))
                if v["commission"] >= b:
                    continue
                n_in = sum(1 for d in self.W.drives if d["vid"] == v["vid"] and d["install"] < b and (d["exit"] is None or d["exit"] >= a))
                n_f = sum(1 for d in self.W.drives if d["vid"] == v["vid"] and d["exit"] is not None and a <= d["exit"] < b
                          and d["kind"] in ("FAIL", "PULL", "SPUR"))
                ws3.append([rack_of[v["vid"]], P.FAMILY[v["family"]]["model"].split(" ")[1], y, min(n_in, 1200), n_f])
        for w_ in (ws, ws2, ws3):
            w_["A1"].font = Font(bold=True)
        wb.save(path)
        PP.normalize_ooxml(path, "Brightstore NOC", P.PEOPLE["dc3"], "2024-02-26T15:02:11Z", "2024-02-29T22:48:30Z",
                           excel=True, company=P.ACQUIRED)

    # ---- the Kestrel field guide (a vendor PDF)
    def kestrel(self, path):
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import Paragraph, Spacer, Table
        ss = getSampleStyleSheet()
        body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13)
        head = ParagraphStyle("h", parent=body, fontName="Helvetica-Bold", fontSize=11, spaceBefore=6)
        title = ParagraphStyle("t", parent=body, fontName="Helvetica-Bold", fontSize=14, leading=18)
        k = DC.KESTREL
        rows = [["Family", "Factory firmware", "Builds"]] + [list(r) for r in k["firmware_rows"]]
        story = [Paragraph(k["title"], title), Spacer(1, 6), Paragraph(k["intro"], body), Paragraph("1. Serial numbers", head),
                 Paragraph(k["serial"], body), Paragraph("2. Factory firmware", head), Table(rows),
                 Paragraph("3. Field support", head), Paragraph(k["support"], body),
                 Spacer(1, 8), Paragraph("Kestrel Data Products, Field Engineering. Document FE-118, revision C.", body)]
        O.build(path, story, k["title"], "Kestrel Field Engineering", "Serial numbers and firmware", "Kestrel Data Products | FE-118 rev C",
                dt.datetime(2025, 4, 8, 10, 14, 0, tzinfo=UTC), dt.datetime(2025, 4, 9, 8, 2, 41, tzinfo=UTC), producer="LibreOffice 7.5")

    # ---- capacity_plan_2027.xlsx
    def capacity(self, path):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "installs"
        ws.append(["Scheduled vault installs, 2026-Q4 to 2027-Q3 (approved at the September capacity review)"])
        ws.append(["quarter", "dc", "model", "vaults", "drives"])
        for q, dc, fam, n in P.INSTALLS_PLAN:
            ws.append([q.replace("Q", "-Q"), dc, P.FAMILY[fam]["model"].split(" ")[1], n, n * P.VAULT_DRIVES])
        ws["A1"].font = Font(bold=True)
        wb.save(path)
        PP.normalize_ooxml(path, P.PEOPLE["capacity"], P.PEOPLE["capacity"], "2026-08-24T14:05:00Z", "2026-09-21T16:40:12Z",
                           excel=True, company=P.FIRM)

    # ---- procurement_and_costs.yaml
    def costs(self, path):
        L = ["# procurement and cost inputs for drive spares and vault work (finance, updated 2026-09-30)",
             "lead_time_quarters: %d" % P.COSTS["lead_quarters"], "spares_on_hand_2026_09_30:"]
        for fam, n in P.SPARES_ON_HAND.items():
            L.append("  %s: %d" % (P.FAMILY[fam]["model"].split(" ")[1], n))
        L.append("unit_cost_usd:")
        for fam, c in P.COSTS["spare_unit"].items():
            L.append("  %s: %d" % (P.FAMILY[fam]["model"].split(" ")[1], c))
        L += ["vault_migration_cost_usd: %d   # move a vault's data to new drives and retire it" % P.COSTS["migrate_vault"],
              "failure_handling_cost_usd: %d   # per replacement: rebuild, technician time, shipping" % P.COSTS["failure_handling"],
              "stockout_tolerance: %.2f   # chance of running short in a quarter that ops accepts" % P.COSTS["stockout"], ""]
        open(path, "w").write("\n".join(L))

    # ---- the quarter's close-out page (an image exported from the reliability dashboard)
    def closeout(self, path):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        qs = quarters_between(dt.date(2024, 10, 1), P.END)
        rates = {dc: [] for dc in ("DC-1", "DC-2", "DC-3")}
        for q in qs:
            a, b = quarter_bounds(q)
            for dc in rates:
                ev = ex = 0
                for d in self.W.drives:
                    if d["dc"] != dc:
                        continue
                    s = self.seen(d)
                    if s is None:
                        continue
                    lo, hi = max(a, s[0]), min(b, s[1] + dt.timedelta(days=1))
                    if hi > lo:
                        ex += (hi - lo).days
                    if d["exit"] is not None and d["kind"] in ("FAIL", "PULL", "SPUR") and a <= WD.to_date(d["exit"]) < b:
                        ev += 1
                rates[dc].append(100.0 * ev / max(ex, 1) * 365.0)
        fig, ax = plt.subplots(figsize=(8.0, 4.2), dpi=110)
        for dc, c in zip(rates, ("#2a6f97", "#c46a28", "#5b8c3a")):
            ax.plot(range(len(qs)), rates[dc], marker="o", color=c, label=dc, linewidth=1.8)
        ax.set_xticks(range(len(qs)))
        ax.set_xticklabels([q.replace("Q", " Q") for q in qs], fontsize=8)
        ax.set_ylabel("Annualized replacement rate (%)", fontsize=9)
        ax.set_title("Halden Vault fleet reliability: data-drive replacements by site, quarter ended 30 Sep 2026", fontsize=10)
        ax.grid(axis="y", alpha=0.3)
        ax.legend(frameon=False, fontsize=8)
        fig.text(0.01, 0.01, "Replacements (FAIL + PULL) per drive-day, annualized. Source: telemetry warehouse, drive-days method. "
                 "Prepared by fleet reliability.", fontsize=6.5, color="#555555")
        fig.tight_layout(rect=(0, 0.03, 1, 1))
        fig.savefig(path, metadata={"Software": None})
        plt.close(fig)
        strip_png(path)

    # ---- distractors
    def environment(self, path):
        rng = self.rng
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["date", "dc", "inlet_avg_c", "inlet_max_c", "rel_humidity_pct"])
            d = P.REC_START
            while d <= P.END:
                for dc, base in (("DC-1", 22.0), ("DC-2", 23.1), ("DC-3", 24.0)):
                    t = base + 1.2 * math.sin(2 * math.pi * (d.timetuple().tm_yday - 110) / 365.25) + rng.normal(0, 0.4)
                    w.writerow([d.isoformat(), dc, round(t, 1), round(t + abs(rng.normal(2.5, 0.8)), 1), round(rng.normal(41, 4), 1)])
                d += dt.timedelta(days=1)

    def datasheets(self, path):
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import Paragraph, Spacer, Table
        ss = getSampleStyleSheet()
        body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13)
        title = ParagraphStyle("t", parent=body, fontName="Helvetica-Bold", fontSize=13, leading=17)
        rows = [["Model", "Capacity", "MTTF (vendor)", "AFR (vendor)"]] + [list(r) for r in DC.DATASHEETS]
        story = [Paragraph("Enterprise HDD reliability specifications, as published by each vendor", title), Spacer(1, 6),
                 Paragraph("Collected by procurement from vendor product briefs for the 2026 supplier review. Vendors quote "
                           "MTTF and AFR under their own test conditions (24x7 at 40 C, workload rated per product brief).", body),
                 Spacer(1, 6), Table(rows)]
        O.build(path, story, "Vendor reliability specifications", P.PEOPLE["capacity"], "Supplier review 2026",
                "Halden Vault | procurement | supplier review 2026", dt.datetime(2026, 5, 12, 15, 30, tzinfo=UTC),
                dt.datetime(2026, 5, 13, 9, 11, 5, tzinfo=UTC), producer="LibreOffice 7.6")

    def ssd(self, path):
        rng = self.rng
        n = 0
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["serial", "quarter", "dc", "host", "wear_level_pct", "media_errors", "power_on_hours", "avg_temp_c"])
            for i in range(380):
                s = "SB%09d" % rng.integers(0, 10 ** 9)
                dc = ["DC-1", "DC-2", "DC-3"][i % 3]
                wear = rng.uniform(1, 12)
                for q in quarters_between(dt.date(2024, 1, 1), P.END):
                    wear += rng.uniform(0.4, 1.6)
                    w.writerow([s, q, dc, "%s-h%03d" % (dc.lower(), i), round(wear, 1), int(rng.poisson(0.05)),
                                int(rng.integers(8000, 40000)), round(rng.normal(36, 2), 1)])
                    n += 1
        return n


def s187_on(d, hi):
    return d["s187"] is not None and WD.to_date(d["s187"]) <= hi and (d["exit"] is None or WD.to_date(d["exit"]) >= hi or True)


def strip_png(path):
    """Keep a PNG's image chunks only, as the dashboard's exporter writes it (no software or time text)."""
    import struct
    import zlib
    b = open(path, "rb").read()
    out = [b[:8]]
    i = 8
    while i < len(b):
        n = struct.unpack(">I", b[i:i + 4])[0]
        t = b[i + 4:i + 8]
        if t in (b"IHDR", b"PLTE", b"IDAT", b"IEND", b"pHYs"):
            out.append(b[i:i + 12 + n])
        i += 12 + n
    open(path, "wb").write(b"".join(out))


def write(W, tgt):
    pk = Pack(W)
    return pk.write(tgt), pk
