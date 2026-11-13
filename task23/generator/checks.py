"""task23 architecture 1 checks: the bar (R1 to R7), the forks (SF1 to SF18), the input gates and the realism sweep,
asserted on the built task (target/ as cut, figures.json and effort.json as written).

    python3 task23/generator/checks.py
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import warnings  # noqa: E402

warnings.filterwarnings("ignore")
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402

import analysis as A  # noqa: E402
import params as P  # noqa: E402
import results as RS  # noqa: E402
import world as WD  # noqa: E402

N = {"pass": 0, "fail": 0}


def ok(label, cond, detail=""):
    if cond:
        N["pass"] += 1
        print("PASS  " + label)
    else:
        N["fail"] += 1
        print("FAIL  " + label + ("  " + str(detail) if detail != "" else ""))


def pdf_text(path, layout=False):
    try:
        args = ["pdftotext"] + (["-layout"] if layout else []) + [path, "-"]
        return subprocess.run(args, capture_output=True, text=True).stdout
    except Exception:
        return ""


def has(text, phrase):
    """The phrase in the document's text, compared on letters and digits alone (a PDF's line breaks, its hyphens at
    line ends and its table cells set aside)."""
    k = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    return k(phrase) in k(text)


def flat(t):
    """The document's text as one line: a word broken at a line end by its hyphen joined again."""
    return re.sub(r"\s+", " ", re.sub(r"(\w)-\n(\w)", r"\1-\2", t))


