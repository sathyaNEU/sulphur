"""task10 architecture 7: builds the pack, the golden deliverables, figures.json, effort.json, submission.md and
metadata.json.

    python3 task10/generator/build.py              # into the task folder
    python3 task10/generator/build.py --out DIR    # the same build into DIR (the rebuild gate compares two of these)
"""
import json
import math
import os
import shutil
import sys

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

# Every reasonable variant of the golden's own choices, one at a time, by the fork it answers (the design note's
# semantic fork table): each is run on the pack, and every stated band is the range they span.
VARIANTS = [
    # SF7, the form of the mornings' temperature response
    ("mornings on two straight lines meeting at a knee the fit chooses", dict(mform="hinge")),
    ("mornings curved below a knee the fit chooses", dict(mform="quadratic")),
    ("mornings on a line through the days at or below 1 C alone", dict(mform="cold")),
    # SF8, the hours taken as the morning
    ("the morning taken as the half-hours ending 09:00 to 15:00", dict(morning="late")),
    # SF9, the winters behind the latest winter's demand
    ("the two latest winters", dict(winters=["2024/25", "2025/26"])),
    ("the latest winter alone", dict(winters=["2025/26"])),
    ("each winter's level allowed to drift, read at 15 January", dict(trend=True)),
    # SF10, how an evening is tied to its morning
    ("each half-hour regressed on the day's own morning", dict(anchor="ols")),
    # SF12, a customer's own level and the build-up's shape
    ("a customer's own level from its latest six months", dict(conn_months=6)),
    ("every customer on its type's level, its own months set aside", dict(conn="type")),
    ("a build-up without a slow start", dict(conn_shape="exp")),
    # SF15, the record a site still to come is read on
    ("each class's record with its own provider", dict(comm="class_provider")),
    ("each class's days late as a fitted distribution", dict(comm="lognormal")),
    ("sites withdrawn counted as still to come in the record", dict(comm="nolost")),
    # SF17, the share's line and the calls that were met
    ("the share curved in temperature", dict(avail_form="quadratic")),
    ("the share flat above 2 C", dict(avail_form="hinge")),
    ("the calls that fell short alone", dict(censor=False)),
]


def r1(v):
    v = round(float(v) + 1e-9, 1)
    return 0.0 if v == 0 else v


def r2(v):
    return round(float(v) + 1e-9, 2)


def pct(v):
    return int(round(100.0 * float(v)))


def band_mw(vals, gold, pad=0.1, floor=0.2):
    lo = math.floor((min(vals) - pad) * 10 + 1e-9) / 10.0
    hi = math.ceil((max(vals) + pad) * 10 - 1e-9) / 10.0
    return [round(min(lo, r1(gold) - floor), 1), round(max(hi, r1(gold) + floor), 1)]


def band_share(vals, gold, pad, floor):
    lo = math.floor((min(vals) - pad) * 100 + 1e-9) / 100.0
    hi = math.ceil((max(vals) + pad) * 100 - 1e-9) / 100.0
    return [round(min(lo, r2(gold) - floor), 2), round(max(hi, r2(gold) + floor), 2)]


def band_pct(vals, gold, pad=3, floor=4):
    lo = int(math.floor(100 * min(vals) - pad))
    hi = int(math.ceil(100 * max(vals) + pad))
    return [max(0, min(lo, pct(gold) - floor)), min(100, max(hi, pct(gold) + floor))]


def family(X, G):
    """The golden and every reasonable variant of its choices, run on the pack."""
    runs = {"golden": G}
    for name, o in VARIANTS:
        runs[name] = E.analyse(X, **o)
    return runs


