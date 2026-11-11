"""task10 architecture 7: the generator's assertions, on the cut pack (target/) and on the clean truth.
python3 task10/generator/checks.py

The call and every result against the clean truth; every variant of the golden's choices inside the stated bands and
on the same list; each shortcut's list and its distance from firm capacity; every semantic fork row of the design
note by its id; the bar block (labels BAR R1 to BAR R7: the field's raw material, neutral mess, each result's hurried
figure, no plant, no one thing with each factor's footprint across the data, the one-fact test computed, the rivals
ruled out by named data); Layer 1, the input gates, realism and the containers."""
import datetime as dt
import json
import math
import os
import re
import subprocess
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import build as B          # noqa: E402
import effort_passes as EP  # noqa: E402
import estim as E          # noqa: E402
import golden as GO        # noqa: E402
import pack as PK          # noqa: E402
import parse as PA         # noqa: E402
import world as W          # noqa: E402

CALL = ["Ashcombe Road", "Charlecote Way", "Dunmore Street", "Fenwick Street"]
HOLD = ["Hartwell Common"]
NONE_AT = ["Ashcombe Road", "Charlecote Way", "Dunmore Street"]     # no further contract would hold them
MARGIN = 0.6            # megawatts either side of firm capacity, for the weakest variant of the golden's own choices
ROUTE_MARGIN = 0.4      # and for every shortcut's list (the straight line through the mornings keeps Dunmore Street 0.48 over)
RESULTS = []
TPMAP = {"Corvane": "Corvane Flex", "Quillon": "Quillon Energy Services"}


def check(cid, ok, detail):
    RESULTS.append((cid, bool(ok), detail))
    print("%-4s %-46s %s" % ("PASS" if ok else "FAIL", cid, detail))


def truth_inputs(T):
    X = E.from_world(W, T)
    X["rates"] = {p["code"]: PK.dfes_rates(p["key"]) for p in W.PRIMARIES}
    return X


def by_name(run):
    return {q["name"]: q for q in run["zones"].values()}


def margins(run, names):
    z = by_name(run)
    return {n: z[n]["p90"] - z[n]["firm"] for n in names}


def commits(run, names):
    z = by_name(run)
    return [n for n in names if z[n]["commit"]]


def outside(tab, bands, tol=0.0, gold=None):
    """The cells of a result outside its bands; a cell with no band (a primary where no amount would do) must equal the
    golden's."""
    out = []
    for k in bands:
        v, b = tab.get(k), bands[k]
        if b is None:
            if gold is not None and v != gold.get(k):
                out.append(k)
        elif v is None or isinstance(v, str) or not (b[0] - tol <= v <= b[1] + tol):
            out.append(k)
    return out


def car_sens_verdicts(names):
    return ["Ashcombe Road: hold"] + ["%s: reinforce, or contract more flexibility" % n
                                      for n in ("Charlecote Way", "Dunmore Street", "Fenwick Street")] + ["Hartwell Common: hold"]


