"""Rebuild the clean tables (tables.Pack) from the shipped files alone, the way an analyst would: the accounting
export's batches de-duplicated, its two clocks read as the headers state them, job ids tied to their submission so
the counter's wrap does not merge two jobs, segments gathered under their job, node lists expanded, limits and
elapsed times parsed from Slurm's day-hour strings, states read without their suffixes; the node event log, the
rack layout, the allocations, the maintenance calendar, the capacity report and the configuration history."""
import datetime as dt
import os
import re

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import pack as PK
import params as P
import sim
import tables as T


def parse_dhms(s):
    s = str(s).strip()
    if s in ("", "Unknown", "None", "nan", "UNLIMITED", "Partition_Limit"):
        return np.nan
    d = 0
    if "-" in s:
        d, s = s.split("-", 1)
        d = int(d)
    parts = [int(x) for x in s.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    return d * 24.0 + parts[0] + parts[1] / 60.0 + parts[2] / 3600.0


def utc_hours(series):
    t = pd.to_datetime(series, format="%Y-%m-%dT%H:%M:%S", errors="coerce", utc=True)
    return ((t - pd.Timestamp(P.T0)) / pd.Timedelta(hours=1)).values


def local_hours(series):
    t = pd.to_datetime(series, format="%Y-%m-%dT%H:%M:%S", errors="coerce")
    # naive local stamps: localise with the DST rule, ambiguous autumn hour taken as the first (DST) occurrence
    t = t.dt.tz_localize(P.TZ, ambiguous=np.ones(len(t), dtype=bool), nonexistent="shift_forward")
    return ((t - pd.Timestamp(P.T0)) / pd.Timedelta(hours=1)).values


def expand_nodes(s):
    s = str(s)
    if not s.startswith("gpu"):
        return []
    m = re.match(r"gpu\[(.*)\]$", s)
    if not m:
        return [int(s[3:]) - 1]
    out = []
    for part in m.group(1).split(","):
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a) - 1, int(b)))
        else:
            out.append(int(part) - 1)
    return out


def load_sacct(path, cut_h):
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    raw = raw.drop_duplicates()
    raw["submit_h"] = utc_hours(raw["Submit_UTC"])
    raw["elig_h"] = utc_hours(raw["Eligible_UTC"])
    raw["start_h"] = local_hours(raw["Start_local"].where(~raw["Start_local"].isin(["Unknown", "None"]), None))
    raw["end_h"] = local_hours(raw["End_local"].where(raw["End_local"] != "Unknown", None))
    raw["elapsed_h"] = [parse_dhms(x) for x in raw["Elapsed"]]
    raw["wall_h"] = [parse_dhms(x) for x in raw["Timelimit"]]
    raw["jobid"] = raw["JobID"].astype(int)
    raw["seg"] = raw["Restarts"].astype(int)
    raw["nodes"] = raw["ReqNodes"].astype(int)
    raw["state"] = raw["State"].str.split(" ").str[0]
    raw["kill_uid"] = raw["State"].str.extract(r"by (\d+)")[0].fillna("0").astype(int)
    # the id counter wraps: an id's epoch is the number of wraps before its submission
    raw = raw.sort_values(["submit_h", "jobid", "seg"], kind="stable").reset_index(drop=True)
    first_sub = raw.groupby(["jobid"])["submit_h"].transform("min")
    # two jobs share an id when their submissions are far apart; epoch = rank of the id's distinct submissions
    key = raw.groupby(["jobid", "submit_h"]).ngroup()
    ep = raw.groupby("jobid")["submit_h"].rank(method="dense").astype(int) - 1
    raw["epoch"] = ep.values
    raw["node_ids"] = [expand_nodes(x) for x in raw["NodeList"]]
    seg = raw[raw["state"] != "PENDING"].copy()
    seg = seg[~((seg["start_h"].isna()))].copy()
    seg["running"] = seg["state"] == "RUNNING"
    seg["end_h_cut"] = seg["end_h"]
    seg["nh"] = seg["elapsed_h"] * seg["nodes"]
    seg = seg[["jobid", "epoch", "seg", "start_h", "end_h_cut", "state", "nodes", "node_ids", "elapsed_h", "nh", "running"]]
    seg["end_h"] = seg["end_h_cut"]
    # jobs: one per (jobid, epoch)
    g = raw.groupby(["jobid", "epoch"], sort=False)
    jobs = g.agg(name=("JobName", "first"), user=("User", "first"), account=("Account", "first"), qos=("QOS", "first"),
                 nodes=("nodes", "first"), wall_h=("wall_h", "first"), submit_h=("submit_h", "first"),
                 elig_h=("elig_h", "first"), kill_uid=("kill_uid", "max")).reset_index()
    segs = seg.groupby(["jobid", "epoch"]).agg(start_h=("start_h", "min"), nseg=("seg", "size"), elapsed_h=("elapsed_h", "sum"),
                                              nh=("nh", "sum"), last_state=("state", "last"), end_last=("end_h_cut", "last")).reset_index()
    jobs = jobs.merge(segs, on=["jobid", "epoch"], how="left")
    jobs["nseg"] = jobs["nseg"].fillna(0).astype(int)
    jobs["elapsed_h"] = jobs["elapsed_h"].fillna(0.0)
    jobs["nh"] = jobs["nh"].fillna(0.0)
    nostart = raw[raw["start_h"].isna()].groupby(["jobid", "epoch"]).agg(st=("state", "first"), end=("end_h", "first")).reset_index()
    jobs = jobs.merge(nostart, on=["jobid", "epoch"], how="left")
    jobs["state"] = np.where(jobs["nseg"] > 0, jobs["last_state"], jobs["st"])
    jobs["end_h"] = np.where(jobs["nseg"] > 0, jobs["end_last"], jobs["end"])
    jobs["restarts"] = np.where(jobs["nseg"] > 0, jobs["nseg"] - 1, 0)
    first_nodes = seg[seg["seg"] == 0].set_index(["jobid", "epoch"])["node_ids"]
    jobs["node_ids"] = [first_nodes.get((a, b), []) for a, b in zip(jobs["jobid"], jobs["epoch"])]
    cols = ["jobid", "epoch", "name", "user", "account", "qos", "state", "nodes", "wall_h", "submit_h", "elig_h",
            "start_h", "end_h", "elapsed_h", "nh", "restarts", "nseg", "node_ids", "kill_uid"]
    return jobs[cols].sort_values(["submit_h", "jobid"]).reset_index(drop=True), \
        seg.sort_values(["start_h", "jobid"]).reset_index(drop=True)


