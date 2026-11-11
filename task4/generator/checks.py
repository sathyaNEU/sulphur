"""The build's assertions, run on the cut pack (python3 checks.py [target]): the golden against the clean truth,
every semantic fork in the design note (SF1 to SF36), the bar block R1 to R7, each hurried route's figures outside
the bands, the night's cut under four schedulers and its margins, the charging split's rivals, the input gates and
the realism sweep. Exit 1 on any failure."""
import datetime as dt
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import night  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import sim  # noqa: E402
import writeup as WU  # noqa: E402

FAIL = []
N = [0]


def ok(name, cond, detail=""):
    N[0] += 1
    if not cond:
        FAIL.append("%s %s" % (name, detail))


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", "\n".join((p.extract_text() or "") for p in PdfReader(path).pages))


def cands(pk, E, lim, eta, m=1.0, codes=None, pad=0, cond=0.0):
    """the qualifying blocks' night jobs in priority order: the recharge (times m) and the steady draw beside it"""
    q = codes if codes is not None else [c for c in sorted(pk.weekday, key=lambda c: pk.priority[c]) if E[c] <= lim]
    return [(c, E[c] * m / eta, max(pk.blocks[c]["ret"] + pad, A.NIGHT_FROM), min(pk.blocks[c]["dep"] + 1440 - pad, A.NIGHT_TO + 1440),
             cond * m) for c in q]


