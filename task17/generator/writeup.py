"""figures.json and submission.md, every figure emitted from the golden's computation on the shipped pack (never
typed), at the rounding the prompt names: the cap in steps of 10,000 node-hours, grant use to the nearest 10,000,
node-hours to the nearest 1,000, hours whole, repair days to a half, the share of work beyond 48 hours to the nearest
5 per cent, other shares to the nearest per cent."""
import golden as GD

STEP = GD.STEP


def r(x, unit):
    return int(round(x / unit) * unit)


def pct(x, unit=1):
    return int(round(100.0 * x / unit) * unit)


def fmt(n):
    return "{:,}".format(int(n))


def figures(pk, g):
    cap = int(g["cap"])
    fine = g["cap_fine"]
    req = g["requests_total"]
    r1, r4, r5 = g["r1"], g["r4"], g["r5"]
    fam = g["r3"][g["family"]]
    weib = g["r3"]["weibull"]
    routes = g["routes"]
    passing = {k: v for k, v in g["r3"].items() if not k.startswith("_") and v["passes"]}
    lost = {str(q): r(v, 10) for q, v in r4["quarters"].items()}
    f = {
        "cap": cap, "cap_str": fmt(cap), "cap_next_str": fmt(cap + STEP), "cap_prev_str": fmt(cap - STEP),
        "requests_total": int(round(req)), "requests_str": fmt(int(round(req))),
        "cut_share_pct": pct(1.0 - cap / req),
        "p_at_cap_pct": pct(fine[str(cap)]["p"]), "p_next_pct": pct(fine[str(cap + STEP)]["p"]),
        "p_prev_pct": pct(fine[str(cap - STEP)]["p"]) if str(cap - STEP) in fine else None,
        "p_by_step": {k: round(v["p"], 3) for k, v in fine.items()},
        "n_futures": g["cap_fine"][str(cap)]["n"],
        "expected_use_at_cap": r(g["expected_use_at_cap"], 10000), "expected_use_at_cap_str": fmt(r(g["expected_use_at_cap"], 10000)),
        "expected_use_requests": r(g["expected_use"]["age"], 10000), "expected_use_requests_str": fmt(r(g["expected_use"]["age"], 10000)),
        "expected_use_pooled": r(g["expected_use"]["pooled"], 10000),
        "expected_use_grant": r(g["expected_use"]["grant"], 10000),
        "backtest_p90_h": int(round(g["backtest"]["mean"])), "backtest_p90_raw": round(g["backtest"]["mean"], 2),
        "backtest_p90_median": round(g["backtest"]["median"], 2),
        "report_p90_h": int(round(r1["report_p90"])), "report_p90": round(r1["report_p90"], 2),
        "backtest_routes": {k: round(v, 2) for k, v in g["backtest_routes"].items()},
        "backtest_careful_h": int(round(g["backtest_routes"]["careful but hurried"])),
        "use_new_pct": pct(g["ratios"]["new"]), "use_cont_pct": pct(g["ratios"]["cont"]), "use_pooled_pct": pct(g["ratios"]["pooled"]),
        "use_new_raw": round(g["ratios"]["new"], 4), "use_cont_raw": round(g["ratios"]["cont"], 4),
        "burst_index": int(round(g["burst"]["utc"])), "burst_index_raw": round(g["burst"]["utc"], 2),
        "burst_variants": {k: round(v, 2) for k, v in g["burst"].items()},
        "mean96_h": int(round(fam["mean96"])), "mean96_raw": round(fam["mean96"], 2),
        "share48_pct": pct(fam["share48"], 5), "share48_raw": round(100 * fam["share48"], 1),
        "family": g["family"],
        "families": {k: {"mean96": round(v["mean96"], 2), "share48_pct": round(100 * v["share48"], 1), "passes": bool(v["passes"]),
                         "z": round(v["validation"]["z"], 2)} for k, v in g["r3"].items() if not k.startswith("_")},
        "passing_mean96_range": [round(min(v["mean96"] for v in passing.values()), 2), round(max(v["mean96"] for v in passing.values()), 2)],
        "passing_share48_range": [round(100 * min(v["share48"] for v in passing.values()), 1), round(100 * max(v["share48"] for v in passing.values()), 1)],
        "weibull_mean96_h": int(round(weib["mean96"])), "weibull_share48_pct": pct(weib["share48"], 5),
        "weibull_mean96_raw": round(weib["mean96"], 2), "weibull_share48_raw": round(100 * weib["share48"], 1), "weibull_z": round(weib["validation"]["z"], 1),
        "cut48_mean96_h": int(round(g["r3"]["_cut48"]["mean96"])), "cut48_mean96_raw": round(g["r3"]["_cut48"]["mean96"], 2),
        "validation_n": fam["validation"]["n"], "validation_n_beyond": fam["validation"]["n_beyond"],
        "q3_jobs": r(r1["jobs"], 10), "q3_jobs_raw": int(r1["jobs"]), "q3_nh": r(r1["nh"], 1000), "q3_nh_raw": round(r1["nh"], 1),
        "q3_delivered": round(r1["delivered"], 1), "q3_report_delivered": round(r1["report_delivered"], 1),
        "q3_segments": int(r1["segments_started"]), "q3_jobs_by_submit": int(r1["jobs_by_submit"]),
        "lost_by_quarter": lost, "lost_q_mean_str": fmt(r(sum(r4["quarters"][q] for q in (1, 2, 3)) / 3.0, 10)),
        "lost_raw": {str(q): round(v, 1) for q, v in r4["quarters"].items()},
        "multi_share_pct": pct(r4["share_multi"]), "multi_share_raw": round(100 * r4["share_multi"], 2),
        "repair_software_h": int(round(r4["median_software_h"])), "repair_software_raw": round(r4["median_software_h"], 2),
        "repair_hardware_d": round(r4["median_hardware_d"] * 2) / 2.0, "repair_hardware_raw": round(r4["median_hardware_d"], 2),
        "repair_hardware_d_str": ("%.1f" % (round(r4["median_hardware_d"] * 2) / 2.0)).rstrip("0").rstrip("."),
        "repair_rack_h": int(round(r4["median_rack_h"])), "repair_rack_raw": round(r4["median_rack_h"], 2),
        "n_rack_events": int(r4["n_rack_events"]), "outage_counts": {k: int(v) for k, v in r4["counts"].items()},
        "rows_not_rejoined": {"software_h": round(g["r4_rows"]["median_software_h"], 2), "hardware_d": round(g["r4_rows"]["median_hardware_d"], 2),
                              "rack_h": round(g["r4_rows"]["median_rack_h"], 2)},
        "rework_pct": pct(r5["share"]), "rework_raw": round(100 * r5["share"], 2), "rework_stem_raw": round(100 * g["r5_stem"]["share"], 2),
        "rework_whole_segment_pct": pct(r5["whole_segment_share"]), "rework_whole_raw": round(100 * r5["whole_segment_share"], 2),
        "rework_requeued": int(r5["n_requeued"]), "rework_covered": int(r5["n"]), "rework_frac": round(r5["frac"], 3),
        "ckpt_mix": g["ckpt_mix"],
        "quick_cap": r(g["quick_cap"], STEP), "quick_cap_raw": round(g["quick_cap"]),
        "route_caps": {k: int(v["cap"]) for k, v in routes.items()},
        "route_quick_str": fmt(r(g["quick_cap"], STEP)),
        "route_careful_str": fmt(routes["careful but hurried"]["cap"]),
        "route_poisson_str": fmt(routes["Poisson submissions"]["cap"]),
        "route_notail_str": fmt(routes["the tail cut at the limit"]["cap"]),
        "route_weibull_str": fmt(routes["a Weibull tail by AIC"]["cap"]),
        "route_const_str": fmt(routes["constant availability"]["cap"]),
        "route_norework_str": fmt(routes["no rework after failures"]["cap"]),
        "route_indep_str": fmt(routes["independent node failures"]["cap"]),
        "route_pooled_str": fmt(routes["one pooled use ratio"]["cap"]),
        "route_flat_str": fmt(routes["sessions spread evenly over the year"]["cap"]),
        "route_cuts_pct": {k: pct(max(0.0, 1.0 - v["cap"] / req)) for k, v in routes.items()},
        "rivals": {k: {"cap": int(v["cap"]) if v["cap"] else None, "p_at_cap": round(v["p"][str(cap)], 3), "p_next": round(v["p"][str(cap + STEP)], 3)}
                   for k, v in g["rivals"].items()},
        "hazard_per_1000": [round(1000 * x, 2) for x in g["outage"]["sw_hazard"]],
        "hw_per_node_year": round(g["outage"]["hw_rate"] * 8760, 2), "switch_per_rack_year": round(g["outage"]["switch_rate"], 2),
        "pdu_per_rack_year": round(g["outage"]["pdu_rate"], 2), "mean_availability": round(g["outage"]["mean_availability"], 4),
        "conventions": {"level_h": 4, "probability_pct": 80, "step": STEP, "limit_2027_h": 96, "limit_now_h": 48,
                        "limit_before_h": 24, "change_date": "2026-05-03", "nodes": 64, "racks": 8},
    }
    return f


