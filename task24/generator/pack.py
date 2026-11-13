"""task24: the pack's records, written as each of Pellucid Annotation's systems exports them (the labelling tool's
task passes, the QA system's reviews, the punch clock, payroll's register, HR's roster, the project register, the
video delivery archive), the clients' sample labels as their previous vendors delivered them, and two side files the
operations team keeps. Layer 1 mess comes from each system's own behaviour: sync retries, released tasks, double
taps, shifts auto-closed at midnight and edited the next day, a voided payroll run, the QA system's own staff keys."""
import datetime as dt
import json
import math
import os
import sqlite3

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Font

import postprocess as PP
import world as Wd

FIRM = "Pellucid Annotation Ltd"
TZ = {"KSM": dt.timezone(dt.timedelta(hours=3)), "ILO": dt.timezone(dt.timedelta(hours=8))}
F = dict(passes="pellucid_task_passes_2026-04-06_2026-11-01.csv", reviews="qa_reviews_2026-04-06_2026-11-01.csv",
         punch="punch_clock_2026-04-06_2026-11-01.csv", pay="pay_register_2026_apr_oct.xlsx",
         roster="staff_roster_2026-11-06.xlsx", projects="project_register_2026.csv",
         archive="video_delivery_archive_2026.sqlite", survey="pulse_survey_2026_q2_q3.csv",
         gpu="prelabel_gpu_usage_2026.csv")
SAMPLES = {"A": "vantorra_VTA-2027-014_preview_labels.json", "B": "shelfgrid_SG27-03_preview_labels.json",
           "C": "ardley_HWY-Q1-27_preview_sequences.json", "D": "brindle_BPS-2027-02_preview_labels.json",
           "E": "kestrin_KW-2701_preview_labels.json"}


def save_xlsx(wb, path, creator, created, modified):
    wb.save(path)
    PP.normalize_ooxml(path, creator, creator, created, modified, excel=True, company=FIRM)


def head(ws, cols, widths=None):
    ws.append(cols)
    for c in ws[1]:
        c.font = Font(bold=True)
    if widths:
        for i, wdt in enumerate(widths):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wdt


def iso(t):
    return t.isoformat(timespec="seconds")


