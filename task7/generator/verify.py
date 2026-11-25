"""The independent verifier (dataset-generation 11): reads only the shipped bundle and the golden files, on its own code
path (its own parse of every file, never read.py), recomputes the golden through core.py's estimators and checks it,
the figures.json values and the golden deliverables against each other.

    python3 task7/generator/verify.py [--target <folder>]
"""
import csv
import datetime as dt
import itertools
import json
import math
import os
import re
import subprocess
import sys
import zipfile
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core as C  # noqa: E402

TASK = os.path.dirname(HERE)
OUT = []


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


def table(path):
    with open(path, newline="") as fh:
        rd = csv.reader(fh)
        head = next(rd)
        return head, [row for row in rd]


def col(head, name):
    return head.index(name)


def key_addr(a):
    t = re.sub(r"[.,]", " ", a.upper())
    t = re.sub(r"\s+", " ", t).strip()
    rep = {"STREET": "ST", "AVENUE": "AVE", "DRIVE": "DR", "LANE": "LN", "COURT": "CT", "PLACE": "PL", "ROAD": "RD",
           "NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W"}
    return " ".join(rep.get(w, w) for w in t.split(" "))


def main(target):
    T = lambda f: os.path.join(target, f)
    Fj = json.load(open(os.path.join(HERE, "figures.json")))
    # ---- the register ----
    h, rows = table(T("lm_switch_register.csv"))
    ac = [r for r in rows if r[col(h, "load_controlled")] == "Central air conditioner" and r[col(h, "status")] == "Active"]
    n_s = len(ac)
    hp, pts = table(T("scada_point_list.csv"))
    feeders = sorted({p[col(hp, "feeder")] for p in pts})
    fi = {f: i for i, f in enumerate(feeders)}
    dmap = {p[col(hp, "feeder")]: p[col(hp, "district")] for p in pts}
    dist = np.array([["Larkin", "Medora Flats", "Halverson", "Pruett"].index(dmap[f]) for f in feeders])
    sf = np.array([fi[r[col(h, "feeder")]] for r in ac])
    x = np.array([float(r[col(h, "grid_x_km")]) for r in ac])
    y = np.array([float(r[col(h, "grid_y_km")]) for r in ac])
    inst = [dt.date(*map(int, r[col(h, "install_date")].split("-"))) for r in ac]
    yr = np.array([d.year for d in inst])
    vhf = np.array([r[col(h, "receiver")][:3] == "VHF" for r in ac])
    grp = np.array([int(r[col(h, "paging_group")][-2:]) - 1 for r in ac])
    # ---- the encoder log: first shed transmit per group per afternoon ----
    he, enc = table(T("paging_encoder_log_2026.csv"))
    first = {}
    for r in enc:
        if r[col(he, "command")] != "SHED" or not r[col(he, "group")].startswith("AC"):
            continue
        t = dt.datetime.strptime(r[col(he, "tx_time_local")], "%m/%d/%Y %H:%M:%S")
        if t.hour < 15:
            continue
        k = (t.date(), int(r[col(he, "group")][-2:]) - 1)
        if k not in first or t < first[k]:
            first[k] = t
    days = sorted({k[0] for k in first})
    disp = np.zeros((len(days), 16), bool)
    for d, g in first:
        disp[days.index(d), g] = True
    # ---- SCADA: point to feeder by the point list's service dates; first reading of a duplicated minute ----
    span = defaultdict(list)
    for p in pts:
        a = p[col(hp, "in_service")]
        b = p[col(hp, "retired")]
        fa = dt.datetime.fromisoformat(a if " " in a else a + " 00:00")
        fb = dt.datetime.fromisoformat(b) if b else dt.datetime(2100, 1, 1)
        span[p[col(hp, "point")]].append((p[col(hp, "feeder")], fa, fb))
    minutes = {}
    want = set(days)
    with open(T("scada_feeder_1min_2026.csv"), newline="") as fh:
        rd = csv.reader(fh)
        next(rd)
        for t, tag, kw in rd:
            u = dt.datetime(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16])) - dt.timedelta(hours=5)
            if u.date() not in want:
                continue
            fc = next(c for c, a, b in span[tag] if a <= u < b)
            k = (fc, u.date(), (u.hour - 15) * 60 + u.minute)
            if k not in minutes:
                minutes[k] = float(kw)
    series = {}
    for fc in feeders:
        for d in days:
            v = [minutes[(fc, d, m)] for m in range(300)]
            good = [True] * 300
            i = 0
            for val, grp_it in itertools.groupby(range(300), key=lambda j: v[j]):
                run = list(grp_it)
                if len(run) >= 3:
                    for j in run[1:]:
                        good[j] = False
            series[(fc, d)] = (np.array(v), np.array(good))
    obs_e, obs_g, obs_f, step = [], [], [], []
    for e, d in enumerate(days):
        for g in np.flatnonzero(disp[e]):
            t0 = first[(d, int(g))]
            M = (t0.hour - 15) * 60 + t0.minute
            for f, fc in enumerate(feeders):
                v, good = series[(fc, d)]
                bb = [j for j in range(M - 5, M) if good[j]]
                aa = [j for j in range(M, M + 5) if good[j]]
                obs_e.append(e)
                obs_g.append(int(g))
                obs_f.append(f)
                step.append(v[bb].mean() - v[aa].mean())
    load = np.array([np.mean(np.concatenate([series[(fc, d)][0][:45][series[(fc, d)][1][:45]] for d in days])) for fc in feeders])
    hi_, ix = table(T("sunflower_basin_cooling_index_2026.csv"))
    index = {dt.date.fromisoformat(r[0]): float(r[1]) for r in ix}
    wx = np.array([index[d] for d in days])
    # ---- reach ----
    ws = load_workbook(T("paging_transmitters.xlsx"), read_only=True)["Paging sites"]
    sites = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]
    ws2 = load_workbook(T("radio_shop_outage_log_2026.xlsx"), read_only=True)["2026"]
    outs = [r for r in ws2.iter_rows(min_row=2, values_only=True) if r[0]]
    nick = {"HQ tower": "Headquarters", "MF sub stick": "Medora Flats substation", "Hal sub VHF": "Halverson substation",
            "Halverson VHF": "Halverson substation", "TCP Larkin": "Larkin water tower", "TCP Sandhill": "Sandhill",
            "TCP Ostrander": "Ostrander", "TCP Pruett": "Pruett", "TCP Bluestem": "Bluestem"}
    sx = np.array([float(s[4]) for s in sites])
    sy = np.array([float(s[5]) for s in sites])
    sv = np.array([s[2] == "VHF" for s in sites])
    listed = np.array([s[7] is None for s in sites])
    dmat = np.hypot(x[:, None] - sx[None, :], y[:, None] - sy[None, :])
    own = np.where(vhf[:, None], sv[None, :], ~sv[None, :])
    reach = np.empty((len(days), n_s))
    for e, d in enumerate(days):
        w0, w1 = dt.datetime.combine(d, dt.time(16)), dt.datetime.combine(d, dt.time(18))
        on = np.array([(s[6].date() if isinstance(s[6], dt.datetime) else s[6]) <= d and s[7] is None and
                       not any(nick[o[0]] == s[1] and o[1] < w1 and o[2] > w0 for o in outs) for s in sites])
        reach[e] = np.where(own & on[None, :], dmat, 1e9).min(1)
    now = np.where(own & listed[None, :], dmat, 1e9).min(1)
    dvn = np.where(sv[None, :] & listed[None, :], dmat, 1e9).min(1)
    dcn = np.where(~sv[None, :] & listed[None, :], dmat, 1e9).min(1)
    # ---- the replaced-unit list ----
    pno = {r[col(h, "premise_no")]: i for i, r in enumerate(ac)}
    old = {r[col(h, "old_premise_no")]: i for i, r in enumerate(ac) if r[col(h, "old_premise_no")]}
    adr = {(key_addr(r[col(h, "service_address")]), r[col(h, "city")].upper()): i for i, r in enumerate(ac)}
    flag = np.zeros(n_s, bool)
    hr_, reb = table(T("hvac_rebates_2012_2026.csv"))
    for r in reb:
        if r[col(hr_, "equipment")] in ("Central air conditioner", "Central heat pump (air source)"):
            i = pno.get(r[col(hr_, "premise_no")], old.get(r[col(hr_, "premise_no")]))
            if i is not None and dt.date.fromisoformat(r[col(hr_, "equipment_installed")]) > inst[i]:
                flag[i] = True
    hq, per = table(T("county_mechanical_permits_2010_2026.csv"))
    for r in per:
        if r[col(hq, "work")] in ("REPLACE A/C CONDENSING UNIT", "REPLACE CONDENSING UNIT AND COIL", "HEAT PUMP CHANGE-OUT, SPLIT SYSTEM"):
            i = adr.get((key_addr(r[col(hq, "site_address")]), r[col(hq, "city")].upper()))
            if i is not None and dt.date.fromisoformat(r[col(hq, "issued")]) > inst[i]:
                flag[i] = True
    # ---- the study homes ----
    hh, homes = table(T("study_homes.csv"))
    hid = sorted(r[0] for r in homes)
    meter = {r[0]: r[col(hh, "interval_meter")] for r in homes}
    ha, asg = table(T("study_event_assignments_2026.csv"))
    shed = {(r[0], r[1]) for r in asg if r[2] == "shed"}
    kwh = defaultdict(float)
    with open(T("study_meters_hourly_2026.csv"), newline="") as fh:
        rd = csv.reader(fh)
        next(rd)
        for m, t, v in rd:
            hr = int(t[11:13])
            if hr in (13, 14):
                kwh[(m, t[:10], "pre")] += float(v)
            elif hr in (16, 17):
                kwh[(m, t[:10], "shed")] += float(v)
    s_resp = np.zeros((len(days), len(hid)))
    s_tr = np.zeros((len(days), len(hid)), bool)
    for e, d in enumerate(days):
        ds = d.isoformat()
        tr = np.array([(h_, ds) in shed for h_ in hid])
        pre = np.array([kwh[(meter[h_], ds, "pre")] for h_ in hid])
        sh = np.array([kwh[(meter[h_], ds, "shed")] for h_ in hid])
        ratio = sh[~tr].sum() / pre[~tr].sum()
        s_tr[e] = tr
        s_resp[e] = np.where(tr, (pre * ratio - sh) / (2 * wx[e]), 0)
    age = 2026 - yr
    wd = dict(n_s=n_s, n_feed=len(feeders), n_events=len(days), dist=dist, sf=sf, x=x, y=y, yr=yr, vhf=vhf, age=age, grp=grp,
              disp=disp, obs=(np.array(obs_e), np.array(obs_g), np.array(obs_f)), step=np.array(step), load=load, w=wx, wx=wx,
              reach=reach, now=now, static_any=np.where(listed[None, :], dmat, 1e9).min(1),
              d_new_v=np.minimum(dvn, np.hypot(x + 31.0, y - 12.0)), d_new_c=np.minimum(dcn, np.hypot(x - 3.0, y - 25.0)),
              flag=flag, study=(s_resp, s_tr), batch_age=np.array([age[grp == g].mean() for g in range(16)]))
    ln, cnt = C.lines(wd)
    gm = C.model(wd)
    g = C.all_figures(wd, gm, ln)
    # ---- the recomputed golden against figures.json ----
    for m in C.MEMBERS:
        ok("A1 %s recomputes to %s kW" % (m, Fj["proposals"][m]["kw"]), round(g[m]) == Fj["proposals"][m]["kw"], "%.2f" % g[m])
        ok("A1 %s break-even %s kW" % (m, Fj["proposals"][m]["breakeven"]), round(ln[m]) == Fj["proposals"][m]["breakeven"])
    ok("A2 the fringe share recomputes", 100 - round(100 * g["c1_fringe_loss"]) == Fj["c1_through"], "%.4f" % g["c1_fringe_loss"])
    ok("A2 the pre-2016 working share recomputes", 100 - round(100 * g["c2_failed_old"]) == Fj["c2_work"], "%.4f" % g["c2_failed_old"])
    ok("A2 the still-wired share recomputes", 100 - round(100 * g["c3_unwired"]) == Fj["c3_wired"], "%.4f" % g["c3_unwired"])
    for k in ("lost_reach", "lost_hw", "lost_unwired", "delivered", "plan_kw"):
        ok("A3 %s recomputes to %s" % (k, Fj[k]), abs(g[k] - Fj[k]) <= 1.0, "%.2f" % g[k])
    ok("A3 the plan's cost per kW-year recomputes", round(g["plan_cost_per_kw"], 1) == Fj["plan_cost_per_kw"])
    ok("A4 the counts recompute", n_s == Fj["counts"]["switches"] and len(step) == Fj["counts"]["steps"]
       and int(flag.sum()) == Fj["counts"]["flagged"] and cnt["recon_in"] == Fj["counts"]["recon_in"])
    funded = [m for m in C.MEMBERS if g[m] >= ln[m]]
    ok("A5 the funded set recomputes", funded == ["rep_w", "fix_t", "recon_in"])
    # ---- the golden deliverables against figures.json ----
    gdir = os.path.join(TASK, "golden")
    hc, cr = table(os.path.join(gdir, "load_management_proposals_2027.csv"))
    ok("D1 the golden CSV has a row per proposal", len(cr) == 6)
    for r in cr:
        m = next(k for k, v in Fj["proposals"].items() if v["name"] == r[1])
        ok("D1 %s: CSV kW and break-even agree" % r[1], int(r[4]) == Fj["proposals"][m]["kw"] and int(r[7]) == Fj["proposals"][m]["breakeven"]
           and (r[10] == "yes") == Fj["proposals"][m]["funded"])
    wb = load_workbook(os.path.join(gdir, "load_management_trial_2026.xlsx"), read_only=True)
    ok("D2 the workbook's first sheet states the call", wb.sheetnames[0] == "Call" and
       any(isinstance(c, str) and c.startswith("Fund the Kettle Ridge VHF repeater") for row in wb["Call"].iter_rows(values_only=True) for c in row))
    br = {r[0]: r[1] for r in wb["Bridge"].iter_rows(min_row=2, values_only=True) if r[0]}
    ok("D2 the workbook's bridge agrees", br.get("Delivered") == Fj["delivered"] and br.get("Commands not received") == -Fj["lost_reach"])
    z = zipfile.ZipFile(os.path.join(gdir, "load_management_2027_board.pptx"))
    slides = sorted(n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n))
    s1 = z.read("ppt/slides/slide1.xml").decode()
    ok("D3 the deck's first slide states the call", "Fund the Kettle Ridge VHF repeater" in s1 and len(slides) == 3, "%d slides" % len(slides))
    # ---- every format the pack ships reads back ----
    plan_xml = zipfile.ZipFile(T("work_plan_2027_load_management.docx")).read("word/document.xml").decode()
    ok("E1 the work plan's appraisal reads back", "USD 88 a kW-year" in plan_xml and "1.15" in plan_xml)
    inv = subprocess.run(["pdftotext", T("wholesale_invoices_2026.pdf"), "-"], capture_output=True, text=True).stdout
    rep = subprocess.run(["pdftotext", T("load_management_report_2025.pdf"), "-"], capture_output=True, text=True).stdout
    ok("E2 the invoices read back (four statements)", inv.count("Billing demand") == 4)
    ok("E2 the 2025 report reads back", "planning figure" in rep)
    png = open(T("tricounty_coverage_map_2026.png"), "rb").read(24)
    ok("E3 the coverage map is a PNG", png[:8] == b"\x89PNG\r\n\x1a\n")
    fails = [o for o in OUT if not o[1]]
    for lab, good, det in OUT:
        print("%s  %-80s %s" % ("PASS" if good else "FAIL", lab[:80], det))
    print("%s  task7 verify: %d checks, %d FAIL" % ("FAIL" if fails else "PASS", len(OUT), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    tgt = sys.argv[sys.argv.index("--target") + 1] if "--target" in sys.argv else os.path.join(TASK, "target")
    sys.exit(main(tgt))
