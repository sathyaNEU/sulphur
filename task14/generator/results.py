"""task14: the golden, the rivals that set each band, the passes and the routes, figures.json and effort.json, all
from the cut pack."""
import json
import math

import numpy as np
import pandas as pd

import analysis as AN
import effort_passes as EP
import measure as MS
import project as PJ

REG = ["NAT"] + MS.REGIONS
NAMES = {"NAT": "Penmarra", "HC": "Hallam Central", "HN": "Hallam North", "HE": "Hallam East", "HS": "Hallam South",
         "KC": "Kerrow Coast", "MV": "Midvale", "WS": "Westerly"}
BANDS = {"R1": 0.003, "R2": 0.02, "R3_change": 0.15, "R3_share": 2.0, "R4": 0.5, "R5_nat": 0.15, "R5_reg": 0.25,
         "R5_series": 0.30, "R6_end": 0.10, "R7_nat": 0.10, "R7_reg": 0.20, "R8": 0.10, "R8_fall": 0.12}
R6_HALF = (0.05, 0.20)
Q24 = MS.quarter_end(2024, 3)
CAREFUL = {
    "the panel's rises carried to every landlord": dict(ops_from="model"),
    "the latest recorded rent carried forward at the panel's rate": dict(small_from="carry", ops_from="carry"),
    "the recorded rent where an additional bond exists, the model otherwise": dict(small_from="hybrid"),
}


def r1d(x):
    return float(round(x + 1e-12, 1))


def compute(target, boot=AN.B_BOOT):
    G = AN.Golden(target, "golden")
    gold = EP.run_config(G)
    # the December range: the panel's sampling error and the projection's own error on earlier Decembers
    sep_b, dec_b, decr_b = G.boot(B=boot)
    bt = G.backtest()
    err = np.array([b["projected"] - b["actual"] for b in bt])
    rmse = float(np.sqrt((err ** 2).mean()))
    sd = float(dec_b.std(ddof=1))
    half = 1.645 * math.hypot(sd, rmse)
    dn = gold["R7"]["NAT"]
    gold["R6"] = {"lo": dn - half, "hi": dn + half, "half": half}
    # rivals: each defensible alternative, run on the clean pack
    riv = {}
    Gn = AN.Golden(target, "norm")
    riv["premises matched without the slip and reversal allowances"] = EP.run_config(Gn)
    for lab, (byr, wt) in (("panel rates unweighted", (True, False)), ("panel rates pooled across regions", (False, True))):
        m, p = MS.review_model(G.pairs, by_region=byr, weighted=wt)
        riv[lab] = rival_run(G, MS.cumlog(m), p)
    c26g = EP.contributions(G.E, AN.SEP26, AN.SEP25, G.CL)
    for lab, kw in (("December rates read with hindsight", dict(how="hindsight")),
                    ("December going rents held at November", dict(hold="hold")),
                    ("December rates without landlord class", dict(by_class=False)),
                    ("December rates from 2024 and 2025 only", dict(rate_years=(2024, 2025)))):
        d = PJ.project(G.E, G.CL, ix=G.ix, cpi=G.cpi, **kw)
        riv[lab] = {"R7": _reg(d), "R8": _split(d["_parts"], c26g)}
    rng_var = {"the panel's error alone": 1.645 * sd, "the projection's error alone": 1.645 * rmse,
               "the two errors added": 1.645 * (sd + rmse),
               "a t multiplier for three back-test years": math.hypot(1.645 * sd, 2.920 * rmse),
               "the back-test bias removed": 1.645 * math.hypot(sd, float(np.std(err, ddof=1)))}
    # the careful but hurried pass: three variants of the rent step, the best-scoring one taken
    variants = {lab: careful_run(G, Gn, kw) for lab, kw in CAREFUL.items()}
    Gp = AN.Golden(target, "pid")
    quick = EP.quick(Gp)
    # shortcut routes, each with its own September and December figures
    Ec = G.E
    asst = Ec.measure(AN.DEC26, AN.DEC25, G.CL)["NAT"]["measure"]
    st_err = [Ec.as_of(MS.day(y, 11, 27)).measure(MS.day(y, 12, 31), MS.day(y - 1, 12, 31), G.CL)["NAT"]["measure"]
              - b["actual"] for y, b in zip((2023, 2024, 2025), bt)]
    routes = {"the golden": gold}
    routes.update({"careful but hurried: " + k: v for k, v in variants.items()})
    routes["the additional bonds read as every rise"] = EP.run_config(G, small_from="recorded", december="trend")
    routes["re-lettings tied by property identifier alone"] = EP.run_config(Gp, december="trend")
    routes["re-lettings against the earlier tenancy's starting rent"] = EP.run_config(G, earlier="start",
                                                                                     december="trend")
    routes["the quarterly figures carried on a straight trend"] = EP.run_config(G, december="trend")
    routes["the September figure carried into December"] = EP.run_config(G, december="carry")
    routes["the register read as it stands on 31 December"] = EP.run_config(G, december="asstands")
    adj = dict(EP.run_config(G, december="asstands"))
    adj["R7"] = {g: v - float(np.mean(st_err)) if g == "NAT" else v for g, v in adj["R7"].items()}
    routes["the register as it stands, corrected by its own back-test"] = adj
    nos = dict(gold)
    nos["R7"] = _reg(PJ.project(G.E, G.CL, ix=G.ix, cpi=G.cpi, scheduled=False))
    routes["December projected without the review not yet on file"] = nos
    routes["new-letting rents for the measure"] = quick
    sched = PJ.review_schedule(G.E, cpi=G.cpi)
    link = panel_bond_split(G)
    valid = validate_estimators(G)
    dbt = december_backtests(G)
    churn = december_churn(G)
    analog = analog_backtest(G)
    Ge = AN.Golden(target, "exact")
    exact_relet_n = Ge.E.measure(AN.SEP26, AN.SEP25, Ge.CL)["NAT"]["n_relet"]
    land = G.E.T["landlord_id"].values
    bl = [lid for lid, v in sched.items() if (v[0], v[1]) == (11, 1)][0]
    reviewed_onfile = int(((G.E.tops["effective"] == MS.day(2026, 11, 1)) & (land[G.E.tops["i"].values] == bl)).sum())
    out = {"exact_relet_n": exact_relet_n, "reviewed_onfile_n": reviewed_onfile, "panel_link": link,
           "validation": valid, "dec_backtests": dbt, "dec_parts": gold["_dec_parts"], "c26": gold["_c26"],
           "churn": churn, "analog": analog,"G": G, "gold": gold, "variants": variants, "quick": quick, "rivals": riv, "range_variants": rng_var,
           "routes": routes, "backtest": bt, "st_err": st_err, "as_stands": asst, "sched": sched,
           "pending": len(PJ.pending_reviews(G.E, AN.CUT, sched)),
           "scheduled": len(PJ.scheduled_reviews(G.E, AN.CUT, AN.DEC26, sched, G.cpi)),
           "boot": {"sd_dec": sd, "sd_sep": float(sep_b.std(ddof=1)), "rmse": rmse,
                    "decr_sd": decr_b.std(axis=0, ddof=1).tolist()},
           "contrib26": EP.contributions(G.E, AN.SEP26, AN.SEP25, G.CL),
           "reviews": operator_reviews(G), "published": AN.published_sep26(G.D["files"]), "pairs": len(G.pairs)}
    out["careful_name"], out["careful"], out["variant_scores"] = pick_careful(out)
    out["hints"] = hint_rescues(G, Gn, out)
    return out


