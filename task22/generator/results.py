"""task22 results: the golden figures (figures.json) and the effort test (effort.json), each pass computed end to end
on the same frames the pack ships. The careful but hurried pass is the run record's: every file cleaned and read,
the field's method run, but today's GIS for every month, the breaker metering's gaps carried at the feeder's own
average, technical losses from the 2019 study, and the 2027 connections at the load they applied for."""
import datetime as dt
import json
import os

import numpy as np

import analysis as A

KEY_FEEDERS = ["CHL-2", "APT-4", "NTH-4", "CHL-3", "NTH-3", "APT-3"]


def customers_at(F, st, when):
    """Service points connected at the end of a month (their first read on or before it) on each feeder."""
    r = F["reads"].drop_duplicates()
    first = r.groupby("ServicePointID")["ReadDate"].min()
    h = A.hidx_utc(when) - 1
    out = {f: 0 for f in A.FEEDERS}
    for sp, d0 in first.items():
        n = st["sp_node"].get(sp)
        if n is None or sp in st["lp_sp"]:
            continue
        if dt.date.fromisoformat(d0) > (when.astimezone(A.TZ) - dt.timedelta(hours=1)).date():
            continue
        j = st["nfh"][n][h]
        if j >= 0:
            out[A.FEEDERS[j]] += 1
    return out


def month_end(y, m):
    n = dt.date(y + (m == 12), m % 12 + 1, 1)
    return dt.datetime(n.year, n.month, 1, tzinfo=A.TZ).astimezone(A.UTC)