# ------------------------------------------------------------------ shifts and the punch clock
def shifts(T):
    """One shift per worked day for every annotator and reviewer: start, lunch (unpaid), end, in local time."""
    rng = Wd.rng_for("shifts")
    rows = []
    for _, w in T["WK"].iterrows():
        days = w.workdays
        mins = int(round(w.paid_hours * 60))
        per = np.full(len(days), mins // len(days))
        per[: mins - per.sum()] += 1
        lunch = Wd.CENTRES[w.centre]["lunch_min"]
        for d, m in zip(days, per):
            st = dt.datetime(d.year, d.month, d.day, 7, 30, tzinfo=TZ[w.centre]) + dt.timedelta(minutes=int(rng.integers(0, 66)))
            rows.append(dict(staff_id=w.annotator_id, site=w.centre, day=d, start=st, paid_min=int(m), lunch_min=lunch,
                             role="annotator", week=w.week))
    rev = T["rev"]
    for _, r in rev.iterrows():
        cfg = Wd.CENTRES[r.centre]
        for wk in range(Wd.NWEEKS):
            mon = Wd.WEEK0 + dt.timedelta(days=7 * wk)
            for k in range(5):
                d = mon + dt.timedelta(days=k)
                if d in cfg["holidays"] or rng.random() < 0.04:
                    continue
                st = dt.datetime(d.year, d.month, d.day, 7, 45, tzinfo=TZ[r.centre]) + dt.timedelta(minutes=int(rng.integers(0, 40)))
                rows.append(dict(staff_id=r.reviewer_id, site=r.centre, day=d, start=st,
                                 paid_min=int(8 * 60 + rng.integers(-12, 13)), lunch_min=cfg["lunch_min"], role="reviewer", week=wk))
    return pd.DataFrame(rows)


def punch_rows(S):
    rng = Wd.rng_for("punch")
    out = []
    for _, s in S.iterrows():
        end = s.start + dt.timedelta(minutes=int(s.paid_min + s.lunch_min))
        src = "BADGE" if rng.random() < 0.93 else "WEB"
        out.append((s.staff_id, s.site, iso(s.start), "IN", src, ""))
        if rng.random() < 0.012:      # a double tap on the reader
            out.append((s.staff_id, s.site, iso(s.start + dt.timedelta(seconds=int(rng.integers(20, 140)))), "IN", src, ""))
        if rng.random() < 0.011:      # forgot to clock out: the clock closes the shift at midnight, a supervisor edits it
            mid = dt.datetime(s.day.year, s.day.month, s.day.day, 23, 59, tzinfo=end.tzinfo)
            out.append((s.staff_id, s.site, iso(mid), "OUT", "AUTO_CLOSE", "shift closed by system"))
            nxt = mid + dt.timedelta(hours=int(rng.integers(9, 14)), minutes=int(rng.integers(0, 50)))
            out.append((s.staff_id, s.site, iso(end), "OUT", "SUPERVISOR_EDIT",
                        "edit %s: out time per team lead" % nxt.strftime("%Y-%m-%d")))
        else:
            out.append((s.staff_id, s.site, iso(end), "OUT", src, ""))
    df = pd.DataFrame(out, columns=["staff_id", "site", "punch_local", "direction", "source", "note"])
    return df


# ------------------------------------------------------------------ the tool's task passes and QA's reviews
def stamp_passes(T, S):
    """Place each annotator-week's passes in its shifts in recorded order; each pass takes its tool time plus the
    worker's own idle share of wall time. Reviews land on a reviewer's next shift after submission."""
    P, R = T["P"].copy(), T["R"].copy()
    ann = T["ann"].set_index("annotator_id")
    rng = Wd.rng_for("stamps")
    sh = S[S.role == "annotator"].sort_values(["staff_id", "start"])
    by = {k: g for k, g in sh.groupby(["staff_id", "week"])}
    opened = np.empty(len(P), dtype=object); submitted = np.empty(len(P), dtype=object)
    for (a, w), g in P.groupby(["annotator_id", "week"], sort=False):
        days = by.get((a, w))
        if days is None:
            continue
        prod = ann.loc[a, "productive"]
        slots = [(r.start, r.start + dt.timedelta(minutes=int(r.paid_min + r.lunch_min)), r.lunch_min) for r in days.itertuples()]
        si = 0
        cur = slots[0][0]
        for idx, sec in zip(g.index, g.active_seconds.to_numpy()):
            wall = sec / prod * math.exp(rng.normal(0, 0.08))
            st, en, lm = slots[si]
            lunch_at = st + dt.timedelta(hours=4)
            if cur < lunch_at <= cur + dt.timedelta(seconds=wall):
                cur = cur + dt.timedelta(minutes=lm)
            if cur + dt.timedelta(seconds=wall) > en and si < len(slots) - 1:
                si += 1
                cur = slots[si][0]
            opened[idx] = cur
            cur = cur + dt.timedelta(seconds=wall)
            submitted[idx] = cur
    P["opened"] = opened; P["submitted"] = submitted
    # reviews: each on its reviewer's first shift after the submission
    rv = S[S.role == "reviewer"].sort_values("start")
    rv_starts = {k: (g.start.to_numpy(), g.paid_min.to_numpy()) for k, g in rv.groupby("staff_id")}
    rtime = np.empty(len(R), dtype=object)
    sub = P.set_index("pass_key").submitted
    for i, (pk, rid) in enumerate(zip(R.pass_key.to_numpy(), R.reviewer_id.to_numpy())):
        t = sub.get(pk)
        if t is None:
            continue
        starts, pm = rv_starts[rid]
        t_utc = t.astimezone(dt.timezone.utc) + dt.timedelta(minutes=int(rng.integers(20, 300)))
        j = int(np.searchsorted([s.astimezone(dt.timezone.utc) for s in starts[-0:]], t_utc)) if False else None
        k = 0
        for k in range(len(starts)):
            e = starts[k] + dt.timedelta(minutes=int(pm[k]))
            if e.astimezone(dt.timezone.utc) > t_utc:
                break
        st = max(starts[k].astimezone(dt.timezone.utc), t_utc)
        rtime[i] = st + dt.timedelta(minutes=int(rng.integers(0, 120)))
    R["reviewed_at"] = rtime
    return P, R


def passes_frame(T, P):
    rng = Wd.rng_for("passes_out")
    proj = T["proj"].set_index("project")
    vch = T["vchunks"]
    key2item = {}
    rows = []
    serial = 5100000
    item_no = {}
    for r in P.itertuples():
        serial += int(rng.integers(1, 4))
        key2item.setdefault(r.pass_key, serial)
        if r.kind == "video":
            c = vch.iloc[int(r.chunk_key)]
            ref = "SEQ-%s-%03d/%04d-%04d" % (r.project[4:], int(c.seq), int(c.frame_from), int(c.frame_to))
        else:
            if r.item not in item_no:
                item_no[r.item] = "IMG-%s-%06d" % (r.project[4:], len(item_no) + 100000 + int(rng.integers(0, 7)))
            ref = item_no[r.item]
        rows.append((serial, r.item, r.pass_no, ref, r.project, r.annotator_id, r.kind, r))
    return rows


def write_passes(T, P, path):
    """The tool's export: one row per pass; corrections carry their parent pass."""
    rng = Wd.rng_for("passes_csv")
    vch = T["vchunks"]
    P = P.sort_values(["opened"], kind="stable").reset_index(drop=True) if False else P
    ids = {}
    last_pass_of_item = {}
    out = []
    serial = 5100003
    refs = {}
    for r in P.itertuples():
        serial += int(rng.integers(1, 5))
        pid = "TP%07d" % serial
        ids[r.pass_key] = pid
        parent = last_pass_of_item.get(r.item, "") if r.pass_no > 1 else ""
        last_pass_of_item[r.item] = pid
        if r.kind == "video":
            c = vch.iloc[int(r.chunk_key)]
            ref = "SEQ-%s-%03d/%04d-%04d" % (r.project[4:], int(c.seq) + 1, int(c.frame_from), int(c.frame_to))
            counts = dict(frames=int(c.frames), boxes_on_screen=int(c.frame_objects))
        else:
            if r.item not in refs:
                refs[r.item] = "IMG-%s-%06d" % (r.project[4:], 200000 + len(refs) * 3 + int(rng.integers(0, 3)))
            ref = refs[r.item]
            if r.kind == "box":
                counts = dict(obj_small=int(r.n_S_clr), obj_small_occl=int(r.n_S_occ), obj_medium=int(r.n_M_clr),
                              obj_medium_occl=int(r.n_M_occ), obj_large=int(r.n_L_clr), obj_large_occl=int(r.n_L_occ))
            else:
                counts = dict(polygons=int(r.n_poly - r.n_poly_occ), polygons_occl=int(r.n_poly_occ), vertices=int(r.vertices))
        site = r.annotator_id[:3]
        row = dict(pass_id=pid, parent_pass_id=parent, project_code=r.project, item_ref=ref, annotator_id=r.annotator_id,
                   pass_type="annotate" if r.pass_no == 1 else "correct", opened_at=iso(r.opened), submitted_at=iso(r.submitted),
                   tool_active_s=int(round(r.active_seconds)))
        row.update(counts)
        out.append(row)
        if rng.random() < 0.0016:                 # the tool's sync retry writes the row twice
            out.append(dict(row))
        if rng.random() < 0.004 and r.pass_no == 1:   # a task opened and released before work began
            serial += 1
            rel = dict(row, pass_id="TP%07d" % serial, pass_type="released", submitted_at="",
                       tool_active_s=int(rng.integers(8, 140)))
            out.append(rel)
    cols = ["pass_id", "parent_pass_id", "project_code", "item_ref", "annotator_id", "pass_type", "opened_at",
            "submitted_at", "tool_active_s", "obj_small", "obj_small_occl", "obj_medium", "obj_medium_occl", "obj_large",
            "obj_large_occl", "polygons", "polygons_occl", "vertices", "frames", "boxes_on_screen"]
    df = pd.DataFrame(out).reindex(columns=cols)
    for c in cols[9:]:
        df[c] = df[c].astype("Int64")
    df.to_csv(path, index=False)
    return ids


def write_reviews(T, R, ids, path):
    rng = Wd.rng_for("reviews_csv")
    rows = []
    serial = 880000
    for r in R.itertuples():
        serial += int(rng.integers(1, 3))
        rid = r.reviewer_id
        if rid.startswith("ILO"):
            rid = rid.replace("-", "")            # the Iloilo QA desk's own staff keys
        found = int(r.found_missed) + int(r.found_misplaced)
        note = ""
        if found and rng.random() < 0.18:
            bits = []
            if r.found_missed:
                bits.append("missed %d" % r.found_missed)
            if r.found_misplaced:
                bits.append("box off %d" % r.found_misplaced)
            note = "; ".join(bits)
        rows.append(dict(review_id="QR%07d" % serial, pass_id=ids[r.pass_key], reviewer_id=rid,
                         reviewed_at_utc=r.reviewed_at.strftime("%Y-%m-%dT%H:%M:%SZ"), review_s=int(round(r.seconds)),
                         decision="RETURN" if found and r.pass_no < 4 else "ACCEPT", missed=int(r.found_missed),
                         misplaced=int(r.found_misplaced), comment=note))
    pd.DataFrame(rows).to_csv(path, index=False)


# ------------------------------------------------------------------ payroll, roster, register, archive
def pay_register(T, S, P, path, stamp):
    """Annotator weeks settled as the 2026 pay policy files: piece pay on first submissions credited to the pay
    week of submission, paid hours from the clock, the floor topped up per annotator per pay week."""
    rng = Wd.rng_for("payroll")
    sh = S.copy()
    sh["paid_h"] = sh.paid_min / 60.0
    hrs = sh.groupby(["staff_id", "week"]).paid_h.sum()
    first = P[P.pass_no == 1].copy()
    first["week"] = [((s.date() - Wd.WEEK0).days // 7) for s in first.submitted]
    vch = T["vchunks"]
    first["frames"] = np.where(first.kind == "video", vch.frames.reindex(first.chunk_key.fillna(0).astype(int)).to_numpy(), 0)
    u = first.assign(box=np.where(first.kind == "box", first.nobj, 0), poly=np.where(first.kind == "polygon", first.nobj, 0),
                     track=np.where(first.kind == "video", first.nobj, 0))
    units = u.groupby(["annotator_id", "week"])[["box", "poly", "track", "frames"]].sum()
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "annotator weeks"
    head(ws, ["run_id", "staff_id", "site", "week_start", "paid_hours", "boxes_paid", "polygons_paid", "tracks_paid",
              "frames_paid", "piece_pay_usd", "floor_topup_usd", "transport_allowance_usd", "adjustment_usd", "gross_usd"],
         [10, 13, 6, 12, 10, 10, 12, 10, 10, 12, 13, 14, 12, 11])
    lines = []
    for (a, w), h in hrs.items():
        if not a.split("-")[1].startswith("A"):
            continue
        site = a[:3]
        un = units.loc[(a, w)] if (a, w) in units.index else pd.Series(dict(box=0, poly=0, track=0, frames=0))
        piece = round(un.box * Wd.RATES["box"] + un.poly * Wd.RATES["polygon"] + un.track * Wd.RATES["track"] +
                      un.frames * Wd.RATES["frame"], 2)
        top = round(max(0.0, Wd.CENTRES[site]["floor"] * round(h, 2) - piece), 2)
        allow = Wd.CENTRES[site]["allowance"]
        adj = 0.0
        if rng.random() < 0.03:
            adj = float(rng.choice([5.0, 7.5, -2.5, 10.0]))
        lines.append(["PR-%02d" % (w + 1), a, site, (Wd.WEEK0 + dt.timedelta(days=7 * w)).isoformat(), round(h, 2), int(un.box),
                      int(un.poly), int(un.track), int(un.frames), piece, top, allow, adj, round(piece + top + allow + adj, 2)])
    lines.sort(key=lambda x: (x[3], x[1]))
    void_week = (Wd.WEEK0 + dt.timedelta(days=7 * 9)).isoformat()
    out = []
    for ln in lines:
        out.append(ln)
    dup = [ln for ln in lines if ln[3] == void_week]
    for ln in dup:                                   # the week paid twice by a re-run, then voided
        out.append(["PR-10B"] + ln[1:])
    for ln in dup:
        out.append(["PR-10B-VOID"] + ln[1:4] + [-ln[4], -ln[5], -ln[6], -ln[7], -ln[8], -ln[9], -ln[10], -ln[11], -ln[12], -ln[13]])
    for ln in out:
        ws.append(ln)
    ws2 = wb.create_sheet("reviewer weeks")
    head(ws2, ["run_id", "staff_id", "site", "week_start", "paid_hours", "hourly_rate_usd", "pay_usd", "allowance_usd",
               "gross_usd"], [10, 13, 6, 12, 10, 14, 10, 13, 11])
    rlines = []
    for (a, w), h in hrs.items():
        if not a.split("-")[1].startswith("Q"):
            continue
        site = a[:3]
        rate = Wd.CENTRES[site]["rev_rate"]
        pay = round(round(h, 2) * rate, 2)
        allow = Wd.CENTRES[site]["allowance"]
        rlines.append(["PR-%02d" % (w + 1), a, site, (Wd.WEEK0 + dt.timedelta(days=7 * w)).isoformat(), round(h, 2), rate,
                       pay, allow, round(pay + allow, 2)])
    rlines.sort(key=lambda x: (x[3], x[1]))
    for ln in rlines:
        ws2.append(ln)
    ws3 = wb.create_sheet("period totals")
    head(ws3, ["month", "site", "piece_pay_usd", "floor_topup_usd", "reviewer_pay_usd", "allowances_usd",
               "adjustments_usd", "gross_usd"], [9, 6, 13, 14, 15, 13, 14, 12])
    tot = {}
    for ln in out:
        k = (ln[3][:7], ln[2])
        t = tot.setdefault(k, [0.0] * 6)
        t[0] += ln[9]; t[1] += ln[10]; t[3] += ln[11]; t[4] += ln[12]; t[5] += ln[13]
    for ln in rlines:
        k = (ln[3][:7], ln[2])
        t = tot.setdefault(k, [0.0] * 6)
        t[2] += ln[6]; t[3] += ln[7]; t[5] += ln[8]
    for (m, site) in sorted(tot):
        t = tot[(m, site)]
        ws3.append([m, site] + [round(x, 2) for x in t])
    save_xlsx(wb, path, "Chege Ouma", stamp[0], stamp[1])
    return pd.DataFrame(lines, columns=["run_id", "staff_id", "site", "week_start", "paid_hours", "boxes", "polys", "tracks",
                                        "frames", "piece", "topup", "allowance", "adjustment", "gross"])


def roster(T, path, stamp):
    ann, rev = T["ann"], T["rev"]
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "annotators"
    head(ws, ["staff_id", "site", "hire_date", "leave_date", "contract_hours_week", "skills", "grade"],
         [13, 6, 11, 11, 18, 20, 7])
    for a in ann.sort_values("annotator_id").itertuples():
        grade = "A2" if a.hire_date < dt.date(2025, 1, 1) else "A1"
        if a.hire_date < dt.date(2023, 6, 1):
            grade = "A3"
        ws.append([a.annotator_id, a.centre, a.hire_date.isoformat(), a.left_date.isoformat() if a.left_date else "",
                   int(a.scheduled_hours), ";".join(a.skills), grade])
    ws2 = wb.create_sheet("qa reviewers")
    head(ws2, ["staff_id", "site", "hire_date", "contract_hours_week", "hourly_rate_usd"], [13, 6, 11, 18, 14])
    rng = Wd.rng_for("rev_hire")
    for r in rev.sort_values("reviewer_id").itertuples():
        ws2.append([r.reviewer_id, r.centre, (dt.date(2024, 1, 15) + dt.timedelta(days=int(rng.integers(0, 600)))).isoformat(),
                    int(r.scheduled_hours), Wd.CENTRES[r.centre]["rev_rate"]])
    save_xlsx(wb, path, "Mourine Kipngetich", stamp[0], stamp[1])


def project_register(T, P, R, path):
    proj = T["proj"]
    acc = R.drop(columns=["item"], errors="ignore").merge(P[["pass_key", "item", "project"]], on="pass_key")
    acc = acc[(acc.found_missed + acc.found_misplaced == 0) | (acc.pass_no >= 4)]
    delivered = acc.groupby("project").item.nunique()
    vch = T["vchunks"]
    rows = []
    for p in proj.itertuples():
        d0 = Wd.WEEK0 + dt.timedelta(days=7 * p.w0 + int(Wd.rng_for("pd", p.project).integers(0, 3)))
        d1 = Wd.WEEK0 + dt.timedelta(days=7 * p.w1 + 4)
        unit = {"box": "image", "polygon": "image", "video": "frame"}[p.kind]
        n = int(delivered.get(p.project, 0))
        if p.kind == "video":
            keys = P[(P.project == p.project) & (P.pass_no == 1)].chunk_key.dropna().astype(int).unique()
            n = int(vch.iloc[keys].frames.sum())
        rows.append(dict(project_code=p.project, client=p.client,
                         task_type={"box": "bounding boxes", "polygon": "polygon segmentation", "video": "video tracking"}[p.kind],
                         scene=p.scene, start_date=d0.isoformat(), end_date=min(d1, dt.date(2026, 10, 30)).isoformat(),
                         delivered_units=n, unit=unit, rate_card="RC-2026-02"))
    pd.DataFrame(rows).to_csv(path, index=False)


def archive(T, P, path):
    if os.path.exists(path):
        os.remove(path)
    vt = T["vtracks"]
    proj = T["proj"].set_index("project")
    labels = {"urban": ["car", "car", "pedestrian", "cyclist", "bus"], "plaza": ["pedestrian", "pedestrian", "cyclist"],
              "parking": ["car", "car", "van", "pedestrian"], "store": ["person"], "dock": ["truck", "forklift", "person"]}
    rng = Wd.rng_for("archive")
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE sequences (project_code TEXT, sequence_id TEXT, frames INTEGER, fps INTEGER)")
    con.execute("CREATE TABLE tracks (sequence_id TEXT, track_id INTEGER, label TEXT, first_frame INTEGER, last_frame INTEGER)")
    vch = T["vchunks"]
    seqlen = vch.groupby(["project", "seq"]).frame_to.max() + 1
    worked = set(P[P.kind == "video"].project.unique())
    for (pj, sq), F_ in seqlen.items():
        if pj not in worked:
            continue
        sid = "SEQ-%s-%03d" % (pj[4:], int(sq) + 1)
        con.execute("INSERT INTO sequences VALUES (?,?,?,?)", (pj, sid, int(F_), 10))
    rows = []
    for t in vt.itertuples():
        sid = "SEQ-%s-%03d" % (t.project[4:], int(t.seq) + 1)
        lab = labels[proj.loc[t.project, "scene"]]
        rows.append((sid, int(t.track) + 1, lab[int(rng.integers(0, len(lab)))], int(t.first_frame), int(t.last_frame)))
    con.executemany("INSERT INTO tracks VALUES (?,?,?,?,?)", rows)
    con.commit()
    con.execute("VACUUM")
    con.close()


# ------------------------------------------------------------------ the clients' samples
def _boxes(rng, counts, W=1920, H=1080):
    out = []
    for size, lo, hi in (("S", 120, 1023), ("M", 1024, 9215), ("L", 9216, 160000)):
        for occ in (False, True):
            n = int(counts["n_%s_%s" % (size, "occ" if occ else "clr")])
            for _ in range(n):
                area = math.exp(rng.uniform(math.log(lo), math.log(hi)))
                ar = math.exp(rng.normal(0, 0.45))
                w = max(4.0, math.sqrt(area * ar)); h = area / w
                x = rng.uniform(0, W - w); y = rng.uniform(0, H - h)
                out.append((round(x, 1), round(y, 1), round(w, 1), round(h, 1), occ))
    rng.shuffle(out)
    return out


def samples(target, S):
    for key, fn in SAMPLES.items():
        rng = Wd.rng_for("samplejson", key)
        rq = Wd.REQUESTS[key]
        s = S[key]
        if rq["kind"] == "box":
            images, anns, aid = [], [], 1
            dialect = "xyxy" if key == "B" else "xywh"
            for i, row in s.reset_index(drop=True).iterrows():
                images.append(dict(id=i + 1, file_name="%s_%05d.jpg" % (key.lower(), i + 1), width=1920, height=1080))
                for (x, y, w, h, occ) in _boxes(rng, row):
                    if dialect == "xyxy":
                        a = dict(id=aid, image_id=i + 1, category_id=1 + int(rng.integers(0, 4)),
                                 bbox=[x, y, round(x + w, 1), round(y + h, 1)], occlusion=int(occ), iscrowd=0)
                    else:
                        a = dict(id=aid, image_id=i + 1, category_id=1 + int(rng.integers(0, 4)), bbox=[x, y, w, h],
                                 area=round(w * h, 1), attributes={"occluded": bool(occ)}, iscrowd=0)
                    anns.append(a); aid += 1
            doc = dict(info={"description": "%s sample for %s" % (rq["client"], fn.split("_")[1]), "bbox_format": dialect,
                             "sampled_from_full_set": True, "images_in_full_set": rq["volume"]},
                       images=images, annotations=anns,
                       categories=[dict(id=k + 1, name=n) for k, n in enumerate(_cats(rq["scene"]))])
        elif rq["kind"] == "polygon":
            images, anns, aid = [], [], 1
            for i, row in s.reset_index(drop=True).iterrows():
                images.append(dict(id=i + 1, file_name="pallet_%05d.png" % (i + 1), width=2448, height=2048))
                n, no, v = int(row.n_poly), int(row.n_poly_occ), int(row.vertices)
                per = np.maximum(3, rng.multinomial(v - 3 * n, np.ones(n) / n) + 3) if n else []
                for k in range(n):
                    cx, cy, rad = rng.uniform(200, 2200), rng.uniform(200, 1800), rng.uniform(40, 260)
                    ang = np.sort(rng.uniform(0, 2 * math.pi, int(per[k])))
                    pts = []
                    for t_ in ang:
                        rr = rad * math.exp(rng.normal(0, 0.12))
                        pts += [round(cx + rr * math.cos(t_), 1), round(cy + rr * math.sin(t_), 1)]
                    anns.append(dict(id=aid, image_id=i + 1, category_id=1 + int(rng.integers(0, 3)), segmentation=[pts],
                                     attributes={"occluded": bool(k < no)}, iscrowd=0)); aid += 1
            doc = dict(info={"description": "Brindle Pallet Systems sample for BPS-2027-02", "sampled_from_full_set": True,
                             "images_in_full_set": rq["volume"]}, images=images, annotations=anns,
                       categories=[dict(id=1, name="pallet"), dict(id=2, name="wrapped_load"), dict(id=3, name="loose_item")])
        else:
            tr, ch = s
            videos, images, anns = [], [], []
            img_id, aid = 1, 1
            seqlen = ch.groupby("seq").frame_to.max() + 1
            for q, F_ in seqlen.items():
                videos.append(dict(id=int(q) + 1, name="hwy_%03d" % (int(q) + 1), frames=int(F_)))
                t = tr[tr.seq == q]
                fid0 = img_id
                for f in range(int(F_)):
                    images.append(dict(id=img_id, video_id=int(q) + 1, frame_id=f)); img_id += 1
                for r in t.itertuples():
                    x, y = rng.uniform(0, 1700), rng.uniform(300, 900)
                    for f in range(int(r.first_frame), int(r.last_frame) + 1):
                        anns.append(dict(id=aid, image_id=fid0 + f, track_id=int(r.track) + 1, category_id=1,
                                         bbox=[round(x, 1), round(y, 1), 60.0, 40.0])); aid += 1
            doc = dict(info={"description": "Ardley Autonomy highway sample for HWY-Q1-27", "fps": 10,
                             "frames_in_full_set": rq["volume"]}, videos=videos, images=images, annotations=anns,
                       categories=[dict(id=1, name="vehicle")])
        with open(os.path.join(target, fn), "w") as fh:
            json.dump(doc, fh, separators=(",", ":"))


def _cats(scene):
    return {"street": ["car", "pedestrian", "cyclist", "bus"], "retail": ["product", "price_tag", "shelf_gap", "promo"],
            "warehouse": ["label", "barcode", "carton", "pallet_tag"]}[scene]


# ------------------------------------------------------------------ side files (not used by the golden)
def survey(T, path):
    rng = Wd.rng_for("survey")
    rows = []
    for a in T["ann"].itertuples():
        for q in ("2026Q2", "2026Q3"):
            if rng.random() < 0.15:
                continue
            rows.append(dict(staff_id=a.annotator_id, quarter=q, workload_1to5=int(rng.integers(2, 6)),
                             tooling_1to5=int(rng.integers(2, 6)), pay_fairness_1to5=int(rng.integers(1, 6)),
                             would_recommend_0to10=int(rng.integers(3, 11))))
    pd.DataFrame(rows).to_csv(path, index=False)


def gpu(T, path):
    rng = Wd.rng_for("gpu")
    rows = []
    for p in T["proj"].itertuples():
        for w in range(p.w0, p.w1 + 1):
            rows.append(dict(project_code=p.project, week_start=(Wd.WEEK0 + dt.timedelta(days=7 * w)).isoformat(),
                             prelabel_model="pl-det-%s" % ("v7" if w < 15 else "v8"),
                             gpu_hours=round(float(rng.gamma(4, 6 if p.kind != "video" else 14)), 1)))
    pd.DataFrame(rows).to_csv(path, index=False)
