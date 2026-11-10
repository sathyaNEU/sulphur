"""task2 architecture 5: the pack's data files. The audits and the monthly volumes are system exports (CSV); the
register, the rollout plan, the quarterly reports and two distractors are workbooks passed through the house writer.
Mess is each system's own: the audit system's two exports (the release string, the error rate as a fraction then a
percentage), first-pass and adjudicated rows, unscorable audio, a volume export run twice for two months."""
import csv
import datetime as dt
import math
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import postprocess as PP
import world as W

UTC = dt.timezone.utc
OLD_EXPORT_TO = W.mi(2024, 12)          # the audit system's first export format runs to December 2024


def month_str(t):
    y, m = divmod(t, 12)
    return "%04d-%02d" % (W.START[0] + y, m + 1)


def ym(t):
    y, m = divmod(t, 12)
    return W.START[0] + y, m + 1


def release_string(rel, t, stage, rng):
    if stage == "adjudicated":
        return "r" + rel
    if t <= OLD_EXPORT_TO:
        patch = {"3.4": "3.4.7", "4.0": "4.0.2", "5.0": "5.0.1"}.get(rel, rel + ".0")
        return "LS-Med " + patch
    return rel


def write_audits(w, target, rng):
    path = os.path.join(target, "dictation_audits_2023_2026.csv")
    rows = []
    auditors = ["AF%02d" % k for k in range(3, 19)]
    for a in w.audits:
        y, m = ym(a["t"])
        dicd = dt.date(y, m, a["day"])
        aud = a["audited_at"].replace(tzinfo=UTC)
        base = dict(audit_id=a["audit"], dictation_id=a["dictation"], site=a["h"], staff_no=a["staff"],
                    dictated_on=dicd.isoformat(), auditor=str(rng.choice(auditors)))
        stages = [("first pass", (a["sub"], a["dele"], a["ins"]), aud)]
        if a["adjudicated"] is not None:
            stages.append(("adjudicated", a["adjudicated"], a["adjudicated_at"].replace(tzinfo=UTC)))
        for stage, (s, d, i), when in stages:
            r = dict(base)
            r["audited_at"] = when.strftime("%Y-%m-%dT%H:%M:%SZ")
            r["release"] = release_string(a["release"], a["t"], stage, rng)
            r["audit_stage"] = stage
            if a["unscorable"]:
                r.update(outcome="unscorable audio", ref_words="", substitutions="", deletions="", insertions="", wer="")
            else:
                e = s + d + i
                wer = e / a["ref"]
                r.update(outcome="scored", ref_words=a["ref"], substitutions=s, deletions=d, insertions=i,
                         wer=("%.4f" % wer) if a["t"] <= OLD_EXPORT_TO else ("%.2f" % (100 * wer)))
            rows.append(r)
    cols = ["audit_id", "dictation_id", "site", "staff_no", "dictated_on", "audited_at", "release", "audit_stage",
            "outcome", "ref_words", "substitutions", "deletions", "insertions", "wer", "auditor"]
    rows.sort(key=lambda r: (r["audited_at"], r["audit_id"]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, lineterminator="\r\n")
        wr.writeheader()
        wr.writerows(rows)
    return len(rows)


RERUN = (W.mi(2025, 3), W.mi(2025, 4))


def pick(rng, table):
    names = [a for a, _ in table]
    pr = np.array([b for _, b in table], dtype=float)
    return names[int(rng.choice(len(names), p=pr / pr.sum()))]   # the volume export for these months was run twice and both runs kept


def write_volumes(w, target, rng):
    path = os.path.join(target, "dictation_volumes_2022_2026.csv")
    site = {s: sp["h"] for s, (pp, sp) in w.spell_of.items()}
    rows = []
    for (staff, t), n in w.vol.items():
        mins = round(n * 1.62 * math.exp(rng.normal(0, 0.08)), 1)
        rows.append((t, site[staff], staff, n, mins))
    rows.sort()
    out = []
    for r in rows:
        out.append(r)
    dup = [r for r in rows if r[0] in RERUN]
    out = sorted(out + dup, key=lambda r: (r[0], r[1], r[2]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(["month", "site", "staff_no", "dictations", "audio_minutes"])
        for t, h, s, n, m in out:
            wr.writerow([month_str(t), h, s, n, "%.1f" % m])
    return len(out)


def xl_header(ws, cols, widths=None):
    ws.append(cols)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DCE6F0")
    for k, wd in enumerate(widths or []):
        ws.column_dimensions[chr(65 + k)].width = wd
    ws.freeze_panes = "A2"


def month_date(t, rng):
    """a day within month index t (which may fall before 2022)"""
    y, m = W.START[0] + int(t // 12), int(t % 12) + 1
    return dt.date(y, m, int(rng.integers(1, 28)))


def write_register(w, target, rng):
    """the group's HR register: every medical and advanced practice post held at one of the eight hospitals at any time
    from 1 January 2022 to 31 December 2026, dictating or not, a move to another group hospital under a new number"""
    path = os.path.join(target, "clinician_register_2026.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.title = "clinicians"
    xl_header(ws, ["staff_no", "site", "grade", "specialty", "in_post_from", "previous_staff_no", "status", "left_on"],
              [10, 7, 26, 26, 13, 17, 9, 12])
    end_rec = W.DEC + 1
    rows = []
    for p in w.people:
        for sp in p["spells"]:
            if sp["end"] <= 0 or sp["start"] >= end_rec:
                continue
            rows.append((sp["staff"], sp, p))
    n = 0
    for staff, sp, p in sorted(rows, key=lambda r: r[0]):
        start = month_date(math.floor(sp["start"]), rng)
        if sp["end"] >= end_rec:
            status, lo = "in post", None
        else:
            status, lo = "left", month_date(math.floor(sp["end"]), rng)
        ws.append([staff, sp["h"], p["grade"], p["spec"], start, sp["prev"], status, lo])
        n += 1
    for row in ws.iter_rows(min_row=2):
        row[4].number_format = "dd/mm/yyyy"
        row[7].number_format = "dd/mm/yyyy"
    wb.save(path)
    PP.normalize_ooxml(path, "Alexander Sigerson", "Alexander Sigerson", "2026-12-16T10:12:00Z", "2027-01-06T09:41:00Z",
                       title="Clinician register (medical and advanced practice staff)", excel=True,
                       company="Shannonside Hospital Group")
    return n


def write_rollout(w, target):
    path = os.path.join(target, "shannonside_dictation_rollout_2027.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 go-lives"
    xl_header(ws, ["Hospital", "Site code", "Clinicians in post (HR, December 2026)", "Dictation compulsory from",
                   "Training from", "Ward lead"], [34, 10, 36, 26, 16, 22])
    size = {c: sum(1 for pp in w.people for sp in pp["spells"]
                   if sp["h"] == c and sp["start"] < W.DEC + 1 <= sp["end"]) for c in W.TEACHING}
    ws.append(["Shannonside University Hospital", "SSU", size["SSU"], dt.date(2027, 2, 1), dt.date(2026, 12, 14), "Colum Wallace"])
    ws.append(["Ballykeel University Hospital", "BKU", size["BKU"], dt.date(2027, 10, 1), dt.date(2027, 8, 16), "Pearce Stapleton"])
    for row in ws.iter_rows(min_row=2):
        row[3].number_format = "dd mmm yyyy"
        row[4].number_format = "dd mmm yyyy"
    ws2 = wb.create_sheet("Scope")
    for line in ["Shannonside Hospital Group, ICT Programme Office.",
                 "From the dates above every clinician in post at the hospital dictates clinical correspondence, "
                 "discharge summaries and reports through the Larkmoor service, as at the group's other hospitals.",
                 "Clinicians in post are the hospital's medical and advanced practice staff on the HR system at 31 "
                 "December 2026, including those already dictating.",
                 "Training runs in the six weeks before each date; support desks are staffed on site for four weeks after."]:
        ws2.append([line])
    ws2.column_dimensions["A"].width = 120
    wb.save(path)
    PP.normalize_ooxml(path, "Yasmine Ganley", "Yasmine Ganley", "2026-11-20T14:05:00Z", "2026-12-09T11:27:00Z",
                       title="Dictation rollout 2027", excel=True, company="Shannonside Hospital Group")


def audit_rows_clean(w):
    """the audits as the quarterly report counts them: the adjudicated score where there is one, unscorable out"""
    out = []
    for a in w.audits:
        if a["unscorable"]:
            continue
        s, d, i = a["adjudicated"] if a["adjudicated"] is not None else (a["sub"], a["dele"], a["ins"])
        out.append((a["t"], a["h"], (s + d + i) / a["ref"] > W.LINE))
    return out


def write_quarterly(w, target):
    path = os.path.join(target, "quality_reports_2023_2026.xlsx")
    rows = audit_rows_clean(w)
    wb = Workbook()
    ws = wb.active
    ws.title = "Group"
    xl_header(ws, ["Quarter", "Audited dictations", "Heavy correction (WER above 15%)", "Share"], [10, 20, 32, 10])
    for y in range(2023, 2027):
        for q in (1, 2, 3, 4):
            ms = set(W.mi(y, 3 * (q - 1) + k + 1) for k in range(3))
            sel = [hv for t, h, hv in rows if t in ms]
            ws.append(["%d Q%d" % (y, q), len(sel), sum(sel), round(sum(sel) / len(sel), 4)])
            ws.cell(ws.max_row, 4).number_format = "0.0%"
    ws2 = wb.create_sheet("By hospital")
    xl_header(ws2, ["Quarter", "Site", "Audited dictations", "Heavy correction", "Share"], [10, 7, 18, 16, 10])
    for y in range(2023, 2027):
        for q in (1, 2, 3, 4):
            ms = set(W.mi(y, 3 * (q - 1) + k + 1) for k in range(3))
            for h in W.CODES:
                sel = [hv for t, hh, hv in rows if t in ms and hh == h]
                if sel:
                    ws2.append(["%d Q%d" % (y, q), h, len(sel), sum(sel), round(sum(sel) / len(sel), 4)])
                    ws2.cell(ws2.max_row, 5).number_format = "0.0%"
    wb.save(path)
    PP.normalize_ooxml(path, "Jody Cahir", "Jody Cahir", "2023-04-11T08:30:00Z", "2027-01-08T16:02:00Z",
                       title="Shannonside quality reports", excel=True, company="Larkmoor Speech")


# ---------------------------------------------------------------- distractors
def write_tickets(w, target, rng):
    path = os.path.join(target, "support_tickets_2024_2026.csv")
    cats = [("Login or account", 0.22), ("EHR integration", 0.16), ("Recognition accuracy", 0.18),
            ("Microphone or headset", 0.14), ("Mobile app", 0.12), ("Training request", 0.10), ("Other", 0.08)]
    act = [dict(h=sp["h"], staff=sp["staff"], first=sp["first"], last=sp["end"]) for pp in w.people for sp in pp["spells"]
           if sp["first"] is not None and sp["first"] <= W.mi(2026, 12)]
    rows = []
    tid = 880000
    for t in range(W.mi(2024, 1), W.mi(2026, 12) + 1):
        live = [c for c in act if c["first"] <= t < c["last"]]
        for _ in range(int(rng.poisson(0.045 * len(live)))):
            c = live[int(rng.integers(0, len(live)))]
            y, m = ym(t)
            op = dt.datetime(y, m, int(rng.integers(1, 29)), int(rng.integers(7, 19)), int(rng.integers(0, 60)))
            cl = op + dt.timedelta(hours=float(rng.exponential(30)))
            tid += int(rng.integers(1, 5))
            pr = str(rng.choice(["P3", "P3", "P3", "P2", "P4", "P1"]))
            rows.append([tid, op.strftime("%d/%m/%Y %H:%M"), c["h"], c["staff"], pick(rng, cats), pr,
                         cl.strftime("%d/%m/%Y %H:%M")])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(["ticket", "opened", "site", "staff_no", "category", "priority", "closed"])
        wr.writerows(rows)
    return len(rows)


def write_microphones(w, target, rng):
    path = os.path.join(target, "headset_inventory_2026.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.title = "Headsets"
    xl_header(ws, ["Asset tag", "Site", "Issued to (staff no)", "Model", "Issued"], [12, 7, 20, 30, 12])
    models = [("Philips SpeechMike Premium Air", 0.38), ("Philips SpeechMike Premium Touch", 0.22),
              ("Nuance PowerMic 4", 0.0), ("Jabra Evolve2 65", 0.24), ("Grundig Digta SonicMic 4", 0.16)]
    models = [m for m in models if m[1] > 0]
    tag = 52000
    live = [dict(h=sp["h"], staff=sp["staff"], first=sp["first"]) for pp in w.people for sp in pp["spells"]
            if sp["first"] is not None and sp["first"] <= W.mi(2026, 12) < sp["end"]]
    for c in sorted(live, key=lambda c: c["staff"]):
        if rng.random() < 0.8:
            tag += int(rng.integers(1, 7))
            y, m = ym(max(0, c["first"]))
            ws.append(["HS-%d" % tag, c["h"], c["staff"], pick(rng, models), dt.date(y, m, int(rng.integers(1, 28)))])
            ws.cell(ws.max_row, 5).number_format = "dd/mm/yyyy"
    wb.save(path)
    PP.normalize_ooxml(path, "Kristopher McLoughlin", "Kristopher McLoughlin", "2025-02-03T10:20:00Z", "2026-12-18T15:44:00Z",
                       title="Headset inventory", excel=True, company="Shannonside Hospital Group")


def write_uptime(w, target, rng):
    path = os.path.join(target, "ehr_integration_uptime_2026.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.title = "Uptime"
    xl_header(ws, ["Month", "Site", "Scheduled minutes", "Unplanned downtime (min)", "Availability"], [10, 7, 18, 24, 12])
    for t in range(W.mi(2026, 1), W.mi(2026, 12) + 1):
        y, m = ym(t)
        days = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.date(y, m, 1)).days
        for h in W.CODES:
            down = int(rng.exponential(55))
            ws.append(["%04d-%02d" % (y, m), h, days * 1440, down, 1 - down / (days * 1440)])
            ws.cell(ws.max_row, 5).number_format = "0.000%"
    wb.save(path)
    PP.normalize_ooxml(path, "Pearce Stapleton", "Pearce Stapleton", "2026-02-02T09:00:00Z", "2027-01-05T12:13:00Z",
                       title="EHR integration uptime 2026", excel=True, company="Shannonside Hospital Group")


def write_all(w, target):
    rng = np.random.default_rng(W.SEED + 7)
    counts = {}
    counts["audits"] = write_audits(w, target, rng)
    counts["volumes"] = write_volumes(w, target, rng)
    counts["register"] = write_register(w, target, rng)
    write_rollout(w, target)
    write_quarterly(w, target)
    counts["tickets"] = write_tickets(w, target, rng)
    write_microphones(w, target, rng)
    write_uptime(w, target, rng)
    return counts