def compute(F, topology="history", fill="balance", tech="golden", df_how="aggregate", lights="actual",
            r8="golden"):
    """Every result on one route."""
    st = A.state(F, topology, fill)
    t = A.tech_for(F, st, "golden" if tech in ("study_pct", "study_req") else tech)
    b = A.balance(F, st, t, A.WIN26)
    if tech in ("study_pct", "study_req"):
        n, _ = A.ntl_route(F, topology=topology, fill=fill, tech=tech)
        sd = A.study_table(F)
        tech_f = {f: b[f]["e_in"] + b[f]["rcv"] - b[f]["dlv"] - b[f]["lp"] - b[f]["lights"] - n[f] for f in A.FEEDERS}
    else:
        n = {f: b[f]["ntl"] for f in A.FEEDERS}
        tech_f = {f: b[f]["tech"] for f in A.FEEDERS}
    if lights == "deemed":
        # lights' consumption taken as their deemed kWh: each feeder's area gets its lights' billed kWh
        pass
    jan = (dt.date(2026, 1, 1), dt.date(2026, 2, 1))
    R = {}
    R["e_in_chl3_26"] = b["CHL-3"]["e_in"] / 1000.0
    R["e_in_chl3_jan26"] = A.window_sum(st["P"]["CHL-3"], jan) / 1000.0
    R["e_in_system_26"] = sum(b[f]["e_in"] for f in A.FEEDERS) / 1000.0
    R["purchases_26"] = A.purchases(F, A.WIN26) / 1000.0
    R["substation_26"] = R["purchases_26"] - R["e_in_system_26"]
    c_mar = customers_at(F, st, month_end(2026, 3))
    c_may = customers_at(F, st, month_end(2026, 5))
    R["nth4_cust_mar26"], R["nth4_cust_may26"] = c_mar["NTH-4"], c_may["NTH-4"]
    R["nth3_cust_mar26"], R["nth3_cust_may26"] = c_mar["NTH-3"], c_may["NTH-3"]
    R["nth4_metered_26"] = (b["NTH-4"]["dlv"] + b["NTH-4"]["lp"]) / 1000.0
    R["nth3_metered_26"] = (b["NTH-3"]["dlv"] + b["NTH-3"]["lp"]) / 1000.0
    R["chl2_metered_26"] = (b["CHL-2"]["dlv"] + b["CHL-2"]["lp"]) / 1000.0
    R["lights_actual_26"] = sum(b[f]["lights"] for f in A.FEEDERS) / 1000.0
    R["lights_deemed_26"] = A.deemed_lights(F, A.WIN26) / 1000.0
    R["tech_apt3_26"] = tech_f["APT-3"] / 1000.0
    R["tech_apt4_26"] = tech_f["APT-4"] / 1000.0
    R["tech_system_26"] = sum(tech_f.values()) / 1000.0
    R["tech_system_pct_26"] = 100.0 * sum(tech_f.values()) / sum(b[f]["e_in"] for f in A.FEEDERS)
    R["ntl"] = {f: n[f] / 1000.0 for f in A.FEEDERS}
    R["sweep"] = A.top4(n)
    br = A.bridge(F, st, t, tech_method="golden" if tech not in ("study_pct", "study_req") else tech,
                  topology=topology, fill=fill)
    R["loss_pct_24"] = br["2024"]["pct"]
    R["loss_pct_26"] = br["2026"]["pct"]
    R["loss_change"] = br["change_total"]
    R["d_technical"] = br["change"]["technical"]
    R["d_nontechnical"] = br["change"]["nontechnical"]
    R["d_other"] = br["change"]["lights"] + br["change"]["billing"] + br["change"]["substation"]
    R["bridge"] = br
    df = A.demand_factors(F, df_how)
    R["df_grow"] = df["grow"]
    R["df_cold"] = df["cold"]
    R["new_peaks"] = new_peaks(F, df)
    R["new_peaks_nameplate"] = new_peaks(F, df, nameplate=True)
    if r8 == "golden":
        t27 = A.tech_2027(F, st, df=df)
    elif r8 == "nameplate_study":
        sd = A.study_table(F)
        t27n = A.tech_2027(F, st, df=dict(df, grow=1.0, cold=1.0))
        t27 = {f: dict(tech=sd[f]["pct"] / 100.0 * t27n[f]["e_in"]) for f in t27n}
    elif r8 == "base_pct":
        pct = {f: 100.0 * tech_f[f] / b[f]["e_in"] for f in A.FEEDERS}
        t27 = A.tech_2027(F, st, df=df, base_pct=pct)
    elif r8 == "nameplate":
        t27 = A.tech_2027(F, st, df=df, flat_nameplate=True)
    elif r8 == "no_reconductor":
        t27 = A.tech_2027(F, st, df=df, ignore_reconductor=True)
    R["tech27_apt4"] = t27["APT-4"]["tech"] / 1000.0
    R["tech27_apt3"] = t27["APT-3"]["tech"] / 1000.0
    R["tech27_system"] = sum(v["tech"] for v in t27.values()) / 1000.0
    R["_balance"] = b
    R["_tech27"] = t27
    return R


def new_peaks(F, df, nameplate=False):
    """The peak hourly demand each approved 2027 connection adds: its applied load at the share of applied load
    comparable connected customers draw at their own peaks."""
    out = {}
    for r in F["applications"].itertuples(index=False):
        if r.Status != "Approved":
            continue
        k = 1.0 if nameplate else (df["cold"] if "cold storage" in r.Applicant.lower() else df["grow"])
        out[r.AppNo] = float(r.Connected_kW) * k
    return out


def golden(F):
    return compute(F)


# what each pass files, result by result: the route it runs
CAREFUL = dict(topology="today", fill="mean", tech="study_pct", r8="nameplate_study")
QUICK = dict(topology="today", fill="drop", tech="none")


