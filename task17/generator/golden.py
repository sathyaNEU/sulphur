"""The golden: every figure computed from the shipped files alone (load.py rebuilds the tables, analysis.py fits
the inputs and runs the simulation), the rivals and the routes beside it, and the two deliverables the prompt asks
for: gpu_round_2027.xlsx (the cap and the cut, the per-step probabilities, the backtest, the use of grants and the
round's expected use, the Q3 2026 record, the outage and rework figures, a routes sheet) and gpu_round_2027_note.docx
(one page for the board)."""
import datetime as dt
import json
import os

import numpy as np
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Mm, Pt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import analysis as A
import load as L
import params as P
import postprocess
import sim

XLSX = "gpu_round_2027.xlsx"
DOCX = "gpu_round_2027_note.docx"
HERE = os.path.dirname(os.path.abspath(__file__))
STEP = 10000
LEVEL = 4.0
N_FINE = 2000
N_COARSE = 200
N_ROUTE = 500
N_RIVAL = 800
N_BACKTEST = 1000
OPT_GOLD = {"param_draw": True, "ratio_draw": True}

ROUTES = [
    # name, family override, options (each a hurried form of one input; the careful pass is their union)
    ("careful but hurried", "weibull", {"weibull": True, "const_avail": True, "no_rework": True, "ratio_how": "pooled"}),
    ("Poisson submissions", None, {"poisson": True}),
    ("the tail cut at the limit", None, {"no_tail": True, "no_habit": True}),
    ("a Weibull tail by AIC", "weibull", {"weibull": True}),
    ("constant availability", None, {"const_avail": True}),
    ("no rework after failures", None, {"no_rework": True}),
    ("independent node failures", None, {"independent": True}),
    ("one pooled use ratio", None, {"ratio_how": "pooled"}),
    ("sessions spread evenly over the year", None, {"flat_profile": True}),
]
REPLAY_VARIANTS = ["careful but hurried", "constant availability", "no rework after failures", "independent node failures"]
RIVALS = [
    ("EASY backfill", None, {"mode": 0}),
    ("no parameter uncertainty", None, {}),
    ("4,000 futures", None, OPT_GOLD),
]


def r10(x, step=STEP):
    return int(round(x / step) * step)