def panel_bond_split(G, years=(2022, 2023, 2024, 2025)):
    """The rent panel's dwellings tied to the register by their parsed address: each anniversary's rise with and
    without an additional bond lodged at that dwelling in the anniversary's year (design-weighted mean factors)."""
    import conform as CF
    T, E = G.E.T, G.E
    key = {}
    for dwk, adr, pc in zip(T["dwelling"], T["premises"], T["postcode"]):
        pa = CF.parse_address(adr)
        if pa:
            key.setdefault((str(pc), pa[0], pa[1], pa[2]), dwk)
    PN = G.D["PN"].drop_duplicates("dwelling_ref").set_index("dwelling_ref")
    dmap = {}
    for r, row in PN.iterrows():
        pa = CF.parse_address(row["address"])
        dmap[r] = key.get((str(row["postcode"]), pa[0], pa[1], pa[2])) if pa else None
    tp = E.tops
    yrs = pd.to_datetime(tp["when"], unit="D").dt.year.values
    has = set(zip(E.dw_key[tp["i"].values], yrs))
    pr = G.pairs.copy()
    pr["dw"] = pr["dwelling_ref"].map(dmap)
    pr = pr[pr["dw"].notna()]
    pr["topped"] = [(d, int(y)) in has for d, y in zip(pr["dw"], pr["year"])]
    out = {"linked": int(sum(v is not None for v in dmap.values())), "dwellings": int(len(dmap)), "years": {}}
    for y in years:
        s = pr[pr["year"] == y]
        a, b = s[s["topped"]], s[~s["topped"]]
        out["years"][y] = {"with": 100 * (np.average(a["factor"], weights=a["w"]) - 1),
                           "without": 100 * (np.average(b["factor"], weights=b["w"]) - 1),
                           "all": 100 * (np.average(s["factor"], weights=s["w"]) - 1),
                           "n_with": int(len(a)), "n_without": int(len(b))}
    return out


def careful_run(G, Gn, kw, share="panel_all", december="asstands", nboot=None):
    """The careful pass under one rent route: its range from the panel resampled (the bootstrap's own draws)."""
    v = EP.run_config(Gn, share=share, december=december, **kw)
    draws = G.boot_CL if nboot is None else G.boot_CL[:nboot]
    if december == "asstands":
        dd = [Gn.E.measure(AN.DEC26, AN.DEC25, CL, **kw)["NAT"]["measure"] for CL in draws]
    else:
        dd = [PJ.project(Gn.E, CL, ix=Gn.ix, cpi=Gn.cpi, **kw)["NAT"] for CL in draws]
    h = 1.645 * float(np.std(dd, ddof=1))
    v["R6"] = {"lo": v["R7"]["NAT"] - h, "hi": v["R7"]["NAT"] + h, "half": h}
    return v