def quick(F):
    """Ten minutes: the breaker readings as they come (missing hours count nothing), today's GIS, no technical
    losses (the whole residual is non-technical), the lights' deemed kWh, the 2027 connections at their applied
    load on the base year's line loss rate."""
    st = A.state(F, "today", "drop")
    t = A.tech_for(F, st, "golden")
    b = A.balance(F, st, t, A.WIN26)
    R = {}
    R["e_in_chl3_26"] = b["CHL-3"]["e_in"] / 1000.0
    R["e_in_chl3_jan26"] = A.window_sum(st["P"]["CHL-3"], (dt.date(2026, 1, 1), dt.date(2026, 2, 1))) / 1000.0
    R["e_in_system_26"] = sum(b[f]["e_in"] for f in A.FEEDERS) / 1000.0
    c_mar = customers_at(F, st, month_end(2026, 3))
    c_may = customers_at(F, st, month_end(2026, 5))
    R["nth4_cust_mar26"], R["nth4_cust_may26"] = c_mar["NTH-4"], c_may["NTH-4"]
    R["nth4_metered_26"] = (b["NTH-4"]["dlv"] + b["NTH-4"]["lp"]) / 1000.0
    R["lights_actual_26"] = A.deemed_lights(F, A.WIN26) / 1000.0
    R["tech_apt3_26"] = 0.0
    R["tech_system_26"] = 0.0
    raw = {f: b[f]["e_in"] + b[f]["rcv"] - b[f]["dlv"] - b[f]["lp"] for f in A.FEEDERS}
    R["ntl"] = {f: raw[f] / 1000.0 for f in A.FEEDERS}
    R["sweep"] = A.top4(raw)
    br = A.bridge(F, st, t)
    R["loss_change"] = br["change_total"]
    R["d_technical"] = 0.0
    R["d_nontechnical"] = br["change_total"]
    R["d_other"] = 0.0
    R["df_grow"] = 1.0
    t27 = A.tech_2027(F, st, df=dict(A.demand_factors(F), grow=1.0, cold=1.0))
    R["tech27_apt4"] = 0.0
    R["tech27_apt3"] = 0.0
    R["tech27_system"] = 0.0
    return R


# ---------------------------------------------------------------------------------------------------------------
# figures.json and effort.json
# ---------------------------------------------------------------------------------------------------------------

def tables(R):
    """The graded tables, keyed as the answer blocks state them."""
    return {
        "R1_energy_in": {"CHL-3, twelve months to September 2026": round(R["e_in_chl3_26"], 1),
                         "CHL-3, January 2026": round(R["e_in_chl3_jan26"], 1),
                         "fourteen feeders, twelve months to September 2026": round(R["e_in_system_26"], 1)},
        "R2_membership": {"NTH-4 customers, 31 March 2026": int(R["nth4_cust_mar26"]),
                          "NTH-4 customers, 31 May 2026": int(R["nth4_cust_may26"]),
                          "NTH-4 metered use, twelve months": round(R["nth4_metered_26"], 1),
                          "NTH-3 metered use, twelve months": round(R["nth3_metered_26"], 1)},
        "R3_lights": {"real use": round(R["lights_actual_26"], 1), "deemed kWh billed": round(R["lights_deemed_26"], 1)},
        "R4_technical": {"APT-3": round(R["tech_apt3_26"], 1), "APT-4": round(R["tech_apt4_26"], 1),
                         "fourteen feeders": round(R["tech_system_26"], 1)},
        "R5_ntl": {f: round(R["ntl"][f], 1) for f in KEY_FEEDERS},
        "R6_bridge": {"line loss, twelve months to September 2024": round(R["loss_pct_24"], 2),
                      "line loss, twelve months to September 2026": round(R["loss_pct_26"], 2),
                      "technical losses, points": round(R["d_technical"], 2),
                      "non-technical losses, points": round(R["d_nontechnical"], 2),
                      "everything else, points": round(R["d_other"], 2)},
        "R7_new_peaks": {k: round(v, 1) for k, v in sorted(R["new_peaks"].items())},
        "R8_tech2027": {"APT-4": round(R["tech27_apt4"], 1), "APT-3": round(R["tech27_apt3"], 1),
                        "fourteen feeders": round(R["tech27_system"], 1)},
        "R9_sweep": list(R["sweep"]),
    }