def figures(X, G, FAM, info):
    codes = sorted(G["zones"], key=lambda c: G["zones"][c]["name"])
    names = [G["zones"][c]["name"] for c in codes]
    Z = {G["zones"][c]["name"]: G["zones"][c] for c in codes}
    fam = {k: {q["name"]: q for q in v["zones"].values()} for k, v in FAM.items()}
    provs = sorted(G["fits"])
    disp = {p: next((W.PROVIDERS[k]["legal"] for k in W.PROVIDERS if PA.provider_key(W.PROVIDERS[k]["legal"]) == p), p)
            for p in provs}
    pname = {p: disp[p].replace(" Ltd", "") for p in provs}

    def tab(key, f=r1):
        return {n: f(Z[n][key]) for n in names}

    def bands(key, **kw):
        return {n: band_mw([fam[k][n][key] for k in fam], Z[n][key], **kw) for n in names}

    share = {pname[p]: r2(G["fits"][p]["share"]) for p in provs}
    back = {pname[p]: r2(float(np.sum(G["fits"][p]["reb"]))) for p in provs}
    share_b = {pname[p]: band_share([v["fits"][p]["share"] for v in FAM.values()], G["fits"][p]["share"], 0.01, 0.02)
               for p in provs}
    back_b = {pname[p]: band_share([float(np.sum(v["fits"][p]["reb"])) for v in FAM.values()],
                                   float(np.sum(G["fits"][p]["reb"])), 0.03, 0.04) for p in provs}
    over_b = {n: band_pct([fam[k][n]["exceed"] for k in fam], Z[n]["exceed"]) for n in names}
    B = dict(R1=bands("before26", floor=0.3), R2=bands("conn_add"), R3=bands("before28", floor=0.3),
             R4=bands("commissioned"), R5=share_b, R6=bands("delivered"), R7=back_b,
             R8=bands("mean_peak", floor=0.3), R9=bands("p90", floor=0.3), R10=over_b)
    # the customers behind each primary's connections figure, and the sites still to come behind its megawatts in service
    conn_rows, site_rows = {}, {}
    for n in names:
        rows = sorted(Z[n]["conn_rows"], key=lambda r: -abs(r[5]))
        conn_rows[n] = [dict(reference=r[0], type=r[1], kva=r[2], energised=r[3].strftime("%d/%m/%Y"), on_supply=bool(r[4]),
                             adds_mw=round(r[5], 2)) for r in rows]
        by = {}
        for s in Z[n]["sites"]:
            c = by.setdefault(s[1], dict(sites=0, mw=0.0, expected_mw=0.0))
            c["sites"] += 1
            c["mw"] += s[2] / 1000.0
            c["expected_mw"] += s[2] / 1000.0 * s[4]
        site_rows[n] = {k: dict(sites=v["sites"], mw=round(v["mw"], 2), expected_mw=round(v["expected_mw"], 2),
                                chance_pct=pct(v["expected_mw"] / v["mw"]) if v["mw"] else 0) for k, v in sorted(by.items())}
    reg = E.register_as_at(X["assets"], X["register_date"])
    inc = E.incidence(reg, X["register_date"], group=("cls",))
    classes = {}
    for (cls,), c in sorted(inc.items()):
        classes[cls] = dict(sites=c["n"], commissioned=c["commissioned"], withdrawn=c["lost"],
                            median_days_late=int(round(c["median_late"])),
                            in_service_by_150_days_pct=pct(E._at(c["curve"], 150)[0]))
    # what the mornings show at the cold end, primary by primary (two straight lines meeting at a fitted knee)
    cold = {}
    for c in codes:
        Dd, Pp = X["_frames"][(c, "full")]
        h = E._mfit(Dd, "hinge")
        cold[G["zones"][c]["name"]] = dict(knee_c=round(h["knee"], 1), per_degree_above=round(-float(h["coef"][0]), 2),
                                           per_degree_below=round(-float(h["coef"][0]) + float(h["coef"][1]), 2))
    zones = {}
    for n in names:
        q = Z[n]
        zones[n] = dict(code=[c for c in codes if G["zones"][c]["name"] == n][0], provider=disp[q["provider"]],
                        firm=q["firm"], contracted=q["contracted"], peak_hh=q["peak_hh"], commit=bool(q["commit"]),
                        margin=r1(q["p90"] - q["firm"]), over_or_under_by=r1(abs(q["p90"] - q["firm"])),
                        off_peak=r1(q["off_peak"]), in_service_now=r1(q["commissioned_now"]),
                        still_to_come_mw=r1(sum(s[2] for s in q["sites"]) / 1000.0), sites_still_to_come=len(q["sites"]),
                        growth_pct=round(100 * (q["growth"] - 1), 1),
                        days_without_service_2526=int(q["clean_days"]), coldest_without_service_2526=round(q["coldest_clean"], 1),
                        days_without_service=int(q["clean_all"]), coldest_without_service=round(q["coldest_all"], 1),
                        working_weekdays=int(q["morning_days"]), at_or_below_freezing=int(q["morning_cold"]),
                        in_service_share_of_contract_pct=pct(q["commissioned"] / q["contracted"]),
                        customers=len(q["conn_rows"]))
    F = dict(
        call=[n for n in names if Z[n]["commit"]], hold=[n for n in names if not Z[n]["commit"]],
        order=names, providers_order=[pname[p] for p in provs],
        r1_demand_2526=tab("before26"), r2_connections=tab("conn_add"), r3_before=tab("before28"),
        r4_in_service=tab("commissioned"), r5_share=share, r6_delivered=tab("delivered"), r7_comeback=back,
        r8_peak=tab("mean_peak"), r9_one_in_ten=tab("p90"), r10_share_over={n: pct(Z[n]["exceed"]) for n in names},
        bands_by_result={k: v for k, v in B.items()},
        zones=zones, customers=conn_rows, sites=site_rows, classes=classes, cold_end=cold,
        providers={pname[p]: dict(key=p, legal=disp[p], share=r2(G["fits"][p]["share"]), spread_pct=pct(G["fits"][p]["cv"]),
                                  back_first=r2(G["fits"][p]["reb"][0]), back_total=r2(float(np.sum(G["fits"][p]["reb"]))),
                                  events=int(G["fits"][p]["n"]), fell_short=int(G["fits"][p]["n_short"]),
                                  met=int(G["fits"][p]["n_met"]),
                                  zones=[n for n in names if Z[n]["provider"] == p]) for p in provs},
        family_sets={k: [n for n in names if fam[k][n]["commit"]] for k in fam},
        family=dict(one_in_ten={k: {n: round(fam[k][n]["p90"], 2) for n in names} for k in fam},
                    margin={k: {n: round(fam[k][n]["p90"] - Z[n]["firm"], 2) for n in names} for k in fam}),
        variants=dict(n=len(VARIANTS), names=[n for n, _ in VARIANTS]),
        totals=dict(contracted=r1(sum(Z[n]["contracted"] for n in names)),
                    in_service=r1(sum(r1(Z[n]["commissioned"]) for n in names)),
                    delivered=r1(sum(r1(Z[n]["delivered"]) for n in names))),
        conventions=dict(design_day_degrees_below_zero=3.0, assurance_days_in_ten=9, credited_half_hours=["17:30", "18:00"],
                         assessment_date="15 January 2028", latest_winter_date="15 January 2026",
                         register_extract=X["register_date"].strftime("%d %B %Y").lstrip("0"), winters=3,
                         window="16:00 to 19:30", post_window_half_hours=4),
        pack=dict(scada_rows=info["scada_rows"], event_rows=info["event_rows"], weather_rows=info["weather_rows"],
                  switching_rows=info["switching_rows"], growth_rows=info["growth_rows"], monitor_rows=info["monitor_rows"],
                  asset_rows=info["asset_rows"], register_sites=int(len(X["assets"])),
                  register_customers=int(len(X["connections"]))))
    return F


