"""task22 checks: the bar (R1 to R7), the forks, the input gates and the realism sweep, asserted on the built task
folder (target/, generator/figures.json and effort.json) and on the clean truth.

    python3 task22/generator/checks.py
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

import analysis as A  # noqa: E402
import deliver as DL  # noqa: E402
import golden as GD  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import results as RS  # noqa: E402
import world as WD  # noqa: E402

N = [0, 0]


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        N[1] += 1
    print("%s  %-78s %s" % ("PASS" if cond else "FAIL", label[:78], str(detail)[:150]))


def main():
    target = os.path.join(TASK, "target")
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    F = GD.load(target)
    W = WD.build()
    import records as RC
    RC.customer_metered(W)
    TG = {r["figure"]: r["golden"] for r in E["results"]}
    BAND = {r["figure"]: r.get("bands") or r.get("band") for r in E["results"]}

    # ---------------------------------------------------------------- the truth closes
    g = W.g
    m26 = (g.dord >= P.WIN26[0].toordinal()) & (g.dord < P.WIN26[1].toordinal())
    for s in P.SUBSTATIONS:
        lhs = W.dp[s][m26].sum()
        rhs = sum(W.head_P[f][m26].sum() for f in P.SUB_FEEDERS[s]) + W.sub_loss[s][m26].sum() + W.dp[s + "_ss"][m26].sum()
        ok("truth: %s delivery point = feeders + transformer losses + station service" % s, abs(lhs - rhs) < 1e-3 * lhs)
    tot_tech = sum(W.tech[f][m26].sum() for f in P.FEEDER_ORDER) / sum(W.head_P[f][m26].sum() for f in P.FEEDER_ORDER)
    ok("truth: system technical losses between 4 and 6.5 per cent", 0.04 < tot_tech < 0.065, "%.2f%%" % (100 * tot_tech))
    for f in P.FEEDER_ORDER:
        pct = W.tech[f][m26].sum() / W.head_P[f][m26].sum()
        ok("truth: %s technical losses between 3 and 10 per cent" % f, 0.03 < pct < 0.10, "%.2f%%" % (100 * pct))

    # ---------------------------------------------------------------- R1: the field's raw material ships, no result
    heads = []
    for name in os.listdir(target):
        p = os.path.join(target, name)
        if name.endswith(".csv"):
            heads += list(pd.read_csv(p, nrows=2).columns)
        elif name.endswith(".xlsx"):
            for sh, df in pd.read_excel(p, sheet_name=None, nrows=2).items():
                heads += [str(c) for c in df.columns]
    bad = [h for h in heads if re.search(r"non.?technical|technical.?loss|theft|residual|ntl", str(h), re.I)]
    ok("R1 no shipped column holds a result (non-technical or technical loss, theft)", not bad, bad[:5])
    ok("R1 the breakers' hourly record ships (feeder x hour)", len(F["scada"]) > 300000, len(F["scada"]))
    ok("R1 the delivery points' hourly record ships", len(F["dp"]) > 100000, len(F["dp"]))
    ok("R1 every service point's reads ship", F["reads"]["ServicePointID"].nunique() > 8500,
       F["reads"]["ServicePointID"].nunique())
    ok("R1 the network ships at segment grain", len(F["gis_segments"]) > 1000, len(F["gis_segments"]))

    # ---------------------------------------------------------------- R3: each result's hurried figure
    for r in E["results"]:
        g_ = r["golden"]
        c_ = r["passes"]["careful"]
        if r["id"] == "R3":
            ok("R3 the careful pass earns R3 (lights at real use)", right(c_, g_, r), "")
            continue
        ok("R3 %s: the careful but hurried figure falls outside the band" % r["id"], not right(c_, g_, r),
           str(c_)[:100])
        ok("R3 %s: the golden is inside its own band" % r["id"], right(g_, g_, r))
        if r["passes"]["careful"] is not None and r["id"] != "R3":
            ok("R3 %s cites a precedent" % r["id"], bool(r.get("precedent")), r.get("precedent"))

    # ---------------------------------------------------------------- R5 and R6: no one thing; the hints computed
    hints = E["hints"]
    ok("R6 four hints, each executed on the careful pass", len(hints) == 4)
    for h in hints:
        ok("R5/R6 one sentence rescues at most a third: %s" % h["sentence"][:40], len(h["rescues"]) <= 3, h["rescues"])
    routes = E["routes"]
    gold = sorted(figs["R9_sweep"])
    alone = [r for r in routes if r["name"].startswith("only ")]
    ok("R5 no single correction on the careful pass files the golden four", all(sorted(r["answer"]) != gold
                                                                                 for r in alone), len(alone))
    pairs = [r for r in routes if r["name"].startswith(("the log and", "the gaps and"))]
    ok("R5 no pair of corrections files the golden four", all(sorted(r["answer"]) != gold for r in pairs), len(pairs))
    wrong = {tuple(sorted(r["answer"])) for r in routes if not r.get("golden")}
    ok("R5 the shortcuts land on four or more different wrong fours", len(wrong) >= 4, len(wrong))
    # footprints: far-end load on several feeders; switching in every substation; gaps on every feeder
    far = {lp["feeder"] for lp in W.lp if lp["key"] not in P.LP_BEFORE_2019}
    ok("R5 load added since 2019 sits on five or more feeders", len(far) >= 5, sorted(far))
    sw_subs = {W.net.sw[o["sw"]]["feeder"][:3] for o in W.ops}
    ok("R5 switching in every substation", sw_subs == set(P.SUBSTATIONS), sorted(sw_subs))
    gaps = F["scada"][F["scada"]["Quality"] != "GOOD"].groupby("Point").size()
    ok("R5 breaker gaps on every feeder", len(gaps) == 14 and gaps.min() > 20, int(gaps.min()) if len(gaps) else 0)
    led = {L["feeder"] for L in W.lights if L["led"] and not L["billed_led"]}
    ok("R5 unbilled LED conversions on ten or more feeders", len(led) >= 10, len(led))
    theft_f = {t["feeder"] for t in W.theft}
    ok("R5 illegal grows on every feeder", theft_f == set(P.FEEDER_ORDER), len(theft_f))

    # ---------------------------------------------------------------- R7: the rivals
    fo = E["forcing"]
    ok("R7 every golden-family variant files the golden four", all(sorted(x["answer"]) == gold
                                                                   for x in fo["golden_family"]),
       [x["name"][:30] for x in fo["golden_family"]])
    ok("R7 every perturbation leaves the four standing", all(sorted(x["answer"]) == gold for x in fo["perturbations"]),
       len(fo["perturbations"]))
    ok("R7 every shortcut files another four", all(sorted(x["answer"]) != gold for x in fo["shortcuts"]),
       len(fo["shortcuts"]))
    # load by transformer rating ruled out by the meters: loading spread across transformers
    st = A.state(F)
    t = A.tech_for(F, st, "golden")
    nm = t["node_month"]
    kva = F["gis_xf"].groupby("Node")["kVA"].sum()
    win_months = [y * 100 + m for (y, m) in [(2025, 10), (2025, 11), (2025, 12)] + [(2026, k) for k in range(1, 10)]]
    load = {n: sum(v.get(m, 0.0) for m in win_months) / 8760.0 for n, v in nm.items()}
    ratios = sorted(load[n] / kva[n] for n in load if n in kva.index and kva[n] > 0 and load[n] > 0)
    q10, q90 = np.percentile(ratios, 10), np.percentile(ratios, 90)
    ok("R7 kVA allocation ruled out: node loading (average kW per kVA) spans fourfold or more", q90 / q10 > 4,
       "%.3f to %.3f" % (q10, q90))
    # the LED factor carries R3 alone: the lights at their deemed kWh leave the four standing
    tw = pd.read_excel(os.path.join(TASK, "golden", DL.WORKBOOK), sheet_name="Twelve months", header=2)
    tw = tw[tw["Feeder"].isin(P.FEEDER_ORDER)].set_index("Feeder")
    deem = {f: 0.0 for f in P.FEEDER_ORDER}
    d = P.WIN26[0]
    while d < P.WIN26[1]:
        for L in W.lights:
            if L["install"] <= d:
                deem[L["feeder"]] += P.DEEMED_KWH[RC.lamp_billed(L, d)] / 1000.0
        d = (d.replace(day=28) + dt.timedelta(days=5)).replace(day=1)
    alt = {f: tw.loc[f, "Non-technical loss"] + tw.loc[f, "City lights"] - deem[f] for f in P.FEEDER_ORDER}
    four = sorted(sorted(alt, key=lambda f: -alt[f])[:4])
    ok("R3 the lights at their deemed kWh leave the four standing", four == gold,
       "%s; gap to the fifth %.1f" % (four, sorted(alt.values())[-4] - sorted(alt.values())[-5]))

    # ---------------------------------------------------------------- R2: mess neutrality
    base = sorted(figs["R9_sweep"])
    F2 = dict(F)
    F2["_bid"] = "dupkept"
    r = F["reads"].copy()
    F2["reads"] = pd.concat([r, r[(r["ReadDate"] >= "2025-06-30") & (r["ReadDate"] <= "2025-07-01")]])
    # calendarize dedupes by design; the mishandling is not deduping, run it by hand
    n2 = ntl_without_dedupe(F2)
    ok("R2 the CIS overlap kept twice moves no feeder in or out of the four", sorted(A.top4(n2)) == base,
       A.top4(n2))
    ok("R2 the stuck APT-2 transducer kept moves no feeder in or out of the four", stuck_kept(F) == base)

    # ---------------------------------------------------------------- forks
    scope = GD.pdf_text(os.path.join(target, PK.FILES["scope"]))
    budget = GD.pdf_text(os.path.join(target, PK.FILES["budget"]))
    study = GD.pdf_text(os.path.join(target, PK.FILES["study"]))
    flat = lambda t: re.sub(r"\s+", " ", t)
    ok("SF1/SF4/SF5/SF6 the scope files the non-technical loss", "neither recorded by a customer's meter" in flat(scope))
    ok("SF2/SF19 the scope files the four and the twelve months", "four feeders that carried the largest" in flat(scope)
       and "September 30, 2026" in flat(scope))
    ok("SF7/SF8/SF9 the study files its conventions", "50 C" in flat(study) and "six times" in flat(study) and
       "0.7 percent" in flat(study))
    ok("SF16/SF17/SF18 the budget instructions file the base year and what 2027 adds",
       "stands for the same month of 2027" in flat(budget) and "scheduled service dates" in flat(budget))
    pur = A.purchases(F, A.WIN26)
    bc, _ = A.billed_in(F, A.WIN26)
    met = sum(st_x["dlv"] - st_x["rcv"] + st_x["lp"] for st_x in RS.compute(F)["_balance"].values())
    ok("SF3 metered use by the days a read covers and by bill month differ by under half a per cent of purchases",
       abs(met - bc) < 0.005 * pur, "%.2f%%" % (100 * (met - bc) / pur))
    fam = {x["name"]: sorted(x["answer"]) for x in fo["golden_family"]}
    ok("SF10 the tree that served each node (today's tree is a shortcut)", any(
        "today's GIS" in x["name"] and sorted(x["answer"]) != gold for x in fo["shortcuts"]))
    ok("SF11 customers served counts connected service points", figs["R2_membership"][
        "NTH-4 customers, 31 May 2026"] > figs["R2_membership"]["NTH-4 customers, 31 March 2026"])
    br = figs
    parts = sum(br["bridge_parts_2026"].values())
    ok("SF12/SF13 the bridge's parts add to the line loss in each window", abs(parts - br["loss_pct_26"]) < 0.02,
       "%.3f vs %.3f" % (parts, br["loss_pct_26"]))
    parts24 = sum(br["bridge_parts_2024"].values())
    ok("SF13 and in 2024", abs(parts24 - br["loss_pct_24"]) < 0.02)
    rep = pd.read_excel(os.path.join(target, PK.FILES["lineloss"]), header=2)
    rv = dict(zip(rep["Period"].astype(str), rep["Line loss %"]))
    ok("SF12 the utility's report shows the same line loss for the two windows",
       abs(rv["12 months to September 2024"] - br["loss_pct_24"]) < 0.01 and
       abs(rv["12 months to September 2026"] - br["loss_pct_26"]) < 0.01, (rv["12 months to September 2024"],
                                                                          rv["12 months to September 2026"]))
    ok("SF14 the measured share of applied load is under 0.8 for the grows", figs["df_grow"] < 0.8, figs["df_grow"])
    df_mean = A.demand_factors(F, "mean")["grow"]
    ok("SF14 the mean of the grows' ratios agrees with their aggregate within 0.01", abs(df_mean - figs["df_grow"]) < 0.01,
       df_mean)
    ok("SF20 the North afternoon lies outside both windows and is under 0.25 per cent of a year", north_outage_small(F), "")
    ok("SF15 the cold store's own share", 0.55 < figs["df_cold"] < 0.8, figs["df_cold"])

    # ---------------------------------------------------------------- the margin
    v = sorted(figs["ntl_all"].values(), reverse=True)
    ok("margin: the fourth and fifth feeders are 150 MWh or more apart", v[3] - v[4] >= 150, v[3] - v[4])
    ok("the sweep is the four largest non-technical losses", sorted(figs["R9_sweep"]) == sorted(
        sorted(figs["ntl_all"], key=lambda f: -figs["ntl_all"][f])[:4]))
    ok("R4 bands separate the study's figure for APT-3", not (BAND["R4_technical"]["APT-3"][0] <=
                                                             figs["careful_tech_apt3_26"] <= BAND["R4_technical"]["APT-3"][1]))

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    ok("gate: ten or more usable files", len(files) >= 10, len(files))
    cats = {os.path.splitext(f)[1] for f in files}
    ok("gate: two or more file categories", len(cats & {".csv", ".xlsx", ".pdf"}) >= 2, sorted(cats))
    big = {f: sum(1 for _ in open(os.path.join(target, f))) for f in files if f.endswith(".csv")}
    ok("gate: a CSV of 20,000 rows or more", max(big.values()) >= 20000, max(big.values()))
    ok("gate: a second large CSV (ten or more printed pages)", sorted(big.values())[-2] >= 600, sorted(big.values())[-2])
    md = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("gate: two or more distractors named in metadata.json", len(md["distractor_files"]) >= 2, md["distractor_files"])
    loader = open(os.path.join(HERE, "golden.py")).read()
    ok("gate: the golden never reads a distractor", all('p["%s"]' % k not in loader for k in PK.DISTRACTORS))
    ok("gate: no file name says distractor, answer or trap", not any(re.search(r"distract|answer|trap|key", f, re.I)
                                                                     for f in files))
    ok("gate: no readme, dictionary or manifest ships", not any(re.search(r"readme|dictionary|manifest|notes", f, re.I)
                                                                for f in files))

    # ---------------------------------------------------------------- realism sweep
    sp = F["gis_sp"]["ServicePointID"].astype(int).sort_values().values
    ok("realism: service point ids are not an arithmetic sequence", len(set(np.diff(sp))) > 50)
    segs = F["gis_segments"]["SegmentID"].str[3:].astype(int).sort_values().values
    ok("realism: segment ids are not an arithmetic sequence", len(set(np.diff(segs))) > 50)
    names = F["applications"]["Applicant"].tolist()
    ok("realism: applicant names take more than two shapes", len({n.split()[-1] for n in names}) > 2)
    ok("realism: applicants not in alphabetical order", names != sorted(names))
    for k in ("study", "cwp", "rates", "budget", "scope", "wholesale"):
        meta = subprocess.run(["pdfinfo", os.path.join(target, PK.FILES[k])], capture_output=True, text=True).stdout
        ok("realism: %s PDF made by Writer, authored by its issuer" % k, "Writer" in meta and "LibreOffice" in meta and
           "Author:" in meta, re.findall(r"Author:\s*(.*)", meta)[:1])
    em = [f for f in files if f.endswith((".csv",)) and "—" in open(os.path.join(target, f)).read()]
    ok("realism: no em dash in any shipped text", not em, em)
    # the prompt's figures are the data's
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    a24, a26 = "%.1f" % br["loss_pct_24"], "%.1f" % br["loss_pct_26"]
    ok("prompt: the utility's two line losses (%s and %s per cent) are the prompt's" % (a24, a26),
       ("from %s to %s per cent" % (a24, a26)) in prompt)
    print("\n%d checks, %d FAIL" % (N[0], N[1]))
    return 1 if N[1] else 0


def right(v, g, r):
    if isinstance(g, dict):
        b = r.get("bands") or {}
        if not isinstance(v, dict):
            return False
        for k, gv in g.items():
            pv = v.get(k)
            if pv is None:
                return False
            if k in b:
                if not (b[k][0] <= pv <= b[k][1]):
                    return False
            elif pv != gv:
                return False
        return True
    if isinstance(g, list):
        return isinstance(v, list) and sorted(v) == sorted(g)
    band = r.get("band")
    if band:
        return band[0] <= v <= band[1]
    return v == g


def ntl_without_dedupe(F2):
    """The golden route with the CIS overlap counted twice (calendarize keeps its own dedupe, so the duplicate rows are
    made distinct by a trailing space on their meter number)."""
    r = F2["reads"].copy()
    dup = r.duplicated(keep="first")
    r.loc[dup, "MeterNo"] = r.loc[dup, "MeterNo"] + " "
    F2["reads"] = r
    n, _ = A.ntl_route(F2)
    return n


def stuck_kept(F):
    sc = F["scada"].copy()
    # a run that keeps the stuck values: break the exact repeats by a tenth of a watt so the rule does not see them
    sel = (sc["Point"] == "APT_F2") & sc["MW"].notna()
    rep = sel & (sc["MW"] == sc["MW"].shift(1))
    sc.loc[rep, "MW"] = sc.loc[rep, "MW"] + 1e-7 * np.arange(rep.sum())
    F3 = dict(F)
    F3["scada"] = sc
    F3["_bid"] = "stuck"
    n, _ = A.ntl_route(F3)
    return sorted(A.top4(n))


def north_outage_small(F):
    st = A.state(F)
    P_ = st["P"]
    day = dt.date(2025, 6, 11)
    a = A.hidx_utc(dt.datetime(2025, 6, 11, 13, tzinfo=A.TZ).astimezone(A.UTC))
    tot = sum(P_[f][a:a + 14].sum() for f in A.SUB_FEEDERS["NTH"])
    outside = not any(w[0] <= day < w[1] for w in (A.WIN24, A.WIN26))
    return outside and tot > 0 and all(P_[f][a:a + 14].sum() < 0.0025 * A.window_sum(P_[f], A.WIN26)
                                       for f in A.SUB_FEEDERS["NTH"])


if __name__ == "__main__":
    sys.exit(main())