def bands(T):
    def pct(x, p):
        return [round(x * (1 - p), 1), round(x * (1 + p), 1)]
    b = {}
    t = T["R1_energy_in"]
    b["R1_energy_in"] = {"CHL-3, twelve months to September 2026": pct(t["CHL-3, twelve months to September 2026"], 0.006),
                         "CHL-3, January 2026": pct(t["CHL-3, January 2026"], 0.03),
                         "fourteen feeders, twelve months to September 2026": pct(
                             t["fourteen feeders, twelve months to September 2026"], 0.0012)}
    t = T["R2_membership"]
    b["R2_membership"] = {"NTH-4 customers, 31 March 2026": [t["NTH-4 customers, 31 March 2026"] - 3,
                                                             t["NTH-4 customers, 31 March 2026"] + 3],
                          "NTH-4 customers, 31 May 2026": [t["NTH-4 customers, 31 May 2026"] - 3,
                                                           t["NTH-4 customers, 31 May 2026"] + 3],
                          "NTH-4 metered use, twelve months": pct(t["NTH-4 metered use, twelve months"], 0.015),
                          "NTH-3 metered use, twelve months": pct(t["NTH-3 metered use, twelve months"], 0.015)}
    t = T["R3_lights"]
    b["R3_lights"] = {"real use": pct(t["real use"], 0.04), "deemed kWh billed": pct(t["deemed kWh billed"], 0.003)}
    t = T["R4_technical"]
    b["R4_technical"] = {"APT-3": pct(t["APT-3"], 0.07), "APT-4": pct(t["APT-4"], 0.07),
                         "fourteen feeders": pct(t["fourteen feeders"], 0.04)}
    b["R5_ntl"] = {f: [round(v - max(75.0, 0.09 * v), 1), round(v + max(75.0, 0.09 * v), 1)]
                   for f, v in T["R5_ntl"].items()}
    t = T["R6_bridge"]
    b["R6_bridge"] = {k: [round(v - (0.05 if "line loss" in k else 0.10), 2), round(v + (0.05 if "line loss" in k else
                                                                                           0.10), 2)]
                      for k, v in t.items()}
    b["R7_new_peaks"] = {k: pct(v, 0.05) for k, v in T["R7_new_peaks"].items()}
    t = T["R8_tech2027"]
    b["R8_tech2027"] = {"APT-4": pct(t["APT-4"], 0.07), "APT-3": pct(t["APT-3"], 0.07),
                        "fourteen feeders": pct(t["fourteen feeders"], 0.03)}
    return b


RESULTS = [
    ("R1", "each feeder's energy in, the breaker metering's missing hours rebuilt", "Component 3", "R1_energy_in",
     [], "the delivery point meters and the breakers' telemetry", ["N10"]),
    ("R2", "who each feeder served, month by month, and what their meters recorded", "Component 2", "R2_membership",
     [], "the GIS, the switching log and the meter reads", ["N09", "N14"]),
    ("R3", "the unmetered lights' real use against their deemed kWh", "Ask 3", "R3_lights", [],
     "the lighting inventory, the lamp watts and burning hours, the lighting bills", []),
    ("R4", "each feeder's technical losses at its loads' positions", "Component 1", "R4_technical", ["R1"], "",
     ["L22", "L36"]),
    ("R5", "each feeder's non-technical loss, twelve months to September 2026", "Ask 1", "R5_ntl",
     ["R1", "R2", "R3", "R4"], "", ["L11", "L32"]),
    ("R6", "the rise in line loss bridged to its causes", "Component 4", "R6_bridge", ["R1", "R4"], "",
     ["L26", "L27"]),
    ("R7", "the peak hourly demand each approved 2027 connection adds", "Ask 4", "R7_new_peaks", [],
     "the large power interval meters and the applications", ["L15"]),
    ("R8", "each feeder's technical losses in 2027", "Ask 5", "R8_tech2027", ["R4", "R7"], "", ["N13", "N01"]),
    ("R9", "the four feeders the 2027 sweep covers", "Recommendation", "R9_sweep", ["R5"], "", ["L11"]),
]