def main():
    target = os.path.join(TASK, "target")
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    F = A.load(target)
    cache = {}
    G = A.run(F, {}, cache)
    C = A.run(F, RS.ROUTES["careful"], cache)
    Gf, Cf = RS.figures(G), RS.figures(C)
    files = sorted(os.listdir(target))
    lim = P.LIMIT_T
    plan_text = pdf_text(os.path.join(target, P.FILES["plan"]))

    # ------------------------------------------------------------------------ R1: the field's raw material ships
    ok("R1 every scale ticket since January 2021 ships", len(F["tickets"]) > 200000, len(F["tickets"]))
    ok("R1 the station's hourly weather since 2016 ships", len(F["weather"]) > 90000, len(F["weather"]))
    ok("R1 the chambers' hourly fluxes ship (three chambers)", F["chambers"]["chamber"].nunique() == 3
       and len(F["chambers"]) > 25000, len(F["chambers"]))
    ok("R1 every well's monthly reading with its liquid level ships", len(F["wells"]) > 8000
       and F["wells"]["depth_to_liquid_ft"].notna().sum() > 1000, len(F["wells"]))
    ok("R1 the gas plant's hourly record ships", len(F["scada"]) > 30000, len(F["scada"]))
    ok("R1 the campaigns, the drone flights and the oxidation plots ship", len(F["campaigns"]) == 8
       and len(F["drone"]) >= 6 and F["oxplots"]["plot_id"].nunique() == 44)
    shipped_cols = set()
    for fn in files:
        p = os.path.join(target, fn)
        if fn.endswith(".csv"):
            shipped_cols |= set(pd.read_csv(p, nrows=2).columns)
        elif fn.endswith(".xlsx"):
            for _, df in pd.read_excel(p, sheet_name=None, nrows=3).items():
                shipped_cols |= set(map(str, df.columns))
    bad = [c for c in shipped_cols if re.search(r"generat|annual|corrected|efficien|emission_t|oxidized_share|"
                                                 r"pressure_factor|decay", c, re.I)]
    ok("R1 no shipped column holds a result (generation, annual emission, corrected rate, efficiency, decay)",
       not bad, bad)

    # ------------------------------------------------------------------------ R2: the mess is real and neutral
    t = F["tickets"]
    voids = t[t["status"].fillna("") == "VOID"]
    reiss = set(t.loc[t["status"].fillna("") == "REISSUE", "ticket_no"])
    ok("R2 every voided ticket ships beside its reissue under the same ticket number",
       len(voids) > 100 and set(voids["ticket_no"]) <= reiss, len(voids))
    blanks = t["disposal_area"].isna().sum()
    ok("R2 tickets without a disposal area ship (before September 2022 and in the scale software's outages)",
       blanks > 1000, blanks)
    old = t["material_code"].isin(list(A.OLD_TO_NEW)).sum()
    ok("R2 the old material codes ship before July 2021", old > 1000 and
       t.loc[t["material_code"].isin(list(A.OLD_TO_NEW)), "ticket_date"].max() < dt.date(2021, 7, 2), old)
    Rr = A.run(F, dict(tickets="raw"), {})
    fr = RS.figures(Rr)
    ok("R2 the tickets as filed move R1 (which grades them) out of its band",
       RS.grade("R1_cell5_msw_tons", figs["R1_cell5_msw_tons"], fr["R1_cell5_msw_tons"]) != "right",
       fr["R1_cell5_msw_tons"])
    moved = [k for k in ("R4_cell5_generation_2027_t", "R5_cell5_oxidized_share_2027_pct", "R7_emissions_2027_t")
             if RS.grade(k, figs[k], fr[k]) != "right"]
    ok("R2 the tickets as filed move no other graded figure beyond its band (cell 5's level rests on its campaigns)",
       not moved and Rr["R8"] == G["R8"], moved)
    sc = F["scada"]
    dup_hours = sc["timestamp_local"].duplicated(keep=False).sum()
    ok("R2 the plant's local wall clock repeats the fall-back hour (PDT to PST) and skips the spring hour",
       dup_hours >= 6 and set(sc["tz"].unique()) == {"PST", "PDT"}, dup_hours)
    sm = A.scada_monthly(F)
    s2 = sc.drop_duplicates("timestamp_local", keep="first").copy()
    F2 = dict(F)
    F2["scada"] = s2
    sm2 = A.scada_monthly(F2)
    y25 = [m for m in range(A.mi(2025, 1), A.mi(2026, 1))]
    ok("R2 dropping the repeated hour moves 2025's collected methane by under 0.1 per cent",
       abs(sm2[y25].sum() / sm[y25].sum() - 1) < 0.001, round(float(sm2[y25].sum() / sm[y25].sum() - 1), 5))
    wx = F["weather"].copy()
    ts = pd.to_datetime(wx["timestamp_lst"].str[:16])
    wx.loc[ts >= pd.Timestamp("2023-06-21 10:00"), "baro_hpa"] += 0.6
    F3 = dict(F)
    F3["weather"] = wx
    R3 = A.run(F3, {}, {})
    ok("R2 the barometer's June 2023 re-siting step, removed, moves 2025's emission by under 1 per cent",
       abs(R3["R2"] / G["R2"] - 1) < 0.01, round(R3["R2"] / G["R2"] - 1, 4))
    reg = F["register"]
    ok("R2 some register rows leave the cell blank (the well id carries it)", reg["cell"].isna().sum() >= 1)

    # ------------------------------------------------------------------------ R3: each result's hurried figure
    for r in E["results"]:
        gr = RS.grade(r["figure"], r["golden"], r["passes"]["careful"])
        if r["id"] == "R1":
            ok("R3 the careful pass earns R1 (the ticket clean-up is a reflex)", gr == "right", gr)
        else:
            ok("R3 the careful pass loses %s (%s)" % (r["id"], gr), gr != "right", r["passes"]["careful"])
    ok("R3 the careful pass picks package A (the reflex route)", C["R8"] == "A", C["R8"])
    b5 = RS.band_scalar("R5_cell5_oxidized_share_2027_pct", figs["R5_cell5_oxidized_share_2027_pct"])
    b4 = RS.band_scalar("R4_cell5_generation_2027_t", figs["R4_cell5_generation_2027_t"])
    ok("R3 the reporting rule's 10 per cent sits a point or more outside R5's band (%.1f to %.1f)" % b5,
       b5[0] - 10.0 >= 1.0)
    ok("R3 the hurried cell 5 generations (the rule's default decay %s t, the dry decay %s t) sit far outside R4's band"
       % (figs["_quick"]["R4_cell5_generation_2027_t"], figs["_extra"]["careful"]["R4"]),
       max(figs["_quick"]["R4_cell5_generation_2027_t"], figs["_extra"]["careful"]["R4"]) < 0.8 * b4[0])

    # ------------------------------------------------------------------------ R4: no plant
    rep = flat(pdf_text(os.path.join(target, P.FILES["ghg2025"]), layout=True))
    m = re.search(r"Methane emissions \(t\) ([\d,]+)", rep)
    ok("R4 the 2025 report's figure reproduces from its own equation on the plant's record (an incumbent)",
       m is not None and int(m.group(1).replace(",", "")) == figs["report_2025_t"] == round(G["R6"]["report"]),
       m.group(1) if m else None)
    mc = re.search(r"Methane collected and sent to the flare and engines \(t\) ([\d,]+)", rep)
    ok("R4 the report's collected methane is the plant record's 2025 sum", mc is not None and
       int(mc.group(1).replace(",", "")) == round(float(sm[y25].sum())), mc.group(1) if mc else None)
    sv = flat(pdf_text(os.path.join(target, P.FILES["survey"]), layout=True))
    ms = re.search(r"equivalent to ([\d,]+) metric tons over a year of 8,760 hours", sv)
    c25 = F["campaigns"][pd.to_datetime(F["campaigns"]["date"]).dt.year == 2025]
    ok("R4 the survey's 2025 figure is the 2025 campaigns' mean times 8,760 hours", ms is not None and
       int(ms.group(1).replace(",", "")) == round(c25["site_kg_h"].mean() * 8.76) == figs["survey_2025_t"],
       ms.group(1) if ms else None)
    st = flat(pdf_text(os.path.join(target, P.FILES["oxstudy"])))
    s = F["oxplots"].dropna(subset=["fraction_oxidized"])
    means = s.groupby("cover")["fraction_oxidized"].mean()
    nfail = int(F["oxplots"]["fraction_oxidized"].isna().sum())
    word = ["No", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"][nfail]
    ok("R4 the oxidation study's count of failed isotope runs is its plot file's (%d)" % nfail,
       has(st, "%s runs whose isotope analysis failed are excluded" % word))
    ok("R4 the oxidation study's means reproduce from its plot file", all(
        ("%.2f" % means[c]) in st for c in ("final", "intermediate", "active")), means.round(2).to_dict())
    dr = F["drone"][pd.to_datetime(F["drone"]["date"]).dt.year == 2025]
    d_t = float(dr["flux_kg_h"].mean()) * 8.76
    ok("R4 the drone flights are an instrument of their own near the survey (within 15 per cent), not a copy",
       abs(d_t / figs["survey_2025_t"] - 1) < 0.15 and abs(d_t - figs["survey_2025_t"]) > 50, round(d_t))
    ok("R4 no shipped artifact ranks the packages on 2027 emissions (Gate G)",
       not re.search(r"2027 emissions? (?:of|at|under)", flat(pdf_text(os.path.join(target, P.FILES["plan"]), True))))

    # ------------------------------------------------------------------------ R5: no one thing; the truth
    W = WD.World()
    ch = F["chambers"]
    ch = ch[ch["qc"] == "OK"].copy()
    ch["t"] = pd.to_datetime(ch["utc"].str[:19]) - pd.Timedelta(hours=8)
    gap = pd.Series(A.ema(cache["wx"]["baro_hpa"].values, G["baro"]["tau"]) - cache["wx"]["baro_hpa"].values,
                    index=cache["wx"].index)
    coefs = {}
    for name, g in ch.groupby("chamber"):
        g = g[g["flux_g_m2_d"] > 0]
        x = gap.reindex(g["t"]).values
        y = np.log(g["flux_g_m2_d"].values)
        mon = g["t"].dt.strftime("%Y-%m").values
        okm = ~np.isnan(x)
        X = pd.get_dummies(pd.Series(mon[okm])).values.astype(float)
        X = np.c_[X, x[okm]]
        coefs[name] = float(np.linalg.lstsq(X, y[okm], rcond=None)[0][-1])
    ok("R5 every chamber, on every cover, breathes with the barometer (AC-2 on cell 3's geomembrane cap too)",
       all(v > 0.01 for v in coefs.values()), {k: round(v, 3) for k, v in coefs.items()})
    c26 = G["campaigns"][pd.to_datetime(G["campaigns"]["date"]).dt.year == 2026]
    ok("R5 the fair-weather rule lowers the 2026 campaigns and the drone flights too, not only 2025's",
       c26["m"].mean() < 0.9 and G["drone"]["m"].mean() < 0.9, (round(c26["m"].mean(), 3),
                                                                round(G["drone"]["m"].mean(), 3)))
    z = G["z"]
    ok("R5 the flooded wells spread across cell 4 (a quarter or more of its wells) and the pilot pumped only some",
       z["n_wet"] >= 0.25 * z["n_wells"] and z["n_pumped"] < z["n_wet"], (z["n_wet"], z["n_pumped"]))
    rec = F["recirc"]
    ok("R5 recirculation runs in both open cells (cell 4 since 2023, cell 5 since July 2026)",
       set(rec["cell"].unique()) == {4, 5} and rec[rec["cell"] == 5]["month"].min() == "2026-07")
    rho = {}
    for cv, g in s[s["fraction_oxidized"] < 0.995].groupby("cover"):
        J = g["surface_flux_g_m2_d"] / (1 - g["fraction_oxidized"])
        rho[cv] = spearmanr(J, g["fraction_oxidized"]).correlation
    ok("R5 the share oxidized falls with the flux on every cover in the study, not only daily cover",
       all(v < -0.3 for v in rho.values()), {k: round(v, 2) for k, v in rho.items()})
    tr = figs["_truth"]
    ok("R5 the golden's 2025 emission is within its band of the simulation's (%s against %s)"
       % (figs["R2_actual_2025_t"], tr["actual_2025_t"]),
       RS.grade("R2_actual_2025_t", figs["R2_actual_2025_t"], tr["actual_2025_t"]) == "right")
    ok("R5 the golden's cell 4 change is within its band of the simulation's (%s against %s)"
       % (figs["R3_cell4_generation_change_pct"], tr["cell4_generation_change_pct"]),
       RS.grade("R3_cell4_generation_change_pct", figs["R3_cell4_generation_change_pct"],
                tr["cell4_generation_change_pct"]) == "right")
    ok("R5 the golden's cell 5 generation is within its band of the simulation's (%s against %s)"
       % (figs["R4_cell5_generation_2027_t"], tr["cell5_generation_2027_t"]),
       RS.grade("R4_cell5_generation_2027_t", figs["R4_cell5_generation_2027_t"], tr["cell5_generation_2027_t"])
       == "right")
    ok("R5 the golden's 2027 package figures are each within their band of the simulation's",
       RS.grade("R7_emissions_2027_t", figs["R7_emissions_2027_t"], tr["emissions_2027_t"]) == "right",
       tr["emissions_2027_t"])
    tcall = next(p for p in P.PACKAGES if tr["emissions_2027_t"]["package %s" % p] <= lim)
    ok("R5 the simulation's own 2027 figures pick the golden's package (%s)" % tcall, tcall == G["R8"])

    # ------------------------------------------------------------------------ R6: the one-fact test, computed
    for sent, o in RS.HINTS:
        oo = dict(RS.ROUTES["careful"])
        oo.update(o)
        R = A.run(F, oo, cache)
        h = RS.figures(R)
        resc = [rid for rid, _, fig, *_ in RS.META if RS.grade(fig, figs[fig], h[fig]) == "right"
                and RS.grade(fig, figs[fig], Cf[fig]) != "right"]
        listed = [x["rescues"] for x in E["hints"] if x["sentence"] == sent][0]
        ok("R6 the hint rescues what effort.json lists, a third of the results or fewer: %s" % sent[:50],
           sorted(resc) == sorted(listed) and len(resc) <= len(RS.META) / 3, resc)

    # ------------------------------------------------------------------------ R7: the rivals and the margins
    for name, o in RS.FAMILY[1:]:
        R = A.run(F, o, cache)
        f = RS.figures(R)
        out = [k for k in ("R2_actual_2025_t", "R3_cell4_generation_change_pct", "R4_cell5_generation_2027_t",
                           "R5_cell5_oxidized_share_2027_pct", "R6_bridge", "R7_emissions_2027_t")
               if RS.grade(k, figs[k], f[k]) != "right"]
        ok("R7 rival inside every band and on package %s: %s" % (G["R8"], name[:60]), not out and R["R8"] == G["R8"],
           (out, R["R8"]))
    Rh = A.run(F, dict(baro="ema_hl16_all"), cache)
    fh = RS.figures(Rh)
    outh = [k for k in ("R2_actual_2025_t", "R4_cell5_generation_2027_t", "R6_bridge", "R7_emissions_2027_t")
            if RS.grade(k, figs[k], fh[k]) != "right"]
    ok("R7 the judge's reading (all three chambers, a 16-hour half-life not chosen by fit) stays inside every band and "
       "on package %s (2025 at %.0f t, C %.0f t)" % (Rh["R8"], Rh["R2"], Rh["R7"]["C"]), not outh and Rh["R8"] == G["R8"],
       outh)
    F6 = dict(F)
    cl6 = F["cells"].copy()
    cl6.loc[cl6["cell"] == 5, "footprint_acres"] = figs["_extra"]["cell5_acres_2025_report"]
    F6["cells"] = cl6
    R6x = A.run(F6, {}, {})
    ok("SF19 ruled out by the options paper (leachate across cell 5's whole footprint) and the lifts: the 2025 report's "
       "%.1f acres for cell 5 in 2027 gives an oxidized share of %.1f per cent and still files package %s"
       % (figs["_extra"]["cell5_acres_2025_report"], R6x["R5"], R6x["R8"]),
       R6x["R8"] == G["R8"] and has(plan_text, "across its whole footprint"))
    for how in ("dp12", "dp24"):
        Bx = A.baro_fit(F, how, cache["wx"])
        Rx = A.run(F, dict(baro=how), cache)
        ok("R7 ruled out by the chambers: the pressure's %s-hour change leaves %.0f per cent more unexplained variance "
           "than the fitted lag (and still files package %s, R2 inside its band)" % (how[2:], 100 * (Bx["sse"] /
                                                                                      cache["B_ema"]["sse"] - 1), Rx["R8"]),
           Bx["sse"] > 1.2 * cache["B_ema"]["sse"] and Rx["R8"] == G["R8"]
           and RS.grade("R2_actual_2025_t", figs["R2_actual_2025_t"], round(Rx["R2"])) == "right")
    for name, o in RS.PERTURB:
        R = A.run(F, o, cache)
        ok("R7 the call holds under %s" % name, R["R8"] == G["R8"], (R["R8"], round(R["R7"]["C"]), round(R["R7"]["D"])))
    for name, o in RS.SHORTCUTS:
        R = A.run(F, o, cache)
        ok("R7 the shortcut misses the call: %s (%s)" % (name, R["R8"]), R["R8"] != G["R8"])
    ok("margin package C is 12 per cent or more over the limit (%s t)" % figs["R7_emissions_2027_t"]["package C"],
       figs["R7_emissions_2027_t"]["package C"] >= 1.12 * lim)
    ok("margin package D is 12 per cent or more under the limit (%s t)" % figs["R7_emissions_2027_t"]["package D"],
       figs["R7_emissions_2027_t"]["package D"] <= 0.88 * lim)
    ok("margin every rival, perturbation and sweep combination keeps C 3 per cent over and D 8 per cent under the limit",
       figs["_extra"]["nearest"]["C_min_t"] >= 1.03 * lim and figs["_extra"]["nearest"]["D_max_t"] <= 0.92 * lim,
       figs["_extra"]["nearest"])
    # the holistic audit's test, re-run here: every combination of the choices inside the answer blocks' bands
    swr = [(n, A.run(F, o, cache)) for n, o in RS.sweep_routes()]
    off = [n for n, R in swr if R["R8"] != G["R8"]]
    cmin = min(swr, key=lambda x: x[1]["R7"]["C"])
    dmax = max(swr, key=lambda x: x[1]["R7"]["D"])
    ok("sweep all %d combinations of the pressure response, cell 5's calibration across R4's band, package C's gain "
       "and cell 4's carry file package %s" % (len(swr), G["R8"]), not off and len(swr) == E["forcing"]["sweep"]["runs"],
       off[:3])
    swb = [(n, R) for n, R in swr if RS.in_band(R, Gf)]
    cib = min(swb, key=lambda x: x[1]["R7"]["C"])
    ok("sweep package C stays 3 per cent over the limit at its lowest among the %d combinations that keep R2, R4 and "
       "R5 inside their bands (%.0f t: %s)" % (len(swb), cib[1]["R7"]["C"], cib[0]), cib[1]["R7"]["C"] >= 1.03 * lim)
    ok("sweep package C stays over the limit at its lowest of all %d (%.0f t: %s, R4 %+.1f per cent)"
       % (len(swr), cmin[1]["R7"]["C"], cmin[0], 100 * (cmin[1]["R4"] / G["R4"] - 1)), cmin[1]["R7"]["C"] > lim)
    ok("sweep no pressure specification beyond the swept ones keeps R2 and R4 inside their bands (36 and 40 hours)",
       all(not RS.in_band(A.run(F, dict(baro=b), cache), Gf) for b in ("ema_tau36", "ema_tau40")))
    ok("sweep package D stays 8 per cent under the limit at its highest (%.0f t: %s)" % (dmax[1]["R7"]["D"], dmax[0]),
       dmax[1]["R7"]["D"] <= 0.92 * lim)
    fl = figs["_extra"]["r4_flip"]
    ok("flip cell 5's 2027 generation at which package C would pass sits below R4's band, on the golden route (%s t) "
       "and on a 24-hour lag with package C's gain +7 per cent (%s t), against the band's floor %s t"
       % (fl["golden_t"], fl["run_route_t"], fl["band_low_t"]),
       fl["golden_t"] < 0.85 * fl["band_low_t"] and fl["run_route_t"] < 0.95 * fl["band_low_t"], fl)

    # ------------------------------------------------------------------------ the forks
    plan = pdf_text(os.path.join(target, P.FILES["plan"]))
    ok("SF1 the resolution defines methane emissions as every surface, the flare and the engines",
       has(plan, "from every surface of the landfill and from the flare and the engines"))
    ok("SF1 same call: the flare and engines' unburned methane is under 3 per cent of package D's total",
       G["R7_slip"]["D"] < 0.03 * G["R7"]["D"], round(G["R7_slip"]["D"]))
    ok("SF2/SF3/SF4 the resolution files the least-cost package at or under the limit in a year of normal weather",
       has(plan, "least-cost package") and has(plan, "at or under the limit in Section 2 in a year of normal weather"))
    c2 = dict(cache)
    msoil = cache["msoil"]
    c2["norm"] = {mth: msoil[A.mi(2025, mth)] for mth in range(1, 13)}
    R25 = A.run(F, {}, c2)
    ok("SF2 same call: 2025's soil temperatures in place of the normals keep package %s (C %s, D %s)"
       % (G["R8"], round(R25["R7"]["C"]), round(R25["R7"]["D"])), R25["R8"] == G["R8"] and
       abs(R25["R5"] - G["R5"]) < 2.0)
    ok("SF5 the packages are cumulative in the options paper", has(plan, "each includes the works of the one before"))
    wd = P.WORKS["wells5"]
    ok("SF6 the options paper files each works' in-service date", all(has(plan, x) for x in (
        "May 1, 2027", "%s %d, %d (wells)" % (wd.strftime("%B"), wd.day, wd.year), "October 1, 2027 (cap)")))
    ok("SF7 design capture is filed as the share of cell 5's methane", has(plan, "the share of the methane generated in cell 5"))
    ok("SF8 the report is filed as submitted in March 2026", "Submitted March 27, 2026" in rep)
    ok("SF9 the survey annualizes the 2025 campaigns only", "The 2025 campaigns averaged" in sv)
    ok("SF10 the bridge follows the report's equation (collection efficiency, then oxidation)",
       rep.find("collection efficiency") < rep.find("oxidation fraction") and "in the order of its own equation"
       in open(os.path.join(TASK, "prompt.txt")).read())
    ok("SF11 municipal waste is the MSW material code (old codes MSW-COM, MSW-RES, MSW-TS)",
       set(k for k, v in A.OLD_TO_NEW.items() if v == "MSW") == {"MSW-COM", "MSW-RES", "MSW-TS"})
    ok("SF12 generation is filed apart from collection in the report's own terms", "Methane generated" in rep
       and "Methane collected" in rep)
    ok("SF13/SF17 the prompt files 2022 and the twelve months to October 2026, and a normal-weather year",
       "2022 to the 12 months to October 2026" in open(os.path.join(TASK, "prompt.txt")).read())
    ok("SF14 the prompt files the share of the methane reaching cell 5's cover",
       "the methane reaching cell 5's cover" in open(os.path.join(TASK, "prompt.txt")).read())
    ok("SF15 the plan of record is package A (no new works in 2027)", has(plan, "no new works in 2027"))
    pr = open(os.path.join(TASK, "prompt.txt")).read()
    ok("SF16/SF18 the prompt files metric tons for methane and short tons for the waste",
       "metric tons" in pr and "short tons" in pr and "net_tons" in F["tickets"].columns)
    R17 = A.run(F, dict(), dict(cache, norm={mth: msoil[A.mi(2025, mth)] for mth in range(1, 13)}))
    ok("SF17 same band: R5 under 2025's soil temperatures stays inside its band (%.1f)" % R17["R5"],
       RS.grade("R5_cell5_oxidized_share_2027_pct", figs["R5_cell5_oxidized_share_2027_pct"], round(R17["R5"], 1))
       == "right")

    ok("SF20 the options paper files the pumps' level as the pilot pumps' own", has(plan, "hold the liquid where the "
       "June 2025 pilot pumps hold it"))
    ok("SF23 the options paper files the gas model's delay (a month's waste producing methane six months after it is "
       "placed), the golden's", has(plan, "begins producing methane six months after it is placed")
       and A.fod.__defaults__[0] == P.RULE["lag_months"] == 6)
    d0 = A.fod.__defaults__
    lagc = {}
    for lag in (0, 3, 9):
        A.fod.__defaults__ = (lag,) + tuple(d0[1:])
        lagc[lag] = A.run(F, {}, {})
    A.fod.__defaults__ = d0
    ok("SF23 same call under the delays the filed sentence rules out: none, three and nine months still file package %s "
       "(C %s t), with cell 5's generation %s per cent off" % (G["R8"], ", ".join("%.0f" % lagc[k]["R7"]["C"] for k in (0, 3, 9)),
                                                               ", ".join("%+.0f" % (100 * (lagc[k]["R4"] / G["R4"] - 1)) for k in (0, 3, 9))),
       all(r["R8"] == G["R8"] for r in lagc.values()))
    Rf = A.run(F, dict(pumps="full"), cache)
    ok("SF20 the pilot wells leave %.2f of the screen under liquid since their pumps (read off the pack, not cleared); "
       "a cleared screen instead still files package %s (C %.0f t)" % (G["z"]["s_after"], Rf["R8"], Rf["R7"]["C"]),
       0.01 < G["z"]["s_after"] < 0.1 and Rf["R8"] == G["R8"])
    Ro = A.run(F, dict(pumps="october"), cache)
    ok("SF21 the pumps' scope is every well flooded at its last 2026 gauging (%d wells); only the wells gauged in "
       "October 2026 (%d) still files package %s" % (G["pump_wells"], Ro["pump_wells"], Ro["R8"]),
       has(plan, "when the well was last gauged in 2026") and G["pump_wells"] >= Ro["pump_wells"]
       and Ro["R8"] == G["R8"])
    hk = t[t["hauler"] == P.CONTRACT["hauler"]]
    ok("SF22 the transfer contract's trailers are on the tickets from %s only, and the daily log notes their first day"
       % P.CONTRACT["start"], len(hk) > 1000 and hk["ticket_date"].min() >= P.CONTRACT["start"]
       and F["dailylog"]["supervisor_notes"].fillna("").str.contains(P.CONTRACT["hauler"]).sum() == 1, len(hk))
    fp = F["fillplan"]
    t25 = t[(t["status"].fillna("") != "VOID") & (t["ticket_date"] >= dt.date(2025, 3, 1))
            & (t["ticket_date"] < dt.date(2026, 3, 1)) & (t["material_code"] == "MSW")]
    ok("SF22 the fill plan carries the contract's receipts into 2027 (its 2027 monthly municipal waste above the "
       "twelve months before the contract)", fp[fp["month"].astype(str).str.startswith("2027")]["msw_tons"].mean()
       > 1.3 * t25["net_tons"].sum() / 12)
    F7 = dict(F)
    fp7 = F["fillplan"].copy()
    fp7["msw_tons"] = fp7["msw_tons"] / P.CONTRACT["factor"]
    F7["fillplan"] = fp7
    R7x = A.run(F7, {}, {})
    ok("SF22 same call: the fill plan's receipts carried at the rate before the contract still file package %s (C %.0f t)"
       % (R7x["R8"], R7x["R7"]["C"]), R7x["R8"] == G["R8"] and has(plan, "Waste receipts for cell 5 through 2027 are in "
                                                                   "the Division's 2027 fill plan"))
    docs_txt = " ".join(flat(pdf_text(os.path.join(target, P.FILES[k]))) for k in ("plan", "ghg2025", "survey", "oxstudy"))
    ok("SF22 no document names the contract (the records carry it)", P.CONTRACT["hauler"] not in docs_txt)

    # ------------------------------------------------------------------------ the input gates and the house rules
    cats = {os.path.splitext(f)[1] for f in files}
    ok("gate ten or more usable files", len(files) >= 10, len(files))
    ok("gate two or more file categories", len(cats & {".csv", ".xlsx", ".pdf"}) >= 2, cats)
    rows = {f: sum(1 for _ in open(os.path.join(target, f), errors="replace")) for f in files if f.endswith(".csv")}
    ok("gate a CSV of 20,000 rows or more", any(v > 20000 for v in rows.values()), rows)
    ok("gate a second large CSV of 10 to 20 printed pages or more", sum(v > 500 for v in rows.values()) >= 2, rows)
    import metadata as MD
    ok("gate two or more distractors, none read by the analysis", len(MD.DISTRACTORS) >= 2 and all(
        d not in open(os.path.join(HERE, "analysis.py")).read() for d in MD.DISTRACTORS))
    ok("gate metadata.json outside the pack", os.path.exists(os.path.join(TASK, "metadata.json"))
       and "metadata.json" not in files)
    ok("H9 no readme, dictionary, notes or manifest file under target/",
       not [f for f in files if re.search(r"readme|dictionar|notes|manifest|codebook", f, re.I)])
    dash = [p for p in (os.path.join(TASK, "submission.md"), os.path.join(TASK, "prompt.txt"))
            if "\u2014" in open(p).read()]
    ok("house no em dashes in the prompt or the answer blocks", not dash, dash)
    print("\n%d checks, %d passed, %d failed" % (N["pass"] + N["fail"], N["pass"], N["fail"]))
    return 1 if N["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