def load_events(path, cut_h):
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    ev = pd.DataFrame({"node": [int(n[3:]) - 1 for n in raw["NodeName"]],
                       "start_h": local_hours(raw["TimeStart"]),
                       "end_h": local_hours(raw["TimeEnd"].where(raw["TimeEnd"] != "Unknown", None)),
                       "state": raw["State"].values, "reason": raw["Reason"].values, "user": raw["User"].values})
    low = ev["reason"].str.lower()
    ev["kind"] = np.where(low.str.contains("maintenance|wartung|pm window"), "maintenance", "unplanned")
    return ev.sort_values(["start_h", "node"]).reset_index(drop=True)


def load_rack(path):
    r = pd.read_csv(path)
    out = pd.DataFrame({"node": [int(n[3:]) - 1 for n in r["node"]], "name": r["node"],
                        "rack": [int(x[1:]) for x in r["rack"]], "switch": r["leaf_switch"], "pdu": r["pdu"]})
    out["in_service_h"] = [max(0.0, sim.hrs(dt.datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=P.TZ))) for d in r["in_service_from"]]
    return out.sort_values("node").reset_index(drop=True)


def sheet(path, name):
    wb = load_workbook(path, read_only=True, data_only=True)
    rows = list(wb[name].iter_rows(values_only=True))
    return rows


def load_alloc(path):
    rows = sheet(path, "Grants 2023-2026")
    head = list(rows[0])
    g = pd.DataFrame(rows[1:], columns=head)
    first = g.groupby("project_id")["round"].min()
    g["first_year"] = g["project_id"].map(first)
    grants = pd.DataFrame({"project": g["project_id"], "category": g["category"], "first_year": g["first_year"].astype(int),
                           "year": g["round"].astype(int), "granted": g["granted_nh"].astype(float),
                           "requested": g["requested_nh"].astype(float)})
    rows = sheet(path, "Requests 2027")
    head = list(rows[0])
    r = pd.DataFrame(rows[1:], columns=head)
    requests = pd.DataFrame({"project": r["project_id"], "category": r["category"],
                             "first_year": [int(first.get(p, 2027)) for p in r["project_id"]],
                             "requested": r["requested_nh"].astype(float), "new": r["standing"] == "new"})
    projects = {}
    for _, x in g.iterrows():
        projects[x["project_id"]] = {"category": x["category"], "first_year": int(first[x["project_id"]]),
                                     "title": x["title"], "university": x["university"], "institute": x["institute"],
                                     "pi_name": x["pi"]}
    for _, x in r.iterrows():
        if x["project_id"] not in projects:
            projects[x["project_id"]] = {"category": x["category"], "first_year": 2027, "title": x["title"],
                                         "university": x["university"], "institute": x["institute"], "pi_name": x["pi"]}
    return grants, requests, projects