def quick_tables(Q, TG):
    """The quick pass's tables: only the cells it computes; a cell it never reaches is filed empty."""
    out = {}
    for key, gold in TG.items():
        if isinstance(gold, dict):
            out[key] = {k: None for k in gold}
        else:
            out[key] = None
    out["R1_energy_in"] = {"CHL-3, twelve months to September 2026": round(Q["e_in_chl3_26"], 1),
                           "CHL-3, January 2026": round(Q["e_in_chl3_jan26"], 1),
                           "fourteen feeders, twelve months to September 2026": round(Q["e_in_system_26"], 1)}
    out["R2_membership"].update({"NTH-4 customers, 31 March 2026": int(Q["nth4_cust_mar26"]),
                                 "NTH-4 customers, 31 May 2026": int(Q["nth4_cust_may26"]),
                                 "NTH-4 metered use, twelve months": round(Q["nth4_metered_26"], 1)})
    out["R3_lights"] = {"real use": round(Q["lights_actual_26"], 1), "deemed kWh billed": round(Q["lights_actual_26"], 1)}
    out["R4_technical"] = {k: 0.0 for k in TG["R4_technical"]}
    out["R5_ntl"] = {f: round(Q["ntl"][f], 1) for f in TG["R5_ntl"]}
    out["R6_bridge"].update({"technical losses, points": 0.0,
                             "non-technical losses, points": round(Q["d_nontechnical"], 2),
                             "everything else, points": 0.0})
    out["R8_tech2027"] = {k: 0.0 for k in TG["R8_tech2027"]}
    out["R9_sweep"] = list(Q["sweep"])
    return out


def pass_values(R, careful=False, F=None):
    T = tables(R)
    if careful:
        T["R7_new_peaks"] = {k: round(v, 1) for k, v in sorted(R["new_peaks_nameplate"].items())}
    return T


