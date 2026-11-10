"""Write the pack's data files from the clean tables, with the mess the centre's systems produce: the accounting
export in monthly batches (a job that straddles a month boundary is in both batches, and the August 2026 batch was
appended twice by a re-run of the export), submit and eligible times in UTC beside start and end times in local
time, node lists as compressed ranges, time limits and elapsed times as day-hour strings, states with their
suffixes, job ids that wrapped at MaxJobId; the node event log as sacctmgr prints it, with the operators' own words
and the rows cut by controller restarts; the rack layout; the allocations workbook; the maintenance calendar; the
weekly capacity report; the user directory; and two files the sizing never reads (the storage quota report and the
helpdesk ticket export)."""
import csv
import datetime as dt
import os

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import params as P
import sim
import tables as T

FILES = {
    "sacct": "sacct_gpu_2024-01_2026-11.csv",
    "events": "node_events_sturmvogel_2024-2026.csv",
    "rack": "rack_layout_gpu.csv",
    "alloc": "allocations_gpu_2023-2027.xlsx",
    "maint": "maintenance_calendar_2024-2027.xlsx",
    "report": "gpu_capacity_report_2024-2026.xlsx",
    "users": "user_directory_2026-11.csv",
    "config": "slurm_config_history_sturmvogel.txt",
    "policy": "gpu_allocation_policy_v3.pdf",
    "plan": "gpu_partition_plan_2027.pdf",
    "storage": "storage_quota_report_2026-11.csv",
    "tickets": "helpdesk_tickets_2026.csv",
}
DISTRACTORS = ["storage", "tickets"]
CAT_NAMES = {"FOR": "Forschungsprojekt", "NWG": "Nachwuchsgruppe", "LEH": "Lehre", "KOP": "Kooperation"}
HEAD_FILL = PatternFill("solid", fgColor="DCE3EA")


def utc_str(h):
    return pd.Series(pd.to_datetime(P.T0) + pd.to_timedelta(np.asarray(h, dtype=float), unit="h")).dt.strftime("%Y-%m-%dT%H:%M:%S").values


def local_str(h):
    s = pd.Series(pd.to_datetime(P.T0) + pd.to_timedelta(np.asarray(h, dtype=float), unit="h")).dt.tz_convert(P.TZ)
    return s.dt.strftime("%Y-%m-%dT%H:%M:%S").values


def dhms(hours):
    out = []
    for x in np.asarray(hours, dtype=float):
        secs = int(round(x * 3600.0))
        d, r = divmod(secs, 86400)
        hh, r = divmod(r, 3600)
        mm, ss = divmod(r, 60)
        out.append("%d-%02d:%02d:%02d" % (d, hh, mm, ss) if d else "%02d:%02d:%02d" % (hh, mm, ss))
    return out


def node_range(ids):
    """Slurm's compressed form: gpu[003-006,011]"""
    if not ids:
        return "None assigned"
    ids = sorted(ids)
    if len(ids) == 1:
        return T.node_name(ids[0])
    parts = []
    s = p = ids[0]
    for k in ids[1:] + [None]:
        if k is not None and k == p + 1:
            p = k
            continue
        parts.append("%03d" % (s + 1) if s == p else "%03d-%03d" % (s + 1, p + 1))
        if k is not None:
            s = p = k
    return "gpu[%s]" % ",".join(parts)


def month_edges(first, last):
    out = []
    y, m = first.year, first.month
    while (y, m) <= (last.year, last.month):
        a = sim.hrs(dt.datetime(y, m, 1, tzinfo=P.TZ))
        y2, m2 = (y + 1, 1) if m == 12 else (y, m + 1)
        b = sim.hrs(dt.datetime(y2, m2, 1, tzinfo=P.TZ))
        out.append(((y, m), a, b))
        y, m = y2, m2
    return out