def tolerance(rid):
    return 0.0051 if rid in ("R5", "R7") else (1.51 if rid == "R10" else 0.051)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    eff = json.load(open(os.path.join(HERE, "effort.json")))
    names, Bd = F["order"], F["bands_by_result"]
    pmap = {v["key"]: d for d, v in F["providers"].items()}
    X = PA.load(TARGET)
    G = E.analyse(X)
    gp = EP.results_of(G, names, pmap, CALL)
    GOLD = {"R11": F["r12_further"], "R12": F["r13_schedule"], "R13": F["r14_customer"]}
    T = W.build()
    XT = truth_inputs(T)
    GT = E.analyse(XT)
    gt = EP.results_of(GT, names, TPMAP, CALL)
    DT = W.design_truth(T)
    key = {W.BY[z["key"]]["name"]: z["key"] for z in W.ZONES}
    Zp, Zt = by_name(G), by_name(GT)

    # ------------------------------------------------------------------------------------------------ the call
    check("call", commits(G, names) == CALL and F["call"] == CALL and F["hold"] == HOLD, "reinforce %s; hold %s" % (", ".join(F["call"]), ", ".join(F["hold"])))
    check("call on the clean truth", commits(GT, names) == CALL, "the same list before any mess or document: %s" % ", ".join(commits(GT, names)))
    same = {rid: outside(gt[rid], Bd[rid], tolerance(rid) if rid != "R10" else 0.51, GOLD.get(rid)) for rid in Bd}
    check("pack against the clean truth", not any(same.values()),
          "every result computed from the clean tables sits inside the band stated from the pack (%s)" % (same if any(same.values()) else "none outside"))
    figs = {rid: F[m] for rid, m in (("R1", "r1_demand_2526"), ("R2", "r2_connections"), ("R3", "r3_before"), ("R4", "r4_in_service"),
                                     ("R5", "r5_share"), ("R6", "r6_delivered"), ("R7", "r7_comeback"), ("R8", "r8_peak"),
                                     ("R9", "r9_one_in_ten"), ("R10", "r10_share_over"), ("R11", "r12_further"),
                                     ("R12", "r13_schedule"), ("R13", "r14_customer"), ("R14", "r11_verdicts"))}
    check("figures.json is the pack's golden", all(figs[r] == gp[r] for r in figs) and F["call"] == commits(G, names),
          "all fourteen results and the list recompute from target/")
    # the golden against what the world's own parameters give (never seen by an analyst)
    d = dict(demand=max(abs(Zp[n]["before26"] - DT[key[n]]["before26"]) for n in names),
             customers=max(abs(Zp[n]["conn_add"] - DT[key[n]]["conn_add"]) for n in names),
             in_service=max(abs(Zp[n]["commissioned"] - DT[key[n]]["commissioned"]) for n in names),
             share=max(abs(Zp[n]["share"] - DT[key[n]]["share"]) for n in names))
    check("golden against the world's own parameters", d["demand"] <= 0.35 and d["customers"] <= 0.4 and d["in_service"] <= 0.45 and d["share"] <= 0.03,
          "largest gap: 2025/26 demand %.2f MW, customers %.2f MW, megawatts in service %.2f MW, share %.3f" % (d["demand"], d["customers"], d["in_service"], d["share"]))

    # ------------------------------------------------------------------------------------- the variants and the bands
    fam_t = {name: E.analyse(XT, **o) for name, o in B.VARIANTS}
    bad, lists = [], set()
    for name, run in fam_t.items():
        rv = EP.results_of(run, names, TPMAP, CALL)
        for rid in Bd:
            for k in outside(rv[rid], Bd[rid], tolerance(rid), GOLD.get(rid)):
                bad.append("%s %s %s" % (name[:28], rid, k))
        lists.add(tuple(commits(run, names)))
    check("BAR R7 every variant inside the bands, on the clean truth", not bad, "%d variants x 13 results%s" % (len(fam_t), (": " + "; ".join(bad[:6])) if bad else ""))
    check("every variant commits the same list", lists == {tuple(CALL)} and all(v == CALL for v in F["family_sets"].values()),
          "%d variants on the clean truth and on the pack" % len(fam_t))
    fm = F["family"]["margin"]
    weakest = {n: (min if n in CALL else max)(fm[k][n] for k in fm) for n in names}
    check("margins: the weakest variant", all(weakest[n] >= MARGIN for n in CALL) and all(weakest[n] <= -MARGIN for n in HOLD),
          "; ".join("%s %+.2f" % (n, weakest[n]) for n in names) + " MW against firm capacity")
    widths = {rid: max(Bd[rid][k][1] - Bd[rid][k][0] for k in Bd[rid] if Bd[rid][k] is not None) for rid in Bd}
    check("bands are narrow enough to grade", widths["R1"] <= 1.0 and widths["R3"] <= 1.0 and widths["R9"] <= 1.2 and widths["R4"] <= 1.2
          and widths["R5"] <= 0.09 and widths["R2"] <= 0.9,
          "widest band: demand 2025/26 %.1f, customers %.1f, before %.1f, in service %.1f, nine in ten %.1f MW; share %.2f"
          % (widths["R1"], widths["R2"], widths["R3"], widths["R4"], widths["R9"], widths["R5"]))

    # -------------------------------------------------------------------------- the three choices around the list
    low_t = {name: {n: by_name(run)[n]["further_low"][0] for n in NONE_AT if by_name(run)[n].get("further") is None}
             for name, run in list(fam_t.items()) + [("golden", GT)]}
    low_p = F["family_lowest"]
    every_none = all(len(v) == len(NONE_AT) for v in low_t.values()) and all(len(v) == len(NONE_AT) for v in low_p.values())
    lowest = min(min(v.values()) for v in list(low_t.values()) + list(low_p.values()))
    check("R12 no further contract would hold Ashcombe Road, Charlecote Way or Dunmore Street", every_none and lowest >= 0.2
          and F["r12_further"]["Fenwick Street"] != "none",
          "in every variant on the pack and the clean truth; the lowest share of design days over firm any further contract "
          "reaches is %.0f per cent at the weakest (Fenwick Street %s MW, %s to %s)" % (100 * lowest, F["r12_further"]["Fenwick Street"],
                                                                                         *Bd["R11"]["Fenwick Street"]))
    sch = [(name, by_name(run)[E.SCHEDULE_AT[0]]["schedule"]) for name, run in list(fam_t.items()) + [("golden", GT)]]
    check("R13 the schedule, and no schedule holds Ashcombe Road", all(not v["full"] and v["p90"] > F["zones"][E.SCHEDULE_AT[0]]["firm"] + 0.3
                                                                  for _, v in sch),
          "every variant schedules %.1f to %.1f MW and stays %.2f MW or more over firm capacity nine days in ten"
          % (min(v["schedule"] for _, v in sch), max(v["schedule"] for _, v in sch),
             min(v["p90"] for _, v in sch) - F["zones"][E.SCHEDULE_AT[0]]["firm"]))
    cus = [by_name(run)[E.CUSTOMER_AT]["customer"] for run in list(fam_t.values()) + [GT]]
    check("R14 Hartwell Common holds the data hall", all(c["p90"] <= F["zones"][E.CUSTOMER_AT]["firm"] - 0.1 for c in cus),
          "nine days in ten at most %.2f MW against %.1f in every variant on the clean truth"
          % (max(c["p90"] for c in cus), F["zones"][E.CUSTOMER_AT]["firm"]))

    # ------------------------------------------------------------------------------------------- the shortcuts' lists
    short_t = {name: E.analyse(XT, **o) for name, o in EP.SHORTCUTS}
    R = F["routes"]
    mt = {name: margins(run, names) for name, run in short_t.items()}
    sets_t = {name: commits(run, names) for name, run in short_t.items()}
    verd_t = {name: EP.verdicts(by_name(run), names) for name, run in short_t.items()}
    check("routes: the same answers on the clean truth and the pack", all(verd_t[n] == R[n] for n in verd_t) and
          all(sets_t[n] == F["route_sets"][n] for n in sets_t),
          "; ".join("%s: %s" % (n[:34], "".join(x[0] for x in sets_t[n])) for n in list(sets_t)[:6]) + " ...")
    LINE = [n for n, o in EP.SHORTCUTS if o.get("baseline") in ("pooled", "latest", "sched") and len(o) == 1]
    NEW = [n for n, o in EP.SHORTCUTS if o.get("conn") in ("full", "ratio", "mature", "new_buildup") and len(o) == 1]
    OBS = [n for n, o in EP.SHORTCUTS if o.get("conn") == "observed"]
    SVC = [n for n, o in EP.SHORTCUTS if "comm" in o and "baseline" not in o and "conn" not in o and n != EP.BY_CLASS_NAME]
    REPLAY = [n for n, o in EP.SHORTCUTS if o == dict(replay=False)]
    dun = max(mt[n]["Dunmore Street"] for n in LINE)
    check("the line through the days without a service drops Dunmore Street", dun <= -MARGIN and all(sets_t[n] == ["Ashcombe Road", "Charlecote Way", "Fenwick Street"] for n in LINE),
          "three versions of the line, Dunmore Street at most %+.2f MW from firm capacity" % dun)
    ch = max(mt[n]["Charlecote Way"] for n in NEW + OBS)
    ha = min(mt[n]["Hartwell Common"] for n in NEW + OBS if "build-up" not in n or n in OBS)
    check("the connections read short drop Charlecote Way and add Hartwell Common", ch <= -MARGIN and ha >= MARGIN,
          "Charlecote Way at most %+.2f MW; Hartwell Common at least %+.2f MW, on the customers due after the latest winter in full, at the average share, at their type's established share, and on every customer held at its latest months" % (ch, ha))
    fe = max(mt[n]["Fenwick Street"] for n in SVC)
    check("the megawatts in service read long drop Fenwick Street", fe <= -MARGIN and all(sets_t[n] == ["Ashcombe Road", "Charlecote Way", "Dunmore Street"] for n in SVC),
          "six readings (contracted twice, planned dates, the zone's own ratio, the provider's record, every class together), Fenwick Street at most %+.2f MW" % fe)
    check("the delivery off the 17:00 to 18:00 peak drops Ashcombe Road", mt[REPLAY[0]]["Ashcombe Road"] <= -MARGIN, "%+.2f MW" % mt[REPLAY[0]]["Ashcombe Road"])
    bc = EP.BY_CLASS_NAME
    rb = EP.results_of(short_t[bc], names, TPMAP, CALL)
    rbp = F["route_figures"][bc]
    out_b = outside(rb["R4"], Bd["R4"])
    check("each class's record read from the commissioned sites alone: the same list, the megawatts in service outside their bands",
          sets_t[bc] == CALL and F["route_sets"][bc] == CALL and {"Ashcombe Road", "Fenwick Street"} <= set(out_b) and
          rb["R4"]["Fenwick Street"] - Bd["R4"]["Fenwick Street"][1] >= 0.3 and
          rb["R4"]["Ashcombe Road"] - Bd["R4"]["Ashcombe Road"][1] >= 0.3 and rbp["Fenwick Street"]["commit"],
          "megawatts in service read %.1f at Ashcombe Road and %.1f at Fenwick Street (%s and %s); %d of %d process load sites whose planned date has passed were still to come at the extract and %d had been withdrawn"
          % (rb["R4"]["Ashcombe Road"], rb["R4"]["Fenwick Street"], F["r4_in_service"]["Ashcombe Road"], F["r4_in_service"]["Fenwick Street"],
             F["classes"]["Process load"]["sites"] - F["classes"]["Process load"]["commissioned"] - F["classes"]["Process load"]["withdrawn"],
             F["classes"]["Process load"]["sites"], F["classes"]["Process load"]["withdrawn"]))
    # the come-back read as the record's megawatts puts Ashcombe Road a few tenths under firm capacity, as Response 2
    # filed it (27.4 MW, 5 per cent): its list is the run record's own knife edge, reported here and kept off the gate
    every = [n for n, o in EP.SHORTCUTS if o.get("comeback") != "fixed"]
    mp = F["route_margins"]
    nearest = min((abs(m[n][z]), n, z, where) for where, m in (("clean truth", mt), ("pack", mp)) for n in every for z in names)
    fx = [n for n, o in EP.SHORTCUTS if o.get("comeback") == "fixed"]
    check("every shortcut, every primary: distance from firm capacity", nearest[0] >= ROUTE_MARGIN,
          "nearest is %.2f MW (%s, %s, on the %s), over %d routes with the quick pass among them; the %d routes with the come-back "
          "as the record's megawatts put Ashcombe Road %s MW from firm capacity on the pack and every other primary %.2f MW or more"
          % (nearest[0], nearest[2], nearest[1][:50], nearest[3], len(every), len(fx),
             " and ".join("%+.2f" % mp[n]["Ashcombe Road"] for n in fx),
             min(abs(m[n][z]) for m in (mt, mp) for n in fx for z in names if z != "Ashcombe Road")))
    sens = eff["sensitivity"]
    # recorded, not the gate: a run that reads the cold end as the golden does and still replays the record's megawatts
    # misses one judgment, and told it, recovers everything it lost (the note's Effort test says so)
    check("sensitivity: the careful pass with the cold end read as a curve", sens["score"] < 60.0 and
          sens["commits"] == car_sens_verdicts(names) and set(sens["hints"][0]["rescues"]) == {"R7", "R8", "R9", "R10", "R11", "R12", "R14"},
          "verdicts as the careful pass's; scores %.1f, under the bar; told the come-back sentence it recovers %s (half the "
          "results: the one judgment it misses)" % (sens["score"], ", ".join(sens["hints"][0]["rescues"])))
    wrong = {tuple(v) for k, v in R.items() if v != F["r11_verdicts"]}
    careful_name = [n for n, o in EP.SHORTCUTS if o is EP.CAREFUL][0]
    car_v = dict(v.split(": ", 1) for v in R[careful_name])
    check("routes: different shortcuts, different answers", len(wrong) >= 5 and car_v["Ashcombe Road"] == "hold"
          and all(car_v[n].startswith("reinforce, or") for n in ("Charlecote Way", "Dunmore Street")),
          "%d distinct wrong answers; the careful but hurried pass holds Ashcombe Road and offers Charlecote Way and Dunmore "
          "Street to more flexibility" % len(wrong))

    # ------------------------------------------------------------------------------------------------ BAR R3, R5, R6
    car = F["careful"]
    out = {rid: outside(car[rid], Bd[rid], 0.0, GOLD.get(rid)) if car[rid] is not None else ["missing"] for rid in Bd}
    check("BAR R3 the hurried figures sit outside the bands", "Dunmore Street" in out["R1"] and out["R7"] == ["missing"]
          and {"Ashcombe Road", "Dunmore Street"} <= set(out["R9"]) and set(NONE_AT) <= set(out["R11"])
          and "schedule" in out["R12"] and not out["R2"] and not out["R4"] and not out["R5"] and not out["R13"],
          "the careful but hurried pass: Dunmore Street's 2025/26 demand %.1f MW (band %s to %s), no come-back per megawatt, "
          "Ashcombe Road %.1f and Dunmore Street %.1f MW nine days in ten, further contracts of %s MW where none would do, "
          "Ashcombe Road scheduled at %.1f MW; the customers, the megawatts in service, the share and the data hall inside "
          "their bands"
          % (car["R1"]["Dunmore Street"], *Bd["R1"]["Dunmore Street"], car["R9"]["Ashcombe Road"], car["R9"]["Dunmore Street"],
             ", ".join("%s" % car["R11"][n] for n in NONE_AT), car["R12"]["schedule"]))
    hints = eff["hints"]
    lost = [r["id"] for r in eff["results"] if EP.grade(r["id"], r["passes"]["careful"], r["golden"], Bd) != "right"]
    worst = max(len(h["rescues"]) for h in hints)
    check("BAR R6 the one-fact test, computed", worst <= len(eff["results"]) / 3.0
          and hints[0]["rescues"] == ["R7", "R11", "R12", "R14"] and hints[1]["rescues"] == ["R1", "R3", "R6"]
          and all(not h["rescues"] for h in hints[2:]),
          "the careful pass loses %d of %d results; told one sentence it recovers %s; the two together, %d"
          % (len(lost), len(eff["results"]), ", ".join("%d" % len(h["rescues"]) for h in hints),
             len(eff["compound"][0]["rescues"])))
    told = {i: EP.results_of(E.analyse(X, **o), names, pmap, CALL) for i, (_, o) in enumerate(EP.HINTS[:2])}
    still = {i: [rid for rid in lost if EP.grade(rid, told[i][rid], F[[m[3] for m in EP.META if m[0] == rid][0]], Bd) != "right"]
             for i in told}
    check("BAR R5 no one thing", all(len(h["rescues"]) <= len(eff["results"]) / 3.0 for h in hints) and all(len(v) >= 3 for v in still.values()),
          "each sentence rescues a third of the results or fewer; told the come-back the careful pass still loses %s, told "
          "the cold end %s" % (", ".join(still[0]), ", ".join(still[1])))

    # each factor's footprint across the data, counted in the form that misleads
    cold = {}
    for p in W.PRIMARIES:
        Dd, Pp = E.day_frame(XT, p["code"])
        zone = p["key"] in key.values()
        if zone:
            h = E._mfit(Dd, "hinge")
            cold[p["name"]] = (-float(h["coef"][0]), -float(h["coef"][0]) + float(h["coef"][1]))
        else:       # no service ever ran here: the evening peak itself, every working weekday
            d2 = Dd[Dd["work"] & ~Dd["switch"] & Dd["complete"]]
            pk = Pp.loc[d2.index].max(axis=1).values
            ws = sorted(set(d2["winter"]))
            best = None
            for k in np.arange(-1.0, 4.01, 0.5):
                Xk = np.column_stack([(d2["winter"] == w).values.astype(float) for w in ws] + [d2["T"].values, np.maximum(0.0, k - d2["T"].values)])
                b, *_ = np.linalg.lstsq(Xk, pk, rcond=None)
                sse = float(((pk - Xk @ b) ** 2).sum())
                if best is None or sse < best[0]:
                    best = (sse, b)
            cold[p["name"]] = (-float(best[1][-2]), -float(best[1][-2]) + float(best[1][-1]))
    steeper = [n for n, (a, b) in cold.items() if b > a * 1.08]
    unzoned = [p["name"] for p in W.PRIMARIES if p["key"] not in key.values()]
    lm = by_name(short_t[LINE[0]])
    mis_line = [n for n in names if not (Bd["R1"][n][0] <= round(lm[n]["before26"], 1) <= Bd["R1"][n][1])]
    check("BAR R5 the cold end: across the nine primaries", len(steeper) >= 6 and all(n in steeper for n in unzoned)
          and "Ashcombe Road" in mis_line and "Dunmore Street" in mis_line,
          "demand rises faster per degree below the knee at %d of 9 primaries (%s); the line through the days without a service misreads 2025/26 demand at %s and decides only Dunmore Street"
          % (len(steeper), ", ".join("%s %.2f to %.2f" % (n.split()[0], a, b) for n, (a, b) in cold.items()), ", ".join(mis_line)))
    C_, M_ = E.conn_frame(XT)
    young = M_[M_["age"] <= 9].groupby("type")["ratio"].mean()
    old = M_[M_["age"] >= 30].groupby("type")["ratio"].mean()
    rising = [t for t in old.index if t in young.index and young[t] < 0.75 * old[t]]
    fits = E.buildup_fit(M_)
    other = [p["code"] for p in W.PRIMARIES if p["key"] not in key.values()]
    diff = {c: abs(E.connections_add(XT, c, "mature", fits, C_, M_)[0] - E.connections_add(XT, c, "own", fits, C_, M_)[0]) for c in other}
    check("BAR R5 the build-up: across every type and primary", len(rising) >= 8 and sum(1 for v in diff.values() if v >= 0.25) >= 2,
          "%d of %d customer types draw under three quarters of their established share in their first nine months; at the four primaries with no flexibility zone the short reading is off by %s MW and decides nothing"
          % (len(rising), len(old), ", ".join("%.2f" % v for v in diff.values())))
    reg = E.register_as_at(XT["assets"], XT["register_date"])
    inc = E.incidence(reg, XT["register_date"], group=("cls",))
    med = {c[0]: v["median_late"] for c, v in inc.items()}
    zones_slow = reg[reg["cls"].isin(["Process load", "Battery storage"])]["zone"].nunique()
    planned_run = by_name(short_t[[n for n, o in EP.SHORTCUTS if o == dict(comm="planned")][0]])
    mis_svc = [n for n in names if not (Bd["R4"][n][0] <= round(planned_run[n]["commissioned"], 1) <= Bd["R4"][n][1])]
    check("BAR R5 commissioning by class: across the register", med["Process load"] >= 4 * med["Commercial refrigeration"] and med["Battery storage"] >= 2 * med["EV charging aggregation"]
          and zones_slow >= 20 and "Ashcombe Road" in mis_svc and "Fenwick Street" in mis_svc,
          "median days late by class: %s; process load and battery sites sit in %d zones of the licence area; the planned dates misread the megawatts in service at %s and decide only Fenwick Street"
          % (", ".join("%s %d" % (c.split()[0], round(v)) for c, v in sorted(med.items())), zones_slow, ", ".join(mis_svc)))

    # ----------------------------------------------------------------------------- BAR R7: rivals ruled out by named data
    dz = E.day_frame(XT, W.BY["D"]["code"])[0]
    lin = E._mfit(dz, "linear")
    c1 = lin["T"] <= -1.0
    t_lin = float(lin["resid"][c1].mean() / (lin["resid"][c1].std(ddof=1) / math.sqrt(c1.sum())))
    spl = E._mfit(dz, "spline")
    check("BAR R7 a straight line through the mornings is ruled out", lin["resid"][c1].mean() >= 0.3 and t_lin >= 4.0 and abs(spl["resid"][spl["T"] <= -1.0].mean()) <= 0.1,
          "Dunmore Street: on the %d working weekdays at or below minus 1 C the straight line reads the morning %.2f MW low (t %.1f); the curve is within %.2f"
          % (int(c1.sum()), lin["resid"][c1].mean(), t_lin, abs(spl["resid"][spl["T"] <= -1.0].mean())))
    cz = {n: (Zp[n]["coldest_clean"], Zp[n]["clean_days"], Zp[n]["morning_cold"]) for n in names}
    check("BAR R7 the days without a service are not design days", all(cz[n][0] >= 0.0 for n in ("Ashcombe Road", "Dunmore Street", "Fenwick Street"))
          and min(v[2] for v in cz.values()) >= 30,
          "coldest working weekday without a service in 2025/26: %s; working weekdays at or below 0 C on record: %d"
          % (", ".join("%s %.1f C" % (n.split()[0], cz[n][0]) for n in names), cz[names[0]][2]))
    U = {t: f["U"] for t, f in fits.items() if t != "_pooled" and not f.get("borrowed")}
    check("BAR R7 one build-up for every type is ruled out", max(U.values()) >= 2.0 * min(U.values()),
          "established draw as a share of agreed capacity runs from %.2f to %.2f across %d customer types" % (min(U.values()), max(U.values()), len(U)))
    due = reg[np.array([p <= XT["register_date"] for p in reg["planned"]], bool)]
    ontime = np.mean([E._isdate(c) and c <= p for c, p in zip(due["commissioned"], due["planned"])])
    check("BAR R7 the planned dates are ruled out", ontime <= 0.05, "%.1f per cent of %d sites whose planned date has passed were in service by it" % (100 * ontime, len(due)))
    code_of = {G["zones"][c]["name"]: c for c in G["zones"]}
    regp = E.register_as_at(X["assets"], X["register_date"])
    own = {n: [E.in_service(regp, code_of[n], dt.date(y, 1, 15)) / X["previous"][n]["%d/%02d" % (y - 1, y % 100)]
               for y in (2024, 2025, 2026)] for n in names}
    check("BAR R7 the zone's own record does not hold the award's classes", min(own["Fenwick Street"][1:]) >= 0.95 and
          F["sites"]["Fenwick Street"].get("Process load", {}).get("sites", 0) >= 15,
          "Fenwick Street had %s of its contract in service in mid January 2025 and 2026, on refrigeration and HVAC; %d of its sites still to come are process load"
          % (" and ".join("%.2f" % v for v in own["Fenwick Street"][1:]), F["sites"]["Fenwick Street"].get("Process load", {}).get("sites", 0)))

    # the come-back runs in proportion to what a window delivered: per megawatt it is the same on the record's small and
    # large deliveries, in megawatts it is not, so the record's megawatts cannot stand for the design day's
    ev = G["events"]
    code_of_name = {G["zones"][c]["name"]: c for c in G["zones"]}
    corv_codes = [c for c, p in X["provider_of"].items() if p == X["provider_of"][code_of_name["Ashcombe Road"]]]
    corv = ev[ev["code"].isin(corv_codes) & (ev["delivered"] > 0.5)]
    first = np.array([p[0] for p in corv["post"]])
    dl = corv["delivered"].values
    small, large = dl <= np.median(dl), dl > np.median(dl)
    per_s, per_l = first[small].sum() / dl[small].sum(), first[large].sum() / dl[large].sum()
    mw_s, mw_l = first[small].mean(), first[large].mean()
    check("BAR R7 the come-back as the record's megawatts is ruled out", abs(per_l / per_s - 1.0) <= 0.25 and mw_l >= 1.8 * mw_s
          and F["zones"]["Ashcombe Road"]["event_mean_delivered"] * 3.0 <= F["r6_delivered"]["Ashcombe Road"],
          "Corvane's events in the half-hour ending 20:00: %.2f and %.2f MW back per MW delivered on the smaller and larger half "
          "of %d deliveries, %.2f and %.2f MW in all; Ashcombe Road's events delivered a mean of %.2f MW against %.1f on the "
          "design day" % (per_s, per_l, len(dl), mw_s, mw_l, F["zones"]["Ashcombe Road"]["event_mean_delivered"],
                          F["r6_delivered"]["Ashcombe Road"]))

    # ------------------------------------------------------------------------------------------- the semantic forks
    guide, award = X["guideline_text"], X["award_text"]
    body = lambda t: " ".join(" ".join(l for l in t.splitlines() if not re.search(r"\|\s+Page \d+ of \d+", l)).split())
    gflat, aflat = body(guide), body(award)

    def has(text, *sentences):
        return all(s in text for s in sentences)

    check("SF1 the design day", has(gflat, "working weekday on which the daily mean air temperature at Halverton weather station is minus 3.0 degrees Celsius",
                                    "mean of the station's hourly readings for the GMT day", "24 December to 2 January"), "guideline 2")
    check("SF2 the assessment date", has(gflat, "assessed as at 15 January of that winter, the assessment date"), "guideline 2")
    check("SF3 every such day", has(gflat, "The assessment concerns every such day, whether or not a flexibility service would be instructed on it"), "guideline 2")
    Xs = dict(X)
    Xs.pop("_frames", None)
    Xs["switching"] = X["switching"].iloc[0:0]
    vs = E.analyse(Xs)
    rs = EP.results_of(vs, names, pmap, CALL)
    moved = sorted({r for r in Bd if outside(rs[r], Bd[r], 0.0, GOLD.get(r))})
    check("SF4 the normal running arrangement", has(gflat, "no load transferred to or from the primary across a normally open point",
                                                    "What a service delivered is taken only from days on which the primary was in its normal running arrangement")
          and commits(vs, names) == CALL,
          "guideline 3 and 6 rule the logged transfer days out, for the demand and for what a service delivered; left in, the list is the same and %s leave their bands" % (", ".join(moved) or "no figures"))
    check("SF5 growth", has(gflat, "for each year between the two winters, compounded", "grow in the proportion its highest half-hour grows"), "guideline 4")
    check("SF6 the customers counted", has(gflat, "customers on the load growth register will have added to the primary's demand between the two assessment dates",
                                           "an offer counts once it is accepted", "taken to be energised on the date the register holds for it",
                                           "withdrawn, superseded or only quoted are not counted"), "guideline 4")
    fam_ok = lambda keys: all(F["family_sets"][k] == CALL for k in keys)
    V = [n for n, _ in B.VARIANTS]
    check("SF7 the form of the mornings' temperature response", fam_ok(V[0:3]), "three variants (a knee, a curve below a knee, the cold days' own line): the same list, inside the bands")
    check("SF8 the hours taken as the morning", fam_ok(V[3:4]), "one variant (the half-hours ending 09:00 to 15:00): the same list, inside the bands")
    check("SF9 the winters behind the latest winter's demand", fam_ok(V[4:7]), "three variants (two winters, one, a drift read at 15 January): the same list, inside the bands")
    check("SF10 how an evening is tied to its morning", fam_ok(V[7:8]), "one variant (each half-hour regressed on the day's own morning): the same list, inside the bands")
    check("SF11 a customer's demand", has(gflat, "mean demand between 17:00 and 18:00 on working days") and "mean_kw_1700_1800_working_days" in
          open(os.path.join(TARGET, PK.F_MON)).readline(), "guideline 4 and the summary's own column")
    check("SF12 a customer's own level and the build-up's shape", fam_ok(V[8:11]), "three variants: the same list, inside the bands")
    check("SF13 the sites counted", has(aflat, "No site may be added to a 2027/28 schedule after 16 October 2026") and
          max(s for s in X["assets"]["signed"]) <= dt.date(2026, 10, 16), "the award notice; no site on the register was signed after 16 October 2026")
    check("SF14 in service", has(gflat, "in service from the day it passes that test until it is withdrawn or leaves the service",
                                 "sites in service on the assessment date"), "guideline 6")
    check("SF15 the record a site still to come is read on", fam_ok(V[11:14]), "three variants: the same list, inside the bands")
    check("SF16 megawatts delivered", has(gflat, "quoted as its mean delivery in the half-hours ending 17:30 and 18:00"), "guideline 6")
    check("SF17 the share's line and the calls that were met", fam_ok(V[14:17]), "three variants: the same list, inside the bands")
    check("SF18 instructed in full", has(gflat, "instructed in full: the megawatts contracted for that winter in the contract award notice, scheduled for the whole of the service window"), "guideline 6")
    check("SF19 the peak with flexibility", has(gflat, "highest half-hourly demand on the design day with the service delivered through its window, whichever half-hour that falls in"), "guideline 6")
    check("SF20 one design day in ten", has(gflat, "on more than one design day in ten",
                                             "by the same proportion in every half-hour of the day",
                                             "whatever the day's demand", "taken over those three variations together",
                                             "by drawing not fewer than 100,000 design days", "are held at their central values")
          and E.DRAWS >= 100000, "guideline 7 names what varies, how many days are drawn and what is held; the golden draws %d" % E.DRAWS)
    check("SF21 firm capacity", X["firm"] == {p["code"]: p["firm"] for p in W.PRIMARIES} and all(PK.firm_from_nameplate(p["key"]) == p["firm"] for p in W.PRIMARIES),
          "Appendix A read back from the PDF, and the register's ratings agree with it")
    check("SF22 the megawatts contracted", {X["names"][c]: v for c, v in X["contracts_code"].items()} == {W.BY[z["key"]]["name"]: z["mw"]["2027/28"] for z in W.ZONES}
          and all(X["previous"][W.BY[z["key"]]["name"]] == z["mw"] for z in W.ZONES), "the award notice's two tables read back from the PDF")
    # SF23: the one day in ten by a normal reading at the peaking half-hour, against the days drawn
    nrm = {}
    for n in names:
        q = Zp[n]
        if q["peak_hh"] in ("17:30", "18:00"):
            sd = math.hypot(q["sd_day"] * (q["before28"]), q["cv"] * q["delivered"])
            nrm[n] = abs(q["peak"] + 1.2815515655446004 * sd - q["p90"])
    check("SF23 the nine days in ten", max(nrm.values()) <= 0.3, "a normal reading at the peaking half-hour is within %.2f MW of the days drawn, at the %d primaries that peak inside the window" % (max(nrm.values()), len(nrm)))
    # SF26 to SF28: the three choices' own terms
    step_rows = X["assets"][X["assets"]["winter"] == "2027/28"]
    check("SF26 a further contract on the award's terms", set(X["contracts_code"]) <= set(step_rows["zone"]) and
          all(1.0 <= step_rows[step_rows["zone"] == c]["kw"].sum() / 1000.0 / (X["contracts_code"][c] - X["previous"][X["names"][c]]["2026/27"])
              <= 1.25 for c in X["contracts_code"]),
          "the register's service year marks each zone's 2027/28 sites; each provider signed between its step and a quarter "
          "more, as for every earlier winter")
    evs = G["events"]
    metf = E.met(evs)
    check("SF27 a schedule short of what is available", metf.mean() >= 0.3 and
          float(np.median(np.abs(evs["delivered"].values[metf] / evs["scheduled"].values[metf] - 1.0))) <= 0.06,
          "%.0f per cent of the completed events met their schedule, delivering it within %.1f per cent at the median"
          % (100 * metf.mean(), 100 * float(np.median(np.abs(evs["delivered"].values[metf] / evs["scheduled"].values[metf] - 1.0)))))
    fdh = G["buildup"][E.CUSTOMER["type"]]
    check("SF28 the data hall", fdh["n_conn"] >= 5 and not fdh.get("borrowed") and E.CUSTOMER["energised"] < E.ASSESS,
          "%d data halls in the settlement summary carry the type's own build-up; the prompt's customer is energised before "
          "the assessment date" % fdh["n_conn"])
    check("SF29 the primaries assessed", has(gflat, "every primary substation in a constraint managed zone") and len(X["contracts_code"]) == 5
          and sorted(X["names"][c] for c in X["contracts_code"]) == names,
          "guideline 1 and the award notice: the five constraint managed zone primaries")
    # SF24: a cancelled instruction's day left out altogether
    Xc = dict(X)
    Xc.pop("_frames", None)
    canc = X["events"][X["events"]["status"] == "Cancelled"]
    dem = X["prep"] if "prep" in X else E.prepare(X["demand"])
    drop = set(zip(canc["zone"], canc["date"]))
    keep = np.array([(c, d_) not in drop for c, d_ in zip(dem["code"], dem["ldate"])], bool)
    Xc["demand"] = X["demand"][keep].reset_index(drop=True)
    Xc.pop("prep", None)
    Xc.pop("tmean", None)
    vc = E.analyse(Xc)
    rcx = EP.results_of(vc, names, pmap, CALL)
    check("SF24 a cancelled instruction's day", commits(vc, names) == CALL and not any(outside(rcx[r], Bd[r], 0.0, GOLD.get(r)) for r in Bd),
          "%d cancelled instructions: with their days left out, the same list and every figure inside its band" % len(canc))
    # SF25: megawatts delivered between 17:00 and 18:00, as the mean of the half-hours ending 17:30 and 18:00
    # (guideline 6) against either of the two half-hours on its own
    one = {}
    for n in names:
        q = Zp[n]
        ramp = [f["ramp"] for p, f in G["fits"].items() if n in F["providers"][pmap[p]]["zones"]][0]
        one[n] = max(abs(q["delivered"] * (float(ramp[E.WINDOW.index(h)]) - 1.0)) for h in E.CREDIT_HH)
    check("SF25 megawatts delivered between 17:00 and 18:00", has(gflat, "quoted as its mean delivery in the half-hours ending 17:30 and 18:00")
          and max(one.values()) <= 0.05,
          "guideline 6; either half-hour on its own is within %.2f MW of the mean of the two at every primary" % max(one.values()))

    # ------------------------------------------------------------------------------------------------ BAR R2: Layer 1
    neutral = {}
    for item in ("held_values_kept", "first_megawatts", "raw_weather", "superseded_sites_kept", "classes_as_typed"):
        Xm = PA.load(TARGET, mis=(item,))
        vm = E.analyse(Xm)
        rm = EP.results_of(vm, names, pmap, CALL)
        neutral[item] = (commits(vm, names) == CALL, [(r, k) for r in Bd for k in outside(rm[r], Bd[r], 0.0, GOLD.get(r))])
    check("BAR R2 each mess item read the careless way", all(v[0] and not v[1] for v in neutral.values()),
          "; ".join("%s: %s" % (k.replace("_", " "), "same list, inside the bands" if (v[0] and not v[1]) else "MOVES %s" % v[1][:3]) for k, v in neutral.items()))
    raw = pd.read_csv(os.path.join(TARGET, PK.F_SCADA), dtype={"quality": str})
    dup = int(raw.duplicated().sum())
    check("L1 the SCADA export", dup > 0 and raw["point"].nunique() == 18 and set(raw["quality"]) == {"G", "S", "B"} and
          len(X["demand"]) == len(X["demand"].drop_duplicates(subset=["code", "t_utc"])),
          "%d re-sent rows counted once; 18 point names for nine primaries; quality G, S and B" % dup)
    tsw = [s for s in T["switching"] if s["mw_at_start"] > 0]
    check("L1 the switching log", len(X["switching"]) == len(tsw), "%d transfers paired from %d logged operations" % (len(tsw), 2 * len(tsw)))
    done = [e for e in T["events"] if e["status"] == "Completed"]
    check("L1 the dispatch log", int((X["events"]["status"] == "Completed").sum()) == len(done) and X["events"]["provider"].nunique() == 2,
          "%d completed instructions after the latest revision of each; two providers after their spellings" % len(done))
    tc = [c for c in T["connections"]]
    check("L1 the growth register", len(X["connections"]) >= len(tc) and int(X["connections"]["energised"].notna().sum()) == sum(1 for c in tc if c["energised"])
          and X["connections"]["code"].notna().all(),
          "%d live rows (%d customers on supply), every feeder mapped to its primary through both its codes" % (len(X["connections"]), sum(1 for c in tc if c["energised"])))
    ta = [a for a in T["assets"] if a["signed"] <= W.REGISTER_DATE]
    araw = pd.read_csv(os.path.join(TARGET, PK.F_ASSET), dtype=str, keep_default_na=False)
    check("L1 the asset register", len(X["assets"]) == len(ta) and int((araw["status"] == "Superseded").sum()) > 0 and araw["asset_class"].nunique() > 6
          and X["assets"]["cls"].nunique() == 6 and X["assets"]["provider"].nunique() == 5,
          "%d sites after %d superseded entries; six asset classes and five providers after their spellings" % (len(ta), int((araw["status"] == "Superseded").sum())))
    mraw = pd.read_csv(os.path.join(TARGET, PK.F_MON), dtype={"mpan_core": str})
    check("L1 the monthly summary", len(X["monitor"]) < len(mraw) and X["monitor"]["conn"].nunique() == sum(1 for c in tc if c["energised"] and c["energised"] < dt.date(2026, 10, 1)),
          "%d of %d rows belong to the register's customers" % (len(X["monitor"]), len(mraw)))

    # ----------------------------------------------------------------------------------------- BAR R1, R4: the pack
    files = sorted(os.listdir(TARGET))
    exts = {os.path.splitext(f)[1] for f in files}
    heads = {f: open(os.path.join(TARGET, f)).readline().lower() for f in files if f.endswith(".csv")}
    result_cols = [f for f, h in heads.items() if re.search(r"design_day|expected|forecast|available|in_service|delivered", h)]
    check("BAR R1 the field's raw material ships", not result_cols and len(raw) >= 190000 and len(araw) >= 1400 and len(mraw) >= 12000,
          "half-hourly SCADA (%d rows), instructions, hourly weather, site-level register (%d rows), customer-month readings (%d rows); no column holds a result" % (len(raw), len(araw), len(mraw)))
    prof = X["prep"].pivot_table(index=["code", "ldate"], columns="hh", values="mw").dropna()
    rep = int(prof.round(3).duplicated().sum())
    check("BAR R4 no plant", rep == 0 and not any(re.search(r"memo|draft|note|readme|dictionary|manifest|codebook|schema", f, re.I) for f in files),
          "no day's profile repeats another's; no memo, draft or describing file ships")
    check("inputs: files", len(files) >= 10 and {".csv", ".xlsx", ".pdf"} <= exts and sorted(files) == sorted(PK.FILES), "%d files: %s" % (len(files), sorted(exts)))
    check("inputs: large CSVs", len(raw) >= 20000 and len(araw) >= 600, "%d and %d rows" % (len(raw), len(araw)))
    src = "".join(open(os.path.join(HERE, f)).read() for f in ("parse.py", "estim.py"))
    check("distractors unread", all(f not in src for f in PK.DISTRACTORS) and len(PK.DISTRACTORS) >= 2, "%d files the assessment never reads" % len(PK.DISTRACTORS))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    mtxt = json.dumps(meta).lower()
    check("metadata.json", sorted(f["path"] for f in meta["files"]) == sorted("target/" + f for f in files) and
          sorted(meta["distractor_files"]) == sorted("target/" + f for f in PK.DISTRACTORS) and
          not re.search(r"morning|build-up|build up|asset class|days late|knee|straight line", mtxt),
          "every file with its source; the distractors named; no word of the method")

    # ------------------------------------------------------------------------------------------------ realism
    ev = X["events"][X["events"]["status"] == "Completed"]
    counts = ev.assign(w=[E.winter_of(d_) for d_ in ev["date"]]).groupby(["zone", "w"]).size()
    check("realism: event counts", counts.nunique() >= 9 and counts.max() < 80, "per zone and winter: %s" % [int(v) for v in counts.values])
    refs = sorted(int(s[3:]) for s in set(araw["site_ref"]))
    steps = np.diff(refs)
    order_ok = list(araw["site_ref"]) != sorted(araw["site_ref"])
    check("realism: nothing dealt in sequence", len(set(steps.tolist())) > 50 and order_ok and
          araw.groupby("asset_class").size().nunique() >= 6,
          "site references are not a sequence, the register is not in reference order, class counts are uneven")
    lates = [(PA._day(c) - PA._day(p)).days for c, p in zip(araw["commissioning_test_passed"], araw["planned_commissioning"]) if c]
    check("realism: no setting shows", len(set(lates)) >= 200 and all(abs(F["providers"][p]["share"] * 100 % 5) > 0.3 for p in F["providers"]) and
          ev["scheduled_mw"].nunique() >= 10,
          "%d distinct days late; %d distinct megawatts scheduled; the shares (%s) are not round figures"
          % (len(set(lates)), ev["scheduled_mw"].nunique(), ", ".join("%.2f" % F["providers"][p]["share"] for p in F["providers"])))
    duos = subprocess.run(["pdftotext", "-layout", os.path.join(TARGET, PK.F_DUOS), "-"], capture_output=True, text=True).stdout
    text = guide + award + duos
    people = set(re.findall(r"(?<!Appendix )\b(Marion Todd|Clifford Evans|Irene Carpenter|[A-Z]\. [A-Z][a-z]+)\b", text))
    check("realism: personas", people <= {"Marion Todd", "Clifford Evans", "Irene Carpenter", "C. Evans"} and len(people) >= 3, "people named in the documents: %s" % sorted(people))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    check("no em dashes", "\u2014" not in text and "\u2014" not in sub and "\u2013" not in sub, "documents and submission")
    # guideline 7 names the load that comes back after a window as one of the three things that vary from day to day
    # (the reviewer's request that the share's sources of variation be stated); nothing says how it is measured or that
    # it runs in proportion to what a window delivered
    g7 = gflat.lower().replace("the load that comes back after a window varies from one evening to the next", "")
    leak_words = [w for w in ("build-up", "builds up", "build up", "days late", "lateness", "slip", "asset class", "morning", "before the window",
                              "straight line", "knee", "freezing", "comes back", "come back", "rebound", "fell short", "censor", "by class",
                              "in proportion to what", "per megawatt delivered")
                  if w in (g7 + " " + aflat.lower())]
    check("documents name no step", not leak_words and "Halverton weather station" in gflat and "Contract Award Notice" in aflat,
          "the guideline and the award notice carry none of the method's words (%s), and both were read" % (leak_words or "none"))
    check("documents: dates in order", "22/09/2026" in gflat and "21 October 2026" in aflat and X["register_date"] == dt.date(2026, 11, 4)
          and max(c for c in X["assets"]["commissioned"] if E._isdate(c)) <= X["register_date"],
          "guideline 22 September, award notice 21 October, register extract 4 November 2026; no site passes its test after the extract")
    cn = X["connections"]
    gl = [(r.planned - r.accepted).days for r in cn.itertuples() if r.accepted is not None]
    on = cn[cn.energised.notna()]
    check("growth register: dates in order",
          cn.accepted.notna().all() and max(cn.accepted) <= W.GROWTH_SAVED and (on.energised <= W.GROWTH_SAVED).all()
          and min(gl) > 60 and min(gl) < 130 and max(gl) > 540 and all(a.weekday() < 5 for a in cn.accepted),
          "no offer accepted and no customer energised after the register's last save (30 October 2026); acceptance to "
          "energisation runs from %d to %d days over %d live rows, on working days" % (min(gl), max(gl), len(gl)))

    # ------------------------------------------------------------------------------------------------ deliverables
    gz = zipfile.ZipFile(os.path.join(TASK, "golden.zip"))
    check("golden zip", sorted(gz.namelist()) == sorted([GO.F_XLSX, GO.F_PPTX]), "%s" % gz.namelist())
    r = subprocess.run([sys.executable, os.path.join(REPO, ".claude/skills/reduce-house-fixes/scripts/audit_containers.py"), TASK], capture_output=True, text=True)
    check("container gate", r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])

    bad = [c for c, ok, _ in RESULTS if not ok]
    print("\n%d checks, %d failed%s" % (len(RESULTS), len(bad), (": " + ", ".join(bad)) if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
