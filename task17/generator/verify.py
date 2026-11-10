"""An independent recomputation of the golden from the shipped files, sharing no code with analysis.py or load.py:
its own parsers (csv, zipfile and the OOXML trees), its own de-duplication and job assembly, its own use ratios and
burst index, its own censored log-logistic fit (one shape, a shift per job kind, node count and limit habit) with
the 24 to 48 hour shape test, its own outage intervals, classes and medians, its own rework estimate, and its own
forward model run on the pure-Python scheduler (pydes.py) with fewer futures. Exit 1 unless every graded figure lands
in the cell the submission states.

    python3 verify.py [target]
"""
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo

import numpy as np
from scipy import optimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pydes

TZ = ZoneInfo("Europe/Berlin")
T0 = dt.datetime(2023, 9, 1, tzinfo=dt.timezone.utc)
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
FAIL = []


def ok(name, cond, detail=""):
    if not cond:
        FAIL.append("%s %s" % (name, detail))


def hrs(d):
    return (d - T0).total_seconds() / 3600.0


def H(y, m=1, d=1):
    return hrs(dt.datetime(y, m, d, tzinfo=TZ))


def parse_utc(s):
    return hrs(dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc))


def parse_local(s):
    if s in ("Unknown", "None", ""):
        return float("nan")
    d = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
    # the autumn's repeated hour: the first occurrence
    return hrs(d.replace(tzinfo=TZ, fold=0))


def dhms(s):
    d = 0
    if "-" in s:
        d, s = s.split("-")
        d = int(d)
    h, m, sec = [int(x) for x in s.split(":")]
    return d * 24 + h + m / 60.0 + sec / 3600.0