HINTS = [
    ("small landlords lodge additional bond for only some of their rent rises", dict(small_from="model")),
    ("the bonds migrated in March 2023 carry no property identifier; find their dwellings by address", {}),
    ("the rent panel holds none of the operators' dwellings, and their additional bonds record every review",
     dict(ops_from="recorded", share="model")),
    ("project December from what the register showed at the same point of earlier years, operators' scheduled "
     "reviews included", dict(december="project")),
    ("a re-let dwelling's earlier rent is what the earlier tenancy was paying, not what it started at", {}),
]


def hint_rescues(G, Gn, res):
    """Each sentence of help applied to the careful pass: the results it turns from not right to right."""
    B = bands_of(res["gold"])
    base_kw = dict(CAREFUL[res["careful_name"]])
    cv = pass_values(res["careful"])
    out = []
    for sentence, change in HINTS:
        kw = dict(base_kw)
        share, december = "panel_all", "asstands"
        for k, v in change.items():
            if k == "share":
                share = v
            elif k == "december":
                december = v
            else:
                kw[k] = v
        if kw == base_kw and share == "panel_all" and december == "asstands":
            out.append({"sentence": sentence, "rescues": []})
            continue
        h = careful_run(G, Gn, kw, share=share, december=december, nboot=100)
        hv = pass_values(h)
        rescued = [rid for rid in GRADED if grade(cv[rid], B[rid]) < 1.0 and grade(hv[rid], B[rid]) == 1.0]
        out.append({"sentence": sentence, "rescues": rescued})
    return out


def _reg(d):
    return {g: d[g] for g in REG}


def _split(dec_parts, c26):
    out = {"continuing": dec_parts["continuing"] - c26["same"], "relet": dec_parts["relet"] - c26["relet"]}
    out["fall"] = out["continuing"] + out["relet"]
    return out


def validate_estimators(G):
    """On the dwellings both sources hold (the rent panel's small-landlord tenancies tied to the register by parsed
    address, the same tenancy start), each way of reading the rent payable from the register against the rent the
    panel reports on its reference day: the ratio of totals less one, per cent."""
    import conform as CF
    E, T = G.E, G.E.T
    key = {}
    for dwk, adr, pc in zip(T["dwelling"], T["premises"], T["postcode"]):
        pa = CF.parse_address(adr)
        if pa:
            key.setdefault((str(pc), pa[0], pa[1], pa[2]), dwk)
    PN = G.D["PN"]
    R = PN[PN["response"] == "R"].copy()
    R["rd"] = (pd.to_datetime(R["reference_date"]) - pd.Timestamp("1970-01-01")).dt.days
    R["sd"] = (pd.to_datetime(R["tenancy_start"]) - pd.Timestamp("1970-01-01")).dt.days
    pa_ = R["address"].map(CF.parse_address)
    R["dw"] = [key.get((str(pc), p[0], p[1], p[2])) if p else None for pc, p in zip(R["postcode"], pa_)]
    R = R[R["dw"].notna()]
    dwpos = {k: j for j, k in enumerate(E.dw_uniques)}
    out = {}
    for q in ("2024-08-15", "2025-08-15", "2026-08-15"):
        rd = (pd.Timestamp(q) - pd.Timestamp("1970-01-01")).days
        s = R[R["rd"] == rd]
        inp = E.in_place(rd)
        idx, rep = [], []
        for dwk, rent, sd in zip(s["dw"], s["weekly_rent"].astype(float), s["sd"]):
            j = dwpos.get(dwk)
            if j is None or j not in inp.index:
                continue
            i = inp.loc[j]
            if abs(E.start[i] - sd) > 45 or E.op[i]:
                continue
            idx.append(i)
            rep.append(rent)
        idx, rep = np.array(idx), np.array(rep)
        row = {"n": int(len(idx))}
        for lab, kw in (("model", {}), ("recorded", {"small_from": "recorded"}), ("carry", {"small_from": "carry"}),
                        ("hybrid", {"small_from": "hybrid"})):
            row[lab] = 100 * (E.rent_on(idx, rd, G.CL, **kw).sum() / rep.sum() - 1)
        out[q[:4]] = row
    return out


