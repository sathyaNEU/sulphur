"""Each system's export of the simulated process, as that system writes it, into target/.

The assistant platform, the live chat tool and the case system write local time; the telephony platform writes UTC.
Customers type tracking numbers their own way; the IVR takes digits. The case system publishes a case when it is
resolved, and its weekly backlog report counts the open ones. Nothing here describes the data: provenance lives in
metadata.json outside target/.
"""
import csv
import datetime as dt
import os

import numpy as np
import openpyxl
from docx import Document
from docx.shared import Mm, Pt
from openpyxl.styles import Alignment, Font

import params as P
import postprocess

ORG = "Quellstein Paket GmbH"
FILES = {
    "assistant": "assistant_conversations_2026w32_w45.csv",
    "calls": "acd_call_legs_2026-08-03_2026-11-08.csv",
    "chat": "livechat_sessions_2026w32_w45.csv",
    "cases": "case_resolutions_to_2026-11-08.csv",
    "backlog": "case_backlog_weekly.xlsx",
    "cons": "consignments_referenced.csv",
    "network": "network_performance_daily.csv",
    "plan": "season_plan_w47_w53.xlsx",
    "intents": "assistant_intents.csv",
    "wrapup": "wrapup_codes.csv",
    "categories": "case_categories.csv",
    "standard": "KS-07_contact_service_standard.docx",
    "release": "assistant_release_3_0.docx",
    "acd": "acd_weekly_summary.xlsx",
    "csat": "csat_responses_2026w32_w45.csv",
    "roster": "adviser_roster.csv",
    "depots": "depots.csv",
}
DISTRACTORS = ["csat", "roster"]
CET = dt.timezone(dt.timedelta(hours=1))
WRITTEN = {
    "assistant": dt.datetime(2026, 11, 9, 6, 10, 22, tzinfo=CET), "calls": dt.datetime(2026, 11, 9, 6, 2, 47, tzinfo=CET),
    "chat": dt.datetime(2026, 11, 9, 6, 14, 5, tzinfo=CET), "cases": dt.datetime(2026, 11, 9, 6, 20, 51, tzinfo=CET),
    "cons": dt.datetime(2026, 11, 9, 6, 31, 9, tzinfo=CET), "network": dt.datetime(2026, 11, 9, 5, 45, 33, tzinfo=CET),
    "intents": dt.datetime(2026, 9, 25, 15, 12, 40, tzinfo=CET), "wrapup": dt.datetime(2026, 1, 14, 11, 3, 18, tzinfo=CET),
    "categories": dt.datetime(2025, 3, 3, 9, 41, 55, tzinfo=CET), "csat": dt.datetime(2026, 11, 9, 6, 40, 12, tzinfo=CET),
    "roster": dt.datetime(2026, 10, 30, 14, 27, 6, tzinfo=CET), "depots": dt.datetime(2025, 9, 2, 10, 15, 30, tzinfo=CET),
}
OFFICE = {   # created, modified (UTC), last saved by
    "backlog": ("2026-01-05T07:12:00Z", "2026-11-09T06:38:00Z", "Alena Blümel"),
    "plan": ("2026-10-19T08:30:00Z", "2026-11-06T15:12:00Z", "Simon Pertl"),
    "acd": ("2026-01-05T07:40:00Z", "2026-11-09T06:05:00Z", "Simon Pertl"),
}
DOCS = {"standard": ("2025-11-17T09:20:00Z", "2026-05-18T13:44:00Z", "Helena Neumann", 14, 212),
        "release": ("2026-09-21T10:05:00Z", "2026-09-24T16:31:00Z", "Theresa Jovanovic", 5, 64)}

INTENTS = {"TRK": ["track_status", "track_no_scan", "track_where_now"], "DLV": ["delivery_day", "delivery_window", "delivery_today"],
           "RDR": ["redirect_address", "address_correction", "neighbour_or_safe_place"], "RDL": ["missed_delivery", "book_redelivery"],
           "PUP": ["pickup_point_where", "pickup_deadline", "pickup_id_needed"], "CUS": ["customs_status", "import_charges", "customs_documents"],
           "DMG": ["damage_report", "damage_claim_status"], "LST": ["parcel_missing", "trace_request"],
           "RET": ["return_label", "return_status", "return_how"], "PAY": ["cod_payment", "refund_status", "charge_query"]}