def round_floats(o, nd=6):
    if isinstance(o, (float, np.floating)):
        return round(float(o), nd)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, dict):
        return {k: round_floats(v, nd) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [round_floats(v, nd) for v in o]
    return o


def metadata(info):
    covers = {
        PK.F_SCADA: "The Halverton zone's SCADA historian export: the nine 33/11 kV primaries' half-hourly demand, "
                    "November to March of winters 2023/24 to 2025/26, UK local time.",
        PK.F_EVENTS: "The DSO's flexibility dispatch log for the Halverton constraint managed zones, winters 2023/24 to "
                     "2025/26, UK local time.",
        PK.F_SWITCH: "The control room's 11 kV switching log for the Halverton zone, winters 2023/24 to 2025/26.",
        PK.F_WX: "Hourly observations at Halverton weather station, October to March of winters 2023/24 to 2025/26.",
        PK.F_REG: "The primary substation register (asset codes, SCADA points, transformers) and the DFES 2026 growth rates.",
        PK.F_FDR: "The 11 kV feeder schedule and normally-open points of the Halverton zone.",
        PK.F_GROW: "The connections team's load growth register, as saved on 30 October 2026.",
        PK.F_MON: "The settlement team's monthly summary of half-hourly metered customers in the Halverton zone, January "
                  "2021 to October 2026.",
        PK.F_ASSET: "The DSO's flexibility asset register for every constraint managed zone in the licence area, extracted "
                    "4 November 2026.",
        PK.F_GUIDE: "Network Planning's winter capacity assessment guideline, issue 5, September 2026.",
        PK.F_AWARD: "The DSO's flexibility contract award notice for winter 2027/28, 21 October 2026.",
        PK.F_CI: "Customer interruptions and minutes lost by 11 kV feeder, regulatory year 2025/26.",
        PK.F_COND: "Primary transformer oil analysis and health indices, 2026.",
        PK.F_DUOS: "The use of system charging statement effective 1 April 2027.",
    }
    files = [dict(path="target/" + f, source="constructed for task10 by simulating the organisation's systems; no real dataset",
                  date="2026-11-04", licence="CC0 1.0 (constructed)", covers=covers[f]) for f in PK.FILES]
    return dict(task="task10",
                decision="the Halverton zone primary substations whose reinforcement Wealdmoor Power Networks commits for "
                         "winter 2027/28, with each primary's design-day demand, what its flexibility contract delivers, "
                         "its expected peak, the level the peak stays under on nine design days in ten and the share of "
                         "design days over firm capacity",
                deliverables=[GO.F_XLSX, GO.F_PPTX],
                distractor_files=["target/" + f for f in PK.DISTRACTORS],
                files=files,
                rows=dict(scada=info["scada_rows"], events=info["event_rows"], weather=info["weather_rows"],
                          switching=info["switching_rows"], growth=info["growth_rows"], monthly_summary=info["monitor_rows"],
                          asset_register=info["asset_rows"]))


def main(out=None):
    task = out or TASK
    target, golden = os.path.join(task, "target"), os.path.join(task, "golden")
    gen = os.path.join(task, "generator") if not out else task
    os.makedirs(gen, exist_ok=True)
    T = W.build()
    shutil.rmtree(target, ignore_errors=True)
    os.makedirs(target)
    info = PK.write_data(T, target)
    D.write_docs(target)
    PP.own_mtimes(target, PK.EXPORTED)
    X = PA.load(target)
    G = E.analyse(X)
    FAM = family(X, G)
    F = figures(X, G, FAM, info)
    eff, C, Q, runs = EP.effort_json(X, F, G)
    names = F["order"]
    pmap = {v["key"]: d for d, v in F["providers"].items()}
    F["routes"] = {r["name"]: r["answer"] for r in eff["routes"]}
    F["careful"] = EP.results_of(C, names, pmap)
    F["quick"] = EP.results_of(Q, names, pmap, quick=True)
    F["route_figures"] = {name: {n: dict(before=r1(q["before28"]), in_service=r1(q["commissioned"]), delivered=r1(q["delivered"]), peak=r1(q["mean_peak"]),
                                         one_in_ten=r1(q["p90"]), share_over=pct(q["exceed"]), commit=bool(q["commit"]))
                                 for q in run["zones"].values() for n in [q["name"]]} for name, run in runs.items()}
    F["route_margins"] = {name: {q["name"]: q["p90"] - q["firm"] for q in run["zones"].values()} for name, run in runs.items()}
    F["sensitivity"] = eff["sensitivity"]
    F["hints"] = [dict(sentence=h["sentence"], rescues=h["rescues"], commits=h["commits"]) for h in eff["hints"]]
    for h in eff["hints"]:
        h.pop("commits", None)
    shutil.rmtree(golden, ignore_errors=True)
    GO.write(G, F, golden)
    PP.own_mtimes(golden, {})
    json.dump(round_floats(F), open(os.path.join(gen, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(round_floats(eff), open(os.path.join(gen, "effort.json"), "w"), indent=1, sort_keys=True)
    WU.write(F, os.path.join(task, "submission.md"))
    json.dump(metadata(info), open(os.path.join(task, "metadata.json"), "w"), indent=1)
    PP.zip_folder(golden, os.path.join(task, "golden.zip"))
    PP.zip_folder(target, os.path.join(task, "target.zip"))
    print("call:", F["call"], "| hold:", F["hold"])
    for n in names:
        z = F["zones"][n]
        print("  %-16s 25/26 %.1f conn %.1f before %.1f in service %.1f delivered %.1f peak %.1f@%s nine-in-ten %.1f firm %.1f (%+.1f) over %d%%"
              % (n, F["r1_demand_2526"][n], F["r2_connections"][n], F["r3_before"][n], F["r4_in_service"][n], F["r6_delivered"][n],
                 F["r8_peak"][n], z["peak_hh"], F["r9_one_in_ten"][n], z["firm"], z["margin"], F["r10_share_over"][n]))
    print("  share", F["r5_share"], "come-back", F["r7_comeback"])
    print("  routes:", {k[:40]: "".join(x[0] for x in v) for k, v in F["routes"].items()})
    return T, X, G, F, eff


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None)
