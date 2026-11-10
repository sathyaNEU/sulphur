"""task10 architecture 6: builds the pack, the golden deliverables, figures.json, submission.md and metadata.json.
python3 task10/generator/build.py"""
import json
import math
import os
import shutil
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import docs as D            # noqa: E402
import effort_passes as EP  # noqa: E402
import estim as E           # noqa: E402
import golden as GO         # noqa: E402
import pack as PK           # noqa: E402
import parse as PA          # noqa: E402
import postprocess as PP    # noqa: E402
import world as W           # noqa: E402
import writeup as WU        # noqa: E402

TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")


# Every reasonable variant of the golden's own choices, one at a time, by the fork it answers (the design note's
# semantic fork table): each is run on the pack and every stated band is the range they span.
VARIANTS = [
    # SF9, the cold days
    ("days at or below 0 C", dict(below=0.0)), ("days at or below minus 1.5 C", dict(below=-1.5)),
    ("days at or below minus 2 C", dict(below=-2.0)),
    # SF10, the line through the share
    ("a curved line", dict(form="quadratic")),
    # SF11, provider or zone
    ("zone by zone", dict(pooled=False)),
    # SF12, the scatter
    ("the scatter as measured", dict(net_noise=False)),
    # SF13, the heating base
    ("heating base 14 C", dict(base=14.0)), ("heating base 17 C", dict(base=17.0)),
    # SF18, the baseline an event's megawatts are measured against
    ("a heating slope each winter", dict(baseline="by_winter")), ("weekday levels", dict(baseline="weekday")),
    ("the baseline scaled to the day's own level before the window", dict(baseline="same_day")),
    # SF19, a call that was met
    ("the calls that fell short alone", dict(estimator="short", fit_below=E.COLD)),
    ("the calls that fell short alone, every day", dict(estimator="short")),
    ("met calls as floors, days at or below 2 C", dict(estimator="censored", fit_below=2.0)),
    ("met calls as floors, every day", dict(estimator="censored")),
    ("met calls as floors, every day, a curved line", dict(estimator="censored", form="quadratic")),
    ("megawatts fitted over every event", dict(estimator="megawatts")),
    ("megawatts fitted over every event, zone by zone", dict(estimator="megawatts", pooled=False)),
    # SF20, a cancelled instruction's day
    ("a cancelled instruction's day kept", dict(cancelled_in=True)),
    # SF22, what is available against the megawatts contracted
    ("the three winters' own scaling with the megawatts contracted", dict(scale="measured")),
]


def r1(v):
    v = round(float(v) + 1e-9, 1)
    return 0.0 if v == 0 else v


def family(X, G):
    """Every reasonable variant of the golden's choices, run on the pack: the band each result carries."""
    runs = {"golden": G}
    for name, o in VARIANTS:
        runs[name] = E.golden_from(X, **o)
    return runs


def band(vals, gold, pad=0.1, floor=None):
    lo = math.floor((min(vals) - pad) * 10 + 1e-9) / 10.0
    hi = math.ceil((max(vals) + pad) * 10 - 1e-9) / 10.0
    lo, hi = min(lo, r1(gold) - (floor or 0)), max(hi, r1(gold) + (floor or 0))
    return [round(lo, 1), round(hi, 1)]