GENERAL_INTENTS = ["send_a_parcel", "prices", "opening_hours", "business_account", "smalltalk", "job_application"]
WRAP = {"TRK": [("T10", "Tracking status"), ("T11", "No scan since handover")], "DLV": [("D20", "Delivery day"), ("D21", "Delivery time window")],
        "RDR": [("A30", "Redirect to another address"), ("A31", "Address correction")], "RDL": [("M40", "Missed delivery"), ("M41", "Redelivery booking")],
        "PUP": [("P50", "Pickup point collection")], "CUS": [("C60", "Customs clearance"), ("C61", "Import charges")],
        "DMG": [("S70", "Damage")], "LST": [("L80", "Missing parcel")], "RET": [("R90", "Returns")],
        "PAY": [("F95", "Charges and cash on delivery"), ("F96", "Refund")]}
WRAP_OTHER = [("G00", "General enquiry"), ("G01", "Sending and prices"), ("G02", "Complaint about conduct")]
CATS = {"TRK": ("TRC-STATUS", "Status enquiry"), "DLV": ("TRC-DELIVERY", "Delivery date enquiry"), "LST": ("TRC-MISSING", "Missing parcel trace"),
        "RDR": ("ADR-CHANGE", "Address change or redirect"), "RDL": ("ADR-REDELIVERY", "Redelivery request"), "PUP": ("ADR-PICKUP", "Pickup point matter"),
        "DMG": ("CLM-DAMAGE", "Damage claim"), "CUS": ("CUS-CLEARANCE", "Customs documents and charges"),
        "PAY": ("BIL-CHARGE", "Charge, cash on delivery or refund"), "RET": ("BIL-RETURN", "Return shipment")}
EPOCH = dt.datetime.combine(P.START, dt.time())


def local(h):
    return EPOCH + dt.timedelta(seconds=round(h * 3600))


def fmt_local(h):
    return local(h).strftime("%Y-%m-%d %H:%M:%S")