def sheet_rows(path, name):
    z = zipfile.ZipFile(path)
    wbx = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid = [s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id") for s in wbx.find("m:sheets", NS) if s.get("name") == name][0]
    target = [r.get("Target") for r in rels if r.get("Id") == rid][0]
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    ws = ET.fromstring(z.read("xl/" + target.lstrip("/").replace("xl/", "")))
    out = []
    for row in ws.find("m:sheetData", NS):
        vals = []
        for c in row:
            col = 0
            for ch in c.get("r"):
                if ch.isalpha():
                    col = col * 26 + ord(ch) - 64
            while len(vals) < col - 1:
                vals.append(None)
            v = c.find("m:v", NS)
            t = c.get("t")
            if t == "s":
                vals.append(shared[int(v.text)])
            elif t == "inlineStr":
                vals.append("".join(x.text or "" for x in c.iter("{%s}t" % NS["m"])))
            else:
                vals.append(None if v is None else float(v.text))
        out.append(vals)
    return out


def excel_date(v):
    return dt.date(1899, 12, 30) + dt.timedelta(days=int(v))


# ---------------------------------------------------------------- the record
def load_jobs(path):
    seen = set()
    rows = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = tuple(r.values())
            if key in seen:
                continue
            seen.add(key)
            rows.append(r)
    # jobs keyed by id and submission; an id names two jobs when the counter wrapped
    jobs = {}
    for r in rows:
        k = (int(r["JobID"]), r["Submit_UTC"])
        j = jobs.setdefault(k, {"name": r["JobName"], "user": r["User"], "account": r["Account"], "qos": r["QOS"],
                                 "nodes": int(r["ReqNodes"]), "wall": dhms(r["Timelimit"]), "submit": parse_utc(r["Submit_UTC"]),
                                 "elig": parse_utc(r["Eligible_UTC"]), "segs": [], "state": r["State"].split(" ")[0]})
        st = parse_local(r["Start_local"])
        if not math.isnan(st):
            j["segs"].append((int(r["Restarts"]), st, parse_local(r["End_local"]), dhms(r["Elapsed"]), r["State"].split(" ")[0]))
    for j in jobs.values():
        j["segs"].sort()
        j["start"] = j["segs"][0][1] if j["segs"] else float("nan")
        j["elapsed"] = sum(s[3] for s in j["segs"])
        j["nh"] = j["elapsed"] * j["nodes"]
        j["restarts"] = len(j["segs"]) - 1 if j["segs"] else 0
        j["state"] = j["segs"][-1][4] if j["segs"] else j["state"]
        j["killed"] = sum(s[3] for s in j["segs"] if s[4] == "NODE_FAIL")
    return jobs


def stem(name):
    return re.sub(r"(_(r|fix))?(_\d+)?$", "", name)


def kind(stem_):
    s = stem_.lower()
    for k, keys in (("train", ("train", "pretrain", "run_lr")), ("finetune", ("ft_", "finetune", "lora", "sft")),
                    ("md", ("md_", "gromacs", "namd", "lammps")), ("cfd", ("cfd", "les_", "openfoam", "dns_", "channel"))):
        if any(s.startswith(x) or ("_" + x) in s for x in keys):
            return k
    return "other"


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    F = lambda n: os.path.join(target, n)
    jobs = load_jobs(F("sacct_gpu_2024-01_2026-11.csv"))
    J = list(jobs.values())
    # ---- limits from the configuration history
    cfg = open(F("slurm_config_history_sturmvogel.txt"), encoding="utf-8").read()
    lims = []
    cur = None
    for line in cfg.splitlines():
        m = re.match(r"^(\d{4}-\d{2}-\d{2})\s+(.*)$", line)
        if m:
            cur = dt.datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=TZ)
            t = re.search(r"restarted (\d{2}):(\d{2})", m.group(2))
            if t:
                cur = cur.replace(hour=int(t.group(1)), minute=int(t.group(2)))
        mm = re.search(r"QOS normal\s+MaxWall=([\d:-]+)", line)
        if mm and cur is not None and not line.startswith("#"):
            lims.append((max(0.0, hrs(cur)), dhms(mm.group(1))))
    lims.sort()
    change_h = lims[1][0]

    def limit_at(h):
        l = lims[0][1]
        for a, b in lims:
            if h >= a:
                l = b
        return l
    ok("limits parsed as 24 then 48", [l for _, l in lims[:2]] == [24.0, 48.0])

    # ---- R1
    a, b = H(2026, 7, 1), H(2026, 10, 1)
    q3 = [j for j in J if a <= j["elig"] < b and j["segs"] and j["state"] != "CANCELLED"]
    q3_jobs, q3_nh = len(q3), sum(j["nh"] for j in q3)
    ok("R1 jobs", int(round(q3_jobs / 10.0) * 10) == figs["q3_jobs"], "%d" % q3_jobs)
    ok("R1 node-hours", int(round(q3_nh / 1000.0) * 1000) == figs["q3_nh"], "%.0f" % q3_nh)
    deliv = 0.0
    for j in J:
        for s in j["segs"]:
            e = s[2] if not math.isnan(s[2]) else s[1] + s[3]
            deliv += max(0.0, min(e, b) - max(s[1], a)) * j["nodes"]
    ok("R1 delivered reconciles to the report", abs(deliv - figs["q3_report_delivered"]) < 1.0, "%.1f" % deliv)

    # ---- R2
    gr = sheet_rows(F("allocations_gpu_2023-2027.xlsx"), "Grants 2023-2026")
    head = gr[0]
    grants = [dict(zip(head, r)) for r in gr[1:]]
    first = {}
    for g_ in grants:
        first[g_["project_id"]] = min(first.get(g_["project_id"], 9999), int(g_["round"]))
    used = {}
    for j in J:
        y = dt.datetime.fromtimestamp(0, dt.timezone.utc)
        yr = (T0 + dt.timedelta(hours=j["elig"])).astimezone(TZ).year
        used[(j["account"], yr)] = used.get((j["account"], yr), 0.0) + j["nh"]
    acc = {True: [0.0, 0.0], False: [0.0, 0.0]}
    for g_ in grants:
        y = int(g_["round"])
        if y not in (2024, 2025):
            continue
        new = first[g_["project_id"]] == y
        acc[new][0] += used.get((g_["project_id"], y), 0.0)
        acc[new][1] += float(g_["granted_nh"])
    r_new, r_cont = acc[True][0] / acc[True][1], acc[False][0] / acc[False][1]
    ok("R2 first-year ratio", int(round(100 * r_new)) == figs["use_new_pct"], "%.4f" % r_new)
    ok("R2 continuing ratio", int(round(100 * r_cont)) == figs["use_cont_pct"], "%.4f" % r_cont)
    rq = sheet_rows(F("allocations_gpu_2023-2027.xlsx"), "Requests 2027")
    rh = rq[0]
    reqs = [dict(zip(rh, r)) for r in rq[1:]]
    req_total = sum(float(r["requested_nh"]) for r in reqs)
    exp_use = sum(float(r["requested_nh"]) * (r_new if r["standing"] == "new" else r_cont) for r in reqs)
    ok("R2 expected use at the requests", int(round(exp_use / 10000.0) * 10000) == figs["expected_use_requests"], "%.0f" % exp_use)
    ok("requests total", abs(req_total - figs["requests_total"]) < 1)
    # the burst index: hourly submission counts, January to June 2026, dispersion about hour-of-week means
    a6, b6 = H(2026, 1, 1), H(2026, 7, 1)
    n_h = int(math.ceil(b6 - a6))
    cnt = np.zeros(n_h)
    for j in J:
        if a6 <= j["submit"] < b6:
            cnt[int(j["submit"] - a6)] += 1
    how = np.array([(T0 + dt.timedelta(hours=a6 + k + 0.5)).astimezone(TZ).weekday() * 24 + (T0 + dt.timedelta(hours=a6 + k + 0.5)).astimezone(TZ).hour for k in range(n_h)])
    means = np.array([cnt[how == k].mean() for k in range(168)])
    burst = ((cnt - means[how]) ** 2).sum() / means[how].sum()
    ok("R2 burst index", int(round(burst)) == figs["burst_index"], "%.3f" % burst)

    # ---- R3: a log-logistic AFT, strata by kind x nodes x limit habit, censored at the limit
    normal = [j for j in J if j["qos"] == "normal" and j["state"] in ("COMPLETED", "TIMEOUT") and j["restarts"] == 0]
    grp = {}
    for j in normal:
        k = (j["account"], stem(j["name"]))
        g_ = grp.setdefault(k, [0, 0])
        g_[0] += 1
        g_[1] += abs(j["wall"] - limit_at(j["submit"])) < 1e-6
    maxg = {k: v[1] / v[0] >= 0.9 for k, v in grp.items()}
    kinds = ["train", "finetune", "md", "cfd", "other"]

    def cls_of(j):
        ng = int(np.searchsorted([1, 2, 4, 8], j["nodes"]))
        return (kinds.index(kind(stem(j["name"]))) * 4 + ng) * 2 + int(maxg[(j["account"], stem(j["name"]))])

    def data_of(sel):
        t = np.array([j["wall"] if j["state"] == "TIMEOUT" else max(j["elapsed"], 0.005) for j in sel])
        c = np.array([j["state"] == "TIMEOUT" for j in sel])
        k = np.array([cls_of(j) for j in sel])
        return t, c, k

    def fit_ll(t, c, k, n_cls=40):
        key = {}
        for ti, ci, ki in zip(np.round(t, 2), c, k):
            key[(ti, ci, ki)] = key.get((ti, ci, ki), 0) + 1
        tt = np.array([x[0] for x in key]); cc = np.array([x[1] for x in key]); kk = np.array([x[2] for x in key]); ww = np.array(list(key.values()), dtype=float)
        tt = np.maximum(tt, 0.005)

        def nll(th):
            mu = th[:n_cls][kk]
            sig = math.exp(th[n_cls])
            z = (np.log(tt) - mu) / sig
            lS = -np.logaddexp(0.0, z)
            lf = z - 2.0 * np.logaddexp(0.0, z) - math.log(sig) - np.log(tt)
            return -float(np.sum(ww * np.where(cc, lS, lf)))
        lt = np.log(t)
        mu0 = np.array([np.median(lt[k == c_]) if (k == c_).any() else np.median(lt) for c_ in range(n_cls)])
        th0 = np.concatenate([mu0, [math.log(0.6)]])
        r = optimize.minimize(nll, th0, method="L-BFGS-B", options={"maxiter": 2000})
        return r.x[:n_cls], math.exp(r.x[n_cls])

    def S(t, mu, sig):
        return 1.0 / (1.0 + np.exp((np.log(t) - mu) / sig))
    pre = [j for j in normal if j["submit"] < change_h]
    mu_pre, sig_pre = fit_ll(*data_of(pre))
    post = [j for j in normal if j["submit"] >= change_h and maxg[(j["account"], stem(j["name"]))] and j["wall"] >= 47.9]
    t, c, k = data_of(post)
    beyond = t > 24
    obs_s48 = c[beyond].mean()
    obs_ex = (np.minimum(t[beyond], 48) - 24).mean()
    s24 = S(24.0, mu_pre[k], sig_pre); s48 = S(48.0, mu_pre[k], sig_pre)
    grid = np.linspace(24, 48, 241)
    ex = np.array([np.trapezoid(S(grid, mu_pre[ki], sig_pre), grid) for ki in k])
    z_s48 = (s48.sum() / s24.sum() - obs_s48) / math.sqrt(obs_s48 * (1 - obs_s48) / beyond.sum())
    z_ex = (ex.sum() / s24.sum() - obs_ex) / ((np.minimum(t[beyond], 48) - 24).std() / math.sqrt(beyond.sum()))
    ok("R3 the log-logistic passes the 24 to 48 hour shape test", abs(z_s48) <= 3 and abs(z_ex) <= 3, "z %.2f %.2f" % (z_s48, z_ex))
    mu, sig = fit_ll(*data_of(normal))
    t26, c26, k26 = data_of([j for j in normal if j["submit"] >= H(2026)])
    n26 = np.array([j["nodes"] for j in normal if j["submit"] >= H(2026)])
    g96 = np.linspace(0, 96, 1921)
    tot_m, tot_w, tot_t, n_all = 0.0, 0.0, 0.0, 0
    for c_ in sorted(set(k26)):
        m = k26 == c_
        Sg = S(np.maximum(g96, 1e-6), mu[c_], sig)
        Sg[0] = 1.0
        e96 = np.trapezoid(Sg, g96)
        e_tail = np.trapezoid(Sg[g96 >= 48], g96[g96 >= 48])
        tot_m += m.sum() * e96
        tot_w += (n26[m].sum()) * e96
        tot_t += (n26[m].sum()) * e_tail
        n_all += m.sum()
    mean96, share48 = tot_m / n_all, tot_t / tot_w
    ok("R3 mean run time under 96 h", int(round(mean96)) == figs["mean96_h"], "%.2f" % mean96)
    ok("R3 share of work beyond 48 h (nearest 10)", int(round(10 * share48)) * 10 == figs["share48_pct"], "%.3f" % share48)

    # ---- R4
    ev = []
    with open(F("node_events_sturmvogel_2024-2026.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ev.append({"node": int(r["NodeName"][3:]) - 1, "s": parse_local(r["TimeStart"]), "e": parse_local(r["TimeEnd"]), "reason": r["Reason"].lower()})
    cut_h = hrs(dt.datetime(2026, 11, 16, 6, 10, tzinfo=TZ))
    ev.sort(key=lambda x: (x["node"], x["s"]))
    joined = []
    for r in ev:
        e = r["e"] if not math.isnan(r["e"]) else cut_h
        if joined and joined[-1]["node"] == r["node"] and joined[-1]["reason"] == r["reason"] and abs(r["s"] - joined[-1]["e"]) < 1 / 60.0 + 1e-9:
            joined[-1]["e"] = e
            continue
        joined.append({"node": r["node"], "s": r["s"], "e": e, "reason": r["reason"], "open": math.isnan(r["e"])})
    rack_rows = list(csv.DictReader(open(F("rack_layout_gpu.csv"), encoding="utf-8")))
    rack_of = {int(r["node"][3:]) - 1: r["rack"] for r in rack_rows}

    def classify(txt):
        if any(k in txt for k in ("maintenance", "wartung", "pm window")):
            return "maint"
        if any(k in txt for k in ("drain", "reserved")):
            return "admin"
        if any(k in txt for k in ("switch", "leaf", "ib ", "pdu", "strom", "tripped", "trip", "sw-r")):
            return "rack"
        if any(k in txt for k in ("rma", "replac", "swap", "getauscht", "dimm", "psu", "netzteil", "hca", "nvme", "mainboard", "fan", "awaiting", "pending", "ecc")):
            return "hardware"
        return "software"
    for r in joined:
        r["cls"] = classify(r["reason"])
        r["rack"] = rack_of[r["node"]]
    for r in joined:
        if "not responding" in r["reason"]:
            same = sum(1 for q in joined if q["rack"] == r["rack"] and abs(q["s"] - r["s"]) <= 10 / 60.0)
            r["cls"] = "rack" if same >= 3 else "software"
    mw = sheet_rows(F("maintenance_calendar_2024-2027.xlsx"), "Windows")
    windows = []
    for r in mw[1:]:
        d = excel_date(r[0]) if isinstance(r[0], float) else dt.datetime.strptime(str(r[0])[:10], "%Y-%m-%d").date()
        h1, m1 = [int(x) for x in str(r[1]).split(":")]
        e = str(r[2])
        s_ = hrs(dt.datetime(d.year, d.month, d.day, h1, m1, tzinfo=TZ))
        if len(e) > 5:
            e_ = hrs(dt.datetime.strptime(e, "%Y-%m-%d %H:%M").replace(tzinfo=TZ))
        else:
            h2, m2 = [int(x) for x in e.split(":")]
            e_ = hrs(dt.datetime(d.year, d.month, d.day, h2, m2, tzinfo=TZ))
        windows.append((s_, e_))
    un = [r for r in joined if r["cls"] != "maint"]
    for q, (qa, qb) in {1: (H(2026, 1, 1), H(2026, 4, 1)), 2: (H(2026, 4, 1), H(2026, 7, 1)), 3: (H(2026, 7, 1), H(2026, 10, 1))}.items():
        lost = 0.0
        for r in un:
            ov = max(0.0, min(r["e"], qb) - max(r["s"], qa))
            for ms, me in windows:
                lo, hi = max(qa, ms), min(qb, me)
                if hi > lo:
                    ov -= max(0.0, min(r["e"], hi) - max(r["s"], lo))
            lost += ov
        ok("R4 node-days lost Q%d" % q, int(round(lost / 240.0) * 10) == figs["lost_by_quarter"][str(q)], "%.1f" % (lost / 24))
    y = [r for r in un if H(2024) <= r["s"] < cut_h and not r["open"]]
    med = lambda xs: float(np.median(xs)) if len(xs) else float("nan")
    sw = med([r["e"] - r["s"] for r in y if r["cls"] == "software"])
    hw = med([(r["e"] - r["s"]) / 24 for r in y if r["cls"] == "hardware"])
    rk = {}
    for r in y:
        if r["cls"] == "rack":
            key = (r["rack"], int(r["s"] // 0.5))
            rk[key] = max(rk.get(key, 0.0), r["e"] - r["s"])
    rkm = med(list(rk.values()))
    ok("R4 software median", int(round(sw)) == figs["repair_software_h"], "%.2f" % sw)
    ok("R4 hardware median", round(hw * 2) / 2 == figs["repair_hardware_d"], "%.2f" % hw)
    ok("R4 rack median", int(round(rkm)) == figs["repair_rack_h"], "%.2f" % rkm)
    # the share lost while four or more nodes of a rack were down
    ya, yb = H(2026), cut_h
    tot, multi = 0.0, 0.0
    for rack in set(rack_of.values()):
        rows = [r for r in un if r["rack"] == rack and r["e"] > ya and r["s"] < yb]
        pts = sorted(set([max(ya, min(yb, r["s"])) for r in rows] + [max(ya, min(yb, r["e"])) for r in rows] + [ya, yb]))
        for lo, hi in zip(pts[:-1], pts[1:]):
            if hi <= lo:
                continue
            mid = 0.5 * (lo + hi)
            if any(ms <= mid < me for ms, me in windows):
                continue
            down = sum(1 for r in rows if r["s"] <= mid < r["e"])
            tot += down * (hi - lo)
            if down >= 4:
                multi += down * (hi - lo)
    ok("R4 multi-node share", int(round(100 * multi / tot)) == figs["multi_share_pct"], "%.3f" % (multi / tot))

    # ---- R5
    by_sess = {}
    for j in J:
        if j["segs"]:
            by_sess.setdefault((j["account"], j["user"], stem(j["name"])), []).append(j)
    rows = []
    killed_all, tot_nh = 0.0, 0.0
    for j in J:
        if H(2026) <= j["elig"] < H(2027) and j["segs"]:
            tot_nh += j["nh"]
            if j["restarts"] > 0:
                killed_all += j["killed"] * j["nodes"]
                if j["state"] == "COMPLETED":
                    peers = [p for p in by_sess[(j["account"], j["user"], stem(j["name"]))] if p["restarts"] == 0 and p["state"] == "COMPLETED"
                             and p["nodes"] == j["nodes"] and abs(p["submit"] - j["submit"]) < 0.5]
                    if not peers:
                        peers = [p for p in by_sess[(j["account"], j["user"], stem(j["name"]))] if p["restarts"] == 0 and p["state"] == "COMPLETED" and p["nodes"] == j["nodes"]]
                    if peers:
                        ref = float(np.median([p["elapsed"] for p in peers]))
                        rows.append(((j["elapsed"] - ref) * j["nodes"], j["killed"] * j["nodes"]))
    frac = sum(r[0] for r in rows) / sum(r[1] for r in rows)
    share = frac * killed_all / tot_nh
    ok("R5 rework share", int(round(100 * share)) == figs["rework_pct"], "%.4f (frac %.3f)" % (share, frac))

    # ---- the forward model with the Python scheduler: the backtest and the three deciding steps
    sys.path.insert(0, HERE)
    import load as L_
    import analysis as A_
    pk = L_.load_pack(target)
    Fj = A_.fit_all(pk, A_.H(2026, 7, 1), family=figs["family"])
    Fa = A_.fit_all(pk, pk.cut_h, family=figs["family"])
    import multiprocessing as mp

    def run(Fx, year, T, n, window, seed0):
        import analysis as AA
        AA._CTX["F"], AA._CTX["pk"] = Fx, pk
        args = [(year, T, seed0 + i, window) for i in range(n)]
        ctx = mp.get_context("fork")
        with ctx.Pool(max(1, min(16, (os.cpu_count() or 4) - 2))) as pool:
            return pool.map(_py_future, args)
    bt = run(Fj, 2026, None, 120, A_.quarter(2026, 3), 9000)
    p90 = float(np.mean([r["p90"] for r in bt]))
    ok("R6 backtest on the Python scheduler", int(round(p90)) == figs["backtest_p90_h"], "%.2f" % p90)
    cap = figs["cap"]
    ps = {}
    for T in (cap - 10000, cap, cap + 10000):
        res = run(Fa, 2027, T, 240, None, 9500 + T // 1000)
        ps[T] = float(np.mean([r["p90"] <= 4.0 for r in res]))
    ok("R7 the cap holds on the Python scheduler", ps[cap] >= 0.8 > ps[cap + 10000], str(ps))
    ok("R7 the cut share", int(round(100 * (1 - cap / req_total))) == figs["cut_share_pct"])
    print("verify: %d failures" % len(FAIL))
    for f in FAIL:
        print("FAIL", f)
    return 1 if FAIL else 0


def _py_future(args):
    import analysis as AA
    year, T, seed, window = args
    Fx, pk = AA._CTX["F"], AA._CTX["pk"]
    rng = np.random.default_rng(seed)
    jobs = AA.demand_year(Fx, pk, year, T, rng, AA.OPT_GOLD if hasattr(AA, "OPT_GOLD") else {"param_draw": True, "ratio_draw": True})
    outages, maint = AA.outages_year(Fx, pk, year, rng, {"param_draw": True})
    a, b = window or (AA.H(year), AA.H(year + 1))
    R = pydes.simulate(len(pk.rack), jobs, outages[:3], maint, b + 24.0 * 35, bf_max=100, hold=0.05)
    sub = R["submit"]
    dep = jobs["dep"]
    pred = np.where(dep >= 0, R["final_end"][np.maximum(dep, 0)], -1.0)
    elig = np.where((dep >= 0) & (pred > sub), pred, sub)
    m = (elig >= a) & (elig < b) & (R["first_start"] >= 0)
    w = R["first_start"][m] - elig[m]
    return {"p90": float(np.percentile(w, 90))}


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
