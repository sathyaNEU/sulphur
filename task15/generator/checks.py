"""The generator's assertions on the cut pack: input gates, neutral mess, the golden against the world's clean truth,
the bar block (each hurried figure outside its band, every rival inside), the factors' footprints and the semantic
fork table's rows. run() raises on the first failure after printing every line."""
import os
import re

import numpy as np
import pandas as pd

import golden as GD
import pack as PK
import world as W

RESULTS = []


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))


def inside(v, band):
    return band[0] <= v <= band[1]


def _truth(w):
    L, N, A = w.runs["L"], w.runs["N"], w.runs["actual"]
    yr = np.array([1.025 if d.year == 2026 else 1.0 for d in W.DAYS])
    price = W.PRICE[None, None, :] * yr[:, None, None] * np.where(w.promo[:, None, :], 1 - w.promo_disc[None, None, :], 1.0)
    price = np.round(price * W.PREMIUM[None, :, None] / 0.05) * 0.05
    cost = np.round(W.COST[None, :] * yr[:, None], 2)[:, None, :]
    pw, bw, P = W.PILOT, W.BASE25, W.ISPILOT
    tot = lambda x, m: x[m].sum(axis=(0, 2))
    t = {}
    t["lost_pilot_2026"] = float(A["lost"][pw][:, P].sum())
    t["lost_pilot_2025"] = float(A["lost"][bw][:, P].sum())
    sb, sA, sL = tot(A["sold"] * price, bw), tot(A["sold"] * price, pw), tot(L["sold"] * price, pw)
    wb, wA, wL, wN = tot(A["waste"] * cost, bw), tot(A["waste"] * cost, pw), tot(L["waste"] * cost, pw), tot(N["waste"] * cost, pw)
    gN, gL = tot(N["sold"] * (price - cost), pw), tot(L["sold"] * (price - cost), pw)
    t["sales_forecast_pp"] = 100 * (sA[P].sum() - sL[P].sum()) / sb[P].sum()
    t["waste_forecast_pp"] = 100 * (wA[P].sum() - wL[P].sum()) / wb[P].sum()
    save = ((gN - gL) + (wL - wN)) * 2
    t["saving"] = {f: float(save[W.FMT == f].mean()) for f in W.FORMATS}
    t["switch"] = [f for f in W.FORMATS if t["saving"][f] > W.LICENCE[f]]
    t["depth"] = {sno: -100 * 0.115 * np.exp(-km / 1.25) for _, sno, km in W.OPENINGS}
    t["wb"], t["wL"], t["wN"] = wb, wL, wN
    return t