def december_churn(G):
    """December's endings and re-lettings as the projection carries them: the tenancies expected to end between the cut
    day and 31 December, those re-let, the dwellings empty on the cut day and those let again, and the going rents'
    margin over the rents they replace; for December 2026 and, as the register stood, December 2024 and 2025."""
    E = G.E
    out = {}
    for y in (2024, 2025, 2026):
        cut, t1, t2 = MS.day(y, 11, 27), MS.day(y - 1, 12, 31), MS.day(y, 12, 31)
        if y < 2026:
            Ec = E.as_of(cut)
            ix = PJ.letting_index(Ec)
            ix = {r: s.loc[:pd.Period("%d-11" % y, "M")] for r, s in ix.items()}
        else:
            Ec, ix = E, G.ix
        p_stay, p_new, p_vac = PJ.rates(Ec, years=tuple(range(y - 3, y)))
        A = Ec.in_place(t1)
        dws, i1 = A.index.values, A.values
        C = Ec.in_place(cut)
        has = np.isin(dws, C.index.values)
        ic = np.where(has, C.reindex(dws).fillna(-1).values, -1).astype(int)
        last_i = np.where(has, ic, i1)
        going = Ec.rent0[last_i] * np.exp(PJ.index_gap(ix, Ec.ri[last_i], Ec.start[last_i]))
        k = np.flatnonzero(has)
        ii = ic[k]
        band = PJ._bands(cut, Ec.start[ii])
        cls = PJ.landlord_class(Ec, ii)
        ps = np.array([p_stay.get((b, c), p_stay.get((b, 0), 0.95)) for b, c in zip(band, cls)])
        pn = np.array([p_new.get(c, p_new.get(0, 0.3)) for c in cls])
        stay = Ec.rent_on(ii, t2, G.CL)
        v = np.flatnonzero(~has)
        out[y] = {"ending": float((1 - ps).sum()), "relet": float(((1 - ps) * pn).sum()), "empty": int(len(v)),
                  "let_from_empty": float(p_vac * len(v)),
                  "margin": 100 * float(((1 - ps) * pn * going[k]).sum() / ((1 - ps) * pn * stay).sum() - 1)}
    return out


def analog_backtest(G):
    """The register read on 27 November (as it stood) plus the change to December that earlier years showed: run on
    December 2023, 2024 and 2025 (each against the other years' changes) and for December 2026."""
    E = G.E
    rows = {}
    for y in (2022, 2023, 2024, 2025, 2026):
        cut = MS.day(y, 11, 27)
        Ec = E.as_of(cut) if y < 2026 else E
        nov = Ec.measure(cut, MS.day(y - 1, 11, 27), G.CL)["NAT"]["measure"]
        act = E.measure(MS.day(y, 12, 31), MS.day(y - 1, 12, 31), G.CL)["NAT"]["measure"] if y < 2026 else None
        rows[y] = (nov, act)
    err = []
    for y in (2023, 2024, 2025):
        ch = [rows[z][1] - rows[z][0] for z in (2022, 2023, 2024, 2025) if z != y]
        err.append(rows[y][0] + float(np.mean(ch)) - rows[y][1])
    mean_ch = float(np.mean([rows[z][1] - rows[z][0] for z in (2023, 2024, 2025)]))
    return {"errors": err, "nov26": rows[2026][0], "mean_change": mean_ch, "dec26": rows[2026][0] + mean_ch}


def december_backtests(G):
    """Each December shortcut run on December 2023, 2024 and 2025 from the register as it stood on 27 November:
    a straight trend through the quarters to September, the September figure carried forward, and the register read
    as it stands on 31 December, that reading's error split into the reviews not yet on file and the rest."""
    E = G.E
    sg = G.series()
    qs = list(sg.keys())
    sched = PJ.review_schedule(E, cpi=G.cpi)
    rows = []
    for y in (2023, 2024, 2025, 2026):
        cut, t1, t2 = MS.day(y, 11, 27), MS.day(y - 1, 12, 31), MS.day(y, 12, 31)
        Ec = E.as_of(cut) if y < 2026 else E
        A, C = Ec.in_place(t1), Ec.in_place(t2)
        common = A.index.intersection(C.index)
        a, b = A.loc[common].values, C.loc[common].values
        r1, r2 = Ec.rent_on(a, t1, G.CL), Ec.rent_on(b, t2, G.CL)
        fac = PJ.pending_reviews(Ec, cut, sched)
        fac2 = PJ.scheduled_reviews(Ec, cut, t2, sched, G.cpi)
        f = np.array([fac.get(int(i), 1.0) * fac2.get(int(i), 1.0) for i in b])
        st = 100 * (r2.sum() / r1.sum() - 1)
        wr = 100 * ((r2 * f).sum() / r1.sum() - 1)
        ser = [sg[q]["NAT"] for q in qs if int(q[:4]) * 10 + int(q[-1]) <= y * 10 + 3]
        row = {"year": y, "as_stands": st, "reviews_part": wr - st, "trend": EP.trend(ser)[0],
               "carried": sg["%dQ3" % y]["NAT"]}
        if y < 2026:
            act = E.measure(t2, t1, G.CL)["NAT"]["measure"]
            row.update({"actual": act, "rest_part": act - wr})
        rows.append(row)
    return rows


def rival_run(G, CL, p):
    E = G.E
    r = E.measure(AN.SEP26, AN.SEP25, CL, P=p)
    c26 = EP.contributions(E, AN.SEP26, AN.SEP25, CL)
    ser = G.series(CL=CL)
    d = PJ.project(E, CL, ix=G.ix, cpi=G.cpi)
    return {"R3": {"change": r["NAT"]["same"], "share": r["NAT"]["share_rose"]}, "R4": r["NAT"]["relet"],
            "R5": {"sep26": {g: r[g]["measure"] for g in REG}, "series": {q: v["NAT"] for q, v in ser.items()}},
            "R7": _reg(d), "R8": _split(d["_parts"], c26)}