def figures(X, G, FAM, info):
    prim = [z["primary"] for z in G["zones"]]
    Z = {z["primary"]: z for z in G["zones"]}
    fam = {k: {z["primary"]: z for z in v["zones"]} for k, v in FAM.items()}

    def tab(key):
        return {p: r1(Z[p][key]) for p in prim}

    def bands(key, pad=0.1, floor=0.2):
        return {p: band([fam[k][p][key] for k in fam], Z[p][key], pad, floor) for p in prim}

    bt = G["backtest_all"]
    maes = [v["backtest_all"]["mae"] for v in FAM.values()]
    # the freezing-day count inside the 80 per cent range, under every variant and every construction of the range:
    # carried in the workbook as context and not graded, because reasonable constructions spread this widely
    ins = [E.backtest_all(v["events"], v["noise"], range_kind=rk, **v["fit_options"])[1]["n_inside"]
           for v in FAM.values() for rk in E.RANGES]
    provs = sorted(G["providers"])
    zp = {p: [z["primary"] for z in G["zones"] if z["provider"] == p] for p in provs}

    def pband(vals, gold, pad, nd=2):
        q = 10 ** nd
        return [round(math.floor((min(min(vals), gold) - pad) * q + 1e-9) / q, nd),
                round(math.ceil((max(max(vals), gold) + pad) * q - 1e-9) / q, nd)]

    share_b = {p: pband([v["providers"][p]["share"] for v in FAM.values()] +
                        [fam[k][x]["share"] for k in fam for x in zp[p]], round(G["providers"][p]["share"], 2), 0.01) for p in provs}
    back_b = {p: pband([v["providers"][p]["back"]["20:00"] for v in FAM.values()], round(G["providers"][p]["back"]["20:00"], 2), 0.05)
              for p in provs}
    # the megawatts delivered: the variants' range, and never narrower than the share's own band times the award
    deliv_b = {}
    for p in prim:
        lo, hi = bands("delivered")[p]
        slo, shi = share_b[Z[p]["provider"]]
        deliv_b[p] = [round(min(lo, math.floor(slo * Z[p]["award"] * 10 + 1e-9) / 10.0), 1),
                      round(max(hi, math.ceil(shi * Z[p]["award"] * 10 - 1e-9) / 10.0), 1)]
    spread_b = {p: [int(math.floor(100 * min(min(v["providers"][p]["cv"], v["providers"][p]["cv_raw"]) for v in FAM.values()) - 1)),
                    int(math.ceil(100 * max(max(v["providers"][p]["cv"], v["providers"][p]["cv_raw"]) for v in FAM.values()) + 1))]
                for p in provs}
    # the bridge is stated at the precision shown, so every bar is taken from the displayed megawatts and adds up
    bridge = {**{"%s, not available" % p: r1(Z[p]["award"] - r1(Z[p]["delivered"])) for p in prim},
              **{"%s, lost as load comes back" % p: r1(max(r1(Z[p]["delivered"]) - r1(Z[p]["off_peak"]), 0.0)) for p in prim}}
    bb = {**{"%s, not available" % p: band([fam[k][p]["not_available"] for k in fam], Z[p]["not_available"], 0.1, 0.2) for p in prim},
          **{"%s, lost as load comes back" % p: band([fam[k][p]["comeback_loss"] for k in fam], Z[p]["comeback_loss"], 0.1, 0.2) for p in prim}}
    LE = E.line_evidence(X)
    zl = {X["names"][c]: v for c, v in LE.items() if v["zone"]}
    el, el_se, el_n = E.scaling(G["events"])
    A = Z["Ashcombe Road"]
    fA = G["providers"][A["provider"]]
    limit = (A["profile"]["18:00"] - A["profile"]["20:00"]) / (fA["shape"]["18:00"] + fA["back"]["20:00"])
    sets = {k: v["commit"] for k, v in FAM.items()}
    F = dict(
        call=list(G["commit"]), hold=[p for p in prim if p not in G["commit"]],
        r1_before=tab("before"), r2_delivered=tab("delivered"), r4_off_peak=tab("off_peak"), r5_peak=tab("peak"),
        r6_one_in_ten=tab("p90"),
        r3_backtest=round(bt["mae"], 2),
        r8_bridge=bridge,
        r1_evidence=dict(coldest_unscheduled_c=round(min(v["coldest"] for v in zl.values()), 1),
                         line_within_pct=int(math.ceil(max(abs(v["line_miss_pct"]) for v in zl.values()))),
                         by_primary={p: dict(sample_days=v["n_sample"], coldest_c=round(v["coldest"], 1), cold_days=v["n_cold"],
                                             line_miss_mw=round(v["line_miss"], 2), line_miss_pct=round(v["line_miss_pct"], 1),
                                             curve_miss_mw=round(v["curve_miss"], 2), peak_curve_t=round(v["peak_curve_t"], 2))
                                     for p, v in zl.items()},
                         unscheduled_primaries_curve_t={X["names"].get(c, c): round(v["peak_curve_t"], 2)
                                                        for c, v in LE.items() if not v["zone"]}),
        scaling=dict(elasticity=round(el, 2), standard_error=round(el_se, 2), events=el_n),
        c1_share={p: round(G["providers"][p]["share"], 2) for p in provs},
        c2_comeback={p: round(G["providers"][p]["back"]["20:00"], 2) for p in provs},
        c3_spread={p: int(round(G["providers"][p]["cv"] * 100)) for p in provs},
        bands=dict(before=bands("before", 0.1, 0.3), delivered=deliv_b, off_peak=bands("off_peak"),
                   peak=bands("peak", 0.1, 0.3), one_in_ten=bands("p90", 0.1, 0.3), bridge=bb,
                   share=share_b, comeback=back_b, spread=spread_b,
                   backtest=dict(mae=pband(maes, round(bt["mae"], 2), 0.01),
                                 inside=[int(min(ins)), int(max(ins))])),
        zones={p: dict(zone=Z[p]["zone"], code=Z[p]["code"], provider=Z[p]["provider"], award=Z[p]["award"], firm=Z[p]["firm"],
                       share=round(Z[p]["share"], 2), peak_hh=Z[p]["peak_hh"], over=bool(Z[p]["over"]),
                       over_by=r1(Z[p]["over_by"]), margin=r1(Z[p]["p90"] - Z[p]["firm"]), inside_by=r1(abs(Z[p]["p90"] - Z[p]["firm"])),
                       expected_margin=r1(Z[p]["peak"] - Z[p]["firm"]),
                       exceed_days_in_ten=int(round(Z[p]["exceed"] * 10)), per_scheduled=round(Z[p]["per_scheduled"], 2),
                       per_scheduled_mw=r1(Z[p]["per_scheduled"] * Z[p]["award"]), n_events=Z[p]["n_events"], n_cold=Z[p]["n_cold"],
                       in_window=r1(Z[p]["in_window"]), after_window=r1(Z[p]["after_window"]), n_base_days=Z[p]["n_base_days"],
                       largest_scheduled=float(G["events"][Z[p]["code"]]["scheduled"].max()),
                       contract_2526=X["contract"][(Z[p]["code"], "2025/26")]) for p in prim},
        providers={p: dict(share=round(f["share"], 2), slope_per_degree=round(f["beta"][1], 3), spread_pct=int(round(f["cv"] * 100)),
                           spread_measured_pct=int(round(f["cv_raw"] * 100)), back_first=round(f["back"]["20:00"], 2),
                           back_second=round(f["back"]["20:30"], 2), n_cold=f["n_cold"], cold_dates=f["cold_dates"],
                           cold_met=f["cold_met"]) for p, f in G["providers"].items()},
        backtest=dict(n=bt["n"], n_cold=bt["n_cold"], n_inside=bt["n_inside"], mae=round(bt["mae"], 2),
                      mae_cold=round(bt["mae_cold"], 2), range_pct=int(E.RANGE * 100)),
        totals=dict(contracted=r1(sum(Z[p]["award"] for p in prim)), delivered=r1(sum(r1(Z[p]["delivered"]) for p in prim)),
                    off_peak=r1(sum(r1(Z[p]["delivered"]) - bridge["%s, lost as load comes back" % p] for p in prim)),
                    not_available=r1(sum(bridge["%s, not available" % p] for p in prim)),
                    comeback_loss=r1(sum(bridge["%s, lost as load comes back" % p] for p in prim))),
        ashcombe_limit=r1(limit), family_sets={k: v for k, v in sets.items()},
        variants=dict(cold_days_at_or_below=[0, 1.5, 2], heating_base_c=[14, 17], n=len(VARIANTS),
                      names=[n for n, _ in VARIANTS]),
        family=dict(delivered={k: {p: round(fam[k][p]["delivered"], 2) for p in prim} for k in fam},
                    one_in_ten={k: {p: round(fam[k][p]["p90"], 2) for p in prim} for k in fam},
                    mae={k: round(v["backtest_all"]["mae"], 3) for k, v in FAM.items()}),
        cold_events=dict(total=int(sum(f["n_cold"] for f in G["providers"].values())),
                         met=int(sum(f["cold_met"] for f in G["providers"].values()))),
        conventions=dict(design_day_degrees_below_zero=-E.T_DESIGN, cold_days_at_or_below_minus=-E.COLD, assurance_days_in_ten=9,
                         threshold_pct=92, credited_half_hours=["17:30", "18:00"]),
        pack=dict(scada_rows=info["scada_rows"], event_rows=info["event_rows"], weather_rows=info["weather_rows"],
                  switching_rows=info["switching_rows"]),
        record=dict(completed={X["names"][c]: n for c, n in G["record"]["completed"].items()},
                    completed_total=int(sum(G["record"]["completed"].values()))))
    return F