def fmt_utc(h):
    t = local(h)
    t -= dt.timedelta(hours=2 if t < P.DST_END else 1)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _write(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def tracking(n):
    rng = np.random.default_rng(P.SEED + 1)
    base = rng.permutation(900_000_000)[:n] + 40_100_000_000
    return ["QP%011d" % b for b in base]


def typed(rng, t):
    u = rng.random()
    if u < 0.10:
        return "%s %s %s %s" % (t[:2], t[2:6], t[6:10], t[10:])
    if u < 0.16:
        return t.lower()
    if u < 0.20:
        return t[2:]
    return t


def write_all(W, target):
    os.makedirs(target, exist_ok=True)
    for f in os.listdir(target):
        os.remove(os.path.join(target, f))
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    rng = np.random.default_rng(P.SEED + 2)
    rsub = np.random.default_rng((P.SEED, 9))            # which of a family's codes a conversation or adviser picks

    def pick(xs):
        w = np.array([1.0 / (1.6 ** i) for i in range(len(xs))]); u = rsub.random() * w.sum()
        return xs[int(np.searchsorted(np.cumsum(w), u, side="right").clip(0, len(xs) - 1))]
    cons, contacts, phone, prev = W["cons"], W["contacts"], W["phone"], W["prev"]
    trk = tracking(len(cons))
    n = {}
    advisers = ["ADV%04d" % (1000 + i) for i in range(148)]

    # ---- assistant platform (local time)
    rows = []
    ids = rng.permutation(4_000_000)[:len(contacts) + 20000] + 1_000_000
    k = 0
    for j, r in enumerate(contacts):
        if r[2] != "A":
            continue
        idx, _, _, fam, start, end, hand = r
        day = int(start // 24)
        build = "2.9.3" if day < 20 else "2.9.4" if day < P.V3_DAY else "3.0.0" if day < 73 else "3.0.1"
        rows.append(["A%07d" % ids[k], fmt_local(start), fmt_local(end), "app" if rng.random() < 0.63 else "web", build,
                     (pick(INTENTS[P.FAM[fam]]), rng.integers(0, len(INTENTS[P.FAM[fam]])))[0], typed(rng, trk[idx]), int(2 + rng.poisson(3.2)),
                     "Y" if hand else "N", "de" if rng.random() < 0.88 else "en"])
        k += 1
    n_scope = len(rows)
    for _ in range(int(n_scope * 0.09)):               # conversations about no consignment
        h = rng.uniform(0, P.DAYS) * 24
        day = int(h // 24)
        build = "2.9.3" if day < 20 else "2.9.4" if day < P.V3_DAY else "3.0.0" if day < 73 else "3.0.1"
        rows.append(["A%07d" % ids[k], fmt_local(h), fmt_local(h + rng.gamma(2.0, 1.2) / 60), "app" if rng.random() < 0.5 else "web", build,
                     (pick(GENERAL_INTENTS), rng.choice(GENERAL_INTENTS))[0], "", int(1 + rng.poisson(2.0)), "N", "de" if rng.random() < 0.88 else "en"])
        k += 1
    rows.sort(key=lambda x: x[1])
    n["assistant"] = _write(F["assistant"], ["conversation_id", "started_at", "ended_at", "entry", "build", "intent", "tracking_no",
                                             "customer_messages", "handed_to_adviser", "language"], rows)

    # ---- telephony (UTC; one row per leg; callbacks)
    rows = []
    cid = rng.permutation(9_000_000)[:len(contacts) + 40000] + 10_000_000
    k = 0
    weekly = {}

    def wrap(fam):
        rng.integers(0, len(WRAP[fam]))
        return pick(WRAP[fam])[0]
    for j, r in enumerate(contacts):
        if r[2] != "P":
            continue
        idx, _, _, fam, start, end, _ = r
        f = P.FAM[fam]
        path, wait = phone[j]
        pc, has_a = prev[j]
        if has_a:
            tag = "ASSISTANT" if rng.random() < P.TAG_HIT else ""
        elif pc:
            tag = {"P": "PHONE", "C": "CHAT", "W": "WRITTEN"}[pc] if rng.random() < 0.5 else ""
        else:
            tag = "ASSISTANT" if rng.random() < P.TAG_FALSE else ""
        call = "C%08d" % cid[k]; k += 1
        q = P.QUEUE_OF[f]
        keyed = trk[idx][2:] if path == "KEYED" else ""
        talk = (end - start) * 3600
        answer = start + wait / 3600.0
        wk = int(start // 24) // 7
        weekly.setdefault((wk, q), [0, 0, 0]); weekly[(wk, q)][0] += 1
        u = rng.random()
        if u < 0.09:                                    # transferred once (the first adviser passes it on)
            t1 = talk * rng.uniform(0.25, 0.5)
            q2 = q if rng.random() < 0.6 else str(rng.choice(P.QUEUES))
            rows.append([call, 1, "IN", fmt_utc(start), q, path, keyed, int(round(wait)), int(round(t1)), wrap(f), tag, advisers[int(rng.integers(0, 148))]])
            rows.append([call, 2, "IN", fmt_utc(answer + t1 / 3600), q2, "", keyed, int(rng.integers(5, 90)), int(round(talk - t1)), wrap(f), "", advisers[int(rng.integers(0, 148))]])
            weekly[(wk, q)][1] += 1
        else:
            rows.append([call, 1, "IN", fmt_utc(start), q, path, keyed, int(round(wait)), int(round(talk)), wrap(f), tag, advisers[int(rng.integers(0, 148))]])
        if rng.random() < 0.05 and end + 30 < P.DAYS * 24:   # the adviser rings back later
            cb = _next_open(end + rng.uniform(2, 28))
            if cb < P.DAYS * 24:
                rows.append(["C%08d" % cid[k], 1, "OUT", fmt_utc(cb), q, "", trk[idx][2:] if rng.random() < 0.9 else "", 0,
                             int(rng.gamma(2.5, 70)), wrap(f), "", advisers[int(rng.integers(0, 148))]])
                k += 1
                weekly.setdefault((int(cb // 24) // 7, q), [0, 0, 0]); weekly[(int(cb // 24) // 7, q)][2] += 1
    for h, path, wait in W["other_calls"]:
        wk = int(h // 24) // 7
        weekly.setdefault((wk, "GENERAL"), [0, 0, 0]); weekly[(wk, "GENERAL")][0] += 1
        rows.append(["C%08d" % cid[k], 1, "IN", fmt_utc(h), "GENERAL", path, "", int(round(wait)), int(rng.gamma(2.5, 80)),
                     (pick(WRAP_OTHER)[0], rng.integers(0, 3))[0], "", advisers[int(rng.integers(0, 148))]])
        k += 1
    rows.sort(key=lambda x: (x[3], x[0], x[1]))
    n["calls"] = _write(F["calls"], ["call_id", "leg", "direction", "start_utc", "queue", "ivr_path", "tracking_keyed", "queue_wait_s",
                                     "talk_s", "wrapup_code", "previous_contact", "adviser_id"], rows)

    # ---- live chat (local time)
    rows = []
    sid = rng.permutation(3_000_000)[:len(contacts) + 9000] + 500_000
    k = 0
    for j, r in enumerate(contacts):
        if r[2] != "C":
            continue
        idx, _, _, fam, start, end, _ = r
        hand = prev[j][0] == "A" and any(c[0] == idx and c[6] and abs(start - c[5]) < 0.05 for c in _prev_of(contacts, j))
        rows.append(["S%07d" % sid[k], fmt_local(start), fmt_local(end), "assistant" if hand else ("app" if rng.random() < 0.55 else "web"),
                     typed(rng, trk[idx]), wrap(P.FAM[fam]), advisers[int(rng.integers(0, 148))]])
        k += 1
    for _ in range(int(len(rows) * 0.07)):
        h = _next_open(rng.uniform(0, P.DAYS) * 24, lo=8.0)
        if h >= P.DAYS * 24:
            continue
        rows.append(["S%07d" % sid[k], fmt_local(h), fmt_local(h + rng.gamma(3, 2.5) / 60), "web", "", (pick(WRAP_OTHER)[0], rng.integers(0, 3))[0], advisers[int(rng.integers(0, 148))]])
        k += 1
    rows.sort(key=lambda x: x[1])
    n["chat"] = _write(F["chat"], ["session_id", "started_at", "ended_at", "source", "tracking_no", "wrapup_code", "adviser_id"], rows)

    # ---- case system: the resolution extract (a case is published when it is closed) and the weekly backlog report
    ext = P.DAYS * 24.0
    rows = []
    kid = rng.permutation(800_000)[:len(W["cases"])] + 2_600_000
    for i, c in enumerate(W["cases"]):
        cj, created, origin, fam, q, closed, idx = c
        if closed >= ext:
            continue
        cat = CATS[P.FAM[fam]][0] if fam >= 0 else "GEN-OTHER"
        t = typed(rng, trk[idx]) if idx >= 0 and (origin != "EMAIL" or True) else ""
        rows.append(["K%07d" % kid[i], fmt_local(created), origin, cat, q, t, fmt_local(closed),
                     str(rng.choice(["RESOLVED", "RESOLVED", "RESOLVED", "NO_ACTION_NEEDED", "COMPENSATED" if q in ("CLAIMS", "BILLING") else "RESOLVED"]))])
    n["cases"] = _write(F["cases"], ["case_id", "created_at", "origin", "category", "queue", "tracking_no", "closed_at", "outcome"], rows)
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "Open by age"
    ws.append(["Snapshot (Monday 00:00)", "Queue", "Raised by", "Days open", "Open cases"])
    wf = wb.create_sheet("Weekly flow")
    wf.append(["Week starting", "Queue", "Raised by", "Opened", "Closed"])
    queues = list(P.CASE_QUEUES) + ["GENERAL"]
    for s in range(7, P.DAYS + 1, 7):
        snap = s * 24.0
        cnt = {}
        flow = {}
        for cj, created, origin, fam, q, closed, idx in W["cases"]:
            if created >= snap:
                break
            who = "Adviser" if origin == "ADVISER" else "Customer"
            if closed >= snap:
                age = min(int((snap - created) // 24), 42)
                cnt[(q, who, age)] = cnt.get((q, who, age), 0) + 1
            if created >= snap - 168:
                flow.setdefault((q, who), [0, 0])[0] += 1
            if snap - 168 <= closed < snap:
                flow.setdefault((q, who), [0, 0])[1] += 1
        d = (EPOCH + dt.timedelta(days=s)).date()
        for q in queues:
            for who in ("Customer", "Adviser"):
                for age in range(43):
                    if cnt.get((q, who, age), 0):
                        ws.append([d, q, who, age if age < 42 else "42 and over", cnt[(q, who, age)]])
                fl = flow.get((q, who), [0, 0])
                wf.append([d - dt.timedelta(days=7), q, who, fl[0], fl[1]])
    for sh, widths in ((ws, [24, 12, 11, 12, 12]), (wf, [16, 12, 11, 10, 10])):
        for i, w in enumerate(widths):
            sh.column_dimensions[chr(65 + i)].width = w
        for c in sh[1]:
            c.font = Font(bold=True); c.alignment = Alignment(wrap_text=True, vertical="top")
        sh.freeze_panes = "A2"
        for row in sh.iter_rows(min_row=2, max_col=1):
            row[0].number_format = "yyyy-mm-dd"
    wb.save(F["backlog"])

    # ---- network: consignments the contact systems referenced, and the daily service record
    rows = []
    for idx, (dep, due, ci, deliv, exc, alerted) in enumerate(cons):
        c = P.CLASSES[ci]
        promised = P.START + dt.timedelta(days=due)
        delivered = ""
        if 0 <= deliv < P.DAYS:
            delivered = (EPOCH + dt.timedelta(days=deliv, hours=float(rng.uniform(8, 18.5)))).strftime("%Y-%m-%d %H:%M")
        if c == "EX":
            oc = "EXCEPTION"
        elif c == "ON":
            oc = "ON_TIME"
        elif c == "L1":
            oc = "LATE_1" if due + 1 < P.DAYS else "IN_TRANSIT"
        else:
            oc = "LATE_2PLUS" if due + 2 < P.DAYS else "IN_TRANSIT"
        rows.append([trk[idx], P.DEPOTS[dep][0], "IMP" if exc == "CUSTOMS_HOLD" or rng.random() < 0.05 else "DOM",
                     promised.isoformat(), delivered, oc, exc])
    order = rng.permutation(len(rows))
    rows = [rows[i] for i in sorted(range(len(rows)), key=lambda i: (rows[i][3], order[i]))]
    n["cons"] = _write(F["cons"], ["tracking_no", "depot", "service", "promised_date", "delivered_at", "outcome_class", "exception_code"], rows)
    rows = []
    N = W["N"]
    for t in range(P.DAYS):
        for i, (code, _, _) in enumerate(P.DEPOTS):
            a = [int(x) for x in N[t, i]]
            if sum(a) == 0:
                continue
            pend = 0
            if t + 1 >= P.DAYS:
                pend += a[1]; a[1] = 0
            if t + 2 >= P.DAYS:
                pend += a[2]; a[2] = 0
            rows.append([(P.START + dt.timedelta(days=t)).isoformat(), code, sum(a) + pend, a[0], a[1], a[2], a[3], pend])
    n["network"] = _write(F["network"], ["due_date", "depot", "parcels_due", "on_time", "late_1", "late_2plus", "exception", "in_transit"], rows)

    # ---- the season plan (workforce planning's workbook)
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "Volumes"
    ws.append(["Week starting"] + [d[0] for d in P.DEPOTS] + ["All depots"])
    wsum = sum(d[2] for d in P.DEPOTS)
    tilt = {"WIN": 1.06, "WIS": 1.05, "GRZ": 1.02, "BRE": 0.9, "KLU": 0.93}
    rplan = np.random.default_rng((P.SEED, 10))
    for wk, tot in zip(P.PEAK_WEEKS, P.PEAK_PARCELS):
        raw = [d[2] * tilt.get(d[0], 1.0) * float(np.exp(rplan.normal(0, 0.035))) for d in P.DEPOTS]
        vals = [int(round(tot * 1000 * x / sum(raw) / 100.0)) * 100 for x in raw]
        vals[0] += tot * 1000 - sum(vals)
        ws.append([wk] + vals + [tot * 1000])
    sv = wb.create_sheet("Service levels")
    sv.append(["Week starting", "On time %", "One day late %", "Two or more days late %", "Exception %"])
    for wk, s in zip(P.PEAK_WEEKS, P.PEAK_SERVICE):
        sv.append([wk] + list(s))
    nt = wb.create_sheet("Notifications")
    nt.append(["Depot", "Delay alerts live from", "Sent when", "By"])
    for code, name, _ in P.DEPOTS:
        nt.append(["%s %s" % (code, name), (P.START + dt.timedelta(days=P.ALERT_DAY)) if code in P.PILOT else dt.date(2026, 11, 16),
                   "parcel misses its promised day", "SMS, e-mail"])
    ro = wb.create_sheet("Adviser rota")
    ro.append(["Week starting", "Telephone FTE", "Live chat FTE", "Written FTE"])
    for i, wk in enumerate(P.PEAK_WEEKS):
        ro.append([wk, [118, 126, 140, 138, 140, 134, 104][i], [34, 36, 40, 40, 40, 38, 30][i], [41, 43, 47, 47, 48, 46, 38][i]])
    for sh in (ws, sv, nt, ro):
        for c in sh[1]:
            c.font = Font(bold=True); c.alignment = Alignment(wrap_text=True, vertical="top")
        sh.column_dimensions["A"].width = 26 if sh is nt else 15
        for col in "BCDEFGHIJKL":
            sh.column_dimensions[col].width = 30 if (sh is nt and col == "C") else 22 if (sh is nt and col == "B") else 13
        sh.freeze_panes = "B2"
        for row in sh.iter_rows(min_row=2):
            for c in row:
                if isinstance(c.value, dt.date):
                    c.number_format = "yyyy-mm-dd"
                elif isinstance(c.value, int) and c.value > 999:
                    c.number_format = "#,##0"
    wb.save(F["plan"])

    # ---- telephony's weekly summary (handled calls by queue)
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "Handled calls"
    ws.append(["Week starting", "Queue", "Inbound calls handled", "of which transferred", "Outbound callbacks"])
    for wk in range(P.DAYS // 7):
        for q in P.QUEUES:
            a = weekly.get((wk, q), [0, 0, 0])
            ws.append([P.START + dt.timedelta(days=7 * wk), q, a[0], a[1], a[2]])
    for i, w in enumerate([15, 12, 22, 20, 20]):
        ws.column_dimensions[chr(65 + i)].width = w
    for c in ws[1]:
        c.font = Font(bold=True)
    ws.freeze_panes = "A2"
    for row in ws.iter_rows(min_row=2, max_col=1):
        row[0].number_format = "yyyy-mm-dd"
    wb.save(F["acd"])

    # ---- code lists
    _write(F["intents"], ["intent", "reason_family", "family_name"],
           [[i, f, dict(P.FAMILIES)[f]] for f in P.FAM for i in INTENTS[f]] + [[i, "", "(no consignment)"] for i in GENERAL_INTENTS])
    _write(F["wrapup"], ["wrapup_code", "label", "reason_family"],
           [[c, lab, f] for f in P.FAM for c, lab in WRAP[f]] + [[c, lab, ""] for c, lab in WRAP_OTHER])
    _write(F["categories"], ["category", "label", "queue", "reason_family"],
           [[CATS[f][0], CATS[f][1], P.CASE_QUEUE_OF[f], f] for f in P.FAM] + [["GEN-OTHER", "General correspondence", "GENERAL", ""]])
    _write(F["depots"], ["depot", "name", "province", "linehaul_hub", "hub_since"],
           [[c, nm, {"WIN": "Wien", "WIS": "Wien", "STP": "Niederösterreich", "LNZ": "Oberösterreich", "WEL": "Oberösterreich",
                     "SZG": "Salzburg", "GRZ": "Steiermark", "KLU": "Kärnten", "IBK": "Tirol", "BRE": "Vorarlberg"}[c],
             "Traunfeld" if c in P.HUB else "Wals" if c in ("SZG", "IBK", "BRE") else "Kalsdorf",
             "2026-10-05" if c in P.HUB else "2019-03-04" if c in ("SZG", "IBK", "BRE") else "2021-09-06"] for c, nm, _ in P.DEPOTS])
    _write(F["roster"], ["adviser_id", "site", "team", "telephone", "live_chat", "written", "joined"],
           [[a, str(rng.choice(["Linz", "Wien", "Graz"], p=[.45, .35, .2])), "T%02d" % rng.integers(1, 15), "Y" if rng.random() < 0.8 else "N",
             "Y" if rng.random() < 0.35 else "N", "Y" if rng.random() < 0.3 else "N",
             (dt.date(2015, 1, 1) + dt.timedelta(days=int(rng.integers(0, 4200)))).isoformat()] for a in advisers])
    # ---- the post-contact survey (a link sent after a contact; few answer)
    rows = []
    sid2 = rng.permutation(2_000_000)[:len(contacts)] + 100_000
    for j, r in enumerate(contacts):
        idx, _, ch, fam, start, end, _ = r
        if end + 30 >= ext:
            continue
        came_back = bool(W["follow"].get(j)) if ch == "A" else rng.random() < 0.18
        if rng.random() < (0.11 if came_back else 0.055):
            score = int(np.clip(round(rng.normal(2.1 if came_back else 4.1, 1.1)), 1, 5))
            when = end + rng.exponential(9.0) + 0.3
            rows.append(["R%07d" % sid2[j], fmt_local(when), {"A": "assistant", "P": "telephone", "C": "live chat", "W": "written"}[ch],
                         typed(rng, trk[idx]) if rng.random() < 0.8 else "", score, "yes" if score >= 4 or (score == 3 and rng.random() < 0.4) else "no"])
    rows = [x for x in rows if x[1] < fmt_local(ext)]
    rows.sort(key=lambda x: x[1])
    n["csat"] = _write(F["csat"], ["response_id", "answered_at", "channel", "tracking_no", "score_1_to_5", "question_answered"], rows)
    docs(F)
    for kk, (created, modified, who) in OFFICE.items():
        postprocess.normalize_ooxml(F[kk], who, who, created, modified, excel=True, company=ORG)
    postprocess.own_mtimes(target, {FILES[kk]: v for kk, v in WRITTEN.items()})
    return n


def _next_open(t, lo=7.0):
    for _ in range(10):
        day = int(t // 24); h = t - day * 24
        if day % 7 == 6 or h >= 20.0:
            t = (day + 1) * 24 + lo + 0.4
        elif h < lo:
            t = day * 24 + lo + 0.4
        else:
            return t
    return t


_BY = {}


def _prev_of(contacts, j):
    if not _BY:
        for k, r in enumerate(contacts):
            _BY.setdefault(r[0], []).append(k)
    return [contacts[k] for k in _BY[contacts[j][0]] if k < j]


def _doc(path, header, title, meta, paras, key):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(24); sec.top_margin = Mm(22); sec.bottom_margin = Mm(20)
    st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    hp = sec.header.paragraphs[0]; hp.text = header; hp.runs[0].font.size = Pt(8)
    t = doc.add_paragraph(); r = t.add_run(title); r.bold = True; r.font.size = Pt(14)
    for a, b in meta:
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(0)
        x = p.add_run("%s: " % a); x.bold = True
        p.add_run(b)
    doc.add_paragraph()
    for kind, text in paras:
        if kind == "h":
            p = doc.add_paragraph(); r = p.add_run(text); r.bold = True; r.font.size = Pt(11.5)
            p.paragraph_format.space_before = Pt(8)
        else:
            p = doc.add_paragraph(text); p.paragraph_format.space_after = Pt(5)
    doc.save(path)
    created, modified, who, rev, minutes = DOCS[key]
    postprocess.normalize_docx(path, who, who, created, modified, rev, minutes, "task16-" + key, title=title, company=ORG)


def docs(F):
    _doc(F["standard"], "Quellstein Paket, Customer Contact", "KS-07 Contact service standard",
         [("Owner", "Head of Customer Contact"), ("Issue", "4, in force from 1 June 2026"), ("Applies to", "the assistant, live chat, telephone and written contact")],
         [("h", "1 Purpose"),
          ("p", "This standard sets how Customer Contact measures whether a contact settled the customer's matter, and how the "
                "division decides, season by season, which reasons for contact are offered the assistant first."),
          ("h", "2 Terms"),
          ("p", "2.1 A contact is one customer-initiated approach to Quellstein through a contact channel: a conversation with the "
                "assistant, a live chat session, a telephone call answered by an adviser, or a written approach (a web form or an "
                "e-mail, held as a case). A call that is transferred between advisers is one contact. Calls and messages that "
                "Quellstein makes to a customer, and cases that an adviser opens while handling a contact, are not contacts."),
          ("p", "2.2 A contact concerns a consignment when it is about one parcel identified by its tracking number. Contacts that "
                "concern no consignment are outside this standard."),
          ("p", "2.3 Every contact that concerns a consignment has one reason family. The ten reason families and the codes each "
                "channel uses for them are held in the division's code lists. An assistant conversation takes the family of its intent."),
          ("h", "3 Resolution"),
          ("p", "3.1 An assistant conversation that concerns a consignment is resolved when no further contact is made about the same "
                "consignment, through any contact channel, within seven days (168 hours) of the end of the conversation. A conversation "
                "the assistant hands to an adviser is followed by a further contact and is not resolved."),
          ("p", "3.2 The resolution rate of a reason family over a period is the share of the assistant conversations in that family "
                "that ended in the period and are resolved."),
          ("p", "3.3 A resolution rate is reported only for conversations that ended at least seven days before the data were cut."),
          ("h", "4 Assistant-first"),
          ("p", "4.1 Before each season the Head of Customer Contact fixes, reason family by reason family, whether customers are "
                "offered the assistant first or an adviser first for the season."),
          ("p", "4.2 A reason family is assistant-first for a season when its expected resolution rate for that season, for the "
                "assistant version then in service and given the season plan, is at least 75 per cent. Otherwise it is adviser-first."),
          ("p", "4.3 Expected rates are quoted with a 90 per cent range for what the record supports. The season plan is taken "
                "as given."),
          ("h", "5 Records"),
          ("p", "5.1 The telephony record identifies the consignment a call concerns only where the caller keyed a tracking "
                "number in the IVR."),
          ("p", "5.2 The case system publishes a case to the resolution extract when the case is closed. Cases still open are "
                "counted in the case team's weekly backlog report."),
          ("h", "6 Review"),
          ("p", "This standard is reviewed each May. Questions go to the Customer Contact planning team.")], "standard")
    _doc(F["release"], "Quellstein Paket, Digital Channels", "Assistant 3.0: release note",
         [("Product owner", "Theresa Jovanovic"), ("Go-live", "Monday 28 September 2026, 00:00, all customers, app and web"),
          ("Replaces", "2.9.4")],
         [("h", "What changes for customers"),
          ("p", "Version 3.0 answers from the live scan record of the parcel instead of the nightly copy, so the status a customer "
                "sees in the assistant is the one an adviser sees. It can book a redelivery slot and change a pickup point inside the "
                "conversation, and it explains import charges line by line."),
          ("p", "The assistant still asks for the tracking number before it answers a question about a parcel, and it still hands "
                "the conversation to live chat when the customer asks for a person and chat is open."),
          ("h", "Builds"),
          ("p", "3.0.0 goes live on 28 September. A maintenance build, 3.0.1, follows in mid October with wording corrections in "
                "the English flows and no change to the answers. Version 3.0 stays in service through the peak season; the next "
                "feature release is planned for February 2027."),
          ("h", "Reporting"),
          ("p", "The conversation export carries the build of every conversation. The intent table is unchanged from 2.9.")], "release")