def operator_reviews(G):
    """Each operator's review rise by year (median per cent over its additional bonds effective that day)."""
    out = {}
    for lid, (mo, dd, shortest, rule, rises) in PJ.review_schedule(G.E, cpi=G.cpi).items():
        out[(mo, dd)] = {"rises": rises, "rule": rule, "shortest": shortest}
    return out


# ------------------------------------------------------------------------------------------------ grading
def bands_of(g):
    """Each result's golden and band, as effort.json and the answer blocks state them."""
    def cells(d, f):
        return {k: [float(v) - f(k, v), float(v) + f(k, v)] for k, v in d.items()}
    B = {}
    B["R1"] = cells(g["R1"], lambda k, v: max(1.0, abs(v) * BANDS["R1"]))
    B["R2"] = cells(g["R2"], lambda k, v: max(1.0, abs(v) * BANDS["R2"]))
    B["R3"] = {"change": [g["R3"]["change"] - BANDS["R3_change"], g["R3"]["change"] + BANDS["R3_change"]],
               "share": [g["R3"]["share"] - BANDS["R3_share"], g["R3"]["share"] + BANDS["R3_share"]]}
    B["R4"] = [g["R4"] - BANDS["R4"], g["R4"] + BANDS["R4"]]
    B["R5"] = cells(measure_cells(g), lambda k, v: BANDS["R5_series"] if k[0] == "2" and k != "2026Q3"
                    else (BANDS["R5_nat"] if k == "2026Q3" else BANDS["R5_reg"]))
    B["R6"] = {"lo": [g["R6"]["lo"] - BANDS["R6_end"], g["R6"]["lo"] + BANDS["R6_end"]],
               "hi": [g["R6"]["hi"] - BANDS["R6_end"], g["R6"]["hi"] + BANDS["R6_end"]], "half": list(R6_HALF)}
    B["R7"] = [g["R7"]["NAT"] - BANDS["R7_nat"], g["R7"]["NAT"] + BANDS["R7_nat"]]
    B["R7b"] = cells({k: v for k, v in g["R7"].items() if k != "NAT"}, lambda k, v: BANDS["R7_reg"])
    B["R8"] = {k: [v - (BANDS["R8_fall"] if k == "fall" else BANDS["R8"]),
                   v + (BANDS["R8_fall"] if k == "fall" else BANDS["R8"])] for k, v in g["R8"].items()}
    return B


def measure_cells(p):
    """The measure as the Measure sheet carries it: every quarter nationally (2026Q3 is the September figure) and the
    September 2026 quarter by region."""
    d = dict(p["R5"]["series"])
    d["2026Q3"] = p["R5"]["sep26"]["NAT"]
    d.update({k: v for k, v in p["R5"]["sep26"].items() if k != "NAT"})
    return d


def pass_values(p):
    return {"R1": p["R1"], "R2": p["R2"], "R3": p["R3"], "R4": p["R4"], "R5": measure_cells(p), "R6": p.get("R6"),
            "R7": p["R7"]["NAT"], "R7b": {k: v for k, v in p["R7"].items() if k != "NAT"}, "R8": p["R8"]}


GRADED = {"R1": "Ask 2", "R2": "Ask 3", "R3": "Component 2", "R4": "Ask 5", "R5": "Component 1",
          "R6": "Ask 7", "R7": "Recommendation", "R7b": "Ask 7", "R8": "Component 3"}
WEIGHTS = {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}


def grade(v, band):
    if isinstance(band, dict):
        ok = sum(1 for k, b in band.items() if v.get(k) is not None and b[0] <= v[k] <= b[1])
        share = ok / float(len(band))
        return 1.0 if share >= 0.999 else (0.5 if share >= 0.5 else 0.0)
    return 1.0 if band[0] <= v <= band[1] else 0.0


def score(p, B):
    blocks = {}
    for rid, ga in GRADED.items():
        b = "recommendation" if ga == "Recommendation" else ("components" if ga.startswith("Component") else "asks")
        blocks.setdefault(b, []).append(rid)
    tot = WEIGHTS["instruction"]
    pv = pass_values(p)
    for b, ids in blocks.items():
        for rid in ids:
            tot += WEIGHTS[b] / len(ids) * grade(pv[rid], B[rid])
    return tot


def pick_careful(res):
    B = bands_of(res["gold"])
    sc = {k: round(score(v, B), 1) for k, v in res["variants"].items()}
    best = max(sc, key=lambda k: (sc[k], k))
    return best, res["variants"][best], sc