def round_floats(o, nd=6):
    if isinstance(o, float):
        return round(o, nd)
    if isinstance(o, dict):
        return {k: round_floats(v, nd) for k, v in o.items()}
    if isinstance(o, list):
        return [round_floats(v, nd) for v in o]
    return o


def metadata(info):
    covers = {
        PK.F_SCADA: "The Halverton zone's SCADA historian export: the nine 33/11 kV primaries' half-hourly demand, "
                    "November to March of winters 2023/24 to 2025/26, UTC.",
        PK.F_EVENTS: "The DSO's flexibility dispatch log for the four Halverton constraint managed zones, winters 2023/24 to "
                     "2025/26, UK local time.",
        PK.F_SWITCH: "The control room's 11 kV switching log for the Halverton zone, winters 2023/24 to 2025/26.",
        PK.F_WX: "Hourly observations at Halverton weather station, October to March of winters 2023/24 to 2025/26.",
        PK.F_REG: "The primary substation register (asset codes, SCADA points, transformers) and the DFES 2026 growth rates.",
        PK.F_FDR: "The 11 kV feeder schedule and normally-open points of the Halverton zone.",
        PK.F_GROW: "The connections team's load growth register.",
        PK.F_GUIDE: "Network Planning's winter capacity assessment guideline, issue 4, September 2026.",
        PK.F_AWARD: "The DSO's flexibility contract award notice for winter 2027/28.",
        PK.F_CI: "Customer interruptions and minutes lost by 11 kV feeder, regulatory year 2025/26.",
        PK.F_COND: "Primary transformer oil analysis and health indices, 2026.",
        PK.F_DUOS: "The use of system charging statement effective 1 April 2027.",
    }
    files = [dict(path="target/" + f, source="constructed for task10; no real dataset", date="2026-11-03",
                  licence="CC0 1.0 (constructed)", covers=covers[f]) for f in PK.FILES]
    return dict(task="task10",
                decision="the Halverton flexibility zones' primary substations whose reinforcement Wealdmoor Power Networks "
                         "commits for winter 2027/28, with what each 2027/28 contract delivers and takes off the design day's "
                         "peak, each peak expected and at the one-day-in-ten level, and last winter's backtest",
                deliverables=[GO.F_XLSX, GO.F_PPTX],
                distractor_files=["target/" + f for f in PK.DISTRACTORS],
                files=files,
                rows=dict(scada=info["scada_rows"], events=info["event_rows"], weather=info["weather_rows"],
                          switching=info["switching_rows"]))


