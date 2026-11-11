"""task20: figures.json (every figure the answer blocks and the goldens state, at the precision they state it) and
effort.json (each result's golden and band, the value each pass files, the precedents behind each careful-column loss,
the hints, the routes and the forcing), from one analysis run on the cut pack."""
import json
import os

import numpy as np

import analysis as A

HERE = os.path.dirname(os.path.abspath(__file__))


def m2(x):
    return float(round(x / 1e6 + 1e-12, 2))


def m3(x):
    return float(round(x / 1e6 + 1e-12, 3))


def ds(d):
    return d.date().isoformat()


def nice(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def make(R):
    P = R["P"]
    cls, window, prev = R["cls"], R["window"], R["prev"]
    union = R["union"]
    heads = {h: [d for d in union if cls[d] == h] for h in A.CODE}
    fam_counts = sorted(int(v) for v in R["fam_count"].values())
    fam_vol = sorted({sum(1 for v in c.values() if v == "volatility") for c in R["fam_cls"].values()})
    fam_acc = sorted({sum(1 for v in c.values() if v == "sound") for c in R["fam_cls"].values()})
    months = R["addon_months"]
    F = {
        "as_of": "2025-07-14",
        "window_end_text": "30 June 2025",
        "window_start_text": "1 July 2024",
        "window": [ds(window[0]), ds(window[-1])],
        "observations": len(window),
        "official_count": len(R["off"]),
        "official_zone": "Red",
        "exceptions_total": len(union),
        "hyp_count": len(R["hx"]),
        "hyp_only": len([d for d in R["hx"] if d not in R["off"]]),
        "booked_only": len([d for d in R["off"] if d not in R["hx"]]),
        "hyp_only_dates": [ds(d) for d in R["hx"] if d not in R["off"]],
        "booked_only_dates": [ds(d) for d in R["off"] if d not in R["hx"]],
        "exception_dates": [ds(d) for d in union],
        "heading_counts": {h: len(v) for h, v in heads.items()},
        "heading_dates": {h: [ds(d) for d in v] for h, v in heads.items()},
        "model_count": sum(len(heads[h]) for h in ("omitted", "volatility", "sound")),
        "outage_runs": len(R["outage_runs"]),
        "outage_run_dates": [ds(d) for d in R["outage_runs"]],
        "outage_occasions": occasions(P, R["outage_runs"]),
        "outage_exceptions": [ds(d) for d in R["outage_exc"]],
        "outage_caused": len(R["outage_caused"]),
        "cutoff_caused": len(R["cutoff_caused"]),
        "cutoff_dates": [ds(d) for d in R["cutoff_caused"]],
        "late_gross_median_m": m2(R["late_gross_median"]),
        "late_runs": int(R["runs_missing"]),
        "late_runs_assessed": len(window) - 1,
        "late_var_high_runs": int(sum(1 for d in window[1:] if R["late_var_effect"][d] < 0)),
        "late_var_effect_median_m": m3(float(np.median([R["late_var_effect"][d] for d in window[1:]]))),
        "sound_count": len(R["sound_days"]),
        "sound_dates": [ds(d) for d in R["sound_days"]],
        "sound_zone": zone(len(R["sound_days"])),
        "sound_family_counts": fam_counts,
        "sound_family_range": [fam_counts[0], fam_counts[-1]],
        "vol_family_range": [fam_vol[0], fam_vol[-1]],
        "acc_family_range": [fam_acc[0], fam_acc[-1]],
        "interp_inputs": sum(1 for v in R["interp_cls"].values() if v == "inputs"),
        "careful_inputs_dates": sorted(ds(d) for d, v in R["careful_cls"].items() if v == "inputs"),
        "careful_heading_counts": {h: sum(1 for v in R["careful_cls"].values() if v == h) for h in A.CODE},
        "careful_model_count": sum(1 for v in R["careful_cls"].values() if v in ("omitted", "volatility", "sound")),
        "shortcut_counts": {k: int(v) for k, v in R["shortcuts"].items()},
        "addon_months": months,
        "addon_m": [m2(x) for x in R["addon"]],
        "addon_unfloored_dec_m": m2(R["addon_unfloored"][-1]),
        "addon_full_m": [m2(p[0]) for p in R["addon_parts"]],
        "addon_engine_m": [m2(p[1]) for p in R["addon_parts"]],
        "addon_proxied": [int(x) for x in R["proxied_by_month"]],
        "addon_run_for": [ds(d) for d in R["addon_run_for"]],
        "addon_now_m": m2(R["addon_now"]),
        "addon_now_full_m": m2(R["addon_now_parts"][0]),
        "addon_now_engine_m": m2(R["addon_now_parts"][1]),
        "addon_prop_m": [m2(x) for x in R["addon_prop"]],
        "addon_ramp_only_m": [m2(x) for x in R["addon_ramp_only"]],
        "addon_grad_only_m": [m2(x) for x in R["addon_grad_only"]],
        "addon_family_m": {k: [m2(x) for x in v] for k, v in R["addon_family"].items()},
        "gross_30jun_m": {k: float(round(v / 1e6, 1)) for k, v in R["gross_30jun"].items()},
        "proxied_30jun": int(R["proxied_30jun"]),
        "proxied_small_share_pct": int(round(R["proxied_small_share"] * 100)),
        "graduations_by_month": grad_by_month(R),
        "plan_mid_m": [int(round(m["mid"] / 1e6)) for m in P["plan"]],
        "plan_small_m": [int(round(m["small"] / 1e6)) for m in P["plan"]],
        "plan_contracts": [{k: int(v) for k, v in b[1].items()} for b in R["addon_books"]],
        "rows": {},
        "pc_restated": int(R["pc_restated"]),
        "runs_logged": len(R["rep"]),
        "failed_runs": int(R["failed_runs"]),
        "flex_dates": sorted(sensitive_dates(R)),
        "constants": {"mrs4_sections_cited": "3.1 3.2 3.3 3.4 4 5 6 7", "hedge_pct": 86, "window_days": 500, "rank": 5, "decay": [0.94, 0.97], "zone_green_max": 4,
                      "zone_yellow_max": 9, "store_returns": 500, "es_mult": 50, "nq_mult": 20},
    }
    # one row per exception, in USD million at two decimals
    rows = []
    for d in union:
        p = prev[d]
        rows.append(dict(date=ds(d), run=ds(p), booked=m2(R["booked"][d]), hyp=m2(R["hyp"][d]), var=m2(R["vr"][d]),
                         on=("both" if (d in R["off"] and d in R["hx"]) else ("booked" if d in R["off"] else "hypothetical")),
                         heading=A.HEAD[cls[d]], code=A.CODE[cls[d]], good=m2(R["good"][d]), full=m2(R["full"][d]),
                         sound=m2(R["sound"][d]), late_gross=float(round(R["late_gross"][p] / 1e6, 1)),
                         reused=(p in R["outage_runs"]), careful=A.HEAD[R["careful_cls"][d]]))
    F["rows"] = rows
    F["cutoff_rows"] = [r for r in rows if r["date"] in F["cutoff_dates"]]
    F["outage_rows"] = [r for r in rows if r["date"] in F["outage_exceptions"]]
    # bands: the add-on months from the golden family (and the floor), two cents either side
    fam = [R["addon"]] + list(R["addon_family"].values())
    lo = [min(v[j] for v in fam) for j in range(len(months))]
    hi = [max(v[j] for v in fam) for j in range(len(months))]
    B = {"addon": [[float(round(lo[j] / 1e6 - 0.02, 2)), float(round(hi[j] / 1e6 + 0.02, 2))] for j in range(len(months))]}
    B["addon"] = [[max(0.0, x[0]), x[1]] for x in B["addon"]]
    B["sound_count"] = F["sound_family_range"]
    B["volatility"] = F["vol_family_range"]
    B["accuracy"] = F["acc_family_range"]
    F["bands"] = B
    hc = F["heading_counts"]
    F["r1_exceptions"] = {"exceptions": F["exceptions_total"], "hypothetical_only": F["hyp_only"],
                          "booked_only": F["booked_only"]}
    F["r3_inputs"] = {"inputs_dates": F["cutoff_dates"], "reused_extracts_caused": F["outage_caused"]}
    F["omitted_dates"] = F["heading_dates"]["omitted"]
    F["r5_sound"] = {"volatility": hc["volatility"], "sound_count": F["sound_count"], "zone": F["sound_zone"]}
    F["r6_headings"] = {r["date"]: r["code"] for r in rows}
    F["addon_jul_m"] = F["addon_m"][0]
    F["r8_addon"] = {m: v for m, v in zip(months[1:], F["addon_m"][1:])}
    F["r9_call"] = {"against_model": F["model_count"], "inputs": hc["inputs"], "reused_extracts_caused": F["outage_caused"],
                    "zone": F["sound_zone"], "addon_jul": F["addon_m"][0], "addon_dec": F["addon_m"][-1]}
    return F


def zone(n):
    return "Green" if n <= 4 else ("Yellow" if n <= 9 else "Red")


def occasions(P, runs):
    di = {d: n for n, d in enumerate(P["dates"])}
    s = sorted(di[d] for d in runs)
    return int(sum(1 for j, x in enumerate(s) if j == 0 or x != s[j - 1] + 1))


def grad_by_month(R):
    out = []
    rf = R["addon_run_for"]
    for j in range(len(rf)):
        lo = rf[j - 1] if j else None
        out.append(sum(1 for d, _ in R["graduations"] if (lo is None or d > lo) and d <= rf[j]))
    return out


def effort(F, R):
    B = F["bands"]
    months = F["addon_months"]
    hc = F["heading_counts"]
    cl = R["careful_cls"]
    golden_table = {r["date"]: r["code"] for r in F["rows"]}
    flex = {r["date"]: [4, 5] for r in F["rows"] if r["date"] in sensitive_dates(R)}
    careful_table = {d.date().isoformat(): A.CODE[v] for d, v in cl.items()}
    quick_table = {d: 5 for d in [x.date().isoformat() for x in R["off"]]}
    addon_g = {m: v for m, v in zip(months, F["addon_m"])}
    addon_b = {m: b for m, b in zip(months, B["addon"])}
    later = months[1:]
    res = [
        dict(id="R1", name="every exception of the period on either P&L", graded_as="Component 1",
             figure="r1_exceptions", depends=[], independent="product control's P&L and the run log",
             golden=F["r1_exceptions"],
             passes={"quick": {"exceptions": F["official_count"], "hypothetical_only": 0, "booked_only": F["official_count"]},
                     "careful": {"exceptions": F["exceptions_total"], "hypothetical_only": F["hyp_only"],
                                 "booked_only": F["booked_only"]},
                     "thorough": {"exceptions": F["exceptions_total"], "hypothetical_only": F["hyp_only"],
                                  "booked_only": F["booked_only"]}}),
        dict(id="R2", name="the runs that read an older extract", graded_as="Component 2", figure="outage_runs",
             depends=[], independent="the run log and the extracts", golden=F["outage_runs"],
             passes={"quick": None, "careful": F["outage_runs"], "thorough": F["outage_runs"]}),
        dict(id="R3", name="the exceptions the engine's inputs caused, and those the reused extracts caused",
             graded_as="Ask 2", figure="r3_inputs", depends=["R1"], independent="the blotter, the extracts and the run log",
             golden=F["r3_inputs"],
             passes={"quick": None,
                     "careful": {"inputs_dates": F["careful_inputs_dates"],
                                 "reused_extracts_caused": len(F["careful_inputs_dates"])},
                     "thorough": {"inputs_dates": F["cutoff_dates"], "reused_extracts_caused": F["outage_caused"]}},
             precedent=["L26", "L28"]),
        dict(id="R4", name="the exceptions the model's omitted risks answer for", graded_as="Component 3",
             figure="omitted_dates", depends=["R1", "R3"], independent="", golden=F["omitted_dates"],
             passes={"quick": None,
                     "careful": sorted(d.date().isoformat() for d, v in cl.items() if v == "omitted"),
                     "thorough": F["heading_dates"]["omitted"]},
             precedent=["L26", "L28"]),
        dict(id="R5", name="the volatility heading's count, the sound model's count and the zone", graded_as="Ask 3",
             figure="r5_sound", depends=["R1"], independent="the book held and the own-history scenarios",
             golden=F["r5_sound"],
             bands={"volatility": B["volatility"], "sound_count": B["sound_count"]},
             passes={"quick": {"volatility": 0, "sound_count": F["official_count"], "zone": "Red"},
                     "careful": {"volatility": F["careful_heading_counts"]["volatility"],
                                 "sound_count": F["shortcut_counts"]["extract_book"],
                                 "zone": zone(F["shortcut_counts"]["extract_book"])},
                     "thorough": {"volatility": hc["volatility"], "sound_count": F["sound_count"], "zone": F["sound_zone"]}}),
        dict(id="R6", name="every exception dated under one heading", graded_as="Ask 1", figure="r6_headings",
             depends=["R1", "R2", "R3", "R4", "R5"], independent="", golden=golden_table, bands=flex,
             passes={"quick": quick_table, "careful": careful_table, "thorough": golden_table},
             precedent=["L26", "L28"]),
        dict(id="R7", name="the add-on for July 2025 on the planned book", graded_as="Component 4", figure="addon_jul_m",
             depends=[], independent="the plan, the engine's 30 June run and the mapping", golden=F["addon_jul_m"],
             band=B["addon"][0],
             passes={"quick": F["addon_now_m"], "careful": F["addon_ramp_only_m"][0], "thorough": F["addon_m"][0]}),
        dict(id="R8", name="the add-on for each month from August to December 2025", graded_as="Ask 4", figure="r8_addon",
             depends=["R7"], independent="the plan's months, the store's start dates and the 500-return rule",
             golden=F["r8_addon"], bands={m: addon_b[m] for m in later},
             passes={"quick": {m: F["addon_now_m"] for m in later},
                     "careful": {m: v for m, v in zip(months, F["addon_ramp_only_m"]) if m in later},
                     "thorough": {m: addon_g[m] for m in later}},
             precedent=["L26", "L11", "N06"]),
        dict(id="R9", name="the call", graded_as="Recommendation", figure="r9_call",
             depends=["R3", "R4", "R5", "R8"], independent="",
             golden=F["r9_call"],
             bands={"addon_jul": B["addon"][0], "addon_dec": B["addon"][-1]},
             passes={"quick": {"against_model": F["official_count"], "inputs": 0, "zone": "Red",
                               "addon_jul": F["addon_now_m"], "addon_dec": F["addon_now_m"]},
                     "careful": {"against_model": F["careful_model_count"], "inputs": len(F["careful_inputs_dates"]),
                                 "reused_extracts_caused": len(F["careful_inputs_dates"]),
                                 "zone": zone(F["shortcut_counts"]["extract_book"]),
                                 "addon_jul": F["addon_ramp_only_m"][0], "addon_dec": F["addon_ramp_only_m"][-1]},
                     "thorough": {"against_model": F["model_count"], "inputs": hc["inputs"],
                                  "reused_extracts_caused": F["outage_caused"], "zone": F["sound_zone"],
                                  "addon_jul": F["addon_m"][0], "addon_dec": F["addon_m"][-1]}},
             precedent=["L26", "N06"]),
    ]
    hints = [
        {"sentence": "ERE's position extracts are cut as each run starts, before the middle office books the day's "
                     "closing-auction allocations", "rescues": ["R3", "R4", "R6"]},
        {"sentence": "the engine moves names onto their own history through the half as the store reaches 500 returns",
         "rescues": ["R8"]},
        {"sentence": "the planned book's growth sits in names the engine still proxies", "rescues": []},
    ]
    sc = F["shortcut_counts"]
    routes = [
        dict(name="golden", golden=True, answer=[F["model_count"], hc["inputs"], F["outage_caused"], F["sound_zone"],
                                                  F["addon_m"]]),
        dict(name="the official file (quick)", answer=[F["official_count"], 0, None, "Red", [F["addon_now_m"]] * 6]),
        dict(name="the extract book with the reused days re-run (careful but hurried)",
             answer=[F["careful_model_count"], len(F["careful_inputs_dates"]), len(F["careful_inputs_dates"]),
                     zone(sc["extract_book"]), F["addon_ramp_only_m"]]),
        dict(name="the book held, the proxies kept", answer=[None, hc["inputs"], F["outage_caused"], zone(sc["noprox"]), None]),
        dict(name="the plan's months with the 30 June mapping held", answer=[None, None, None, None, F["addon_ramp_only_m"]]),
        dict(name="the full plan from July with the store's graduations", answer=[None, None, None, None,
                                                                                 F["addon_grad_only_m"]]),
        dict(name="the 30 June add-on scaled with the plan's gross", answer=[None, None, None, None, F["addon_prop_m"]]),
    ]
    forcing = dict(kind="numeric", line=4.5, golden_side="below",
                   golden_family=[dict(name="decay %.2f, %s" % k, value=int(v)) for k, v in sorted(R["fam_count"].items())],
                   shortcuts=[dict(name="the booked P&L on the reported VaR (the official file)", value=sc["official"]),
                              dict(name="the book held, the proxies kept, volatility-scaled", value=int(sc["noprox"]))],
                   perturbations=[dict(input="quantile interpolated between the fifth and sixth losses", value=int(sc["interp"])),
                                  dict(input="decay 0.99", value=int(sc["lam099"])),
                                  dict(input="scenario window 250 days", value=int(sc["win250"]))],
                   notes="Two routes land on the golden's side of the zone and are graded elsewhere: no volatility response "
                         "(%d, the volatility heading then empty) and the extract book (%d, the inputs heading then the "
                         "reused days)." % (sc["novol"], sc["extract_book"]))
    return {"results": res, "hints": hints, "routes": routes, "forcing": forcing}


def sensitive_dates(R):
    out = set()
    for d in R["union"]:
        heads = {c.get(d) for c in R["fam_cls"].values()}
        if len(heads) > 1:
            assert heads <= {"volatility", "sound"}, heads
            out.add(d.date().isoformat())
    return out


def write(R, gen_dir=HERE):
    F = make(R)
    E = effort(F, R)
    json.dump(F, open(os.path.join(gen_dir, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(E, open(os.path.join(gen_dir, "effort.json"), "w"), indent=1)
    return F, E