def write(F, gen_dir, G_=None, C_=None, Q_=None, extra=None):
    G_ = G_ or golden(F)
    C_ = C_ or compute(F, **CAREFUL)
    Q_ = Q_ or quick(F)
    TG = tables(G_)
    TC = pass_values(C_, careful=True)
    TQ = quick_tables(Q_, TG)
    TQ["R7_new_peaks"] = {k: round(v, 1) for k, v in sorted(C_["new_peaks_nameplate"].items())}
    B = bands(TG)
    figs = dict(TG)
    figs.update({k: (round(v, 3) if isinstance(v, float) else v) for k, v in G_.items()
                 if not k.startswith("_") and k not in ("ntl", "sweep", "bridge")})
    figs["ntl_all"] = {f: round(v, 1) for f, v in G_["ntl"].items()}
    figs["bridge_parts_2024"] = {k: round(v, 3) for k, v in G_["bridge"]["2024"]["parts"].items()}
    figs["bridge_parts_2026"] = {k: round(v, 3) for k, v in G_["bridge"]["2026"]["parts"].items()}
    if extra:
        figs.update(extra.get("figures", {}))
    figs["bands"] = B
    figs["tolerances_pct"] = [3, 0.6, 0.12, 1.5, 4, 7, 0.05, 0.10, 5]
    figs["monthly_rows"] = 14 * 36
    res = []
    for rid, name, graded, key, dep, indep, prec in RESULTS:
        e = dict(id=rid, name=name, graded_as=graded, figure=key, depends=dep, independent=indep, golden=TG[key])
        if isinstance(TG[key], dict):
            e["bands"] = B[key]
        elif isinstance(TG[key], float):
            e["band"] = [round(TG[key] - 0.03, 3), round(TG[key] + 0.03, 3)]
            e["partly"] = [round(TG[key] - 0.06, 3), round(TG[key] + 0.06, 3)]
        e["passes"] = {"quick": TQ[key], "careful": TC[key], "thorough": TG[key]}
        if prec:
            e["precedent"] = prec
        res.append(e)
    E = dict(results=res, weights={"recommendation": 14, "components": 24, "asks": 55, "instruction": 7})
    if extra:
        E.update({k: v for k, v in extra.items() if k != "figures"})
    os.makedirs(gen_dir, exist_ok=True)
    json.dump(figs, open(os.path.join(gen_dir, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(E, open(os.path.join(gen_dir, "effort.json"), "w"), indent=1)
    return figs, E


def monthly(F, st=None):
    """Each feeder's balance month by month, October 2023 to September 2026, with its customers at month end."""
    st = st or A.state(F)
    t = A.tech_for(F, st, "golden")
    out = []
    y, m = 2023, 10
    while (y, m) <= (2026, 9):
        n = dt.date(y + (m == 12), m % 12 + 1, 1)
        win = (dt.date(y, m, 1), n)
        b = A.balance(F, st, t, win)
        cust = customers_at(F, st, month_end(y, m))
        for f in A.FEEDERS:
            x = b[f]
            out.append(dict(month="%d-%02d" % (y, m), feeder=f, customers=cust[f], e_in=x["e_in"] / 1000.0,
                            rcv=x["rcv"] / 1000.0, dlv=x["dlv"] / 1000.0, lp=x["lp"] / 1000.0,
                            lights=x["lights"] / 1000.0, tech=x["tech"] / 1000.0, ntl=x["ntl"] / 1000.0))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def extra_figures(F, G, C, fo):
    """The figures the answer blocks state beyond the graded tables: the careful pass's answers and the shortcuts'
    figures each step rejects, the conventions and the perturbations the closing passage names."""
    sd = A.study_table(F)
    st = A.state(F)
    t27n = A.tech_2027(F, st, df=dict(A.demand_factors(F), grow=1.0, cold=1.0), flat_nameplate=False)
    t27flat = A.tech_2027(F, st, flat_nameplate=True)
    G["study_apt3_pct"] = sd["APT-3"]["pct"]
    G["careful_tech_apt3_26"] = C["tech_apt3_26"]
    x = {
        "careful_sweep": C["sweep"],
        "careful_tech_apt3_26": round(C["tech_apt3_26"], 1),
        "careful_tech_system_26": round(C["tech_system_26"], 1),
        "careful_e_in_chl3_26": round(C["e_in_chl3_26"], 1),
        "careful_e_in_chl3_jan26": round(C["e_in_chl3_jan26"], 1),
        "careful_nth4_cust_mar26": int(C["nth4_cust_mar26"]),
        "careful_nth4_metered_26": round(C["nth4_metered_26"], 1),
        "careful_nth3_metered_26": round(C["nth3_metered_26"], 1),
        "moved_metered_26": round(C["nth4_metered_26"] - G["nth4_metered_26"], 1),
        "careful_ntl": {f: round(v, 1) for f, v in C["ntl"].items()},
        "careful_d_technical": round(C["d_technical"], 2),
        "careful_d_nontechnical": round(C["d_nontechnical"], 2),
        "careful_tech27_apt4": round(C["tech27_apt4"], 1),
        "careful_tech27_apt3": round(C["tech27_apt3"], 1),
        "careful_tech27_system": round(C["tech27_system"], 1),
        "nameplate_tech27_apt4": round(t27flat["APT-4"]["tech"] / 1000.0, 1),
        "nameplate_tech27_system": round(sum(v["tech"] for v in t27flat.values()) / 1000.0, 1),
        "study_apt3_pct": round(sd["APT-3"]["pct"], 2),
        "study_system_pct": round(100.0 * sum(v["pct"] / 100.0 * v["energy"] for v in sd.values()) /
                                  sum(v["energy"] for v in sd.values()), 2),
        "secondary_pct": 0.7,
        "perturbation_pcts": [5, 10, 20],
        "single_phase_factor": 6,
        "fifth_feeder": sorted(G["ntl"], key=lambda f: -G["ntl"][f])[4],
        "fifth_ntl": round(sorted(G["ntl"].values(), reverse=True)[4], 1),
        "margin_4_5": round(sorted(G["ntl"].values(), reverse=True)[3] - sorted(G["ntl"].values(), reverse=True)[4], 1),
    }
    return x