def write_sacct(pk, path):
    jobs = pk.jobs
    seg = pk.seg
    # one row per segment, plus the jobs without a segment (pending, cancelled before start)
    seg_rows = seg.merge(jobs[["jobid", "epoch", "name", "user", "account", "qos", "nodes", "wall_h", "submit_h",
                              "elig_h", "state", "restarts", "kill_uid"]], on=["jobid", "epoch"], how="left",
                         suffixes=("", "_job"))
    seg_rows["is_last"] = seg_rows["seg"] == seg_rows["restarts"]
    rows = pd.DataFrame({
        "JobID": seg_rows["jobid"], "JobName": seg_rows["name"], "User": seg_rows["user"], "Account": seg_rows["account"],
        "Partition": P.PARTITION, "QOS": seg_rows["qos"], "State": seg_rows["state"],
        "ReqNodes": seg_rows["nodes_job"], "NodeList": [node_range(x) for x in seg_rows["node_ids"]],
        "Submit_UTC": utc_str(seg_rows["submit_h"]), "Eligible_UTC": utc_str(seg_rows["elig_h"]),
        "Start_local": local_str(seg_rows["start_h"]),
        "End_local": np.where(seg_rows["end_h_cut"].isna(), "Unknown", local_str(seg_rows["end_h_cut"].fillna(0.0))),
        "Elapsed": dhms(seg_rows["elapsed_h"]), "Timelimit": dhms(seg_rows["wall_h"]), "Restarts": seg_rows["seg"],
        "submit_h": seg_rows["submit_h"], "end_h": seg_rows["end_h_cut"], "kill_uid": seg_rows["kill_uid"],
    })
    nos = jobs[jobs["nseg"] == 0]
    uid = {u: v["uid"] for u, v in pk.users.items()}
    rows2 = pd.DataFrame({
        "JobID": nos["jobid"], "JobName": nos["name"], "User": nos["user"], "Account": nos["account"],
        "Partition": P.PARTITION, "QOS": nos["qos"], "State": nos["state"], "ReqNodes": nos["nodes"],
        "NodeList": "None assigned", "Submit_UTC": utc_str(nos["submit_h"]), "Eligible_UTC": utc_str(nos["elig_h"]),
        "Start_local": np.where(nos["state"] == "PENDING", "Unknown", "None"),
        "End_local": np.where(nos["end_h"].isna(), "Unknown", local_str(nos["end_h"].fillna(0.0))),
        "Elapsed": "00:00:00", "Timelimit": dhms(nos["wall_h"]), "Restarts": 0,
        "submit_h": nos["submit_h"], "end_h": nos["end_h"], "kill_uid": [uid.get(u, 0) for u in nos["user"]],
    })
    allrows = pd.concat([rows, rows2], ignore_index=True)
    # states as the scheduler writes them
    st = allrows["State"].values.astype(object)
    uids = np.array([uid.get(u, 0) for u in allrows["User"].values])
    st = np.where(st == "CANCELLED", np.char.add("CANCELLED by ", uids.astype(str)), st)
    allrows["State"] = st
    ex = np.select([allrows["State"] == "COMPLETED", allrows["State"] == "FAILED", allrows["State"] == "TIMEOUT",
                    allrows["State"].str.startswith("CANCELLED"), allrows["State"] == "NODE_FAIL"],
                   ["0:0", "1:0", "0:0", "0:15", "0:0"], default="0:0")
    allrows["ExitCode"] = ex
    cols = ["JobID", "JobName", "User", "Account", "Partition", "QOS", "State", "ExitCode", "ReqNodes", "NodeList",
            "Submit_UTC", "Eligible_UTC", "Start_local", "End_local", "Elapsed", "Timelimit", "Restarts"]
    # monthly batches: a job is in the batch of every month it was in the system; August 2026 appended twice
    batches = month_edges(dt.date(2024, 1, 1), P.CUT_DATE)
    order = [b for b in batches]
    aug = next(b for b in batches if b[0] == (2026, 8))
    order.insert(order.index(next(b for b in batches if b[0] == (2026, 10))), aug)
    sub = allrows["submit_h"].values
    # a job is in a month's batch when it was in the system during the month: submitted before the month's end
    # and not yet finished (every one of its rows) at the month's start
    key = list(zip(allrows["JobID"].values, allrows["Submit_UTC"].values))
    fin = pd.Series(allrows["end_h"].fillna(pk.cut_h + 1).values).groupby(pd.Series(key)).transform("max").values
    end = fin
    out = []
    for (ym, a, b) in order:
        m = (sub < b) & (end >= a)
        part = allrows[m].sort_values(["JobID", "Restarts"], kind="stable")
        out.append(part[cols])
    df = pd.concat(out, ignore_index=True)
    df.to_csv(path, index=False, lineterminator="\n")
    return len(df)