# ------------------------------------------------------------------------------------------------ figures
def figures(res):
    g = res["gold"]
    rt = res["routes"]
    F = {}
    F["dec26"] = {k: r1d(v) for k, v in g["R7"].items()}
    F["dec26_range"] = [r1d(g["R6"]["lo"]), r1d(g["R6"]["hi"])]
    F["dec26_half"] = round(g["R6"]["half"], 2)
    F["sep26"] = {k: r1d(v) for k, v in g["R5"]["sep26"].items()}
    F["series"] = {q: r1d(v) for q, v in g["R5"]["series"].items()}
    F["held"] = {k: int(v) for k, v in g["R1"].items()}
    F["relet_n"] = {k: int(v) for k, v in g["R2"].items()}
    F["cont"] = {"change": r1d(g["R3"]["change"]), "share": r1d(g["R3"]["share"])}
    F["cont_change"] = F["cont"]["change"]
    F["cont_share"] = F["cont"]["share"]
    F["relet_change"] = r1d(g["R4"])
    c26r = {k: round(res["c26"][k], 2) for k in ("continuing", "relet")}
    cdr = {k: round(res["dec_parts"][k], 2) for k in ("continuing", "relet")}
    F["contrib_dec"] = cdr
    F["slow"] = {k: round(cdr[k] - c26r[k], 2) for k in c26r}
    F["slow"]["fall"] = round(F["slow"]["continuing"] + F["slow"]["relet"], 2)
    F["sep25"] = r1d(g["R5"]["series"]["2025Q3"])
    c = res["careful"]
    F["careful_name"] = res["careful_name"]
    F["careful_sep26"] = r1d(c["R5"]["sep26"]["NAT"])
    F["careful_dec26"] = r1d(c["R7"]["NAT"])
    F["careful_relet_n"] = int(c["R2"]["NAT"])
    F["careful_cont_change"] = r1d(c["R3"]["change"])
    F["careful_share"] = r1d(c["R3"]["share"])
    F["variant_scores"] = res["variant_scores"]
    F["variants_sep26"] = {k: r1d(v["R5"]["sep26"]["NAT"]) for k, v in res["variants"].items()}
    F["variants_dec26"] = {k: r1d(v["R7"]["NAT"]) for k, v in res["variants"].items()}
    F["variants_relet_change"] = {k: r1d(v["R4"]) for k, v in res["variants"].items()}
    F["variants_cont_change"] = {k: r1d(v["R3"]["change"]) for k, v in res["variants"].items()}
    F["topups_sep26"] = r1d(rt["the additional bonds read as every rise"]["R5"]["sep26"]["NAT"])
    F["pid_sep26"] = r1d(rt["re-lettings tied by property identifier alone"]["R5"]["sep26"]["NAT"])
    F["pid_relet_n"] = int(rt["re-lettings tied by property identifier alone"]["R2"]["NAT"])
    F["start_sep26"] = r1d(rt["re-lettings against the earlier tenancy's starting rent"]["R5"]["sep26"]["NAT"])
    F["relet_start_change"] = r1d(rt["re-lettings against the earlier tenancy's starting rent"]["R4"])
    F["carry_dec26"] = r1d(g["R5"]["sep26"]["NAT"])
    F["trend_dec26"] = r1d(rt["the quarterly figures carried on a straight trend"]["R7"]["NAT"])
    F["asstands_dec26"] = r1d(res["as_stands"])
    F["asstands_adj_dec26"] = r1d(rt["the register as it stands, corrected by its own back-test"]["R7"]["NAT"])
    F["asstands_backtest_err"] = [r1d(e) for e in res["st_err"]]
    F["noreview_dec26"] = r1d(rt["December projected without the review not yet on file"]["R7"]["NAT"])
    F["flow_sep26"] = r1d(res["quick"]["R5"]["sep26"]["NAT"])
    G = res["G"]
    F["topup_share"] = r1d(EP.share_rose(G, G.E, G.CL, G.p, "recorded"))
    F["published_sep26"] = res["published"].get("Penmarra")
    F["backtest"] = [{"year": b["year"], "projected": r1d(b["projected"]), "actual": r1d(b["actual"])}
                     for b in res["backtest"]]
    F["panel_pairs"] = int(res["pairs"])
    F["boot_n"] = AN.B_BOOT
    rv = res["reviews"]
    nov, dec = rv.get((11, 1)), rv.get((12, 1))
    F["b_review"] = {str(y): r1d(v) for y, v in nov["rises"].items()}
    F["a_review"] = {str(y): r1d(v) for y, v in dec["rises"].items()}
    F["b_margin"] = r1d(nov["rule"][1])
    F["a_margin"] = r1d(dec["rule"][1])
    cq = G.cpi
    F["cpi_sep"] = {str(y): cq[(y, 3)] for y in (2023, 2024, 2025, 2026)}
    F["a_review_2026"] = r1d(cq[(2026, 3)] + dec["rule"][1])
    F["a_landlord"] = [lid for lid, v in res["sched"].items() if (v[0], v[1]) == (12, 1)][0]
    F["b_landlord"] = [lid for lid, v in res["sched"].items() if (v[0], v[1]) == (11, 1)][0]
    F["b_review_2026"] = r1d(float(np.median([v for v in PJ.pending_reviews(G.E, AN.CUT, res["sched"]).values()])) * 100 - 100)
    F["pending_n"] = int(res["pending"])
    F["scheduled_n"] = int(res["scheduled"])
    F["contrib26"] = {"continuing": round(res["contrib26"]["same"], 2), "relet": round(res["contrib26"]["relet"], 2)}
    F["exact_relet_n"] = int(res["exact_relet_n"])
    pl = res["panel_link"]
    F["panel_link"] = {"linked": pl["linked"], "dwellings": pl["dwellings"],
                       "years": {str(y): {k: (r1d(v) if isinstance(v, float) else v) for k, v in d.items()}
                                 for y, d in pl["years"].items()}}
    F["survey_share"] = r1d(EP.share_rose(res["G"], res["G"].E, res["G"].CL, res["G"].p, "panel_all"))
    F["validation"] = {y: {k: (round(v, 1) if k != "n" else v) for k, v in d.items()}
                       for y, d in res["validation"].items()}
    F["validation_gap"] = {y: {"model": r1d(abs(d["model"])), "recorded_short": r1d(-d["recorded"]),
                               "carry_over": r1d(d["carry"]), "hybrid_short": r1d(-d["hybrid"])}
                           for y, d in res["validation"].items()}
    F["dec_backtests"] = [{k: (round(v, 2) if k != "year" else v) for k, v in d.items()} for d in res["dec_backtests"]]
    bts = [d for d in res["dec_backtests"] if d["year"] < 2026]
    F["trend_bt_err"] = [r1d(d["trend"] - d["actual"]) for d in bts]
    F["proj_bt_err"] = [r1d(b["projected"] - b["actual"]) for b in res["backtest"]]
    F["asstands_short"] = [round(d["actual"] - d["as_stands"], 2) for d in bts]
    F["dec_churn"] = {str(y): {"ending": int(round(d["ending"], -1)), "relet": int(round(d["relet"], -1)),
                               "empty": d["empty"], "let_from_empty": int(round(d["let_from_empty"], -1)),
                               "margin": r1d(d["margin"])} for y, d in res["churn"].items()}
    an = res["analog"]
    F["analog"] = {"errors": [r1d(e) for e in an["errors"]], "max_error": round(max(abs(e) for e in an["errors"]), 2),
                   "nov26": r1d(an["nov26"]), "mean_change": round(an["mean_change"], 2), "dec26": r1d(an["dec26"])}
    F["reviews_part"] = [round(d["reviews_part"], 2) for d in res["dec_backtests"]]
    F["rest_part"] = [round(a - b, 2) for a, b in zip(F["asstands_short"], F["reviews_part"])]
    F["rest_part_2026"] = round(round(res["gold"]["R7"]["NAT"] - res["dec_backtests"][-1]["as_stands"], 2) -
                                F["reviews_part"][-1], 2)
    F["reviewed_onfile_n"] = int(res["reviewed_onfile_n"])
    F["peak"] = r1d(max(g["R5"]["series"].values()))
    F["peak_q"] = max(g["R5"]["series"], key=lambda q: g["R5"]["series"][q])
    F["bands"] = {"series": BANDS["R5_series"], "region": BANDS["R5_reg"], "national": BANDS["R5_nat"],
                  "held_pct": BANDS["R1"] * 100, "relet_pct": int(BANDS["R2"] * 100), "share_pts": BANDS["R3_share"],
                  "change_pts": BANDS["R3_change"], "relet_change": BANDS["R4"], "fall": BANDS["R8_fall"],
                  "contrib": BANDS["R8"], "dec_national": BANDS["R7_nat"], "dec_region": BANDS["R7_reg"],
                  "range_end": BANDS["R6_end"], "half_lo": R6_HALF[0], "half_hi": R6_HALF[1]}
    F["slow_pts"] = {k: round(-v, 2) for k, v in F["slow"].items()}
    F["conventions"] = {"range_pct": 90, "quarter_end_day": 30, "paper_sections": [2.2, 2.3, 2.4, 2.5, 2.6]}
    F["routes_sep"] = {n: r1d(rr["R5"]["sep26"]["NAT"]) for n, rr in rt.items()}
    F["routes_dec"] = {n: r1d(rr["R7"]["NAT"]) for n, rr in rt.items()}
    F["rivals"] = {n: {k: (r1d(v["NAT"]) if isinstance(v, dict) and "NAT" in v else None) for k, v in rr.items()
                       if k in ("R7",)} for n, rr in res["rivals"].items()}
    F["range_variants"] = {k: round(v, 3) for k, v in res["range_variants"].items()}
    # every result's band and every rival's value, for checks.py's bar block
    Bd = bands_of(g)
    F["band_table"] = {rid: ({k: [round(x[0], 3), round(x[1], 3)] for k, x in b.items()} if isinstance(b, dict)
                             else [round(b[0], 3), round(b[1], 3)]) for rid, b in Bd.items()}
    rv = {}
    for n, rr in res["rivals"].items():
        d = {}
        if "R1" in rr:
            d["R1"] = {k: int(v) for k, v in rr["R1"].items()}
            d["R2"] = {k: int(v) for k, v in rr["R2"].items()}
        if "R3" in rr:
            d["R3"] = {k: round(float(v), 3) for k, v in rr["R3"].items()}
        if "R4" in rr:
            d["R4"] = round(float(rr["R4"]), 3)
        if "R5" in rr:
            d["R5"] = {k: round(float(v), 3) for k, v in measure_cells(rr).items()}
        if "R7" in rr:
            d["R7"] = round(float(rr["R7"]["NAT"]), 3)
            d["R7b"] = {k: round(float(v), 3) for k, v in rr["R7"].items() if k != "NAT"}
        if "R8" in rr:
            d["R8"] = {k: round(float(v), 3) for k, v in rr["R8"].items()}
        rv[n] = d
    F["rival_values"] = rv
    dn = g["R7"]["NAT"]
    F["range_rivals"] = {k: {"lo": round(dn - h, 3), "hi": round(dn + h, 3), "half": round(h, 3)}
                         for k, h in res["range_variants"].items()}
    F["route_values"] = {n: {rid: (round(float(v), 3) if not isinstance(v, dict) else
                                   {kk: round(float(vv), 3) for kk, vv in v.items()})
                             for rid, v in pass_values(rr).items() if v is not None}
                         for n, rr in res["routes"].items()}
    return F


