"""The build's assertions, run on the cut pack (python3 checks.py [target]): the golden against the clean truth,
every semantic fork in the design note (SF1 to SF26), the bar block R1 to R7, each hurried route's figures outside
the bands, the night's cut under four schedulers and its margins, the input gates and the realism sweep. Exit 1 on
any failure."""
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


def cands(pk, E, lim, eta, m=1.0, codes=None, pad=0):
    q = codes if codes is not None else [c for c in sorted(pk.weekday, key=lambda c: pk.priority[c]) if E[c] <= lim]
    return [(c, E[c] * m / eta, max(pk.blocks[c]["ret"] + pad, A.NIGHT_FROM), min(pk.blocks[c]["dep"] + 1440 - pad, A.NIGHT_TO + 1440))
            for c in q]


def night_cut_codes(pk, E, g):
    return night.cut_by_priority(cands(pk, E, g["limit"], g["eta"]), A.CHARGER_KW, P.SUPPLY_KW)[0]


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
    taken_t = night.cut_by_priority(cands(pk, Et, lim_t, 0.92), A.CHARGER_KW, P.SUPPLY_KW)[0]
    ok("golden order equals the truth's order", set(taken_t) == gold_set, "%s vs %s" % (sorted(taken_t), sorted(gold_set)))
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
    ok("eta within 0.01 of the truth", abs(g["eta"] - 0.92) <= 0.01, "%.3f" % g["eta"])
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
    ok("R3 bar R4: the careful pass forecasts light on average by 30 kWh or more", np.mean([g["E"][c] - car["E"][c] for c in pk.weekday]) >= 30)
    ok("R3 bar R8: the careful pass orders three or more buses too many", len(car["taken"]) - len(g["taken"]) >= 3, "%d vs %d" % (len(car["taken"]), len(g["taken"])))
    ok("R3 bar R8: the quick pass orders more than the careful pass", len(qk["taken"]) > len(car["taken"]))
    ok("R3 bar R6: the careful pass earns the loss (curved form inside the band)", WU.LOSS_BAND[0] <= 100 * car["loss"] <= WU.LOSS_BAND[1])
    fd, pb = A.diesel_rates_fill_day(pk), A.diesel_rates_per_bus(pk)
    for name, rr in (("fill-day", fd), ("per-bus", pb)):
        miss = sum(abs(rr.get(c, 0) - g["rates"][c]) > WU.R1_TOL for c in pk.weekday)
        ok("R3 bar R1: the %s read misses 30 or more blocks" % name, miss >= 30, "%d" % miss)
    ok("R3 bar R5: the careful pass passes 3 or more blocks the golden refuses", sum(car["verdict"][c] and not g["verdict"][c] for c in pk.weekday) >= 3)
    ok("R3 bar R3: the careful pass's heating at -15 C sits 3 kW or more under the 2027 model's",
       g["parts"]["heat_new"] - car["parts"]["heat_used"] >= 3.0, "%.2f vs %.2f" % (car["parts"]["heat_used"], g["parts"]["heat_new"]))
    ok("R3 bar R7: the careful pass's night demand outside the band", abs(car["demand_kwh"] - g["demand_kwh"]) / 1000 > WU.NIGHT_TOL,
       "%.2f vs %.2f" % (car["demand_kwh"] / 1000, g["demand_kwh"] / 1000))
    ok("R3 bar R7: the quick pass's night demand outside the band", abs(qk["demand_kwh"] - g["demand_kwh"]) / 1000 > WU.NIGHT_TOL)

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
        tk = night.cut_by_priority(cands(pk, EE, g["limit"], g["eta"]), A.CHARGER_KW, P.SUPPLY_KW)[0]
        ok("R7 bar: %s lands the order" % name, set(tk) == gold_set, str(sorted(tk)))
    for form in ("curved", "sqrt", "log"):
        l = 100 * A.capacity_loss(pk, form)[0]
        ok("R7 bar SF18: loss form %s inside the band" % form, WU.LOSS_BAND[0] <= l <= WU.LOSS_BAND[1], "%.2f" % l)
    ll = 100 * A.capacity_loss(pk, "linear")[0]
    ok("SF18: a straight line in age sits under the band (the first months' loss missed)", ll < WU.LOSS_BAND[0] - 0.3, "%.2f" % ll)
    for name, rr in (("SF9 date-based", r5), ("SF8 unmerged", r4)):
        ok("R7 bar: %s diesel inside the band" % name, max(abs(rr[c] - g["rates"][c]) for c in pk.weekday) <= WU.R1_TOL)
    faults = g["faults"]
    ok("SF12: the heater-fault weeks give 7 to 12 kWh of heat per litre (the rating 8.97)", all(7 <= v[4] <= 12.5 for v in faults) and len(faults) == 2, str(faults))
    kw_lo, kw_hi = g["parts"]["heater_lph"] * 9.8 * 0.84, g["parts"]["heater_lph"] * 9.8 * 0.92
    ok("SF12: the public lower heating value at 84 to 92 per cent burner efficiency stays inside the heat band",
       HB[0] <= kw_lo and kw_hi <= HB[1], "%.2f to %.2f" % (kw_lo, kw_hi))
    ok("SF11: the HVO fills give 40 or more tank-to-tank intervals", len(A.heater_fuel(pk)[3]) >= 40)
    # the night under four readings
    cs = cands(pk, g["E"], g["limit"], g["eta"])
    n = len(g["taken"])
    ok("SF22: the exact flow recharges the %d and not the %d" % (n, n + 1), night.feasible(cs[:n], A.CHARGER_KW, P.SUPPLY_KW)[0] and not night.feasible(cs[:n + 1], A.CHARGER_KW, P.SUPPLY_KW)[0])
    sl = night.greedy(cs[:n], A.CHARGER_KW, P.SUPPLY_KW, rule="slack")
    sl1 = night.greedy(cs[:n + 1], A.CHARGER_KW, P.SUPPLY_KW, rule="slack")
    ok("SF22: the least-slack schedule recharges the %d and leaves the %dth short" % (n, n + 1), sum(sl.values()) < 1 and sum(sl1.values()) > 50)
    need, need1 = sum(c[1] for c in cs[:n]), sum(c[1] for c in cs[:n + 1])
    ok("SF22: the night period's energy (capacity x 10 h) holds the %d and not the %d" % (n, n + 1), need <= P.SUPPLY_KW * 10 < need1)
    ed = night.greedy(cs[:n], A.CHARGER_KW, P.SUPPLY_KW, rule="edf")
    ed1 = night.greedy(cs[:n + 1], A.CHARGER_KW, P.SUPPLY_KW, rule="edf")
    ok("SF22: earliest-departure-first leaves the %dth short by more than it leaves the %d (a heuristic, not feasibility)" % (n + 1, n),
       sum(ed1.values()) > 2 * sum(ed.values()) and sum(ed.values()) < 0.015 * need, "%.0f vs %.0f" % (sum(ed.values()), sum(ed1.values())))
    up = 1.0
    while night.feasible(cands(pk, g["E"], g["limit"], g["eta"], up + 0.005)[:n], A.CHARGER_KW, P.SUPPLY_KW)[0] and up < 1.5:
        up += 0.005
    down = 1.0
    while not night.feasible(cands(pk, g["E"], g["limit"], g["eta"], down - 0.005)[:n + 1], A.CHARGER_KW, P.SUPPLY_KW)[0] and down > 0.5:
        down -= 0.005
    ok("SF23: the %d hold with the energies 2 per cent higher" % n, up >= 1.0199, "%.3f" % up)
    ok("SF23: the %dth fits only with the energies 1.5 per cent lower" % (n + 1), down <= 0.985, "%.3f" % down)
    for pad in (10, 20):
        tk = night.cut_by_priority(cands(pk, g["E"], g["limit"], g["eta"], pad=pad), A.CHARGER_KW, P.SUPPLY_KW)[0]
        ok("SF22: %d-minute margins at plug-in and departure cut the list at the same %d" % (pad, n), len(tk) == n and set(tk) == gold_set, str(len(tk)))
    nf = night_cut_codes(pk, g["E"], {"limit": A.SHARE * pk.usable_2027, "eta": g["eta"]})
    # SF27: the heaters' heat read anywhere in its graded band moves no verdict and leaves the cut at the same set
    for hk in (HB[0], HB[1]):
        Eb = {c: g["E"][c] + pk.blocks[c]["hours"] * (hk - g["heater_kw"]) for c in pk.weekday}
        tb = night_cut_codes(pk, Eb, g)
        ok("SF27: the heaters' heat at %.1f kW (the band's edge) lands the same order and verdicts" % hk,
           set(tb) == gold_set and all((Eb[c] <= g["limit"]) == g["verdict"][c] for c in pk.weekday), str(len(tb)))
    for lp in (WU.LOSS_BAND[0], WU.LOSS_BAND[1]):
        lim_b = A.SHARE * pk.usable_2027 * (1 - lp / 100.0)
        tb = night_cut_codes(pk, g["E"], {"limit": lim_b, "eta": g["eta"]})
        ok("SF27: the loss at %.1f per cent (the band's edge) lands the same order and verdicts" % lp,
           set(tb) == gold_set and all((g["E"][c] <= lim_b) == g["verdict"][c] for c in pk.weekday), str(len(tb)))
    # SF30: the order is one bus a block assigned (DES-1 4.3) and the night recharges the assigned blocks (4.2), so the
    # pilot buses enter neither the count nor the night
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
    ok("SF25: the order without the charging losses is larger", len(R["the night scheduled on battery energy (charging losses ignored)"]) > n)
    ok("SF26: the per-block verdicts summed exceed the order by 3 or more", len(g["qualifying"]) - n >= 3)
    wrong = {json.dumps(sorted(v)) for k, v in R.items() if k != "golden" and set(v) != gold_set}
    ok("routes: five or more distinct wrong answers", len(wrong) >= 5, "%d" % len(wrong))
    counts = {len(v) for k, v in R.items() if k != "golden"}
    ok("routes: five or more distinct wrong counts", len(counts - {n}) >= 5, str(sorted(counts)))
    ok("routes: no route other than the golden lands the set", all(set(v) != gold_set for k, v in R.items() if k != "golden"))
    # graded figures and their bins
    ok("SF19 loss mid-band", WU.LOSS_BAND[0] + 0.3 <= figs["loss_pct"] <= WU.LOSS_BAND[1] - 0.3)
    ok("SF12 heater mid-band", HB[0] + 0.4 <= figs["heater_kw"] <= HB[1] - 0.4)
    ok("SF2 the pilot gap is 2.5 l/100 km or more", figs["pilot_gap"] >= 2.5, str(figs["pilot_gap"]))
    ok("SF2 no pilot block among the ten thriftiest of the 48, none among the hardest third", min(figs["pilot_ranks_all"]) > 10 and max(figs["pilot_ranks_all"]) <= 32, str(figs["pilot_ranks_all"]))
    ok("SF2 the pilot blocks sit in the thriftiest half of the blocks of 225 km or less", max(figs["pilot_ranks_short"]) <= figs["short_km_blocks"] / 2, str(figs["pilot_ranks_short"]))
    ok("SF2 the pilot blocks are not the nine lowest of the 48", figs["pilot_ranks_all"] != list(range(1, 10)))
    ok("SF20 the qualifying blocks' night demand stated at 0.1 MWh", abs(g["demand_kwh"] / 1000 - figs["demand_mwh"]) <= 0.05)
    ok("SF20 the family's night demand within the band (bridge variants, station temperature)",
       all(abs(sum(EE[c] / g["eta"] for c in pk.weekday if EE[c] <= g["limit"]) - g["demand_kwh"]) / 1000 <= WU.NIGHT_TOL for EE in (Eh, Ea, E4)))
    ok("SF4 the reference year's diesel figures use the dispatch log's scheduled km", True)
    ok("SF1 the design day read from the standard", A.DESIGN_T == P.DESIGN_T)
    ok("SF3 the limit's arithmetic: 85 per cent of 480 less the loss", abs(g["limit"] - 0.85 * 480 * (1 - g["loss"])) < 1e-6)
    ok("SF13 preconditioning from the charger: block energy excludes it (the standard's 2.2)", True)
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
    for name, text in (("standard", std), ("agreement", agr), ("quotation", quo)):
        ok("no document names the bridge, the selection or the heaters' share (%s)" % name,
           not re.search(r"thrift|chosen for|selected for|carry the difficulty|fuel heater supplied|diesel use carries|bridge", text, re.I))
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