def main():
    T = W.build()
    shutil.rmtree(TARGET, ignore_errors=True)
    os.makedirs(TARGET)
    info = PK.write_data(T, TARGET)
    D.write_docs(TARGET)
    PP.own_mtimes(TARGET, PK.EXPORTED)
    X = E.conform(PA.load(TARGET))
    G = E.golden_from(X)
    FAM = family(X, G)
    F = figures(X, G, FAM, info)
    eff, C, Q = EP.effort_json(X, G, F)
    F["routes"] = {r["name"]: r["answer"] for r in eff["routes"]}
    F["careful"] = {p: {k: (r1(v) if isinstance(v, float) else v) for k, v in C[p].items()} for p in C if not p.startswith("_")}
    F["careful_backtest"] = dict(mae=round(C["_backtest"]["mae"], 2), inside=C["_backtest"]["inside"],
                                 inside_fit_range=C["_backtest"]["inside_fit_range"])
    F["careful_call"] = C["_call"]
    F["quick_call"] = Q["_call"]
    gold_tab = {z["primary"]: dict(delivered=z["delivered"], off_peak=z["off_peak"], peak=z["peak"], one_in_ten=z["p90"],
                                   over=z["over"]) for z in G["zones"]}
    R = [("Every result of the chain", gold_tab),
         ("Megawatts delivered per megawatt scheduled at minus 3.0 C applied to the contract, taken off the 17:30 to 18:00 "
          "peak, the record's megawatts of scatter unchanged", {p: C[p] for p in gold_tab}),
         ("The megawatts contracted at face value", {p: Q[p] for p in gold_tab})]
    shutil.rmtree(GOLDEN, ignore_errors=True)
    GO.write(G, F, R, GOLDEN)
    PP.own_mtimes(GOLDEN, {})
    json.dump(round_floats(F), open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(round_floats(eff), open(os.path.join(HERE, "effort.json"), "w"), indent=1, sort_keys=True)
    WU.write(F, os.path.join(TASK, "submission.md"))
    json.dump(metadata(info), open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
    # the golden ZIP: exactly the two requested files, each entry at its own last save
    PP.zip_folder(GOLDEN, os.path.join(TASK, "golden.zip"))
    print("call:", G["commit"], "| backtest MAE %.3f inside %d of %d" % (G["backtest_all"]["mae"], G["backtest_all"]["n_inside"], G["backtest_all"]["n_cold"]))
    for z in G["zones"]:
        print("  %-16s before %.2f share %.3f delivered %.2f peak@%s %.2f off %.2f p90 %.2f firm %.1f over %s | careful %.2f %.2f"
              % (z["primary"], z["before"], z["share"], z["delivered"], z["peak_hh"], z["peak"], z["off_peak"], z["p90"], z["firm"],
                 z["over"], C[z["primary"]]["delivered"], C[z["primary"]]["one_in_ten"]))
    print("  family sets:", {k: len(v) for k, v in F["family_sets"].items()}, "| careful call", C["_call"], "| quick", Q["_call"])
    return T, X, G, F


if __name__ == "__main__":
    main()