def write_events(pk, path):
    ev = pk.events.copy()
    ev = ev.sort_values(["start_h", "node"], kind="stable")
    df = pd.DataFrame({"Cluster": P.CLUSTER, "NodeName": [T.node_name(n) for n in ev["node"].values],
                       "TimeStart": local_str(ev["start_h"]),
                       "TimeEnd": np.where(ev["end_h"].isna(), "Unknown", local_str(ev["end_h"].fillna(0.0))),
                       "State": ev["state"].values, "Reason": ev["reason"].values, "User": ev["user"].values})
    df.to_csv(path, index=False, lineterminator="\n")
    return len(df)


def write_rack(pk, path):
    r = pk.rack
    rows = []
    for i in range(len(r)):
        rows.append({"node": r["name"][i], "rack": "r%02d" % r["rack"][i], "position": "U%02d" % (4 + 3 * (i % 8)),
                     "leaf_switch": r["switch"][i], "pdu": r["pdu"][i],
                     "in_service_from": sim.local(r["in_service_h"][i]).strftime("%Y-%m-%d") if r["in_service_h"][i] > 0 else "2023-02-06"})
    pd.DataFrame(rows).to_csv(path, index=False, lineterminator="\n")


def _head(ws, row=1):
    for c in ws[row]:
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")