def run(w, R, F, E, target):
    RESULTS.clear()
    T = R["T"]
    G, C, Q = R["G"], R["C"], R["Q"]
    bands = F["bands"]
    files = sorted(os.listdir(target))
    # ------------------------------------------------------------------------------------------- input gates
    ok("ten or more usable files", len(files) >= 10, "%d files" % len(files))
    ok("two or more file categories (spreadsheet and text)", any(f.endswith((".csv", ".xlsx")) for f in files)
       and any(f.endswith(".pdf") for f in files))
    nrows = {f: sum(1 for _ in open(os.path.join(target, f), "rb")) - 1 for f in files if f.endswith(".csv")}
    ok("a large CSV of 20,000 rows or more", max(nrows.values()) >= 20000, str(max(nrows.values())))
    ok("a second long CSV of ten printed pages or more", sorted(nrows.values())[-2] >= 600, str(sorted(nrows.values())[-2]))
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "golden.py"), encoding="utf-8").read()
    for f in PK.DISTRACTORS:
        ok("distractor %s ships and the golden never reads it" % f, f in files and f not in src)
    ok("no file under target/ describes the data", not any(re.search(r"readme|dictionary|manifest|notes|schema", f, re.I)
                                                            for f in files))
    # ------------------------------------------------------------------------------------------- neutral mess
    ok("the 2025 extract carries re-sent rows that dedup removes", T["n_dup25"] > 100, str(T["n_dup25"]))
    d = T["daily"]
    ok("after dedup each store, item and day appears once", not d.duplicated(["date", "store", "item"]).any())
    old = set(T["items"]["old_no"].dropna().astype(int))
    ok("two items renumbered at the ERP change, joined through the register", len(old) == 2
       and not d.loc[d["year"] == 2026, "item"].isin(old).any())
    bi = T["bi"]
    raw_bi = open(os.path.join(target, PK.F_BI), encoding="utf-8").read()
    ok("the weekly history renamed its category codes in 2026", ";BAG;" in raw_bi and ";Bageri;" in raw_bi)
    fresh_bi = bi[bi["cat"] != "Kolonial"].groupby(["year", "week", "store"])["sales"].sum()
    fresh_d = d.groupby(["year", "week", "store"])["sales"].sum()
    j = pd.concat([fresh_bi.rename("bi"), fresh_d.rename("d")], axis=1).dropna()
    ok("the weekly history's fresh sales tie to the deduplicated daily record", (j["bi"] - j["d"]).abs().max() < 1.0,
       "max %.2f" % (j["bi"] - j["d"]).abs().max())
    # late scans moved back to their own day move the waste gap by nothing material
    import copy
    d2 = d.copy()
    zero = d2.groupby(["date", "store"])["waste"].transform("sum") == 0
    ok("some store-days book no write-offs (the next-morning scans)", zero.mean() > 0.005, "%.3f" % zero.mean())
    H = R["H"]
    dd = T["daily"]
    base, pil = GD.periods(dd)
    isp = dd["store"].isin(T["pilot"])
    edge = dd["date"].isin([pd.Timestamp("2025-03-03"), pd.Timestamp("2026-03-02")])
    w_edge = dd.loc[edge, "waste_val"].sum() / dd.loc[base | pil, "waste_val"].sum()
    ok("SF10 write-offs booked a day late move the window totals by less than a day's share", w_edge < 0.01, "%.4f" % w_edge)
    dash = pd.read_excel(os.path.join(target, PK.F_DASH), sheet_name=0, header=4)
    dr = __import__("docs").dashboard_rows(target)
    ok("the dashboard is computed from the shipped files", len(dash) == len(dr) and
       all(abs(round(r["sales26"], 2) - v) < 0.006 for r, v in zip(dr, dash.iloc[:, 2])), "%d rows" % len(dash))
    tot = {g: sum(r["waste26"] for r in dr if r["group"] == g) / sum(r["waste25"] for r in dr if r["group"] == g) - 1
           for g in ("Pilotbutikker", "Øvrige butikker")}
    ok("the dashboard's waste change agrees with the headline", abs(100 * (tot["Pilotbutikker"] - tot["Øvrige butikker"])
                                                                     - H["gap_waste_pp"]) < 1e-6)
    # ------------------------------------------------------------------------------------------- against the truth
    t = _truth(w)
    lu = F["lost_units"]
    ok("R2 within 3 per cent of the units truly turned away", abs(lu["pilot_2026"] / t["lost_pilot_2026"] - 1) < 0.03
       and abs(lu["pilot_2025"] / t["lost_pilot_2025"] - 1) < 0.03, "%s against %.0f, %.0f" % (lu, t["lost_pilot_2026"], t["lost_pilot_2025"]))
    ok("R2's bands hold the truth", inside(t["lost_pilot_2026"], bands["lost_units"]["pilot_2026"])
       and inside(t["lost_pilot_2025"], bands["lost_units"]["pilot_2025"]))
    for s, e in G["eff"].items():
        ok("R4 opening at %d within 1.6 points of its true effect" % s, abs(100 * e["effect"] - t["depth"][s]) < 1.6,
           "%.1f against %.1f" % (100 * e["effect"], t["depth"][s]))
        ok("R4 band at %d holds the true effect" % s, inside(t["depth"][s], bands["competitor_effect"][str(s)]))
    ok("R5 forecast part within 0.3 points of the truth", abs(G["decomp"]["sales"]["forecast"] - t["sales_forecast_pp"]) < 0.3,
       "%.2f against %.2f" % (G["decomp"]["sales"]["forecast"], t["sales_forecast_pp"]))
    ok("R5 forecast band holds the truth", inside(t["sales_forecast_pp"], bands["sales_split"]["forecast"]))
    ok("R6 forecast part within 3.5 points of the truth (a store's waste moves 0.95 to 1.13 year on year on AutoOrdre)",
       abs(G["decomp"]["waste"]["forecast"] - t["waste_forecast_pp"]) < 3.5,
       "%.2f against %.2f" % (G["decomp"]["waste"]["forecast"], t["waste_forecast_pp"]))
    typ = G["sp"]["type"].reindex(W.SNO).values
    for ty in ("weekend", "commuter"):
        m = (typ == ty) & W.ISPILOT
        tr = 100 * (t["wL"][m] - t["wN"][m]).sum() / t["wb"][m].sum()
        ok("R7 %s rate's band holds the pilot stores' true rate" % ty, inside(tr, bands["waste_rate"][ty]), "%.1f" % tr)
    for f in W.FORMATS:
        ok("R8 %s within 15 per cent or 3,000 DKK of the truth" % f,
           abs(G["format_saving"][f] - t["saving"][f]) < max(3000, 0.15 * abs(t["saving"][f])),
           "%.0f against %.0f" % (G["format_saving"][f], t["saving"][f]))
        ok("R8 %s band holds the truth" % f, inside(t["saving"][f], bands["saving"][f]))
        ok("R9 %s range holds the truth" % f, G["range"][f][0] <= t["saving"][f] <= G["range"][f][1])
    ok("R10 the true call is the golden's", t["switch"] == G["switch"], "%s" % t["switch"])
    # ------------------------------------------------------------------------------------------- the bar block
    ok("R2 the careful pass's plain estimate lies outside both bands",
       not inside(F["lost_units_plain"]["pilot_2026"], bands["lost_units"]["pilot_2026"])
       and not inside(F["lost_units_plain"]["pilot_2025"], bands["lost_units"]["pilot_2025"]))
    ok("R2 the clipped and unclipped estimates both lie inside", all(inside(F["lost_units_clipped"][k], bands["lost_units"][k])
                                                                     for k in lu))
    ok("R5 the residual reading of the forecast's part lies inside its band",
       inside(F["sales_split_residual_forecast"], bands["sales_split"]["forecast"]))
    ok("R5 and R6 the dashboard reading lies outside", not inside(F["gap_sales_pp"], bands["sales_split"]["forecast"])
       and not inside(F["gap_waste_pp"], bands["waste_split"]["forecast"]))
    ok("R6 the residual reading of the forecast's part lies inside its band",
       inside(F["waste_split_residual_forecast"], bands["waste_split"]["forecast"]))
    nadj = R["rivals"]["unc_type_noadj"]["decomp"]
    ok("R5 and R6 the forecast parts with the openings' trade left in stay in their bands",
       inside(nadj["sales"]["forecast"], bands["sales_split"]["forecast"]) and inside(nadj["waste"]["forecast"], bands["waste_split"]["forecast"]),
       "%.2f, %.2f" % (nadj["sales"]["forecast"], nadj["waste"]["forecast"]))
    for nm, r in R["rivals"].items():
        ok("R8 rival %s inside every band and on the golden call" % nm,
           all(inside(r["format_saving"][f], bands["saving"][f]) for f in W.FORMATS) and r["switch"] == G["switch"],
           str({f: round(r["format_saving"][f]) for f in W.FORMATS}))
    for nm in ("clip_type", "unc_type_mean", "clip_type_mean"):
        rr = R["rivals"][nm]["rates"]["waste"]
        ok("R7 rival %s's rates inside their bands" % nm, all(inside(100 * rr[ty], bands["waste_rate"][ty]) for ty in rr))
    cs = F["careful"]["saving"]
    ok("R8 the careful pass lies outside the Kvarter and To Go bands", not inside(cs["Kvarter"], bands["saving"]["Kvarter"])
       and not inside(cs["To Go"], bands["saving"]["To Go"]))
    ok("R8 the quick pass lies outside every band", all(not inside(F["quick"]["saving"][f], bands["saving"][f]) for f in W.FORMATS))
    ok("R8 by format with the right estimator still lies outside Kvarter and To Go",
       not inside(F["routes"]["by_format"]["saving"]["Kvarter"], bands["saving"]["Kvarter"])
       and not inside(F["routes"]["by_format"]["saving"]["To Go"], bands["saving"]["To Go"]))
    ok("R8 by trading week with every sale counted lies outside Kvarter's band",
       not inside(F["routes"]["plain_type"]["saving"]["Kvarter"], bands["saving"]["Kvarter"]))
    ok("SF15 the recorded margin read format by format is too noisy to place Super against its licence",
       F["super_margin_noise_per_year"]["recorded"] > F["margin_over_licence"]["Super"]
       and F["super_margin_noise_per_year"]["turned_away"] < F["margin_over_licence"]["Super"], str(F["super_margin_noise_per_year"]))
    ok("SF15 the recorded margin books to the forecast what a store's shelves did not lose (store 2158)",
       F["store_2158_margin_change"]["recorded"] < F["store_2158_margin_change"]["turned_away"] - 40000, str(F["store_2158_margin_change"]))
    ok("SF14 the pilot stores' rates taken format by format within the trading week stay inside every band",
       all(inside(R["rivals"]["unc_fxt"]["format_saving"][f], bands["saving"][f]) for f in W.FORMATS))
    rt = F["weekend_pilot_super_over_kvarter"]
    ok("R8 the record rules out carrying the margin part on waste: Super's margin given up runs well past its waste ratio",
       rt["margin"] > 1.2 * rt["sales"] and rt["margin"] > 2.0 * rt["waste"], str(rt))

    for v in R["range_variants"]:
        ok("SF13 R9 a resampling variant lands every end in its band", all(inside(v[f][j], bands["range"][f + "_" + e])
                                                                       for f in W.FORMATS for j, e in enumerate(("lo", "hi"))))
    cr = F["careful"]["range"]
    outside = sum(not inside(cr[f][j], bands["range"][f + "_" + e]) for f in W.FORMATS for j, e in enumerate(("lo", "hi")))
    ok("R9 the careful pass's ranges miss at least four of six ends", outside >= 4, "%d" % outside)
    ok("R10 the careful pass's call is wrong", C["switch"] != G["switch"], str(C["switch"]))
    ok("R10 the quick pass's call is wrong", Q["switch"] != G["switch"], str(Q["switch"]))
    wrong = {tuple(r["switch"]) for r in R["routes"].values() if r["switch"] != G["switch"]} | {tuple(C["switch"]), tuple(Q["switch"])}
    ok("different shortcuts land on two or more different wrong calls", len(wrong) >= 2, str(sorted(wrong)))
    # R4 with the stores whose opening predates the record kept among the comparison stores
    bi_ = T["bi"]
    amb = bi_[bi_["cat"] == "Kolonial"].pivot_table(index=["year", "week"], columns="store", values="sales")
    yoy = np.log(amb.loc[2026].reindex(range(10, 36))) - np.log(amb.loc[2025].reindex(range(10, 36)))
    fmt_ = T["stores"].set_index("store")["format"]
    hit_rec = set(G["eff"])
    for s_, e_ in G["eff"].items():
        clean = [c_ for c_ in yoy.columns if c_ not in hit_rec and fmt_[c_] == fmt_[s_]]
        rel = yoy[s_] - yoy[clean].mean(axis=1)
        y_, wk_, _ = e_["date"].isocalendar()
        pre, post = rel.loc[10:wk_ - 1], rel.loc[min(35, wk_ + 4):35]
        v_ = np.exp(post.mean() - pre.mean()) - 1 if y_ == 2026 else np.exp(pre.mean() - post.mean()) - 1
        ok("R4 at %d with the earlier openings' stores as comparisons stays in its band" % s_,
           inside(100 * v_, bands["competitor_effect"][str(s_)]), "%.1f" % (100 * v_))
    # the savings' comparison stores with the stores whose opening predates the record also left out
    eff2 = dict(G["eff"])
    for r_ in GD.openings(T).itertuples():
        if r_.store not in eff2:
            eff2[r_.store] = {"date": r_.date, "km": float(r_.km), "effect": 0.0}
    P2 = GD.store_savings(T, G["sp"], eff2)
    pred2, _ = GD.transport(G["sp"], P2)
    fs2 = pred2.groupby(G["sp"]["format"]).mean()
    ok("SF11 the savings with every store on the openings log left out of the comparison: inside the bands, same call",
       all(inside(fs2[f], bands["saving"][f]) for f in W.FORMATS) and [f for f in W.FORMATS if fs2[f] > GD.LICENCE[f]] == G["switch"],
       str(fs2.round(0).to_dict()))
    for ramp in (2, 6):
        e2 = GD.competitor_effect(T, ramp_weeks=ramp)
        ok("R4 a %d-week ramp keeps every effect in its band" % ramp,
           all(inside(100 * v["effect"], bands["competitor_effect"][str(s)]) for s, v in e2.items()))
    tab = GD.cum_profile(T)
    S = d["sold"].values.astype(float)
    keys = d[["format", "cat", "dow"]].values
    tt = d["t"].values
    for smin in (1, 3):
        idx = np.where((d["close"] > 0).values & (S >= smin))[0]
        Fq = np.clip(np.array([np.interp(tt[k], *tab[(keys[k, 0], keys[k, 1], int(keys[k, 2]))]) for k in idx]), 0.02, 1)
        over = 100 * ((S[idx] / Fq).sum() / S[idx].sum() - 1)
        ok("R3 the check on days with %d or more sales lands in its band" % smin, inside(over, bands["check_plain_over"]),
           "%.1f" % over)
    # ------------------------------------------------------------------------------------------- footprints
    sp = G["sp"]
    ok("commuter-week stores sit in two formats and in the pilot", F["n_commuter"]["Kvarter"] >= 3 and F["n_commuter"]["To Go"] >= 8
       and F["n_commuter_pilot"]["Kvarter"] >= 2, str(F["n_commuter"]))
    kc = G["pred"][(sp["format"] == "Kvarter") & (sp["type"] == "commuter")]
    ok("the trading week misleads where it decides nothing: Kvarter's commuter stores lose, Kvarter still switches",
       (kc < 0).all() and "Kvarter" in G["switch"], str(kc.round(0).tolist()))
    ok("the To Go pilot stores are all weekend-trading", (sp.loc[sp["pilot"] & (sp["format"] == "To Go"), "type"] == "weekend").all())
    fcm = T["fc"][(T["fc"]["date"] >= "2026-03-02") & T["fc"]["f_korn"].notna()].assign(
        wkend=lambda x: x["date"].dt.dayofweek >= 5, type=lambda x: x["store"].map(sp["type"]))
    pl = fcm.groupby(["type", "wkend"]).agg(k=("f_korn", "sum"), a=("f_auto", "sum")).unstack("wkend")
    pooled = (pl[("k", True)] / pl[("a", True)]) / (pl[("k", False)] / pl[("a", False)])
    rr = F["shadow_ratio_range"]
    ok("the shadow forecasts' weekend ratio lies in its stated range however the stores are pooled",
       all(rr[t_][0] <= v_ <= rr[t_][1] for t_, v_ in list(pooled.items()) + list(F["shadow_ratio"].items())),
       str(pooled.round(2).to_dict()))
    ok("the chain-wide forecast over-weights the weekend in commuter-week stores and not in the others",
       F["shadow_ratio"]["commuter"] > 1.5 and F["shadow_ratio"]["weekend"] < 1.1, str(F["shadow_ratio"]))
    so = d.assign(out=d["close"] <= 0, pilot=d["store"].isin(T["pilot"])).groupby(["format", "pilot", "year"])["out"].mean()
    ok("shelves empty in every format, group and year", (so > 0.05).all(), str(so.round(3).to_dict()))
    ok("an opening decides nothing alone: the call holds with the openings left in",
       R["rivals"]["unc_type_noadj"]["switch"] == G["switch"])
    for f in W.FORMATS:
        idx = np.where((d["close"] > 0).values & (S >= 2) & (d["format"] == f).values)[0]
        Fq = np.clip(np.array([np.interp(tt[k], *tab[(keys[k, 0], keys[k, 1], int(keys[k, 2]))]) for k in idx]), 0.02, 1)
        over = 100 * ((S[idx] / Fq).sum() / S[idx].sum() - 1)
        ok("the plain estimate overstates in-stock days in %s too" % f, over > 4.0, "%.1f" % over)
    # ------------------------------------------------------------------------------------------- semantic forks
    # SF1: the same weeks of 2025 by calendar date (one day earlier) instead of ISO week
    cal0, cal1 = pd.Timestamp("2025-03-02"), pd.Timestamp("2025-08-30")
    b2 = (d["date"] >= cal0) & (d["date"] <= cal1)
    g = {}
    for grp, m in (("p", isp), ("o", ~isp)):
        g[grp] = (d.loc[pil & m, "sales"].sum() / d.loc[b2 & m, "sales"].sum() - 1,
                  d.loc[pil & m, "waste_val"].sum() / d.loc[b2 & m, "waste_val"].sum() - 1)
    ok("SF1 the same weeks of 2025 by calendar date move neither gap by 0.15 points",
       abs(100 * (g["p"][0] - g["o"][0]) - H["gap_sales_pp"]) < 0.15 and abs(100 * (g["p"][1] - g["o"][1]) - H["gap_waste_pp"]) < 0.15)
    # SF2: fresh sales in units would read differently; the prompt says kroner
    gu = {grp: d.loc[pil & m, "sold"].sum() / d.loc[base & m, "sold"].sum() - 1 for grp, m in (("p", isp), ("o", ~isp))}
    ok("SF2 the sales gap counted in units lands in the gap's band (same call; the prompt says kroner)",
       inside(100 * (gu["p"] - gu["o"]), bands["gap_sales"]), "%.2f" % (100 * (gu["p"] - gu["o"])))
    # SF3: the format average over the pilot stores only (agreement 4.3 says every store)
    po = G["pred"][sp["pilot"]].groupby(sp["format"]).mean()
    ok("SF7 the pilot stores' own average differs for To Go (closed by 4.3: every store of the format)",
       abs(po["To Go"] - G["format_saving"]["To Go"]) > 5000, str(po.round(0).to_dict()))
    # SF4: the trading-week cut anywhere in the gap between the two groups gives the same grouping
    ws = np.sort(sp["weekend_share"].values)
    k = int(np.argmax(np.diff(ws)))
    ok("SF12 the widest gap in weekend share is wide (any cut inside it groups the stores alike)", ws[k + 1] - ws[k] > 0.03,
       "%.3f to %.3f" % (ws[k], ws[k + 1]))
    # SF5: rounding: each savings figure is 1,000 DKK or more from its licence under every rival
    for f in W.FORMATS:
        vals = [G["format_saving"][f]] + [r["format_saving"][f] for r in R["rivals"].values()]
        ok("SF9 %s every rival 2,000 DKK or more from the licence on the golden's side" % f,
           all((v - GD.LICENCE[f] > 2000) if f in G["switch"] else (GD.LICENCE[f] - v > 2000) for v in vals),
           "closest %.0f" % min(abs(v - GD.LICENCE[f]) for v in vals))
    # SF6: the stores in the store register are the stores in the record
    ok("SF7b every store in the register trades in the record", set(T["stores"]["store"]) == set(d["store"].unique()))
    # SF closure 22: the planned opening near 3136 (0.6 km) taken off that store's 2027 saving
    if 3136 in G["pred"].index:
        shift = abs(G["pred"][3136]) * 0.115 * np.exp(-0.6 / 1.25) / F["n_stores"]["Kvarter"]
        ok("axis 22 the planned opening near 3136 moves Kvarter's average by under 300 DKK", shift < 300, "%.0f" % shift)
    # SF3: waste at cost as booked, against the waste counted in units
    wu = {grp: d.loc[pil & m, "waste"].sum() / d.loc[base & m, "waste"].sum() - 1 for grp, m in (("p", isp), ("o", ~isp))}
    ok("SF3 the waste gap in units lands apart from the gap at cost (closed by the prompt's 'at cost')",
       abs(100 * (wu["p"] - wu["o"]) - H["gap_waste_pp"]) > 0.0, "%.2f" % (100 * (wu["p"] - wu["o"])))
    # SF16: the gap as the difference of the growth rates, against the change in waste as a share of sales
    lvl = {grp: 100 * (d.loc[pil & m, "waste_val"].sum() / d.loc[pil & m, "sales"].sum()
                       - d.loc[base & m, "waste_val"].sum() / d.loc[base & m, "sales"].sum()) for grp, m in (("p", isp), ("o", ~isp))}
    ok("SF16 the level reading of the waste gap (waste as a share of sales) is a different number (closed by the prompt's wording and asks 1 and 2)",
       abs((lvl["p"] - lvl["o"]) - H["gap_waste_pp"]) > 5, "%.2f" % (lvl["p"] - lvl["o"]))
    # SF4: the other stores are every store outside the pilot, as the dashboard groups them
    ok("SF4 the dashboard's two groups are the pilot stores and every other store",
       set(T["pilot"]) | set(d.loc[~isp, "store"]) == set(d["store"]) and len(T["pilot"]) == sum(F["n_pilot"].values()))
    # SF5: waste alone is not 4.2's saving; it lies outside the Super band
    ok("SF5 the waste-only reading of the saving lies outside Super's band (closed by 4.2)",
       not inside(F["routes"]["waste_only_type"]["saving"]["Super"], bands["saving"]["Super"]))
    # SF6: every price and sales column in the pack is labelled excluding VAT
    hdr25 = open(os.path.join(target, PK.F_D25), encoding="cp1252").readline()
    hdr26 = open(os.path.join(target, PK.F_D26), encoding="utf-8").readline()
    ok("SF6 sales columns are labelled excluding VAT in both extracts and the weekly history",
       "ekskl. moms" in hdr25 and "excl_vat" in hdr26 and "ekskl_moms" in raw_bi.splitlines()[0])
    # SF8: a year is twice the 26 pilot weeks (4.3): the golden's yearly figure is twice its 26-week figure
    p26 = (G["P"]["saving"]).groupby(G["P"]["format"]).sum()
    ok("SF8 the transport carries twice the 26 pilot weeks", abs(G["pred"].sum() - 2 * (
        sp["waste_base"] * sp["type"].map(G["rates"]["waste"]) + sp["sales_base"] * sp["type"].map(G["rates"]["margin"])).sum()) < 1.0)
    # ------------------------------------------------------------------------------------------- effort
    ok("effort.json carries ten results", len(E["results"]) == 10)
    for line in RESULTS:
        print(("PASS " if line[1] else "FAIL ") + line[0] + ("  [" + line[2] + "]" if line[2] else ""))
    bad = [r for r in RESULTS if not r[1]]
    print("checks: %d of %d green" % (len(RESULTS) - len(bad), len(RESULTS)))
    if bad:
        raise SystemExit("checks failed: " + "; ".join(r[0] for r in bad))
    return RESULTS


if __name__ == "__main__":
    # the assertions on the pack as it stands: the world from the build's cache, the golden from target/
    import json
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    import build as B
    import figures as FG
    task = os.path.dirname(here)
    target = os.path.join(task, "target")
    w = B.world_and_runs()
    T = GD.load(target)
    R = GD.results(T, reps=400)
    R = FG.extras(R, T)
    F = json.load(open(os.path.join(here, "figures.json")))
    E = json.load(open(os.path.join(here, "effort.json")))
    run(w, R, F, E, target)