def load_maint(path):
    rows = sheet(path, "Windows")
    head = list(rows[0])
    m = pd.DataFrame(rows[1:], columns=head)
    out = []
    for _, x in m.iterrows():
        d = x["date"] if isinstance(x["date"], dt.date) else dt.datetime.strptime(str(x["date"])[:10], "%Y-%m-%d").date()
        hh, mm = [int(v) for v in str(x["start"]).split(":")]
        start = dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=P.TZ)
        e = str(x["end"])
        if len(e) > 5:
            end = dt.datetime.strptime(e, "%Y-%m-%d %H:%M").replace(tzinfo=P.TZ)
        else:
            h2, m2 = [int(v) for v in e.split(":")]
            end = dt.datetime(d.year, d.month, d.day, h2, m2, tzinfo=P.TZ)
        out.append({"start_h": sim.hrs(start), "end_h": sim.hrs(end), "kind": "long" if (end - start) > dt.timedelta(hours=20) else "regular"})
    return pd.DataFrame(out)


def load_report(path):
    rows = sheet(path, "Weekly")
    head = list(rows[2])
    w = pd.DataFrame(rows[3:], columns=head)
    weekly = pd.DataFrame({"week": [x.date() if isinstance(x, dt.datetime) else x for x in w["week_start"]],
                           "nodes": w["nodes_in_service"].astype(float), "utilisation": w["utilisation"].astype(float),
                           "delivered_nh": w["node_hours_delivered"].astype(float), "jobs_started": w["jobs_started"].astype(int),
                           "p50_wait_h": w["p50_wait_h"].astype(float), "p90_wait_h": w["p90_wait_h"].astype(float),
                           "lost_node_days": w["node_days_lost"].astype(float)})
    rows = sheet(path, "Quarterly")
    head = list(rows[0])
    q = pd.DataFrame(rows[1:], columns=head)
    quarterly = pd.DataFrame({"quarter": q["quarter"], "nodes": q["nodes_in_service"].astype(float),
                              "delivered_nh": q["node_hours_delivered"].astype(float), "utilisation": q["utilisation"].astype(float),
                              "p50_wait_h": q["p50_wait_h"].astype(float), "p90_wait_h": q["p90_wait_h"].astype(float),
                              "lost_node_days": q["node_days_lost"].astype(float)})
    return {"weekly": weekly, "quarterly": quarterly}


def load_limits(path):
    txt = open(path, encoding="utf-8").read()
    lims = []
    current = None
    for line in txt.splitlines():
        h = re.match(r"^(\d{4}-\d{2}-\d{2})\s+(.*)$", line)
        if h:
            current = dt.datetime.strptime(h.group(1), "%Y-%m-%d").replace(tzinfo=P.TZ)
            t = re.search(r"restarted (\d{2}):(\d{2})", h.group(2))
            if t:
                current = current.replace(hour=int(t.group(1)), minute=int(t.group(2)))
        if line.startswith("#") or current is None:
            continue
        mm = re.search(r"QOS normal\s+MaxWall=([\d:-]+)", line)
        if mm:
            lims.append((max(0.0, sim.hrs(current)), parse_dhms(mm.group(1))))
    short = 4.0
    ms = re.search(r"QOS short\s+MaxWall=([\d:-]+)", txt)
    if ms:
        short = parse_dhms(ms.group(1))
    mp = re.search(r"planned: QOS normal MaxWall=([\d:-]+) from (\d{4}-\d{2}-\d{2})", txt)
    if mp:
        d = dt.datetime.strptime(mp.group(2), "%Y-%m-%d").replace(tzinfo=P.TZ)
        lims.append((sim.hrs(d), parse_dhms(mp.group(1))))
    restarts = [dt.datetime.strptime(x, "%Y-%m-%d %H:%M").replace(tzinfo=P.TZ)
                for x in re.findall(r"^\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2})$", txt, re.M)]
    return {"normal": sorted(lims), "short": short}, restarts


def load_users(path):
    u = pd.read_csv(path, dtype=str, keep_default_na=False)
    return {r["username"]: {"user": r["username"], "uid": int(r["uid"]), "name": r["name"], "university": r["university"],
                            "institute": r["institute"], "projects": r["projects"].split(";") if r["projects"] else []}
            for r in u.to_dict("records")}


def load_pack(target):
    F = {k: os.path.join(target, v) for k, v in PK.FILES.items()}
    pk = T.Pack()
    pk.cut_h = sim.hrs(P.CUT)
    pk.jobs, pk.seg = load_sacct(F["sacct"], pk.cut_h)
    pk.events = load_events(F["events"], pk.cut_h)
    pk.rack = load_rack(F["rack"])
    pk.grants, pk.requests, projects = load_alloc(F["alloc"])
    pk.maint = load_maint(F["maint"])
    pk.report = load_report(F["report"])
    pk.limits, pk.restarts = load_limits(F["config"])
    pk.users = load_users(F["users"])
    # a project's people from the directory
    for pid, pr in projects.items():
        pr["members"] = [u for u, v in pk.users.items() if pid in v["projects"]]
    pk.projects = projects
    return pk