def compute(target, quick=False, cache=True):
    """every figure; quick=True runs the small sweeps (for checks and tests)"""
    pk = L.load_pack(target)
    g = {}
    g["r1"] = A.assembly(pk)
    g["ratios"] = A.use_ratios(pk)
    g["expected_use"] = {how: A.expected_use(pk, g["ratios"], how=how) for how in ("age", "pooled", "bycat", "grant")}
    g["requests_total"] = float(pk.requests["requested"].sum())
    g["burst"] = {"utc": A.burst_index(pk)[0], "local": A.burst_index(pk, clock="local")[0], "ran": A.burst_index(pk, population="ran")[0],
                  "raw_vmr": A.burst_index(pk)[1]}
    F = A.fit_all(pk, pk.cut_h)
    g["family"] = F.family
    g["r3"] = {fam: {k: v for k, v in d.items() if k != "fit"} for fam, d in F.r3["families"].items()}
    g["r3_strata"] = F.r3["strata"]
    # the stratification rival: by node count only
    r3n = A.r3(pk, strata="nodes", families=[F.family])
    g["r3_nodes_strata"] = {k: v for k, v in r3n["families"][F.family].items() if k != "fit"}
    # requeued jobs included, elapsed summed over runs
    d_rq = A.duration_data(pk, pk.cut_h, include_requeued=True)
    fit_rq = A.fit_family(F.family, d_rq)
    g["r3_with_requeued"] = dict(zip(("mean96", "share48"), A.r3_figures(fit_rq, A.class_mix(d_rq), None)))
    g["r4"] = F.outage_record
    g["r4_rows"] = A.outage_record(pk, A.intervals(pk, rejoin=False))
    g["outage"] = {k: (float(v) if np.isscalar(v) else None) for k, v in F.outage.items() if k != "repair"}
    g["outage"]["sw_hazard"] = [float(x) for x in F.outage["sw_hazard"]]
    g["r5"] = {k: v for k, v in F.rework.items() if k not in ("per_project", "rows")}
    g["r5_stem"] = {k: v for k, v in A.rework(pk, like="stem").items() if k not in ("per_project", "rows")}
    g["ckpt_mix"] = {str(k): sum(1 for v in F.ckpt.values() if v == k) for k in (0.0, 1.0, 6.0)}
    n_bt = 200 if quick else N_BACKTEST
    F6 = A.fit_all(pk, A.H(2026, 7, 1), family=F.family)
    g["family_june"] = F6.family
    # the backtest: the quarter's own jobs through the simulator, the outage and rework processes fitted to June
    bt = A.run_futures(F6, pk, 2026, None, n_bt, {"param_draw": True}, window=A.quarter(2026, 3), seed0=5000, kind="replay")
    g["backtest"] = {"mean": float(np.mean([r["p90"] for r in bt])), "median": float(np.median([r["p90"] for r in bt])),
                     "sd": float(np.std([r["p90"] for r in bt])), "n": n_bt, "report": g["r1"]["report_p90"],
                     "nh_mean": float(np.mean([r["nh"] for r in bt])), "record_nh": g["r1"]["nh"]}
    g["backtest_routes"] = {}
    for name, fam, opt in ROUTES:
        if name not in REPLAY_VARIANTS:
            continue
        o = {"param_draw": True}; o.update({k: v for k, v in opt.items() if k in ("const_avail", "no_rework", "independent")})
        r = A.run_futures(F6, pk, 2026, None, max(100, n_bt // 4), o, window=A.quarter(2026, 3), seed0=5100, kind="replay")
        g["backtest_routes"][name] = float(np.mean([x["p90"] for x in r]))
    for name, fam, opt in RIVALS[:2]:
        o = {"param_draw": True}; o.update(opt)
        if "no parameter" in name:
            o = {}
        r = A.run_futures(F6, pk, 2026, None, max(100, n_bt // 4), o, window=A.quarter(2026, 3), seed0=5200, kind="replay")
        g["backtest_routes"][name] = float(np.mean([x["p90"] for x in r]))
    # the cap
    n_fine = 400 if quick else N_FINE
    cap = A.find_cap(F, pk, OPT_GOLD, n_coarse=N_COARSE, n_fine=n_fine, step=STEP, seed0=7000, lo=150000, hi=900000)
    g["cap"] = cap["cap"]
    g["cap_fine"] = {str(k): v for k, v in sorted(cap["fine"].items())}
    g["cap_coarse"] = {str(k): v for k, v in sorted(cap["coarse"].items())}
    g["cut_share"] = 1.0 - g["cap"] / g["requests_total"]
    g["expected_use_at_cap"] = A.expected_use(pk, g["ratios"], T=g["cap"])
    g["quick_cap"] = A.quick_cap(F, pk)
    # rivals at the deciding steps
    steps = [g["cap"] - STEP, g["cap"], g["cap"] + STEP]
    n_riv = 300 if quick else N_RIVAL
    g["rivals"] = {}
    for name, fam, opt in RIVALS:
        o = dict(OPT_GOLD); o.update(opt)
        if "no parameter" in name:
            o = {}
        n = (800 if quick else 4000) if "4,000" in name else n_riv
        sw = A.cap_sweep(F, pk, steps, n, o, seed0=7100)
        g["rivals"][name] = {"p": {str(k): v["p"] for k, v in sw.items()}, "cap": A.cap_from_sweep(sw)}
    for fam in [f for f, v in g["r3"].items() if not f.startswith("_") and v["passes"] and f != F.family]:
        Ff = A.fit_all(pk, pk.cut_h, family=fam)
        sw = A.cap_sweep(Ff, pk, steps, n_riv, OPT_GOLD, seed0=7100)
        g["rivals"]["family: " + fam] = {"p": {str(k): v["p"] for k, v in sw.items()}, "cap": A.cap_from_sweep(sw)}
    # the routes' caps
    n_route = 200 if quick else N_ROUTE
    g["routes"] = {}
    for name, fam, opt in ROUTES:
        Fr = A.fit_all(pk, pk.cut_h, family=fam) if fam else F
        o = dict(OPT_GOLD); o.update(opt)
        c = A.find_cap(Fr, pk, o, n_coarse=N_COARSE, n_fine=n_route, step=STEP, seed0=7300, fine_span=2, lo=150000, hi=900000)
        g["routes"][name] = {"cap": c["cap"], "p": {str(k): v["p"] for k, v in sorted(c["fine"].items())}}
    g["routes"]["node-hours arithmetic (quick)"] = {"cap": r10(g["quick_cap"]), "p": {}}
    return g, pk, F


# ---------------------------------------------------------------- the deliverables
HEAD = PatternFill("solid", fgColor="D9E1EA")


def _head(ws, row):
    for c in ws[row]:
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")


def write_xlsx(path, g, pk, figs):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cap 2027"
    ws["A1"] = "gpu partition, allocation round 2027: the cap under allocation policy v3"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Largest multiple of 10,000 node-hours of grants whose expected use keeps the 90th percentile queue wait "
                "over 2027 at or under 4 hours in at least 80 per cent of simulated outcomes (policy 3.1 to 3.4).")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:F2")
    ws.row_dimensions[2].height = 32
    ws.append([])
    rows = [("Cap, node-hours of grants", figs["cap"]), ("Requests on file, node-hours", figs["requests_total"]),
            ("Share of the requests cut", figs["cut_share_pct"] / 100.0), ("Expected use at the cap, node-hours", figs["expected_use_at_cap"]),
            ("Expected use at the requests, node-hours", figs["expected_use_requests"]),
            ("Futures per step", figs["n_futures"])]
    for a, b in rows:
        ws.append([a, b])
        ws.cell(ws.max_row, 1).font = Font(bold=True)
    ws.cell(6, 2).number_format = "0%"
    ws.append([])
    ws.append(["Grants, node-hours", "Share of futures meeting the level", "Mean P90 wait, h", "Median P90 wait, h"])
    _head(ws, ws.max_row)
    for k, v in sorted(g["cap_fine"].items(), key=lambda kv: int(kv[0])):
        ws.append([int(k), round(v["p"], 3), round(v["p90_mean"], 2), round(v["p90_median"], 2)])
        ws.cell(ws.max_row, 2).number_format = "0.0%"
    ws.append([])
    ws.append(["Checked under", "Share meeting the level at the cap", "at the next step", "Cap"])
    _head(ws, ws.max_row)
    for name, v in g["rivals"].items():
        ws.append([name, round(v["p"][str(g["cap"])], 3), round(v["p"][str(g["cap"] + STEP)], 3), v["cap"]])
        ws.cell(ws.max_row, 2).number_format = "0.0%"
        ws.cell(ws.max_row, 3).number_format = "0.0%"
    for i, wd in enumerate([42, 30, 18, 18, 12, 12], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd

    ws2 = wb.create_sheet("Backtest Q3 2026")
    ws2.append(["Inputs fitted on the record to 30 June 2026; 2026 simulated under its grants; the 90th percentile "
                "queue wait of the jobs eligible in July to September 2026 (policy 2.1 and 2.2)"])
    ws2.append([])
    ws2.append(["Item", "Hours"])
    _head(ws2, 3)
    ws2.append(["Capacity report, Q3 2026", figs["report_p90"]])
    ws2.append(["Simulated, mean over %d futures" % g["backtest"]["n"], figs["backtest_p90_raw"]])
    ws2.append(["Simulated, median", round(g["backtest"]["median"], 2)])
    ws2.append(["Simulated, standard deviation across futures", round(g["backtest"]["sd"], 2)])
    ws2.append([])
    ws2.append(["The same quarter with one input in its hurried form", "Hours"])
    _head(ws2, ws2.max_row)
    for name, v in g["backtest_routes"].items():
        ws2.append([name, round(v, 2)])
    ws2.column_dimensions["A"].width = 52
    ws2.column_dimensions["B"].width = 12

    ws3 = wb.create_sheet("Grants and use")
    ws3.append(["Realised use of grants in the completed allocation years on record (2024 and 2025): node-hours of "
                "the project's jobs eligible in the grant year over the node-hours granted (policy 3.3)"])
    ws3.append([])
    ws3.append(["Standing", "Project-years", "Share of granted node-hours used"])
    _head(ws3, 3)
    ws3.append(["First year of funding", g["ratios"]["n_new"], figs["use_new_pct"] / 100.0])
    ws3.append(["Continuing", g["ratios"]["n_cont"], figs["use_cont_pct"] / 100.0])
    ws3.append(["Pooled (not used)", g["ratios"]["n_new"] + g["ratios"]["n_cont"], round(g["ratios"]["pooled"], 4)])
    for r in (4, 5, 6):
        ws3.cell(r, 3).number_format = "0.0%"
    ws3.append([])
    ws3.append(["Round 2027", "Node-hours"])
    _head(ws3, ws3.max_row)
    ws3.append(["Requests on file", figs["requests_total"]])
    ws3.append(["Expected use at the requests (by standing)", figs["expected_use_requests"]])
    ws3.append(["Expected use at the cap", figs["expected_use_at_cap"]])
    ws3.append(["Expected use at the requests on one pooled ratio (not used)", round(g["expected_use"]["pooled"])])
    ws3.append([])
    ws3.append(["Submissions, January to June 2026", "Value"])
    _head(ws3, ws3.max_row)
    ws3.append(["Hourly submission counts: variance over mean, about the hour-of-week means", figs["burst_index"]])
    ws3.append(["Raw variance over mean of the hourly counts", round(g["burst"]["raw_vmr"], 2)])
    ws3.column_dimensions["A"].width = 64
    ws3.column_dimensions["B"].width = 14
    ws3.column_dimensions["C"].width = 28

    ws4 = wb.create_sheet("Run times")
    ws4.append(["Run-time families fitted to normal jobs (policy 2.7), stratified by job kind, node count and whether "
                "the job's family requests the limit; fitted on jobs submitted before 3 May 2026 (limit 24 h) to "
                "predict the share of limit-requesting jobs after the change landing in 24 to 48 hours"])
    ws4.append([])
    ws4.append(["Family", "Predicted 24-48 h share", "Observed", "z", "Passes", "Mean run time under 96 h", "Share of work beyond 48 h", "AIC (whole record)"])
    _head(ws4, 3)
    for fam, v in g["r3"].items():
        if fam.startswith("_"):
            continue
        ws4.append([fam, round(v["validation"]["predicted"], 4), round(v["validation"]["observed"], 4), round(v["validation"]["z"], 2),
                    "yes" if v["passes"] else "no", round(v["mean96"], 2), round(v["share48"], 4), round(v["aic"])])
    ws4.append(["record cut at 48 h (no tail)", "", "", "", "no", round(g["r3"]["_cut48"]["mean96"], 2), 0.0, ""])
    ws4.append([])
    ws4.append(["Used: %s" % g["family"], "mean run time, nearest hour", figs["mean96_h"], "", "share beyond 48 h", figs["share48_pct"] / 100.0])
    ws4.cell(ws4.max_row, 6).number_format = "0%"
    ws4.append(["Observed after the change: %d limit-requesting jobs" % g["r3"][g["family"]]["validation"]["n"]])
    for i, wd in enumerate([30, 20, 11, 8, 8, 22, 22, 16], 1):
        ws4.column_dimensions[get_column_letter(i)].width = wd

    ws5 = wb.create_sheet("Outages 2026")
    ws5.append(["Node event log, rows cut by controller restarts rejoined, reasons classed per policy 2.5; node-days "
                "lost outside maintenance windows"])
    ws5.append([])
    ws5.append(["Quarter", "Node-days lost"])
    _head(ws5, 3)
    for q in (1, 2, 3, 4):
        if str(q) in figs["lost_by_quarter"]:
            ws5.append(["2026 Q%d%s" % (q, " (to 15 November)" if q == 4 else ""), figs["lost_by_quarter"][str(q)]])
    ws5.append([])
    ws5.append(["Share of node-days lost while four or more nodes of a rack were down together", figs["multi_share_pct"] / 100.0])
    ws5.cell(ws5.max_row, 2).number_format = "0%"
    ws5.append([])
    ws5.append(["Class", "Median repair", "Unit", "Events"])
    _head(ws5, ws5.max_row)
    ws5.append(["Software (reboot)", figs["repair_software_h"], "hours", g["r4"]["counts"].get("software", 0)])
    ws5.append(["Hardware (part replaced)", figs["repair_hardware_d"], "days", g["r4"]["counts"].get("hardware", 0)])
    ws5.append(["Rack infrastructure (switch or PDU)", figs["repair_rack_h"], "hours", g["r4"]["n_rack_events"]])
    ws5.append([])
    ws5.append(["Fitted process", "Value"])
    _head(ws5, ws5.max_row)
    hz = g["outage"]["sw_hazard"]
    for k, (a, b) in enumerate(zip(A.UPTIME_BINS[:-1], A.UPTIME_BINS[1:])):
        ws5.append(["Software failures per 1,000 node-hours at uptime %s" % ("%d to %d h" % (a, b) if b < 1e8 else "over %d h" % a), round(1000 * hz[k], 2)])
    ws5.append(["Hardware failures per node-year", round(g["outage"]["hw_rate"] * 8760, 2)])
    ws5.append(["Switch events per rack-year", round(g["outage"]["switch_rate"], 2)])
    ws5.append(["PDU events per rack-year", round(g["outage"]["pdu_rate"], 2)])
    ws5.append(["Mean availability outside maintenance, 2024 to 2026", round(g["outage"]["mean_availability"], 4)])
    ws5.column_dimensions["A"].width = 64
    ws5.column_dimensions["B"].width = 14

    ws6 = wb.create_sheet("Rework 2026")
    ws6.append(["Node-hours redone after node failures: requeued jobs' elapsed over every run less the run time of "
                "the same session's jobs that ran through, scaled to every requeued job; by project checkpointing"])
    ws6.append([])
    ws6.append(["Item", "Value"])
    _head(ws6, 3)
    ws6.append(["Share of 2026 node-hours redone", figs["rework_pct"] / 100.0])
    ws6.cell(ws6.max_row, 2).number_format = "0.0%"
    ws6.append(["Requeued jobs in 2026", g["r5"]["n_requeued"]])
    ws6.append(["With a like-job reference", g["r5"]["n"]])
    ws6.append(["Redone share of killed run time", round(g["r5"]["frac"], 3)])
    ws6.append(["If every killed run were counted whole", round(g["r5"]["whole_segment_share"], 4)])
    ws6.append(["Projects by inferred checkpointing: none / hourly / six-hourly",
                "%s / %s / %s" % (g["ckpt_mix"]["0.0"], g["ckpt_mix"]["1.0"], g["ckpt_mix"]["6.0"])])
    ws6.column_dimensions["A"].width = 64
    ws6.column_dimensions["B"].width = 20

    ws7 = wb.create_sheet("Q3 2026 record")
    ws7.append(["Jobs eligible 1 July to 30 September 2026 (local time), policy 2.2 to 2.4; accounting rows "
                "de-duplicated across the monthly batches, a job's runs gathered under its id and submission"])
    ws7.append([])
    ws7.append(["Item", "Value"])
    _head(ws7, 3)
    ws7.append(["Jobs eligible in the quarter", figs["q3_jobs"]])
    ws7.append(["Their node-hours", figs["q3_nh"]])
    ws7.append(["Node-hours delivered in the quarter (clock), rebuilt", round(g["r1"]["delivered"], 1)])
    ws7.append(["Node-hours delivered, capacity report", round(g["r1"]["report_delivered"], 1)])
    ws7.append(["Accounting rows that started in the quarter (runs, not jobs)", g["r1"]["segments_started"]])
    ws7.column_dimensions["A"].width = 64
    ws7.column_dimensions["B"].width = 14

    ws8 = wb.create_sheet("Routes")
    ws8.append(["Each shortcut's cap beside the one adopted (same policy, same records)"])
    ws8.append([])
    ws8.append(["Route", "Cap, node-hours", "Cut of the requests", "Backtest Q3 2026 P90, h"])
    _head(ws8, 3)
    ws8.append(["Adopted", figs["cap"], figs["cut_share_pct"] / 100.0, figs["backtest_p90_raw"]])
    ws8.cell(ws8.max_row, 3).number_format = "0%"
    for name, v in g["routes"].items():
        c = v["cap"]
        ws8.append([name, c, max(0.0, 1.0 - c / g["requests_total"]), round(g["backtest_routes"].get(name, float("nan")), 2) if name in g["backtest_routes"] else ""])
        ws8.cell(ws8.max_row, 3).number_format = "0%"
    ws8.column_dimensions["A"].width = 36
    ws8.column_dimensions["B"].width = 16
    ws8.column_dimensions["C"].width = 18
    ws8.column_dimensions["D"].width = 22
    wb.save(path)


def write_docx(path, g, pk, figs):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(20)
    sec.top_margin = sec.bottom_margin = Mm(18)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)

    def para(text, bold=False, size=None, after=4):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        p.paragraph_format.space_after = Pt(after)
        return p
    para("%s | Allocation committee | %s" % (P.ORG, "16 November 2026"), size=8)
    para("GPU allocation round 2027: cap the grants at %s node-hours" % figs["cap_str"], bold=True, size=13)
    para("Recommendation. Cap the 2027 round at %s node-hours of grants, which cuts the %s node-hours requested by "
         "%d per cent pro rata (policy 3.5). At that total the partition meets its service level (a 90th-percentile "
         "queue wait of at most 4 hours over 2027) in %s per cent of simulated years; at %s node-hours it would in %s "
         "per cent, under the 80 per cent the policy requires."
         % (figs["cap_str"], figs["requests_str"], figs["cut_share_pct"], figs["p_at_cap_pct"], figs["cap_next_str"],
            figs["p_next_pct"]))
    para("Basis. A simulation of the partition under its scheduler (first come first served by eligible time with "
         "backfill on requested walltime, whole nodes; the 2027 maintenance calendar; the normal limit at 96 hours from "
         "April) fed by four inputs fitted on the record. (1) Grants turn into use at %d per cent in a project's first "
         "year and %d per cent after it (2024 and 2025), so the requests would turn into %s node-hours; submissions "
         "arrive in sessions of near-identical jobs, with hourly counts %d times as dispersed as a Poisson stream, and "
         "the simulation resamples those sessions. (2) Run times are heavy-tailed: of the families fitted to jobs "
         "censored at their limits, those that reproduced the 24 to 48 hour mass seen after the May 2026 change were "
         "kept, and under 96 hours a normal job runs %d hours on average with %d per cent of the work beyond the 48th "
         "hour. (3) Nodes fail on a hazard that rises with uptime, hardware repairs take %s days, and a switch or power "
         "feed takes a rack's nodes together for about %d hours; 2026 lost %s node-days a quarter, %d per cent of them "
         "in those rack events. (4) A failure throws away the work since the job's last checkpoint: %d per cent of "
         "2026's node-hours were redone. Built on the record to June and run for July to September 2026, the "
         "simulation gives a 90th-percentile wait of %d hours against %d in the capacity report."
         % (figs["use_new_pct"], figs["use_cont_pct"], figs["expected_use_requests_str"], figs["burst_index"],
            figs["mean96_h"], figs["share48_pct"], figs["repair_hardware_d_str"], figs["repair_rack_h"],
            figs["lost_q_mean_str"], figs["multi_share_pct"], figs["rework_pct"], figs["backtest_p90_h"],
            figs["report_p90_h"]))
    para("What the shortcuts give. Node-hours available at the mean availability over the pooled use ratio: %s, no "
         "cut. Every input in its hurried form together (a Weibull tail by AIC, a constant availability, no rework, "
         "one pooled ratio): %s. One at a time: Poisson submissions %s; the tail cut at the limit %s; constant "
         "availability %s; no rework %s; independent node failures %s. Each understates the queue's variance or its "
         "load and lands the cap above the level the policy sets."
         % (figs["route_quick_str"], figs["route_careful_str"], figs["route_poisson_str"], figs["route_notail_str"],
            figs["route_const_str"], figs["route_norework_str"], figs["route_indep_str"]))
    para("Workbook: gpu_round_2027.xlsx (the cap and the per-step shares, the backtest, grants and use, run times, "
         "outages, rework, the Q3 2026 record, the routes). Mehdi Renner, HPC systems analyst.", size=8)
    doc.save(path)


def write(target, outdir, quick=False):
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        os.remove(os.path.join(outdir, f))
    g, pk, F = compute(target, quick=quick)
    import writeup as WU
    figs = WU.figures(pk, g)
    write_xlsx(os.path.join(outdir, XLSX), g, pk, figs)
    write_docx(os.path.join(outdir, DOCX), g, pk, figs)
    postprocess.normalize_ooxml(os.path.join(outdir, XLSX), "Mehdi Renner", "Mehdi Renner", "2026-11-16T09:12:00Z",
                                "2026-11-18T16:41:00Z", excel=True, company=P.ORG)
    postprocess.normalize_docx(os.path.join(outdir, DOCX), "Mehdi Renner", "Mehdi Renner", "2026-11-18T17:05:00Z",
                               "2026-11-19T08:28:00Z", 4, 112, "task17-note", title="GPU allocation round 2027", company=P.ORG)
    postprocess.own_mtimes(outdir, {})
    json.dump(_jsonable(g), open(os.path.join(HERE, "golden_state.json"), "w"), indent=1, sort_keys=True, default=str)
    return g, pk


def _jsonable(x):
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, np.ndarray):
        return [_jsonable(v) for v in x.tolist()]
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return x