# ------------------------------------------------------------------------------------------------ effort.json
def effort(res, F):
    g, c, q = res["gold"], res["careful"], res["quick"]
    B = bands_of(g)
    gv, cv, qv = pass_values(g), pass_values(c), pass_values(q)

    def rnd(x):
        if isinstance(x, dict):
            return {k: round(float(v), 3) for k, v in x.items()}
        return round(float(x), 3)

    def rb(b):
        if isinstance(b, dict):
            return {k: [round(v[0], 3), round(v[1], 3)] for k, v in b.items()}
        return [round(b[0], 3), round(b[1], 3)]

    meta = {
        "R1": ("bonded tenancies held on 30 September 2026, by region", "held", [], "the two register extracts"),
        "R2": ("dwellings re-let in the year to 30 September 2026, by region", "relet_n", [], "the two register extracts"),
        "R3": ("continuing tenancies: the change in their rent payable and the share whose rent rose", "cont", [],
               "the additional bonds and the rent panel"),
        "R4": ("the change in rent at re-letting", "relet_change", ["R2"], ""),
        "R5": ("the measure: every quarter nationally from March 2022, and September 2026 by region", "measure_cells",
               ["R2", "R3", "R4"], ""),
        "R6": ("the 90 per cent range on the national December 2026 figure", "dec26_rangecells", ["R7"], ""),
        "R7": ("the national measure for the year to December 2026", "dec26_nat", ["R3", "R5"], ""),
        "R7b": ("the regional measures for the year to December 2026", "dec26_reg", ["R3", "R5"], ""),
        "R8": ("the change from September to December 2026 split between continuing tenancies and re-lettings",
               "slow", ["R3", "R7"], ""),
    }
    # figures.json carries each result's golden exactly as graded here
    F["dec26_nat"] = F["dec26"]["NAT"]
    F["dec26_reg"] = {k: v for k, v in F["dec26"].items() if k != "NAT"}
    F["dec26_rangecells"] = {"lo": F["dec26_range"][0], "hi": F["dec26_range"][1], "half": F["dec26_half"]}
    F["measure_cells"] = dict(F["series"])
    F["measure_cells"].update({k: v for k, v in F["sep26"].items() if k != "NAT"})
    shown = {"R1": F["held"], "R2": F["relet_n"], "R3": F["cont"], "R4": F["relet_change"], "R5": F["measure_cells"],
             "R6": F["dec26_rangecells"], "R7": F["dec26_nat"], "R7b": F["dec26_reg"], "R8": F["slow"]}
    results = []
    for rid in ("R1", "R2", "R3", "R4", "R5", "R6", "R7", "R7b", "R8"):
        name, fig, dep, ind = meta[rid]
        r = dict(id=rid, name=name, graded_as=GRADED[rid], figure=fig, depends=dep, independent=ind,
                 golden=shown[rid], passes={"quick": rnd(qv[rid]), "careful": rnd(cv[rid]), "thorough": rnd(gv[rid])})
        if isinstance(B[rid], dict):
            r["bands"] = rb(B[rid])
        else:
            r["band"] = rb(B[rid])
        results.append(r)
    hints = res["hints"]
    routes = [{"name": n, "answer": r1d(rr["R7"]["NAT"]), "golden": n == "the golden"} for n, rr in res["routes"].items()]
    return {"results": results, "hints": hints, "routes": routes, "weights": WEIGHTS,
            "careful_variants": res["variant_scores"], "careful_pass": res["careful_name"]}


def write(res, gen_dir):
    F = figures(res)
    E = effort(res, F)
    json.dump(F, open(gen_dir + "/figures.json", "w"), indent=1, sort_keys=True)
    json.dump(E, open(gen_dir + "/effort.json", "w"), indent=1)
    return F, E