def night_cut_codes(pk, E, g, cond=None, eta=None):
    return night.cut_by_priority(cands(pk, E, g["limit"], g["eta"] if eta is None else eta,
                                       cond=g["cond_kw"] if cond is None else cond), A.CHARGER_KW, P.SUPPLY_KW)[0]


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    effort = json.load(open(os.path.join(HERE, "effort.json")))
    HB = tuple(figs["conventions"]["heat_band"])
    w = sim.world()
    byc = {b["code"]: b for b in w["blocks"]}
    pk = A.load(target)
    g = A.golden(pk)
    car = A.careful(pk)
    qk = A.quick(pk)
    R = A.routes(pk, g)
    lim_t = P.SHARE * P.E_USABLE_2027 * (1 - sim.fade(365))
    Et = {c: sim.design_energy(byc[c]) for c in pk.weekday}
    gold_set = set(figs["call_set"])

    # ---- the clean truth
    de = np.array([g["E"][c] - Et[c] for c in pk.weekday])
    ok("golden energies within 12 kWh of the truth", np.abs(de).max() <= 12, "max %.1f" % np.abs(de).max())
    ok("golden energies unbiased (within half a bin)", abs(de.mean()) <= 5, "mean %.1f" % de.mean())
    ok("golden limit within 2 kWh of the truth", abs(g["limit"] - lim_t) <= 2, "%.1f vs %.1f" % (g["limit"], lim_t))
    q_t = [c for c in sorted(pk.weekday, key=lambda c: pk.priority[c]) if Et[c] <= lim_t]
    taken_t = night.cut_by_priority(cands(pk, Et, lim_t, P.ETA_CHARGE, cond=sim.conditioning_kw(P.DESIGN_T)), A.CHARGER_KW, P.SUPPLY_KW)[0]
    ok("golden order equals the truth's order", set(taken_t) == gold_set, "%s vs %s" % (sorted(taken_t), sorted(gold_set)))
    dem_t = sum(sim.design_night_draw(byc[c]) for c in q_t)
    ok("golden night draw with every qualifying block on charge within 0.1 MWh of the truth", abs(g["demand_kwh"] - dem_t) <= 100,
       "%.0f vs %.0f" % (g["demand_kwh"], dem_t))
    ok("golden verdicts equal the truth's", all(g["verdict"][c] == (Et[c] <= lim_t) for c in pk.weekday))
    ok("SF21 every weekday block clear of the limit by 26 kWh in the truth", min(abs(Et[c] - lim_t) for c in pk.weekday) >= 26)
    ok("SF21 every weekday block clear of the limit by 18 kWh in the golden (the 10 kWh tolerance and the rounding on one side)",
       min(abs(g["E"][c] - g["limit"]) for c in pk.weekday) >= 18, "%.1f" % min(abs(g["E"][c] - g["limit"]) for c in pk.weekday))
    lit, km = {}, {}
    for r in w["diesel_days"]:
        if A.REF[0] <= r["date"] <= A.REF[1]:
            lit[r["code"]] = lit.get(r["code"], 0.0) + r["litres"]
            km[r["code"]] = km.get(r["code"], 0.0) + r["km"]
    tr = {c: lit[c] / km[c] * 100 for c in km}
    er = np.array([g["rates"][c] - tr[c] for c in pk.weekday])
    ok("R1 golden rates within 1.6 l/100 km of the year's actual litres per km on every block", np.abs(er).max() <= 1.6, "max %.2f" % np.abs(er).max())
    ok("R1 golden rates unbiased", abs(er.mean()) <= 0.4, "mean %.2f" % er.mean())
    ok("R6 loss within 0.5 points of the truth", abs(100 * g["loss"] - 100 * sim.fade(365)) <= 0.5)
    ok("eta within 0.005 of the truth", abs(g["eta"] - P.ETA_CHARGE) <= 0.005, "%.4f" % g["eta"])
    ok("R7 the conditioning at the design night within 0.3 kW of the truth", abs(g["cond_kw"] - sim.conditioning_kw(P.DESIGN_T)) <= 0.3,
       "%.2f vs %.2f" % (g["cond_kw"], sim.conditioning_kw(P.DESIGN_T)))
    ok("the pooled ratio is the truth's mix, not the efficiency (2 points or more under it)", P.ETA_CHARGE - g["ratio_pooled"] >= 0.02,
       "%.4f" % g["ratio_pooled"])
    ok("R3 heater heat within 0.5 kW of the truth", abs(g["heater_kw"] - sim.pilot_heating(P.DESIGN_T)[1]) <= 0.5,
       "%.2f vs %.2f" % (g["heater_kw"], sim.pilot_heating(P.DESIGN_T)[1]))
    ok("the 2027 heating within 0.5 kW of the truth", abs(g["parts"]["heat_new"] - sim.new_bus_heating(P.DESIGN_T)) <= 0.5)
    ok("the pilot blocks are the nine with 30 or more electric weekdays", set(figs["pilot_blocks"]) == set(w["pilot"]))
    ok("realism: no electric bus-day ends under 3 per cent state of charge", min(r["soc1"] for r in w["ebus_days"]) >= 3.0,
       "%.1f" % min(r["soc1"] for r in w["ebus_days"]))
    ok("realism: no session starts under 3 per cent", int(pk.sessions["soc_in_pct"].min()) >= 3)

    # ---- R1 of the bar: the raw material ships, no column holds a result
    for k in ("fuel", "dispatch", "ebus", "sessions"):
        hdr = open(os.path.join(target, PK.FILES[k]), encoding="utf-8").readline().lower()
        ok("R1 bar: no result column in %s" % k, not re.search(r"design|energy_per_km|l_per_100|rate|qualif|verdict|difficulty", hdr), hdr)
    ok("R1 bar: the golden reads the fuel, dispatch, telematics, sessions, register, weather, workshop and plan files",
       all(k in A.FILES for k in ("fuel", "dispatch", "ebus", "sessions", "blocks", "vehicles", "weather", "workshop", "plan")))
    ok("R1 bar: the distractors are never read", not any(k in A.FILES for k in PK.DISTRACTORS))

    # ---- R2 of the bar: every mess item neutral
    pk2 = A.load(target)
    pk2.ebus = pd.concat([pk2.ebus, pk2.ebus[(pk2.ebus["date"] >= dt.date(2026, 5, 11)) & (pk2.ebus["date"] <= dt.date(2026, 5, 14))]]).reset_index(drop=True)
    E2, _ = A.design_energies(pk2, "golden", g["rates"])
    ok("R2 bar SF6: the telematics days uploaded twice, kept, move no energy by more than 8 kWh", max(abs(E2[c] - g["E"][c]) for c in pk.weekday) <= 8,
       "%.1f" % max(abs(E2[c] - g["E"][c]) for c in pk.weekday))
    pk3 = A.load(target)
    pk3.fuel = pk3.fuel[~pk3.fuel["card_no"].isin([c["card"] for c in pk3.cards if c["fn"] is None])]
    r3 = A.diesel_rates(pk3)
    ok("R2 bar SF7: the night shift's spare cards (the AdBlue purchases) dropped move no block's diesel figure", max(abs(r3[c] - g["rates"][c]) for c in pk.weekday) <= 0.05,
       "%.2f" % max(abs(r3[c] - g["rates"][c]) for c in pk.weekday))
    ok("R2 bar SF7: the spare cards carry only AdBlue, with the vehicle typed", set(pk.fuel[pk.fuel["card_no"].isin([c["card"] for c in pk3.cards if c["fn"] is None])]["kind"]) == {"adblue"})
    r4 = A.diesel_rates(pk, merge_minutes=0)
    ok("R2 bar SF8: second swipes left unmerged move no block by more than 0.7", max(abs(r4[c] - g["rates"][c]) for c in pk.weekday) <= 0.7)
    r5 = A.diesel_rates(pk, by_timestamp=False)
    ok("R2 bar SF9: fills mapped to days by date alone move no block by more than 1.0", max(abs(r5[c] - g["rates"][c]) for c in pk.weekday) <= 1.0,
       "%.2f" % max(abs(r5[c] - g["rates"][c]) for c in pk.weekday))
    pk4 = A.load(target)
    pk4.ebus["t"] = pk4.ebus["t_station"]
    E4, p4 = A.design_energies(pk4, "golden", g["rates"])
    ok("R2 bar SF10: the station's temperature in place of the sensor's moves no energy by more than 8 kWh", max(abs(E4[c] - g["E"][c]) for c in pk.weekday) <= 8,
       "%.1f" % max(abs(E4[c] - g["E"][c]) for c in pk.weekday))
    # old block codes: the reference year and the pilot both run on the new codes; the early months only feed the e-bus model
    pk5 = A.load(target)
    pk5.ebus = pk5.ebus[pk5.ebus["date"] >= A.NEW_CODES].reset_index(drop=True)
    E5, _ = A.design_energies(pk5, "golden", g["rates"])
    ok("R2 bar SF5: the old-coded months of the pilot dropped move no energy by more than 10 kWh", max(abs(E5[c] - g["E"][c]) for c in pk.weekday) <= 10,
       "%.1f" % max(abs(E5[c] - g["E"][c]) for c in pk.weekday))

    # ---- R3 of the bar: each hurried figure outside its band
    tol = WU.E_TOL
    out_c = sum(abs(car["E"][c] - g["E"][c]) > tol for c in pk.weekday)
    out_q = sum(abs(qk["E"][c] - g["E"][c]) > tol for c in pk.weekday)
    ok("R3 bar R4: the careful pass misses 30 or more of the 48 energies", out_c >= 30, "%d" % out_c)
    ok("R3 bar R4: the quick pass misses 36 or more", out_q >= 36, "%d" % out_q)
    hard = [c for c in pk.weekday if c not in figs["pilot_blocks"] and g["rates"][c] >= 52]
    ok("R3 bar R4: the careful pass forecasts the hard blocks the pilot never ran (diesel 52 or more) light by 25 kWh or more on average",
       len(hard) >= 10 and np.mean([g["E"][c] - car["E"][c] for c in hard]) >= 25, "%d, %.1f" % (len(hard), np.mean([g["E"][c] - car["E"][c] for c in hard])))
    ok("R3 bar R4: and 20 or more of the 39 blocks it never ran light by 10 kWh or more",
       sum(g["E"][c] - car["E"][c] >= 10 for c in pk.weekday if c not in figs["pilot_blocks"]) >= 20)
    ok("R3 bar R9: the careful pass orders another count and another set (blocks in and blocks out)",
       len(car["taken"]) != len(g["taken"]) and set(car["taken"]) - gold_set and gold_set - set(car["taken"]), "%d vs %d" % (len(car["taken"]), len(g["taken"])))
    ok("R3 bar R8: the quick pass orders more than the careful pass", len(qk["taken"]) > len(car["taken"]))
    ok("R3 bar R6: the careful pass earns the loss (curved form inside the band)", WU.LOSS_BAND[0] <= 100 * car["loss"] <= WU.LOSS_BAND[1])
    fd, pb = A.diesel_rates_fill_day(pk), A.diesel_rates_per_bus(pk)
    for name, rr in (("fill-day", fd), ("per-bus", pb)):
        miss = sum(abs(rr.get(c, 0) - g["rates"][c]) > WU.R1_TOL for c in pk.weekday)
        ok("R3 bar R1: the %s read misses 30 or more blocks" % name, miss >= 30, "%d" % miss)
    ok("R3 bar R5: the careful pass passes 3 or more blocks the golden refuses", sum(car["verdict"][c] and not g["verdict"][c] for c in pk.weekday) >= 3)
    E2r, p2r = A.design_energies(pk, "j2_wrong", g["rates"])
    ok("R3 bar R3: the pilot's own cold response sits 3 kW or more under the 2027 model's heating (the heaters' share left out)",
       g["parts"]["heat_new"] - p2r["heat_used"] >= 3.0, "%.2f vs %.2f" % (p2r["heat_used"], g["parts"]["heat_new"]))
    ok("R3 bar R3: the careful pass reads the heaters from the fills (graded up)", abs(car["parts"]["heater_lph"] * A.HEATER_KWH_PER_L - g["heater_kw"]) < 1e-9)
    ok("R3 bar R8: the careful pass's night draw outside the band", abs(car["demand_kwh"] - g["demand_kwh"]) / 1000 > WU.NIGHT_TOL,
       "%.2f vs %.2f" % (car["demand_kwh"] / 1000, g["demand_kwh"] / 1000))
    pooled_dem = sum(g["E"][c] / g["ratio_pooled"] for c in g["qualifying"])
    ok("R3 bar R8: the golden's energies at the sessions' pooled ratio fall outside the night band by 0.1 MWh or more",
       (g["demand_kwh"] - pooled_dem) / 1000 > WU.NIGHT_TOL + 0.1, "%.2f vs %.2f" % (pooled_dem / 1000, g["demand_kwh"] / 1000))
    ok("R3 bar R8: the quick pass's night draw outside the band", abs(qk["demand_kwh"] - g["demand_kwh"]) / 1000 > WU.NIGHT_TOL)
    CB = tuple(figs["conventions"]["cond_band"])
    ok("R3 bar R7: the careful pass files no conditioning (the pooled ratio), outside the band", car["cond_kw"] < CB[0] - 0.6)

    # ---- R4 of the bar: no plant (the realism sweep below covers repeated blocks); R5 footprints
    j1 = {c: Et[c] - (g["E"][c] - (car["E"][c] - (pk.blocks[c]["hours"] * (car["parts"]["heat_used"] - g["parts"]["heat_new"])))) for c in pk.weekday}
    # the bridge's gap on blocks where nothing turns: blocks over the limit by 40 kWh or more still carry it
    far = [c for c in pk.weekday if g["E"][c] - g["limit"] >= 40]
    carried = [c for c in far if (g["E"][c] - car["E"][c]) >= 15]
    ok("R5 bar: the hurried under-forecast sits on blocks far over the limit too (nothing turns there)", len(carried) >= 5, "%d of %d" % (len(carried), len(far)))
    ok("R5 bar: the heaters' share sits on every block (hours x heat on all 48)", all(pk.blocks[c]["hours"] * g["heater_kw"] >= 25 for c in pk.weekday))
    ok("R5 bar: the pilot blocks are not the deciding units (most of the order and most of the flips are blocks the pilot never ran)",
       sum(1 for c in g["taken"] if c not in figs["pilot_blocks"]) >= 10 and
       sum(1 for c in pk.weekday if c not in figs["pilot_blocks"] and car["verdict"][c] != g["verdict"][c]) >= 5)
    nres = len(effort["results"])
    for h in effort["hints"]:
        ok("R6 bar: hint rescues a third or fewer (%s)" % h["sentence"][:40], len(h["rescues"]) <= nres / 3.0, str(h["rescues"]))
    # R7: the rivals inside the bands
    Eh, _ = A.design_energies(pk, "golden", g["rates"], bridge_hours=True)
    Ea, _ = A.design_energies(pk, "golden", g["rates"], own_min_days=10 ** 6)
    for name, EE in (("SF15 bridge with hours per km", Eh), ("SF16 bridge for every block", Ea), ("SF10 station temperature", E4)):
        ok("R7 bar: %s inside the energy band" % name, max(abs(EE[c] - g["E"][c]) for c in pk.weekday) <= tol, "%.1f" % max(abs(EE[c] - g["E"][c]) for c in pk.weekday))
        tk = night_cut_codes(pk, EE, g)
        ok("R7 bar: %s lands the order" % name, set(tk) == gold_set, str(sorted(tk)))
    for form in ("curved", "sqrt", "log"):
        l = 100 * A.capacity_loss(pk, form)[0]
        ok("R7 bar SF18: loss form %s inside the band" % form, WU.LOSS_BAND[0] <= l <= WU.LOSS_BAND[1], "%.2f" % l)
    ll = 100 * A.capacity_loss(pk, "linear")[0]
    ok("SF18: a straight line in age lands inside the widened band and under the curved forms (the first months' loss missed)",
       WU.LOSS_BAND[0] + 0.15 <= ll < 100 * g["loss"] - 1.0, "%.2f" % ll)
    lim_l = A.SHARE * pk.usable_2027 * (1 - ll / 100.0)
    ok("SF18: the straight line's limit moves no verdict and lands the order", all((g["E"][c] <= lim_l) == g["verdict"][c] for c in pk.weekday)
       and set(night_cut_codes(pk, g["E"], {"limit": lim_l, "eta": g["eta"], "cond_kw": g["cond_kw"]})) == gold_set)
    for name, rr in (("SF9 date-based", r5), ("SF8 unmerged", r4)):
        ok("R7 bar: %s diesel inside the band" % name, max(abs(rr[c] - g["rates"][c]) for c in pk.weekday) <= WU.R1_TOL)
    faults = g["faults"]
    ok("SF12: the heater-fault weeks give 7 to 12 kWh of heat per litre (the rating 8.97)", all(7 <= v[4] <= 12.5 for v in faults) and len(faults) == 2, str(faults))
    kw_lo, kw_hi = g["parts"]["heater_lph"] * 9.8 * 0.84, g["parts"]["heater_lph"] * 9.8 * 0.92
    ok("SF12: the public lower heating value at 84 to 92 per cent burner efficiency stays inside the heat band",
       HB[0] <= kw_lo and kw_hi <= HB[1], "%.2f to %.2f" % (kw_lo, kw_hi))
    ok("SF11: the HVO fills give 40 or more tank-to-tank intervals", len(A.heater_fuel(pk)[3]) >= 40)
    # the charging split: every reading a careful fit could take inside the conditioning band, landing the night and the order
    se = A.session_frame(pk)
    ok("SF31: 3,000 or more sessions carry a battery gain from the bus's own day", len(se) >= 3000, str(len(se)))
    riv = {}
    for name, kw in (("the evening's temperature", {"tcol": "t_evening"}), ("the morning's temperature", {"tcol": "t_morning"}),
                     ("the bus's own sensor", {"tcol": "t_sensor"}), ("the knot at 0 C", {"T0": 0.0}), ("the knot at 10 C", {"T0": 10.0}),
                     ("the knot at 5 C", {"T0": 5.0})):
        sub = se.dropna(subset=[kw.get("tcol", "t_night")])
        eta_r, _, _, _, cond_r, _ = A.charging_model(pk, se=sub, **kw)
        riv[name] = (eta_r, cond_r)
        ok("SF32: the conditioning with %s inside the band" % name, CB[0] <= cond_r <= CB[1], "%.2f" % cond_r)
        dem_r = A.night_draw(pk, g["qualifying"], g["E"], eta_r, cond_r)
        ok("SF32: the night draw with %s inside the night band" % name, abs(dem_r - g["demand_kwh"]) / 1000 <= WU.NIGHT_TOL - 0.1,
           "%.2f" % (dem_r / 1000))
        ok("SF32: %s lands the order" % name, set(night_cut_codes(pk, g["E"], g, cond_r, eta_r)) == gold_set)
    eta_nb, _, _, _, cond_nb, rm_nb = A.charging_model(pk, se=se, base=False)
    ok("SF33: a fit with no standing draw fits worse and its night draw stays inside the band",
       rm_nb > g["cond_fit"][3] and abs(A.night_draw(pk, g["qualifying"], g["E"], eta_nb, cond_nb) - g["demand_kwh"]) / 1000 <= WU.NIGHT_TOL,
       "%.2f, %.2f MWh" % (rm_nb, A.night_draw(pk, g["qualifying"], g["E"], eta_nb, cond_nb) / 1000))
    ok("SF33: a fit with no standing draw lands the order", set(night_cut_codes(pk, g["E"], g, cond_nb, eta_nb)) == gold_set)
    e15, rm_m = A.charging_ratio_by_cold(pk, se)
    mdem = sum(g["E"][c] / e15 for c in g["qualifying"])
    mcut = night.cut_by_priority([(c, g["E"][c] / e15, *A.window(pk, c)) for c in g["qualifying"]], A.CHARGER_KW, P.SUPPLY_KW)[0]
    ok("SF34: a loss that scales with the recharge (no hours term) fits the sessions worse", rm_m > g["cond_fit"][3] * 1.05,
       "%.2f vs %.2f" % (rm_m, g["cond_fit"][3]))
    ok("SF34: and still lands the night draw inside the band and the order", abs(mdem - g["demand_kwh"]) / 1000 <= WU.NIGHT_TOL and set(mcut) == gold_set,
       "%.2f MWh, %d" % (mdem / 1000, len(mcut)))
    # its residuals rise with the hours on charge, the golden's do not: the data separate the two
    sub = se[se["t_night"] <= -5]
    k15 = 1.0 / e15
    from numpy import corrcoef
    res_m = sub["energy_kwh"] - sub["gain"] * (sub["energy_kwh"] / sub["gain"]).mean()
    ok("SF34: on the cold nights the multiplicative fit's residual rises with the hours on charge",
       corrcoef(res_m, sub["rel_h"])[0, 1] > 0.3, "%.2f" % corrcoef(res_m, sub["rel_h"])[0, 1])
    eta_ph, _, _, _, cond_ph, _ = A.charging_model(pk, se=se, hcol="plug_h")
    dem_ph = sum(g["E"][c] / eta_ph + cond_ph * (pk.blocks[c]["dep"] + 1440 - pk.blocks[c]["ret"]) / 60.0 for c in g["qualifying"])
    ok("SF35: the hours plugged in (the relay read past) put the steady draw on hours the chargers are held off; the night band holds",
       abs(dem_ph - g["demand_kwh"]) / 1000 <= WU.NIGHT_TOL, "%.2f" % (dem_ph / 1000))
    # SF42: the battery's gain on charge read on every capacity basis a fit could take
    ebx = pk.ebus
    dd = (ebx["soc_start_pct"] - ebx["soc_end_pct"]).values.astype(float)
    mm = dd >= 30
    capx = ebx["energy_used_kwh"].values[mm] / (dd[mm] / 100.0)
    agex = ebx["age"].values[mm] / 365.25
    coldx = np.maximum(0.0, 10.0 - ebx["t"].values[mm])
    busx = ebx["vehicle"].values[mm]
    bl = sorted(set(busx))
    Xx = np.column_stack([np.column_stack([(busx == b).astype(float) for b in bl]), 1 - np.exp(-agex * 3.0), agex, coldx])
    bx, *_ = np.linalg.lstsq(Xx, capx, rcond=None)
    lvx = dict(zip(bl, bx[:len(bl)]))
    agemap = {(int(r.vehicle), r.date): r.age / 365.25 for r in ebx.itertuples()}
    agev = np.array([agemap.get((int(v), d_), np.nan) for v, d_ in zip(se["vehicle"], se["evening"])])
    ptsv = (se["soc_out_pct"] - se["soc_in_pct"]).values / 100.0
    tv = se["t_sensor"].fillna(se["t_evening"]).values
    fade_cap = np.array([lvx[int(v)] + (1 - np.exp(-a * 3.0)) * bx[len(bl)] + a * bx[len(bl) + 1] for v, a in zip(se["vehicle"], agev)])
    for name, gg in (("the fitted fade curve, no cold", ptsv * fade_cap),
                     ("the fitted fade curve and its cold term", ptsv * (fade_cap + bx[-1] * np.maximum(0.0, 10.0 - tv))),
                     ("480 kWh less the first-winter loss", ptsv * 480.0 * (1 - g["loss"]))):
        s2 = se.copy()
        s2["gain"] = gg
        eta_k, _, _, _, cond_k, _ = A.charging_model(pk, se=s2)
        ok("SF42: the gain on %s keeps the conditioning inside the band" % name, CB[0] <= cond_k <= CB[1], "%.2f" % cond_k)
        ok("SF42: the gain on %s lands the night inside its band and the order" % name,
           abs(A.night_draw(pk, g["qualifying"], g["E"], eta_k, cond_k) - g["demand_kwh"]) / 1000 <= WU.NIGHT_TOL
           and set(night_cut_codes(pk, g["E"], g, cond_k, eta_k)) == gold_set)
    s2 = se.copy()
    s2["gain"] = ptsv * 480.0
    eta_n, _, _, _, cond_n, rm_n = A.charging_model(pk, se=s2)
    cut_n = night_cut_codes(pk, g["E"], g, cond_n, eta_n)
    ok("SF42: the quoted 480 kWh as the gain's capacity is ruled out: a charger efficiency of 0.98 or more and the worst fit",
       eta_n >= 0.98 and rm_n > g["cond_fit"][3] * 1.1, "%.4f, %.2f" % (eta_n, rm_n))
    print("SF42 record: the bare 480 kWh basis gives efficiency %.4f, conditioning %.2f kW, residual %.2f against %.2f, and the "
          "exact flow orders %d (ruled out above)" % (eta_n, cond_n, rm_n, g["cond_fit"][3], len(cut_n)))
    # the steady draw as flexible energy (scheduled like the recharge) instead of a steady load over the window
    flex = [(c, g["E"][c] / g["eta"] + g["cond_kw"] * (A.window(pk, c)[1] - A.window(pk, c)[0]) / 60.0, *A.window(pk, c)) for c in g["qualifying"]]
    ok("SF36: the conditioning scheduled as flexible energy lands the same order", set(night.cut_by_priority(flex, A.CHARGER_KW, P.SUPPLY_KW)[0]) == gold_set)
    # the night under four readings
    cs = cands(pk, g["E"], g["limit"], g["eta"], cond=g["cond_kw"])
    n = len(g["taken"])
    ok("SF22: the exact flow recharges the %d and not the %d" % (n, n + 1), night.feasible(cs[:n], A.CHARGER_KW, P.SUPPLY_KW)[0] and not night.feasible(cs[:n + 1], A.CHARGER_KW, P.SUPPLY_KW)[0])
    sl = night.greedy(cs[:n], A.CHARGER_KW, P.SUPPLY_KW, rule="slack")
    sl1 = night.greedy(cs[:n + 1], A.CHARGER_KW, P.SUPPLY_KW, rule="slack")
    ok("SF22: the least-slack schedule recharges the %d and leaves the %dth short" % (n, n + 1), sum(sl.values()) < 1 and sum(sl1.values()) > 50,
       "%.0f, %.0f" % (sum(sl.values()), sum(sl1.values())))
    need = A.night_draw(pk, g["taken"], g["E"], g["eta"], g["cond_kw"])
    need1 = need + cs[n][1] + cs[n][4] * (cs[n][3] - cs[n][2]) / 60.0
    ok("SF22: the night period's energy (capacity x 10 h) holds the %d and not the %d" % (n, n + 1), need <= P.SUPPLY_KW * 10 < need1,
       "%.0f, %.0f" % (need, need1))
    ed = night.greedy(cs[:n], A.CHARGER_KW, P.SUPPLY_KW, rule="edf")
    ed1 = night.greedy(cs[:n + 1], A.CHARGER_KW, P.SUPPLY_KW, rule="edf")
    ok("SF22: earliest-departure-first leaves the %dth short by more than it leaves the %d (a heuristic, not feasibility)" % (n + 1, n),
       sum(ed1.values()) > 2 * sum(ed.values()) and sum(ed.values()) < 0.015 * need, "%.0f vs %.0f" % (sum(ed.values()), sum(ed1.values())))
    up = 1.0
    while night.feasible(cands(pk, g["E"], g["limit"], g["eta"], up + 0.005, cond=g["cond_kw"])[:n], A.CHARGER_KW, P.SUPPLY_KW)[0] and up < 1.5:
        up += 0.005
    down = 1.0
    while not night.feasible(cands(pk, g["E"], g["limit"], g["eta"], down - 0.005, cond=g["cond_kw"])[:n + 1], A.CHARGER_KW, P.SUPPLY_KW)[0] and down > 0.5:
        down -= 0.005
    ok("SF23: the %d hold with the night's draws 2 per cent higher" % n, up >= 1.0199, "%.3f" % up)
    ok("SF23: the %dth fits only with the night's draws 2 per cent lower" % (n + 1), down <= 0.98, "%.3f" % down)
    for pad in (10, 20):
        tk = night.cut_by_priority(cands(pk, g["E"], g["limit"], g["eta"], pad=pad, cond=g["cond_kw"]), A.CHARGER_KW, P.SUPPLY_KW)[0]
        ok("SF22: %d-minute margins at plug-in and departure cut the list at the same %d" % (pad, n), len(tk) == n and set(tk) == gold_set, str(len(tk)))
    nf = night_cut_codes(pk, g["E"], {"limit": A.SHARE * pk.usable_2027, "eta": g["eta"], "cond_kw": g["cond_kw"]})
    # SF27: each graded band's edges move no verdict and leave the cut at the same set
    for hk in (HB[0], HB[1]):
        Eb = {c: g["E"][c] + pk.blocks[c]["hours"] * (hk - g["heater_kw"]) for c in pk.weekday}
        tb = night_cut_codes(pk, Eb, g)
        ok("SF27: the heaters' heat at %.1f kW (the band's edge) lands the same order and verdicts" % hk,
           set(tb) == gold_set and all((Eb[c] <= g["limit"]) == g["verdict"][c] for c in pk.weekday), str(len(tb)))
    for lp in (WU.LOSS_BAND[0], WU.LOSS_BAND[1]):
        lim_b = A.SHARE * pk.usable_2027 * (1 - lp / 100.0)
        tb = night_cut_codes(pk, g["E"], {"limit": lim_b, "eta": g["eta"], "cond_kw": g["cond_kw"]})
        ok("SF27: the loss at %.1f per cent (the band's edge) lands the same order and verdicts" % lp,
           set(tb) == gold_set and all((g["E"][c] <= lim_b) == g["verdict"][c] for c in pk.weekday), str(len(tb)))
    for ck in CB:
        tb = night_cut_codes(pk, g["E"], g, ck)
        ok("SF27: the conditioning at %.1f kW (the band's edge) lands the same order" % ck, set(tb) == gold_set, str(len(tb)))
    # SF30: the six pilot buses go to Kauppala with the 2027 timetable (the fleet plan), so they draw nothing at Niittyla
    from openpyxl import load_workbook as _lw
    plan = [r for r in _lw(os.path.join(target, PK.FILES["plan"]), read_only=True)["Timetable 2027"].iter_rows(values_only=True)]
    ok("SF30: the fleet plan moves the six 2025 buses to Kauppala with the 2027 timetable", any(r[0] and "1201 to 1206" in str(r[0]) and "Kauppala" in str(r[0]) for r in plan))
    ok("SF30: the order is one bus for each block assigned", len(figs["call_set"]) == figs["call_count"], str(figs["call_count"]))
    # SF28: the town station (keskusta) in place of the airport for the sensor dropouts and the heater fit
    pk6 = A.load(target)
    wx = pd.read_csv(os.path.join(target, PK.FILES["weather"]))
    wx["date"] = pd.to_datetime(wx["date"]).dt.date
    kesk = dict(zip(wx["date"], wx["t_mean_keskusta_c"].astype(float)))
    st6 = np.array([kesk.get(d, np.nan) for d in pk6.ebus["date"]])
    amb6 = pk6.ebus["ambient_mean_c"].astype(float).values
    ok6 = ~np.isnan(amb6)
    pk6.ebus["t"] = np.where(ok6, amb6, st6 + float(np.nanmean(amb6[ok6] - st6[ok6])))
    E6, _ = A.design_energies(pk6, "golden", g["rates"])
    ok("SF28: the town station in place of the airport moves no energy by more than 8 kWh and lands the order",
       max(abs(E6[c] - g["E"][c]) for c in pk.weekday) <= 8 and set(night_cut_codes(pk6, E6, g)) == gold_set,
       "%.1f" % max(abs(E6[c] - g["E"][c]) for c in pk.weekday))
    pk7 = A.load(target)
    pk7.ebus["t"] = np.where(ok6, st6 + 0.0, st6)   # the station throughout, no sensor
    E7, _ = A.design_energies(pk7, "golden", g["rates"])
    ok("SF28: the town station throughout moves no energy by more than 10 kWh and lands the order",
       max(abs(E7[c] - g["E"][c]) for c in pk.weekday) <= 10 and set(night_cut_codes(pk7, E7, g)) == gold_set,
       "%.1f" % max(abs(E7[c] - g["E"][c]) for c in pk.weekday))
    # SF29: the loss read on one bus at a time stays inside the band
    per_bus = []
    for fn in pk.ebuses:
        pkb = A.load(target)
        pkb.ebus = pkb.ebus[pkb.ebus["vehicle"] == fn].reset_index(drop=True)
        if (pkb.ebus["age"].max()) >= 365:
            per_bus.append(100 * A.capacity_loss(pkb, "curved")[0])
    ok("SF29: the loss read on any one bus with a full year in service stays inside the band", len(per_bus) >= 3 and
       all(WU.LOSS_BAND[0] <= v <= WU.LOSS_BAND[1] for v in per_bus), str([round(v, 2) for v in per_bus]))
    ok("SF24: with the quoted capacity no block changes side (the loss sets the limit and moves no verdict)",
       set(nf) == gold_set and all((g["E"][c] <= A.SHARE * pk.usable_2027) == g["verdict"][c] for c in pk.weekday))
    ok("SF25: the order without the charging losses and the conditioning is larger", len(R["the night scheduled on battery energy (charging losses and conditioning ignored)"]) > n)
    ok("SF25: the order at the sessions' pooled ratio is larger", len(R["the sessions' pooled ratio for the night (the battery's conditioning left out)"]) > n)
    ok("SF26: the per-block verdicts summed exceed the order by 3 or more", len(g["qualifying"]) - n >= 3)
    wrong = {json.dumps(sorted(v)) for k, v in R.items() if k != "golden" and set(v) != gold_set}
    ok("routes: five or more distinct wrong answers", len(wrong) >= 5, "%d" % len(wrong))
    counts = {len(v) for k, v in R.items() if k != "golden"}
    ok("routes: four or more distinct wrong counts", len(counts - {n}) >= 4, str(sorted(counts)))
    ok("routes: no route other than the golden lands the set", all(set(v) != gold_set for k, v in R.items() if k != "golden"))
    # graded figures and their bins
    ok("SF19 loss mid-band", WU.LOSS_BAND[0] + 0.3 <= figs["loss_pct"] <= WU.LOSS_BAND[1] - 0.3)
    ok("SF12 heater mid-band", HB[0] + 0.4 <= figs["heater_kw"] <= HB[1] - 0.4)
    ok("SF2 the pilot gap is 2.5 l/100 km or more", figs["pilot_gap"] >= 2.5, str(figs["pilot_gap"]))
    ok("SF2 no pilot block among the ten thriftiest of the 48, none among the hardest third", min(figs["pilot_ranks_all"]) > 10 and max(figs["pilot_ranks_all"]) <= 32, str(figs["pilot_ranks_all"]))
    ok("SF2 the pilot blocks sit in the thriftiest half of the blocks of 225 km or less", max(figs["pilot_ranks_short"]) <= figs["short_km_blocks"] / 2, str(figs["pilot_ranks_short"]))
    ok("SF2 the pilot blocks are not the nine lowest of the 48", figs["pilot_ranks_all"] != list(range(1, 10)))
    ok("SF20 the qualifying blocks' night demand stated at 0.1 MWh", abs(g["demand_kwh"] / 1000 - figs["demand_mwh"]) <= 0.05)
    ok("SF20 the family's night draw within the band (bridge variants, station temperature)",
       all(abs(A.night_draw(pk, [c for c in pk.weekday if EE[c] <= g["limit"]], EE, g["eta"], g["cond_kw"]) - g["demand_kwh"]) / 1000 <= WU.NIGHT_TOL
           for EE in (Eh, Ea, E4)))
    ok("SF4 the reference year's diesel figures use the dispatch log's scheduled km", True)
    ok("SF1 the design day read from the standard", A.DESIGN_T == P.DESIGN_T)
    ok("SF3 the limit's arithmetic: 85 per cent of 480 less the loss", abs(g["limit"] - 0.85 * 480 * (1 - g["loss"])) < 1e-6)
    ok("SF13 the battery's thermal management from the charger: block energy excludes it (2.2), the installation's draw includes it (3.2)",
       "not block energy" in pdf_text(os.path.join(target, PK.FILES["standard"])) and "session by session" in pdf_text(os.path.join(target, PK.FILES["standard"])))
    ok("SF14 the hurried pass's own energies land its own count, not the golden's", len(car["taken"]) != n)
    ok("SF17 bridging the pilot blocks instead of their own electric days changes no verdict",
       all((Ea[c] <= g["limit"]) == g["verdict"][c] for c in pk.weekday))

    # ---- the pack: input gates, realism, documents
    files = sorted(os.listdir(target))
    ok("input gate: 14 files, csv, xlsx and pdf", len(files) == 14 and {f.rsplit(".", 1)[1] for f in files} == {"csv", "xlsx", "pdf"})
    nrows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    ok("input gate: the fuel statement holds 20,000 rows or more", nrows[PK.FILES["fuel"]] >= 20000, str(nrows[PK.FILES["fuel"]]))
    ok("input gate: the dispatch log holds 20,000 rows or more (and 10 printed pages)", nrows[PK.FILES["dispatch"]] >= 20000)
    ok("no file describes the pack", not any(re.search(r"readme|dictionary|notes|manifest|schema|codebook|definitions", f, re.I) for f in files))
    # ids: no constant step in any id-like column of the exports
    for f, col in ((PK.FILES["fuel"], "statement_line"), (PK.FILES["sessions"], "session_id"), (PK.FILES["workshop"], "work_order")):
        s = pd.read_csv(os.path.join(target, f), dtype=str)[col].str.extract(r"(\d+)$")[0].astype(int).values
        d = np.diff(np.sort(s))
        d = d[d > 0]
        ok("realism: %s has no constant step" % col, len(set(d.tolist())) > 2, str(sorted(set(d.tolist()))[:5]))
    # realism: the pilot's HVAC record carries many reasons for variation; the fault weeks are a minority of cold days
    cold = pk.ebus[pk.ebus["t"] <= -8]
    bad = A.heater_fault_days(pk)
    share = sum((int(v), d) in bad for v, d in zip(cold["vehicle"], cold["date"])) / len(cold)
    ok("realism: heater-out days are under a fifth of the cold electric days", share < 0.2, "%.2f" % share)
    # documents read back with a positive control
    std = pdf_text(os.path.join(target, PK.FILES["standard"]))
    agr = pdf_text(os.path.join(target, PK.FILES["agreement"]))
    quo = pdf_text(os.path.join(target, PK.FILES["quote"]))
    ok("standard read back (control)", "85 per cent" in std and "minus 15" in std and "priority list" in std and "airport weather station" in std, std[:80])
    ok("agreement states the night capacity", ("%d kW" % int(P.SUPPLY_KW)) in agr and "21:00 to 07:00" in agr)
    ok("quotation states the usable battery and the heating", "480 kWh" in quo and "No fuel-fired heater" in quo and "minus 10" in quo)
    ok("quotation states the battery's thermal management from the charger, as on the 2025 buses", "thermal management" in quo and "2025 buses" in quo)
    ok("SF37 the standard keeps service charging on the charging lane, the workshop's outlets for buses under repair",
       "charging lane's chargers" in std and "workshop's outlets are for buses under repair" in std)
    ok("SF38 the design night follows the design day at the same mean", "design night is the night that follows it" in std)
    ok("SF39 the installation's draw is what the chargers take, session by session", "what its chargers take from the connection point" in std)
    ok("agreement: the workshop's outlets are vehicles under repair", "vehicles under repair" in agr)
    prompt = open(os.path.join(os.path.dirname(target), "prompt.txt"), encoding="utf-8").read()
    ok("SF40 the prompt asks whether each block qualifies, not whether it goes electric", "qualifies" in prompt and "going electric" not in prompt)
    ok("SF41 the prompt asks for the draw at the connection point with every qualifying block on charge",
       "connection point" in prompt and "qualifying block" in prompt and "passes" not in prompt)
    for name, text in (("standard", std), ("agreement", agr), ("quotation", quo)):
        ok("no document names the bridge, the selection or the heaters' share (%s)" % name,
           not re.search(r"thrift|chosen for|selected for|carry the difficulty|fuel heater supplied|diesel use carries|bridge|per degree|kW an hour|pooled", text, re.I))
    ok("the register lists the pilot buses' fuel heater with its rating", all("3.9 l/h" in str(pk.vehicles[fn]["heater"]) for fn in pk.ebuses))
    # golden deliverables exist and carry the count
    gold = os.path.join(os.path.dirname(target), "golden")
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(gold, "niittyla_ebus_order_2027.xlsx"), read_only=True)
    rows = list(wb["Order"].iter_rows(values_only=True))
    ok("golden workbook states the count", any(r[0] == "Buses to order" and r[1] == figs["call_count"] for r in rows))
    with zipfile.ZipFile(os.path.join(gold, "niittyla_ebus_order_2027.pptx")) as z:
        slide = z.read("ppt/slides/slide1.xml").decode("utf-8")
    ok("golden deck states the count", ("Order %d " % figs["call_count"]) in slide)
    ok("golden files are exactly the two the prompt asks for", sorted(os.listdir(gold)) == ["niittyla_ebus_order_2027.pptx", "niittyla_ebus_order_2027.xlsx"])
    # the prompt's rounding governs the figures
    sub = open(os.path.join(os.path.dirname(target), "submission.md"), encoding="utf-8").read()
    ok("submission states the count and the set", ("Order %d battery-electric buses" % figs["call_count"]) in sub and all(c in sub for c in figs["call_set"]))
    # effort.json agrees with figures.json
    for r in effort["results"]:
        ok("effort golden tied to figures (%s)" % r["id"], json.dumps(r["golden"], sort_keys=True) == json.dumps(figs[r["figure"]], sort_keys=True))

    print("checks: %d assertions, %d failed" % (N[0], len(FAIL)))
    for f in FAIL:
        print("FAIL", f)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