def write(path, pk, g, f):
    rc = f["route_caps"]
    lost = f["lost_by_quarter"]
    q4 = (", 2026 Q4 to 15 November %s" % fmt(lost["4"])) if "4" in lost else ""
    txt = """## Tags

**Domain:** General Statistics & Data Science, Resampling, simulation & Monte Carlo methods (sizing a shared GPU partition's allocation round under a queue-wait service level).
**Analytical objective:** Descriptive & Distribution Analysis.

## Final Recommendation

**Cap the 2027 round at {cap} node-hours of grants, which cuts the {req} node-hours requested by {cut} per cent pro rata.** At {cap} node-hours the partition meets its service level (a 90th-percentile queue wait of at most 4 hours over 2027) in {pcap} per cent of simulated years and at {capnext} in {pnext} per cent; the arithmetic of node-hours available over the pooled use ratio ({quick}) cuts nothing, and every input in its hurried form together (a Weibull tail chosen by AIC, a constant availability, no rework after failures, one pooled use ratio) caps at {careful}, because each understates the queue's variance or its load.

## Supplementary Questions

### gpu_round_2027.xlsx

1. Sheet Cap 2027: the cap {cap} node-hours, the requests {req} node-hours, the cut {cut} per cent, the expected use at the cap {eucap} node-hours; one row per step of 10,000 node-hours around the cap with the share of {nf} simulated years meeting the level: {steps}; the same share at the cap and at the next step under EASY backfill, without the inputs' sampling error and over 4,000 futures, each giving the cap {cap}.
2. Sheet Backtest Q3 2026: built on the record to 30 June 2026, the forecast's 90th-percentile wait for the jobs eligible in July to September 2026 is {bt} hours (mean over {nbt} futures, {btraw}), against {rep} hours in the capacity report ({repraw}); the same quarter with every input in its hurried form gives {btcare} hours.
3. Sheet Grants and use: first-year projects used {unew} per cent of their 2024 and 2025 grants and continuing projects {ucont} per cent; at those shares the round's {req} node-hours of requests would turn into {eureq} node-hours of use.
4. Sheet Run times: under the 96 hour limit a normal job runs {m96} hours on average and {s48} per cent of normal work lies beyond the 48th hour (the {family} family; the families that reproduce the 24 to 48 hour window after the May 2026 change span {m96lo} to {m96hi} hours and {s48lo} to {s48hi} per cent); the Weibull, chosen by AIC on the censored record, gives {wm96} hours and {ws48} per cent and fails the window; the record cut at 48 hours gives {c48} hours and 0 per cent.
5. Sheet Q3 2026 record: {q3j} jobs became eligible in July to September 2026 and used {q3nh} node-hours; their clock-apportioned delivery rebuilds the capacity report's {q3del} node-hours exactly (the quarter's accounting rows count {q3seg} runs, not jobs).
6. Sheet Outages 2026: node-days lost outside maintenance windows 2026 Q1 {l1}, Q2 {l2}, Q3 {l3}{q4}; {multi} per cent of them while four or more nodes of one rack were down together; the usual repair takes {rsw} hour for a software failure, {rhw} days for a hardware replacement and {rrk} hours for a rack event (medians).
7. Sheet Rework 2026: {rw} per cent of 2026's node-hours were redone after node failures (requeued jobs' elapsed over every run less the run time of like jobs, scaled to every requeued job); counting every killed run whole would give {rww} per cent.
8. Sheet Routes: each shortcut's cap beside the adopted one: node-hours arithmetic {quick}; every hurried input together {careful}; Poisson submissions {poisson}; the tail cut at the limit {notail}; a Weibull tail by AIC {weibull}; constant availability {const}; no rework {norework}; independent node failures {indep}; one pooled use ratio {pooled}.

### gpu_round_2027_note.docx

9. One page: the recommendation (the cap {cap}, the cut {cut} per cent, {pcap} per cent of years meeting the level against {pnext} at {capnext}), the basis in one paragraph (the four fitted inputs with the figures above and the backtest {bt} against {rep} hours), and what each shortcut gives.

## Critical Components

1. Grants turn into use at **{unew} per cent** in a project's first year and **{ucont} per cent** after it, so the requests would turn into **{eureq}** node-hours; hourly submission counts in January to June 2026 are **{burst}** times as dispersed as a Poisson stream about their hour-of-week means (sessions of near-identical jobs), so the demand is resampled by session, never drawn at an hourly mean.
2. Of the run-time families fitted to jobs censored at their limits, those that reproduce the 24 to 48 hour window of the limit-requesting jobs after the May 2026 change give a mean run time of **{m96} hours** under the 96 hour limit and **{s48} per cent** of normal work beyond the 48th hour; the Weibull the AIC prefers fails the window (z {wz}) and gives {wm96} hours and {ws48} per cent.
3. 2026 lost **{l1}, {l2} and {l3}** node-days to outages in its three full quarters, **{multi} per cent** of them while four or more nodes of a rack were down together (a switch or power feed), with median repairs of {rsw} hour (software), **{rhw} days** (hardware) and **{rrk} hours** (rack), so availability is a clustered process, not a constant.
4. **{rw} per cent** of 2026's node-hours were redone after node failures, from requeued jobs' excess over like jobs by each project's checkpointing (not the {rww} per cent of counting every killed run whole, nor zero).
5. Built on the record to June and run for July to September 2026, the simulation gives a 90th-percentile wait of **{bt} hours** against **{rep}** in the capacity report; every hurried input together gives {btcare}.

## Step-by-Step

1. Rebuilt the job record from `sacct_gpu_2024-01_2026-11.csv`: the monthly batches de-duplicated (a job in the system across a month boundary appears in both, and August 2026 was exported twice), a job's runs gathered under its id and submission (the counter wrapped at MaxJobId, so an id alone names two jobs), submit and eligible in UTC beside start and end in local time, limits and elapsed from day-hour strings; jobs eligible in July to September 2026 {q3j} with {q3nh} node-hours, their clock-apportioned delivery matching `gpu_capacity_report_2024-2026.xlsx` at {q3del}; counting rows gives {q3seg}.
2. From `allocations_gpu_2023-2027.xlsx` and the job record, the share of granted node-hours used in the completed years 2024 and 2025 by standing (policy 3.3): first-year {unew} per cent, continuing {ucont} per cent; applied to the 2027 requests by standing: {eureq} node-hours (one pooled ratio gives {eupool}, the grants themselves {eugrant}); hourly submission counts in January to June 2026 are {burst} times as dispersed as Poisson about their hour-of-week means, so the forecast resamples each project's recorded sessions (hour of week, size, nodes, limits, run times) and places them by its category's weekly profile.
3. Run-time families (Weibull, lognormal, log-logistic, generalised gamma, two-component mixtures) fitted by maximum likelihood to normal jobs censored at their limits (policy 2.7), stratified by job kind, node count and whether the job's family requests the limit; each fitted on jobs before 3 May 2026 and tested on the limit-requesting jobs after it that ran beyond 24 hours ({nbeyond} of {nval}): the shape they predict for 24 to 48 hours against what ran; the families within three standard errors kept and the {family} used: {m96} hours mean under 96 hours, {s48} per cent of work beyond 48; the Weibull (z {wz}) gives {wm96} and {ws48}, the record cut at 48 gives {c48} and 0.
4. From `node_events_sturmvogel_2024-2026.csv` joined to `rack_layout_gpu.csv`: rows cut by the controller restarts in `slurm_config_history_sturmvogel.txt` rejoined, reasons classed (reboot, part replaced, switch or PDU), maintenance windows from `maintenance_calendar_2024-2027.xlsx` excluded: node-days lost {l1}, {l2}, {l3}, {multi} per cent while four or more nodes of a rack were down; medians {rsw} hour, {rhw} days, {rrk} hours; the process fitted for the simulation: a software hazard rising with uptime since the node's last reset ({hz0} to {hz6} per 1,000 node-hours), {hw} hardware failures per node-year, {sw} switch and {pdu} PDU events per rack-year taking a rack's nodes together, repair times resampled by class and hour of failure.
5. Rework: requeued jobs' elapsed over every run less the run time of the same session's jobs that ran through, by project ({rwcov} of {rwreq} requeued jobs with a reference, the rest at the covered jobs' redone share of killed time): {rw} per cent of 2026's node-hours, each project's checkpointing read from its requeues (none, hourly, six-hourly) for the simulation; counting killed runs whole gives {rww} per cent.
6. The simulation: the scheduler as `slurm_config_history_sturmvogel.txt` states it (first come first served by eligible time, conservative backfill on requested walltime over whole nodes, requeue after a node failure from the last checkpoint), the 2027 maintenance calendar, the normal limit at 96 hours from 1 April 2027 with limit-requesting jobs requesting it and censored run times extended by the family's tail; built on the record to June and run for July to September 2026 it gives a 90th-percentile wait of {bt} hours against the report's {rep} (every hurried input together: {btcare}).
7. 2027 at each step of 10,000 node-hours of grants, {nf} futures each with the jobs, failures and repairs redrawn and every fitted rate redrawn from its sampling error (policy 3.4): the share of years at or under 4 hours {steps}; the largest step at or above 80 per cent is {cap}, under EASY backfill, without the inputs' sampling error, over 4,000 futures and under each passing family alike; the cut of the {req} requested is {cut} per cent, the expected use at the cap {eucap} node-hours.
8. The routes: node-hours available at the mean availability over the pooled ratio {quick} (no cut); Poisson submissions {poisson}; the tail cut at the limit {notail}; a Weibull tail {weibull}; constant availability {const}; no rework {norework}; independent failures {indep}; one pooled ratio {pooled}; all hurried inputs together {careful}.

No other conclusion survives the files and the policy: the cap is the largest 10,000 step whose expected use, by standing, meets the level in 80 per cent of outcomes that carry the jobs, failures, repairs and the rates' sampling error (policy 3.3 and 3.4), and every shortcut lands higher by a different amount because it drops variance (Poisson submissions, constant availability, independent failures), load (no rework, one pooled ratio) or the tail the raised limit releases (a Weibull or a cut at 48 hours). The arithmetic of hours available answers the plan's capacity line, not the policy's.
""".format(
        cap=f["cap_str"], req=f["requests_str"], cut=f["cut_share_pct"], pcap=f["p_at_cap_pct"], capnext=f["cap_next_str"],
        pnext=f["p_next_pct"], quick=f["route_quick_str"], careful=f["route_careful_str"], eucap=f["expected_use_at_cap_str"],
        nf=f["n_futures"], steps="; ".join("%s: %d per cent" % (fmt(int(k)), pct(v)) for k, v in sorted(f["p_by_step"].items(), key=lambda kv: int(kv[0]))),
        bt=f["backtest_p90_h"], nbt=g["backtest"]["n"], btraw=f["backtest_p90_raw"], rep=f["report_p90_h"], repraw=f["report_p90"],
        btcare=f["backtest_careful_h"], unew=f["use_new_pct"], ucont=f["use_cont_pct"], eureq=f["expected_use_requests_str"],
        m96=f["mean96_h"], s48=f["share48_pct"], family=f["family"].replace("_", " "), m96lo=f["passing_mean96_range"][0], m96hi=f["passing_mean96_range"][1],
        s48lo=f["passing_share48_range"][0], s48hi=f["passing_share48_range"][1], wm96=f["weibull_mean96_h"], ws48=f["weibull_share48_pct"],
        c48=f["cut48_mean96_h"], q3j=fmt(f["q3_jobs"]), q3nh=fmt(f["q3_nh"]), q3del=fmt(round(f["q3_report_delivered"])), q3seg=fmt(f["q3_segments"]),
        l1=fmt(lost["1"]), l2=fmt(lost["2"]), l3=fmt(lost["3"]), q4=q4, multi=f["multi_share_pct"], rsw=f["repair_software_h"],
        rhw=f["repair_hardware_d_str"], rrk=f["repair_rack_h"], rw=f["rework_pct"], rww=f["rework_whole_segment_pct"],
        poisson=f["route_poisson_str"], notail=f["route_notail_str"], weibull=f["route_weibull_str"], const=f["route_const_str"],
        norework=f["route_norework_str"], indep=f["route_indep_str"], pooled=f["route_pooled_str"], burst=f["burst_index"],
        wz=f["weibull_z"], eupool=fmt(f["expected_use_pooled"]), eugrant=fmt(f["expected_use_grant"]),
        nbeyond=f["validation_n_beyond"], nval=f["validation_n"], hz0=f["hazard_per_1000"][0], hz6=f["hazard_per_1000"][6],
        hw=f["hw_per_node_year"], sw=f["switch_per_rack_year"], pdu=f["pdu_per_rack_year"], rwcov=f["rework_covered"], rwreq=f["rework_requeued"])
    open(path, "w", encoding="utf-8").write(txt)