def write_alloc(pk, path, w):
    wb = Workbook()
    ws = wb.active
    ws.title = "Grants 2023-2026"
    ws.append(["project_id", "title", "category", "university", "institute", "pi", "round", "requested_nh",
               "granted_nh", "valid_from", "valid_to"])
    _head(ws)
    g = pk.grants.sort_values(["year", "project"])
    rng = T.rng_for(w.seed, "alloc-order")
    # the committee's workbook lists each round in the order requests were logged, not alphabetically
    for year in sorted(g["year"].unique()):
        part = g[g["year"] == year]
        idx = rng.permutation(len(part))
        for k in idx:
            r = part.iloc[k]
            pr = pk.projects[r["project"]]
            ws.append([r["project"], pr["title"], r["category"], pr["university"], pr["institute"],
                       pk.users[pr["pi"]]["name"], int(r["year"]), int(r["requested"]), int(r["granted"]),
                       dt.date(int(r["year"]), 1, 1), dt.date(int(r["year"]), 12, 31)])
    for i, wd in enumerate([10, 46, 10, 30, 36, 22, 7, 13, 12, 12, 12], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    for row in ws.iter_rows(min_row=2, min_col=10, max_col=11):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    ws.freeze_panes = "A2"
    ws2 = wb.create_sheet("Requests 2027")
    ws2.append(["project_id", "title", "category", "university", "institute", "pi", "standing", "requested_nh",
                "submitted"])
    _head(ws2)
    rq = pk.requests
    sub_dates = {r["project"]: r["submitted"] for r in w.requests}
    idx = rng.permutation(len(rq))
    for k in idx:
        r = rq.iloc[k]
        pr = pk.projects[r["project"]]
        ws2.append([r["project"], pr["title"], r["category"], pr["university"], pr["institute"],
                    pk.users[pr["pi"]]["name"], "new" if r["new"] else "continuing", int(r["requested"]),
                    sub_dates[r["project"]]])
    for i, wd in enumerate([10, 46, 10, 30, 36, 22, 11, 13, 12], 1):
        ws2.column_dimensions[get_column_letter(i)].width = wd
    for row in ws2.iter_rows(min_row=2, min_col=9, max_col=9):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    ws2.freeze_panes = "A2"
    ws3 = wb.create_sheet("Categories")
    ws3.append(["code", "category"])
    _head(ws3)
    for c in P.CATEGORIES:
        ws3.append([c, CAT_NAMES[c]])
    ws3.column_dimensions["A"].width = 8
    ws3.column_dimensions["B"].width = 22
    wb.save(path)


SCOPES = ["Firmware, driver update", "Cooling loop, leaf switch firmware", "Driver and CUDA update", "Kernel update",
          "Lustre client update", "Slurm update", "PDU firmware", "Fabric manager update", "BIOS update",
          "Security patches", "Switch firmware", "Rack power work"]


def write_maint(pk, path, w):
    wb = Workbook()
    ws = wb.active
    ws.title = "Windows"
    ws.append(["date", "start", "end", "hours", "scope", "status"])
    _head(ws)
    rng = T.rng_for(w.seed, "maint-scope")
    for i, m in enumerate(w.maint):
        if m["month"] < dt.date(2024, 1, 1):
            continue
        a, b = sim.local(m["start"]), sim.local(m["end"])
        scope = "Cooling loop, leaf switch firmware" if m["kind"] == "long" else SCOPES[rng.integers(len(SCOPES))]
        status = "done" if m["end"] < pk.cut_h else "planned"
        ws.append([a.date(), a.strftime("%H:%M"), b.strftime("%H:%M") if a.date() == b.date() else b.strftime("%Y-%m-%d %H:%M"),
                   round(m["end"] - m["start"], 1), scope, status])
    for i, wd in enumerate([12, 8, 18, 8, 36, 9], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    for row in ws.iter_rows(min_row=2, min_col=1, max_col=1):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    ws.freeze_panes = "A2"
    wb.save(path)


def write_report(pk, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Weekly"
    ws.append(["gpu partition capacity report: weeks from 1 January 2024 to 15 November 2026. Queue waits per "
               "allocation policy 2.1 and 2.2 (the jobs that became eligible in the week); node-days lost outside "
               "maintenance windows; node-hours delivered are the hours the partition's nodes ran jobs in the week. "
               "Refreshed 16 November 2026, HPC systems group."])
    ws.append([])
    ws.append(["week_start", "nodes_in_service", "utilisation", "node_hours_delivered", "jobs_started", "p50_wait_h",
               "p90_wait_h", "node_days_lost"])
    _head(ws, 3)
    for r in pk.report["weekly"].to_dict("records"):
        ws.append([r["week"], r["nodes"], r["utilisation"], r["delivered_nh"], int(r["jobs_started"]), r["p50_wait_h"],
                   r["p90_wait_h"], r["lost_node_days"]])
    for i, wd in enumerate([12, 10, 11, 14, 11, 11, 11, 13], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    for row in ws.iter_rows(min_row=4, min_col=1, max_col=1):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    for row in ws.iter_rows(min_row=4, min_col=3, max_col=3):
        for c in row:
            c.number_format = "0.0%"
    ws.freeze_panes = "A4"
    ws2 = wb.create_sheet("Quarterly")
    ws2.append(["quarter", "nodes_in_service", "node_hours_delivered", "utilisation", "p50_wait_h", "p90_wait_h",
                "node_days_lost"])
    _head(ws2)
    for r in pk.report["quarterly"].to_dict("records"):
        ws2.append([r["quarter"], r["nodes"], r["delivered_nh"], r["utilisation"], r["p50_wait_h"], r["p90_wait_h"],
                    r["lost_node_days"]])
    for i, wd in enumerate([10, 10, 14, 11, 11, 11, 13], 1):
        ws2.column_dimensions[get_column_letter(i)].width = wd
    for row in ws2.iter_rows(min_row=2, min_col=4, max_col=4):
        for c in row:
            c.number_format = "0.0%"
    wb.save(path)


def write_users(pk, path, w):
    rows = []
    rng = T.rng_for(w.seed, "users-created")
    for u, v in pk.users.items():
        first = min([pk.projects[p]["first_year"] for p in v["projects"]] or [2023])
        created = dt.date(first, 1, 1) - dt.timedelta(days=int(rng.integers(5, 60)))
        rows.append({"username": u, "uid": v["uid"], "name": v["name"], "university": v["university"],
                     "institute": v["institute"], "projects": ";".join(v["projects"]),
                     "created": created.strftime("%Y-%m-%d")})
    df = pd.DataFrame(rows)
    df = df.iloc[rng.permutation(len(df))]
    df.to_csv(path, index=False, lineterminator="\n")


def write_storage(pk, path, w):
    rng = T.rng_for(w.seed, "storage")
    rows = []
    for pid, pr in pk.projects.items():
        if pr["first_year"] > 2026:
            continue
        active = any(int(y) == 2026 for y in pk.grants[pk.grants["project"] == pid]["year"])
        if not active and rng.uniform() < 0.6:
            continue
        for fs, qmed in (("project", 20.0), ("scratch", 50.0)):
            quota = float(np.round(sim.lognormal_median(rng, qmed, 0.5) / 5.0) * 5.0)
            used = float(min(quota * rng.beta(2.0, 2.2), quota))
            rows.append({"project_id": pid, "filesystem": fs, "quota_tb": quota, "used_tb": round(used, 2),
                         "files_millions": round(float(sim.lognormal_median(rng, 2.0, 1.0)), 2),
                         "last_scan": (P.CUT_DATE - dt.timedelta(days=int(rng.integers(0, 3)))).strftime("%Y-%m-%d")})
    pd.DataFrame(rows).to_csv(path, index=False, lineterminator="\n")


TICKET_SUBJECTS = [("access", "Zugang zum Cluster für neue Mitarbeiterin"), ("access", "SSH key rotation"),
                   ("software", "Module for PyTorch 2.6 missing"), ("software", "CUDA 12.8 toolchain request"),
                   ("software", "conda environment broken after update"), ("storage", "quota increase for scratch"),
                   ("storage", "restore deleted directory"), ("jobs", "job stuck in pending with Priority"),
                   ("jobs", "sbatch: error: Batch job submission failed: Job violates accounting/QOS policy"),
                   ("jobs", "how to request more walltime"), ("jobs", "array jobs limit"),
                   ("account", "project renewal paperwork"), ("account", "add user to project"),
                   ("network", "slow transfer from campus"), ("software", "container runtime permission denied"),
                   ("jobs", "NCCL timeout on 8 nodes"), ("storage", "project space 100% full")]


def write_tickets(pk, path, w):
    rng = T.rng_for(w.seed, "tickets")
    users = list(pk.users)
    rows = []
    tid = 44000 + int(rng.integers(0, 500))
    t = sim.hrs(dt.datetime(2026, 1, 2, tzinfo=P.TZ))
    while t < pk.cut_h:
        t += rng.exponential(9.0)
        l = sim.local(t)
        if l.weekday() >= 5 or not (8 <= l.hour <= 18):
            continue
        u = users[rng.integers(len(users))]
        pr = pk.users[u]["projects"]
        cat, subj = TICKET_SUBJECTS[rng.integers(len(TICKET_SUBJECTS))]
        tid += int(rng.integers(1, 4))
        closed = t + float(sim.lognormal_median(rng, 30.0, 1.1))
        rows.append({"ticket": "RT-%d" % tid, "opened": l.strftime("%Y-%m-%d %H:%M"),
                     "closed": sim.local(closed).strftime("%Y-%m-%d %H:%M") if closed < pk.cut_h else "",
                     "user": u, "project_id": pr[rng.integers(len(pr))] if pr else "", "category": cat,
                     "subject": subj, "status": "resolved" if closed < pk.cut_h else "open",
                     "queue": "hpc-support" if cat != "account" else "accounts"})
    pd.DataFrame(rows).to_csv(path, index=False, lineterminator="\n")


def write_tables(pk, w, target):
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    n = {}
    n["sacct"] = write_sacct(pk, F["sacct"])
    n["events"] = write_events(pk, F["events"])
    write_rack(pk, F["rack"])
    write_alloc(pk, F["alloc"], w)
    write_maint(pk, F["maint"], w)
    write_report(pk, F["report"])
    write_users(pk, F["users"], w)
    write_storage(pk, F["storage"], w)
    write_tickets(pk, F["tickets"], w)
    return n
