"""The independent verifier: reads only the shipped bundle (target/ and the goldens), on its own code path (different
interval construction, normal equations, a square-root age form, the least-slack schedule, pypdf for the documents),
and recomputes every graded figure against figures.json. Exit 1 on any disagreement."""
import datetime as dt
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
FAIL = []


def ok(name, cond, detail=""):
    if not cond:
        FAIL.append("%s %s" % (name, detail))


def mins(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def text(path):
    return re.sub(r"\s+", " ", "\n".join((p.extract_text() or "") for p in PdfReader(path).pages))


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    task = os.path.dirname(target)
    # ---- the documents' filed figures
    std = text(os.path.join(target, "depot_electrification_standard_DES-1.pdf"))
    agr = text(os.path.join(target, "charging_connection_agreement_2025.pdf"))
    quo = text(os.path.join(target, "ebus_quotation_2027.pdf"))
    share = int(re.search(r"no more than\s+(\d+) per cent", std).group(1)) / 100.0
    design_t = -float(re.search(r"minus (\d+) degrees", std).group(1))
    supply = float(re.search(r"(\d{3}) kW from 21:00 to 07:00", agr).group(1))
    usable = float(re.search(r"usable capacity (\d+) kWh", quo).group(1))
    charger = float(re.search(r"up to (\d+) kW to a bus", std).group(1))
    ok("standard: 85 per cent", share == 0.85)
    ok("standard: minus 15", design_t == -15.0)
    ok("agreement: the night capacity equals the build's", supply == figs["supply_kw"])
    ok("quotation: 480 kWh usable", usable == 480.0)
    # ---- registers
    wb = load_workbook(os.path.join(target, "block_register_2026.xlsx"), read_only=True)
    blocks, old2new = {}, {}
    for r in list(wb["Blocks"].iter_rows(values_only=True))[1:]:
        if not r or r[0] is None:
            continue
        ret = mins(r[8])
        if ret <= mins(r[7]):
            ret += 1440
        blocks[r[0]] = {"dtype": r[2], "km": float(r[5]), "dep": mins(r[7]), "ret": ret, "hours": float(r[9]), "climb": float(r[10])}
        old2new[str(r[1])] = r[0]
    weekday = sorted(c for c, b in blocks.items() if b["dtype"] == "Mon-Fri")
    wb = load_workbook(os.path.join(target, "fleet_plan_2027.xlsx"), read_only=True)
    prio = {r[1]: int(r[0]) for r in list(wb["Weekday blocks 2027"].iter_rows(values_only=True))[1:] if r and r[1]}
    wb = load_workbook(os.path.join(target, "vehicle_register_2026.xlsx"), read_only=True)
    veh, reg2fn, cards = {}, {}, []
    for r in list(wb["Vehicles"].iter_rows(values_only=True))[1:]:
        if r and r[0] is not None:
            veh[int(r[0])] = {"drive": r[3], "since": r[10].date() if hasattr(r[10], "date") else r[10], "heater": r[9]}
            reg2fn[r[1]] = int(r[0])
    for r in list(wb["Fuel cards"].iter_rows(values_only=True))[1:]:
        if r and r[0] is not None:
            cards.append((r[0], int(r[1]) if r[1] is not None else None, r[2].date() if hasattr(r[2], "date") else r[2],
                          r[3].date() if hasattr(r[3], "date") else r[3]))
    rating = re.search(r"(\d+) kW fuel-fired \(HVO, ([\d.]+) l/h", veh[1201]["heater"])
    kwh_per_l = float(rating.group(1)) / float(rating.group(2))
    # ---- the dispatch log and the fuel statement: tank to tank, mapped by the fill's timestamp
    dl = pd.read_csv(os.path.join(target, "depot_dispatch_log_2024-01_2026-10.csv"), dtype={"block": str, "vehicle": str})
    dl["date"] = pd.to_datetime(dl["operating_date"]).dt.date
    dl["code"] = [old2new.get(c, c) for c in dl["block"]]
    dl["fn"] = [int(v) if v.isdigit() else reg2fn.get(v) for v in dl["vehicle"]]
    dl["dep_dt"] = [pd.Timestamp(d) + pd.Timedelta(minutes=mins(t)) for d, t in zip(dl["date"], dl["depot_departure"])]
    fu = pd.read_csv(os.path.join(target, "fuel_card_transactions_2024-01_2026-10.csv"), dtype={"card_no": str, "vehicle_entered": str})
    fu["time"] = pd.to_datetime(fu["transaction_time"])
    fu["date"] = fu["time"].dt.date
    bycard = {}
    for c in cards:
        bycard.setdefault(c[0], []).append(c)
    fn_col = []
    for card, d, ent in zip(fu["card_no"], fu["date"], fu["vehicle_entered"].fillna("")):
        f = None
        for _, vfn, a, b in bycard.get(card, []):
            if vfn is not None and a <= d and (b is None or d <= b):
                f = vfn
        if f is None and ent.strip().isdigit() and int(ent) in veh:
            f = int(ent)
        fn_col.append(f)
    fu["fn"] = fn_col
    up = fu["product"].str.upper()
    fu["kind"] = np.where(up.str.contains("HVO"), "hvo", np.where(up.str.contains("DIESEL"), "diesel", "adblue"))
    ref0, ref1 = dt.date(2025, 11, 1), dt.date(2026, 10, 31)
    rows_A, rows_y, codes = [], [], {}
    for fn, g in fu[(fu["kind"] == "diesel") & fu["fn"].notna()].groupby("fn"):
        fn = int(fn)
        if veh[fn]["drive"] != "diesel":
            continue
        g = g.sort_values("time")
        fills = []
        for t, l in zip(g["time"], g["litres"]):
            if fills and (t - fills[-1][0]) <= pd.Timedelta(minutes=10):
                fills[-1][1] += l
            else:
                fills.append([t, l])
        days = dl[dl["fn"] == fn].sort_values("dep_dt")
        for (t0, _), (t1, l) in zip(fills[:-1], fills[1:]):
            sub = days[(days["dep_dt"] > t0) & (days["dep_dt"] <= t1)]
            if len(sub) == 0 or not (ref0 <= t1.date() <= ref1) or sub["date"].min() < ref0:
                continue
            kms = sub.groupby("code")["planned_km"].sum().to_dict()
            for c in kms:
                codes.setdefault(c, len(codes))
            rows_A.append(kms)
            rows_y.append(l)
    A = np.zeros((len(rows_A), len(codes)))
    for i, kms in enumerate(rows_A):
        for c, k in kms.items():
            A[i, codes[c]] = k / 100.0
    y = np.array(rows_y)
    beta = np.linalg.solve(A.T @ A, A.T @ y)
    rates = {c: float(beta[i]) for c, i in codes.items()}
    dmax = max(abs(rates[c] - figs["diesel"][c]) for c in weekday)
    ok("R1: every weekday block's diesel figure within 0.7 of the golden", dmax <= 0.7, "%.2f" % dmax)
    # ---- the pilot: energy per km outside HVAC by block, HVAC per hour by temperature, the heater fuel
    eb = pd.read_csv(os.path.join(target, "ebus_telematics_daily_2025-03_2026-10.csv")).drop_duplicates()
    eb["date"] = pd.to_datetime(eb["date"]).dt.date
    wx = pd.read_csv(os.path.join(target, "weather_vehkasalo_daily_2016_2026.csv"))
    wx["date"] = pd.to_datetime(wx["date"]).dt.date
    both = wx.dropna(subset=["t_mean_airport_c", "t_mean_keskusta_c"])
    off = float((both["t_mean_keskusta_c"] - both["t_mean_airport_c"]).mean())
    st = dict(zip(wx["date"], wx["t_mean_airport_c"].where(wx["t_mean_airport_c"].notna(), wx["t_mean_keskusta_c"] - off)))
    amb = eb["ambient_mean_c"].astype(float).values
    s_ = np.array([st.get(d, np.nan) for d in eb["date"]])
    offb = float(np.nanmean(amb - s_))
    eb["t"] = np.where(np.isnan(amb), s_ + offb, amb)
    eb["hours"] = eb["moving_h"] + eb["idle_h"]
    key = {(int(r.fn), r.date): r.code for r in dl.itertuples()}
    eb["code"] = [key.get((int(v), d)) for v, d in zip(eb["vehicle"], eb["date"])]
    eb = eb.dropna(subset=["code"])
    ws = pd.read_csv(os.path.join(target, "workshop_orders_2024-01_2026-10.csv"))
    bad = set()
    hv_txt = ws["description"].str.lower()
    for _, f in ws[hv_txt.str.contains("heater") & hv_txt.str.contains("f12")].iterrows():
        rep = ws[(ws["vehicle"] == f["vehicle"]) & hv_txt.str.contains("heater") & hv_txt.str.contains("repaired") & (pd.to_datetime(ws["opened"]) > pd.to_datetime(f["opened"]))]
        a, b = pd.to_datetime(f["opened"]).date(), pd.to_datetime(rep.iloc[0]["opened"]).date()
        d = a
        while d < b:
            bad.add((int(f["vehicle"]), d))
            d += dt.timedelta(days=1)
    keep = np.array([(int(v), d) not in bad for v, d in zip(eb["vehicle"], eb["date"])])
    e_block = ((eb["energy_used_kwh"] - eb["hvac_kwh"]).groupby(eb["code"]).sum() / eb["distance_km"].groupby(eb["code"]).sum()).to_dict()
    days = eb["code"].value_counts().to_dict()
    ebh = eb[keep]
    near = ebh[np.abs(ebh["t"] - design_t) <= 2.0]
    h_pilot = float((near["hvac_kwh"] / near["hours"]).mean())
    # heater fuel: HVO fills tank to tank on the electric buses
    hv = fu[(fu["kind"] == "hvo") & fu["fn"].notna()]
    iv = []
    for fn, g in hv.groupby("fn"):
        fn = int(fn)
        if veh[fn]["drive"] != "electric":
            continue
        g = g.sort_values("time")
        fl = list(zip(g["time"], g["litres"]))
        dd = eb[eb["vehicle"] == fn]
        for (t0, _), (t1, l) in zip(fl[:-1], fl[1:]):
            sub = dd[(dd["date"] > t0.date()) & (dd["date"] <= t1.date())]
            if len(sub):
                hrs = np.array([0.0 if (fn, d) in bad else h for h, d in zip(sub["hours"], sub["date"])])
                iv.append((l, hrs, sub["t"].values))
    best = None
    for T0 in np.arange(-12, 2.01, 0.5):
        x = np.array([float(np.sum(h * np.maximum(0, T0 - t))) for _, h, t in iv])
        yv = np.array([l for l, _, _ in iv])
        k = float(x @ yv / (x @ x))
        sse = float(np.sum((yv - k * x) ** 2))
        if best is None or sse < best[0]:
            best = (sse, k, T0)
    lph = best[1] * max(0.0, best[2] - design_t)
    heater_kw = lph * kwh_per_l
    ok("R3: the heaters' heat within 0.3 kW of the golden", abs(heater_kw - figs["heater_kw"]) <= 0.3, "%.2f vs %.2f" % (heater_kw, figs["heater_kw"]))
    heat_new = h_pilot + heater_kw
    # the bridge by weighted polyfit over the blocks an electric bus ran
    xs = np.array([rates[c] for c in e_block if c in rates])
    ys = np.array([e_block[c] for c in e_block if c in rates])
    wts = np.array([days[c] for c in e_block if c in rates], float)
    b1, b0 = np.polyfit(xs, ys, 1, w=np.sqrt(wts))
    E = {}
    for c in weekday:
        e = e_block[c] if days.get(c, 0) >= 30 else b0 + b1 * rates[c]
        E[c] = blocks[c]["km"] * e + blocks[c]["hours"] * heat_new
    emax = max(abs(E[c] - figs["energy"][c]) for c in weekday)
    ok("R4: every design-day energy within 10 kWh of the golden", emax <= 10, "%.1f" % emax)
    # the loss: a square-root age form with a cold term and bus levels
    d = (eb["soc_start_pct"] - eb["soc_end_pct"]).values.astype(float)
    m = d >= 30
    cap = eb["energy_used_kwh"].values[m] / (d[m] / 100.0)
    age = np.array([(dd - veh[int(v)]["since"]).days for v, dd in zip(eb["vehicle"], eb["date"])])[m] / 365.25
    cold = np.maximum(0, 10 - eb["t"].values[m])
    bus = eb["vehicle"].values[m]
    B = np.column_stack([(bus == b).astype(float) for b in sorted(set(bus))])
    X = np.column_stack([B, np.sqrt(age), cold])
    bb, *_ = np.linalg.lstsq(X, cap, rcond=None)
    loss = -bb[B.shape[1]] / np.mean(bb[:B.shape[1]])
    ok("R5: a square-root age form lands inside the loss band", figs["conventions"]["loss_band"][0] <= 100 * loss <= figs["conventions"]["loss_band"][1], "%.2f" % (100 * loss))
    lim = share * usable * (1 - figs["loss_pct"] / 100.0)
    ok("limit within 1 kWh", abs(lim - figs["limit_kwh"]) <= 1.0)
    verdict = {c: "yes" if E[c] <= lim else "no" for c in weekday}
    ok("R6: every verdict agrees", verdict == figs["verdict"], str([c for c in weekday if verdict[c] != figs["verdict"][c]]))
    # the charging split from the sessions, on its own clock rule (EU summer time) and a whole-degree knot grid
    se = pd.read_csv(os.path.join(target, "depot_charging_sessions_2025-03_2026-10.csv"))

    def last_sun(y, mth):
        x = dt.datetime(y, mth, 31, 1, 0)
        while x.weekday() != 6:
            x -= dt.timedelta(days=1)
        return x

    def local(u):
        u = pd.Timestamp(u).tz_localize(None).to_pydatetime() if pd.Timestamp(u).tzinfo else pd.Timestamp(u).to_pydatetime()
        return u + dt.timedelta(hours=3 if last_sun(u.year, 3) <= u < last_sun(u.year, 10) else 2)

    pin = [local(pd.Timestamp(x.replace("Z", ""))) for x in se["plug_in_utc"]]
    pout = [local(pd.Timestamp(x.replace("Z", ""))) for x in se["plug_out_utc"]]
    day = {(int(r.vehicle), r.date): (r.energy_used_kwh, r.soc_start_pct - r.soc_end_pct) for r in eb.itertuples()}
    G, H, T, Y = [], [], [], []
    for v, a_, z_, si, so, kwh in zip(se["vehicle"], pin, pout, se["soc_in_pct"], se["soc_out_pct"], se["energy_kwh"]):
        ev = (a_ - dt.timedelta(hours=12)).date()
        r = day.get((int(v), ev))
        t1, t2 = st.get(ev), st.get(ev + dt.timedelta(days=1))
        if not r or r[1] < 30 or so - si < 30 or t1 is None or t2 is None or np.isnan(t1) or np.isnan(t2):
            continue
        n0 = dt.datetime(ev.year, ev.month, ev.day, 21, 0)
        n1 = n0 + dt.timedelta(hours=10)
        H.append(max(0.0, (min(z_, n1) - max(a_, n0)).total_seconds() / 3600.0))
        G.append((so - si) / 100.0 * r[0] / (r[1] / 100.0))
        T.append(0.5 * (t1 + t2))
        Y.append(kwh)
    G, H, T, Y = map(np.array, (G, H, T, Y))
    best = None
    for T0 in range(-3, 11):
        X = np.column_stack([G, H, H * np.maximum(0, T0 - T)])
        bb2 = np.linalg.solve(X.T @ X, X.T @ Y)
        sse = float(np.sum((Y - X @ bb2) ** 2))
        if best is None or sse < best[0]:
            best = (sse, bb2, T0)
    _, bb2, T0 = best
    eta = 1.0 / bb2[0]
    cond = bb2[1] + bb2[2] * max(0, T0 - design_t)
    ok("eta within 0.005", abs(eta - figs["eta"]) <= 0.005, "%.4f" % eta)
    cb = figs["conventions"]["cond_band"]
    ok("R7: the conditioning at the design night inside the band", cb[0] <= cond <= cb[1], "%.2f" % cond)
    pooled = float(np.sum(G) / np.sum(Y))
    ok("the pooled ratio as stated", abs(pooled - figs["ratio_pooled"]) <= 0.005, "%.4f" % pooled)
    # the night by the least-slack schedule, each bus's steady draw held over its window
    q = [c for c in sorted(weekday, key=lambda c: prio[c]) if E[c] <= lim]

    def win(x):
        return max(blocks[x]["ret"], 21 * 60), min(blocks[x]["dep"] + 1440, 7 * 60 + 1440)

    taken = []
    for c in q:
        jobs = [(x, E[x] / eta, *win(x)) for x in taken + [c]]
        rem = {x: e for x, e, _, _ in jobs}
        mnt = min(j[2] for j in jobs)
        end = max(j[3] for j in jobs)
        while mnt < end:
            here = [j for j in jobs if j[2] <= mnt and mnt + 5 <= j[3]]
            avail = (supply - cond * len(here)) * 5 / 60.0
            live = sorted([j for j in here if rem[j[0]] > 1e-9], key=lambda j: (j[3] - mnt) - rem[j[0]] / (charger - cond) * 60.0)
            for x, e, a2, b2 in live:
                take = min(rem[x], (charger - cond) * 5 / 60.0, avail)
                rem[x] -= take
                avail -= take
                if avail <= 1e-9:
                    break
            mnt += 5
        if sum(rem.values()) > 1.0:
            break
        taken.append(c)
    ok("R9: the order by the least-slack schedule equals the golden", sorted(taken) == figs["call_set"], str(sorted(taken)))
    draw = lambda codes: sum(E[x] / eta + cond * (win(x)[1] - win(x)[0]) / 60.0 for x in codes)
    ok("the night's draw for the order within 0.2 MWh", abs(draw(taken) / 1000 - figs["night_mwh"]) <= 0.2)
    ok("R8: the draw with every qualifying block on charge within 0.2 MWh", abs(draw(q) / 1000 - figs["demand_mwh"]) <= 0.2,
       "%.2f vs %.2f" % (draw(q) / 1000, figs["demand_mwh"]))
    # the goldens
    gold = os.path.join(task, "golden")
    wb = load_workbook(os.path.join(gold, "niittyla_ebus_order_2027.xlsx"), read_only=True)
    rows = {r[0]: r[1] for r in wb["Order"].iter_rows(values_only=True) if r and r[0]}
    ok("golden workbook: the count", rows.get("Buses to order") == figs["call_count"])
    ok("golden workbook: the night draw", rows.get("Design night: draw at the connection point for the buses ordered, MWh") == figs["night_mwh"])
    ok("golden workbook: the conditioning", rows.get("Conditioning draw on charge at -15 C, kW per bus") == figs["cond_kw"])
    with zipfile.ZipFile(os.path.join(gold, "niittyla_ebus_order_2027.pptx")) as z:
        names = z.namelist()
        s1 = z.read("ppt/slides/slide1.xml").decode("utf-8")
    ok("golden deck: three slides with the count on the first", sum(1 for n_ in names if re.match(r"ppt/slides/slide\d+\.xml$", n_)) == 3 and ("Order %d " % figs["call_count"]) in s1)
    print("verify: %s" % ("PASS" if not FAIL else "FAIL"))
    for f in FAIL:
        print("FAIL", f)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
