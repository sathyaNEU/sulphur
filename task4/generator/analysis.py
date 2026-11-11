"""Everything computed from the shipped pack, on the solver's side of the files: the pack loaded and cleaned, each
block's diesel use tank to tank over the dispatch log (R1), the pilot blocks' rank (R2), the pilot's battery energy
model and the heat its fuel heaters supplied (R3), the diesel bridge and the 48 design-day energies (R4), the
verdicts (R5), the first-winter capacity loss (R6), the night under the connection agreement (R7) and the order
(R8); beside the golden, the hurried passes (quick; careful but hurried, the union of the recorded runs) and the
rivals on every result. Nothing here reads the generator's truth."""
import datetime as dt
import math
import os
import re
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import night  # noqa: E402

FILES = {
    "fuel": "fuel_card_transactions_2024-01_2026-10.csv", "dispatch": "depot_dispatch_log_2024-01_2026-10.csv",
    "blocks": "block_register_2026.xlsx", "vehicles": "vehicle_register_2026.xlsx",
    "ebus": "ebus_telematics_daily_2025-03_2026-10.csv", "sessions": "depot_charging_sessions_2025-03_2026-10.csv",
    "weather": "weather_vehkasalo_daily_2016_2026.csv", "workshop": "workshop_orders_2024-01_2026-10.csv",
    "plan": "fleet_plan_2027.xlsx"}
# the standard's and the agreement's filed figures (read back from the PDFs by verify.py; constants here)
SHARE, DESIGN_T, CHARGER_KW = 0.85, -15.0, 150.0
NIGHT_FROM, NIGHT_TO = 21 * 60, 7 * 60
REF = (dt.date(2025, 11, 1), dt.date(2026, 10, 31))
NEW_CODES = dt.date(2025, 8, 11)
HEATER_KWH_PER_L = 35.0 / 3.9          # the register's heater: 35 kW at 3.9 l/h
HP_FLOOR_T = -10.0                      # the quotation: heat pump to -10 C, boosters below


class Pack:
    pass


def _mins(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def load(target, supply_kw=690.0, usable_2027=480.0):
    pk = Pack()
    pk.supply = supply_kw
    pk.usable_2027 = usable_2027
    # blocks
    wb = load_workbook(os.path.join(target, FILES["blocks"]), read_only=True)
    rows = list(wb["Blocks"].iter_rows(values_only=True))[1:]
    pk.blocks = {}
    pk.old2new = {}
    for r in rows:
        if not r or r[0] is None:
            continue
        code, old, dtype, lines, trips, km, km_old, dep, ret, hours, climb, zone = r
        dtp = {"Mon-Fri": "M", "Sat": "L", "Sun/holiday": "S"}[dtype]
        pk.blocks[code] = {"code": code, "old": str(old), "daytype": dtp, "lines": str(lines), "trips": trips, "km": float(km),
                           "km_old": float(km_old), "dep": _mins(dep), "ret": _mins(ret) if _mins(ret) > _mins(dep) else _mins(ret) + 1440,
                           "hours": float(hours), "climb": float(climb), "zone": int(zone)}
        if pk.blocks[code]["ret"] < pk.blocks[code]["dep"]:
            pk.blocks[code]["ret"] += 1440
        pk.old2new[str(old)] = code
    pk.weekday = sorted(c for c, b in pk.blocks.items() if b["daytype"] == "M")
    # the plan's priority
    wb = load_workbook(os.path.join(target, FILES["plan"]), read_only=True)
    pk.priority = {}
    for r in list(wb["Weekday blocks 2027"].iter_rows(values_only=True))[1:]:
        if r and r[1]:
            pk.priority[r[1]] = int(r[0])
    # vehicles and cards
    wb = load_workbook(os.path.join(target, FILES["vehicles"]), read_only=True)
    pk.vehicles = {}
    pk.reg2fn = {}
    for r in list(wb["Vehicles"].iter_rows(values_only=True))[1:]:
        if not r or r[0] is None:
            continue
        fn = int(r[0])
        pk.vehicles[fn] = {"fn": fn, "reg": r[1], "model": r[2], "drive": r[3], "year": r[4], "tank": r[7], "battery": r[8],
                           "heater": r[9], "since": r[10].date() if hasattr(r[10], "date") else r[10],
                           "retired": r[11].date() if hasattr(r[11], "date") else r[11]}
        pk.reg2fn[r[1]] = fn
    pk.cards = []
    for r in list(wb["Fuel cards"].iter_rows(values_only=True))[1:]:
        if not r or r[0] is None:
            continue
        vf = r[2].date() if hasattr(r[2], "date") else r[2]
        vt = r[3].date() if hasattr(r[3], "date") else r[3]
        pk.cards.append({"card": r[0], "fn": int(r[1]) if r[1] is not None else None, "from": vf, "to": vt, "type": r[4]})
    pk.ebuses = sorted(fn for fn, v in pk.vehicles.items() if v["drive"] == "electric")
    # weather: the airport series, its gap filled from the town station less the mean offset
    wx = pd.read_csv(os.path.join(target, FILES["weather"]))
    wx["date"] = pd.to_datetime(wx["date"]).dt.date
    both = wx.dropna(subset=["t_mean_airport_c", "t_mean_keskusta_c"])
    off = float((both["t_mean_keskusta_c"] - both["t_mean_airport_c"]).mean())
    t = wx["t_mean_airport_c"].where(wx["t_mean_airport_c"].notna(), wx["t_mean_keskusta_c"] - off)
    pk.temp = dict(zip(wx["date"], t.astype(float)))
    pk.temp_offset = off
    # dispatch log: codes to the current register, vehicles to fleet numbers
    dl = pd.read_csv(os.path.join(target, FILES["dispatch"]), dtype={"block": str, "vehicle": str})
    dl["date"] = pd.to_datetime(dl["operating_date"]).dt.date
    dl["code"] = [pk.old2new.get(c, c) for c in dl["block"]]
    dl["fn"] = [pk.reg2fn.get(v, None) if not str(v).isdigit() else int(v) for v in dl["vehicle"]]
    dl = dl.dropna(subset=["fn"])
    dl["fn"] = dl["fn"].astype(int)
    dl["dep_min"] = [_mins(x) for x in dl["depot_departure"]]
    dl["dep_dt"] = [dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=int(m)) for d, m in zip(dl["date"], dl["dep_min"])]
    pk.dispatch = dl[["date", "code", "fn", "planned_km", "dep_dt"]].reset_index(drop=True)
    # fuel transactions: card to vehicle by validity, spare cards by the typed fleet number
    fu = pd.read_csv(os.path.join(target, FILES["fuel"]), dtype={"card_no": str, "odometer_km": str, "vehicle_entered": str})
    fu["time"] = pd.to_datetime(fu["transaction_time"])
    fu["date"] = fu["time"].dt.date
    cards_by_no = {}
    for c in pk.cards:
        cards_by_no.setdefault(c["card"], []).append(c)
    fns = []
    for card, d, ent in zip(fu["card_no"], fu["date"], fu["vehicle_entered"].fillna("")):
        fn = None
        for c in cards_by_no.get(card, []):
            if c["fn"] is not None and c["from"] <= d and (c["to"] is None or d <= c["to"]):
                fn = c["fn"]
        if fn is None and ent.strip().isdigit() and int(ent) in pk.vehicles:
            fn = int(ent)
        fns.append(fn)
    fu["fn"] = fns
    prod = fu["product"].str.upper()
    fu["kind"] = np.where(prod.str.contains("HVO"), "hvo", np.where(prod.str.contains("DIESEL"), "diesel", "adblue"))
    pk.fuel = fu
    # telematics: exact duplicates dropped, ambient from the station where the sensor was blank
    eb = pd.read_csv(os.path.join(target, FILES["ebus"]))
    eb = eb.drop_duplicates().reset_index(drop=True)
    eb["date"] = pd.to_datetime(eb["date"]).dt.date
    eb["hours"] = eb["moving_h"] + eb["idle_h"]
    st = np.array([pk.temp.get(d, np.nan) for d in eb["date"]])
    amb = eb["ambient_mean_c"].astype(float).values
    ok = ~np.isnan(amb)
    off_bus = float(np.nanmean(amb[ok] - st[ok]))
    eb["t"] = np.where(ok, amb, st + off_bus)
    eb["t_station"] = st
    pk.ebus_offset = off_bus
    # the block each electric bus-day ran, from the dispatch log
    key = {(r.fn, r.date): r.code for r in pk.dispatch.itertuples()}
    eb["code"] = [key.get((int(v), d)) for v, d in zip(eb["vehicle"], eb["date"])]
    eb = eb.dropna(subset=["code"]).reset_index(drop=True)
    eb["age"] = [(d - pk.vehicles[int(v)]["since"]).days for v, d in zip(eb["vehicle"], eb["date"])]
    pk.ebus = eb
    se = pd.read_csv(os.path.join(target, FILES["sessions"]))
    pk.sessions = se
    pk.workshop = pd.read_csv(os.path.join(target, FILES["workshop"]))
    return pk


# ----------------------------------------------------------------------------------------------- R1: diesel per block
def fuel_intervals(pk, merge_minutes=12, include_street=True, by_timestamp=True, window=REF):
    """tank to tank per diesel bus: consecutive diesel fills, the bus-days between them from the dispatch log.
    Returns a list of (litres, {code: km}) over intervals that start and end inside the window."""
    fu = pk.fuel[(pk.fuel["kind"] == "diesel") & pk.fuel["fn"].notna()].copy()
    fu["fn"] = fu["fn"].astype(int)
    if not include_street:
        fu = fu[fu["station_id"] == 9001]
    out = []
    disp = pk.dispatch
    for fn, g in fu.groupby("fn"):
        if pk.vehicles[fn]["drive"] != "diesel":
            continue
        g = g.sort_values("time")
        fills = []
        for t, lit in zip(g["time"], g["litres"]):
            if fills and (t - fills[-1][0]).total_seconds() <= merge_minutes * 60:
                fills[-1] = (fills[-1][0], fills[-1][1] + lit)
            else:
                fills.append((t, lit))
        days = disp[disp["fn"] == fn].sort_values("dep_dt")
        dts = days["dep_dt"].values
        dates = days["date"].values
        for (t0, _), (t1, lit) in zip(fills[:-1], fills[1:]):
            if by_timestamp:
                m = (dts > np.datetime64(t0)) & (dts <= np.datetime64(t1))
            else:
                d0, d1 = t0.date(), t1.date()
                m = (dates > d0) & (dates <= d1)
            sub = days[m]
            if len(sub) == 0 or t1.date() < window[0] or t1.date() > window[1]:
                continue
            if sub["date"].min() < window[0]:
                continue
            kms = {}
            for c, km in zip(sub["code"], sub["planned_km"]):
                kms[c] = kms.get(c, 0.0) + float(km)
            out.append((float(lit), kms))
    return out


def diesel_rates(pk, intervals=None, bus_effects=False, **kw):
    """litres per 100 scheduled km per block by least squares over the fill intervals (R1)"""
    iv = intervals if intervals is not None else fuel_intervals(pk, **kw)
    codes = sorted({c for _, kms in iv for c in kms})
    idx = {c: i for i, c in enumerate(codes)}
    A = np.zeros((len(iv), len(codes)))
    y = np.zeros(len(iv))
    for i, (lit, kms) in enumerate(iv):
        for c, km in kms.items():
            A[i, idx[c]] = km / 100.0
        y[i] = lit
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    return {c: float(beta[idx[c]]) for c in codes}


def diesel_rates_fill_day(pk, window=REF):
    """the hurried read: each fill's litres charged to the block the bus ran on the day of the fill"""
    fu = pk.fuel[(pk.fuel["kind"] == "diesel") & pk.fuel["fn"].notna()].copy()
    fu["fn"] = fu["fn"].astype(int)
    fu = fu[(fu["date"] >= window[0]) & (fu["date"] <= window[1])]
    key = {(r.fn, r.date): (r.code, r.planned_km) for r in pk.dispatch.itertuples()}
    lit, km = {}, {}
    for fn, d, l in zip(fu["fn"], fu["date"], fu["litres"]):
        if pk.vehicles[fn]["drive"] != "diesel":
            continue
        k = key.get((fn, d)) or key.get((fn, d - dt.timedelta(days=1)))
        if not k:
            continue
        lit[k[0]] = lit.get(k[0], 0.0) + l
    disp = pk.dispatch[(pk.dispatch["date"] >= window[0]) & (pk.dispatch["date"] <= window[1])]
    for c, g in disp.groupby("code"):
        kmv = float(g["planned_km"].sum())
        km[c] = kmv
    return {c: lit.get(c, 0.0) / km[c] * 100.0 for c in km if km[c] > 0}


def diesel_rates_per_bus(pk, window=REF):
    """the other hurried read: a rate per bus over the year, each block given its commonest bus's rate"""
    fu = pk.fuel[(pk.fuel["kind"] == "diesel") & pk.fuel["fn"].notna()].copy()
    fu["fn"] = fu["fn"].astype(int)
    fu = fu[(fu["date"] >= window[0]) & (fu["date"] <= window[1])]
    lit = fu.groupby("fn")["litres"].sum().to_dict()
    disp = pk.dispatch[(pk.dispatch["date"] >= window[0]) & (pk.dispatch["date"] <= window[1])]
    km = disp.groupby("fn")["planned_km"].sum().to_dict()
    rate = {fn: lit.get(fn, 0.0) / km[fn] * 100 for fn in km if km[fn] > 0 and pk.vehicles[fn]["drive"] == "diesel"}
    out = {}
    for c, g in disp.groupby("code"):
        g = g[g["fn"].isin(rate.keys())]
        if len(g) == 0:
            continue
        top = g["fn"].value_counts().index[0]
        out[c] = rate[top]
    return out


# ----------------------------------------------------------------------------------------------- the pilot's model
def heater_fault_days(pk):
    """(vehicle, date) pairs between a fuel heater's logged failure and its logged repair, from the workshop orders"""
    ws = pk.workshop
    faults = ws[ws["description"].str.contains("heater", case=False) & ws["description"].str.contains("not start|does not start|fails", case=False)]
    repairs = ws[ws["description"].str.contains("heater repaired", case=False)]
    out = set()
    for _, f in faults.iterrows():
        fn = int(f["vehicle"])
        a = pd.to_datetime(f["opened"]).date()
        rr = repairs[(repairs["vehicle"] == fn) & (pd.to_datetime(repairs["opened"]).dt.date > a)]
        if len(rr) == 0:
            continue
        b = pd.to_datetime(rr.iloc[0]["opened"]).date()
        d = a
        while d < b:
            out.add((fn, d))
            d += dt.timedelta(days=1)
    return out


def ebus_model(pk, exclude_faults=True):
    """per block, the battery energy per kilometre outside the cabin's heating and cooling (traction and the
    auxiliaries), over the days an electric bus ran it, weighted by kilometres; the HVAC draw per hour by ambient
    temperature in 1-degree bins, the days a fuel heater was logged out left out of the table (the golden) or kept
    (the hurried read). Returns (e_block, days per block, h(T) table)."""
    eb = pk.ebus
    if exclude_faults:
        bad = heater_fault_days(pk)
        keep = np.array([(int(v), d) not in bad for v, d in zip(eb["vehicle"], eb["date"])])
        eb_h = eb[keep]
    else:
        eb_h = eb
    num = (eb["energy_used_kwh"] - eb["hvac_kwh"]).groupby(eb["code"]).sum()
    den = eb["distance_km"].groupby(eb["code"]).sum()
    e = {c: float(num[c] / den[c]) for c in num.index}
    days = eb["code"].value_counts().to_dict()
    tb = np.floor(eb_h["t"].values).astype(int)
    hv = (eb_h["hvac_kwh"] / eb_h["hours"]).values
    table = {}
    for b in range(int(tb.min()), int(tb.max()) + 1):
        m = tb == b
        if m.sum() >= 3:
            table[b] = (float(hv[m].mean()), int(m.sum()))
    return e, days, table


def hvac_at(table, t, width=2):
    """the pilot's HVAC draw per hour at ambient t: the mean of the bins within width degrees"""
    vals, n = [], 0
    for b, (v, k) in table.items():
        if abs(b + 0.5 - t) <= width:
            vals.append(v * k)
            n += k
    return sum(vals) / n if n else float("nan")


def hvac_fit(pk):
    """a smooth form a careful run fits to the pilot's HVAC draw: piecewise linear in temperature with knots, used to
    read the draw at the design day from the pilot's own record (the hurried read of the cold response)"""
    eb = pk.ebus
    t = eb["t"].values
    hv = (eb["hvac_kwh"] / eb["hours"]).values
    knots = [-20, -10, -5, 0, 5, 10, 15, 20, 25]
    X = np.column_stack([np.ones_like(t)] + [np.maximum(0, t - k) for k in knots])
    beta, *_ = np.linalg.lstsq(X, hv, rcond=None)

    def f(tt):
        x = np.array([1.0] + [max(0.0, tt - k) for k in knots])
        return float(x @ beta)
    return f


# ----------------------------------------------------------------------------------------------- R3: the fuel heaters
def heater_fuel(pk):
    """the electric buses' HVO fills tank to tank against the days between, fitted as l/h = k x max(0, T0 - T) with T0
    profiled; returns (k, T0, l/h at the design day, the intervals)"""
    fu = pk.fuel[(pk.fuel["kind"] == "hvo") & pk.fuel["fn"].notna()].copy()
    fu["fn"] = fu["fn"].astype(int)
    fu = fu[[pk.vehicles[f]["drive"] == "electric" for f in fu["fn"]]]
    eb = pk.ebus
    bad = heater_fault_days(pk)          # the days a heater was logged out burnt no fuel
    iv = []
    for fn, g in fu.groupby("fn"):
        g = g.sort_values("time")
        fills = list(zip(g["time"], g["litres"]))
        days = eb[eb["vehicle"] == fn]
        for (t0, _), (t1, lit) in zip(fills[:-1], fills[1:]):
            sub = days[(days["date"] > t0.date()) & (days["date"] <= t1.date())]
            if len(sub) == 0:
                continue
            hrs = np.array([0.0 if (int(fn), d) in bad else h for h, d in zip(sub["hours"], sub["date"])])
            iv.append((float(lit), hrs, sub["t"].values, fn, t0.date(), t1.date()))
    best = None
    for T0 in np.arange(-12.0, 2.01, 0.5):
        x = np.array([float(np.sum(h * np.maximum(0.0, T0 - t))) for _, h, t, *_ in iv])
        y = np.array([l for l, *_ in iv])
        if x.sum() <= 0:
            continue
        k = float(x @ y / (x @ x))
        sse = float(np.sum((y - k * x) ** 2))
        if best is None or sse < best[0]:
            best = (sse, k, T0)
    _, k, T0 = best
    return k, T0, k * max(0.0, T0 - DESIGN_T), iv


def heater_from_faults(pk):
    """the conversion checked on the two buses whose heater was out: the extra HVAC draw per hour on fault days against
    like days, divided by the heater fuel those days would have taken"""
    ws = pk.workshop
    faults = ws[ws["description"].str.contains("heater", case=False) & ws["description"].str.contains("not start|does not start|fails", case=False)]
    repairs = ws[ws["description"].str.contains("heater repaired", case=False)]
    k, T0, _, _ = heater_fuel(pk)
    eb = pk.ebus
    out = []
    for _, f in faults.iterrows():
        fn = int(f["vehicle"])
        a = pd.to_datetime(f["opened"]).date()
        rr = repairs[repairs["vehicle"] == fn]
        rr = rr[pd.to_datetime(rr["opened"]).dt.date > a]
        if len(rr) == 0:
            continue
        b = pd.to_datetime(rr.iloc[0]["opened"]).date()
        on = eb[(eb["vehicle"] == fn) & (eb["date"] >= a) & (eb["date"] < b) & (eb["t"] < T0 - 2)]
        if len(on) < 5:
            continue
        others = eb[(eb["vehicle"] != fn) & (eb["date"] >= a - dt.timedelta(days=45)) & (eb["date"] <= b + dt.timedelta(days=45))]
        excess, fuel = [], []
        for h, t, hv in zip(on["hours"], on["t"], on["hvac_kwh"]):
            ref = others[np.abs(others["t"] - t) <= 1.5]
            if len(ref) < 3:
                continue
            excess.append(hv / h - float((ref["hvac_kwh"] / ref["hours"]).mean()))
            fuel.append(k * max(0.0, T0 - t))
        if fuel and sum(fuel) > 0:
            out.append((fn, a, b, len(excess), float(np.sum(excess) / np.sum(fuel))))
    return out


# ----------------------------------------------------------------------------------------------- R6: the first winter
def capacity_loss(pk, form="curved", min_dsoc=30):
    """the share of usable capacity lost in the first twelve months: each bus-day's energy over its state-of-charge
    drop as the capacity shown, on age with a cold term, per bus levels; the form in age chosen by fit"""
    eb = pk.ebus
    d = (eb["soc_start_pct"] - eb["soc_end_pct"]).values.astype(float)
    m = d >= min_dsoc
    cap = eb["energy_used_kwh"].values[m] / (d[m] / 100.0)
    age = eb["age"].values[m] / 365.25
    t = eb["t"].values[m]
    cold = np.maximum(0.0, 10.0 - t)
    bus = eb["vehicle"].values[m]
    buses = sorted(set(bus))
    B = np.column_stack([(bus == b).astype(float) for b in buses])
    if form == "linear":
        F = np.column_stack([age])
    elif form == "sqrt":
        F = np.column_stack([np.sqrt(age)])
    elif form == "log":
        F = np.column_stack([np.log1p(age * 12)])
    else:
        F = np.column_stack([1 - np.exp(-age * 12 / 4.0), age])
    X = np.column_stack([B, F, cold])
    beta, *_ = np.linalg.lstsq(X, cap, rcond=None)
    nb = len(buses)
    lvl = float(np.mean(beta[:nb]))
    def at(a):
        if form == "linear":
            return a * beta[nb]
        if form == "sqrt":
            return math.sqrt(a) * beta[nb]
        if form == "log":
            return math.log1p(a * 12) * beta[nb]
        return (1 - math.exp(-a * 12 / 4.0)) * beta[nb] + a * beta[nb + 1]
    loss = -(at(1.0) - at(0.0)) / lvl
    resid = cap - X @ beta
    return float(loss), float(np.sqrt(np.mean(resid ** 2))), lvl


def session_frame(pk, min_dsoc=30):
    """the charging sessions on the solver's side: local times (the export is in UTC), the evening each session
    belongs to, the hours it was plugged in while the relay released the chargers (21:00 to 07:00), the night's
    temperature (the evening's and the next morning's daily means at the airport station), and the energy that went
    into the battery (the state-of-charge points times the capacity the bus's own day shows, energy over its drop)"""
    se = pk.sessions.copy()
    for col in ("plug_in_utc", "plug_out_utc"):
        se[col.replace("_utc", "_loc")] = (pd.to_datetime(se[col], utc=True).dt.tz_convert("Europe/Helsinki")
                                           .dt.tz_localize(None))
    se["evening"] = (se["plug_in_loc"] - pd.Timedelta(hours=12)).dt.date
    ev = pd.to_datetime(se["evening"])
    night_from = ev + pd.Timedelta(minutes=NIGHT_FROM)
    night_to = ev + pd.Timedelta(minutes=NIGHT_TO + 1440)
    a = np.maximum(se["plug_in_loc"].values, night_from.values)
    b = np.minimum(se["plug_out_loc"].values, night_to.values)
    se["rel_h"] = np.maximum(0.0, (b - a) / np.timedelta64(1, "m") / 60.0)
    se["plug_h"] = (se["plug_out_loc"] - se["plug_in_loc"]).dt.total_seconds() / 3600.0
    t_ev = np.array([pk.temp.get(d, np.nan) for d in se["evening"]])
    t_mo = np.array([pk.temp.get(d + dt.timedelta(days=1), np.nan) for d in se["evening"]])
    se["t_evening"], se["t_morning"] = t_ev, t_mo
    se["t_night"] = 0.5 * (t_ev + t_mo)
    eb = pk.ebus
    day = {(int(r.vehicle), r.date): r for r in eb.itertuples()}
    gain, sensor = [], []
    for v, d, si, so in zip(se["vehicle"], se["evening"], se["soc_in_pct"], se["soc_out_pct"]):
        r = day.get((int(v), d))
        if r is None or (r.soc_start_pct - r.soc_end_pct) < min_dsoc or (so - si) < min_dsoc:
            gain.append(np.nan)
            sensor.append(np.nan)
            continue
        cap = r.energy_used_kwh / ((r.soc_start_pct - r.soc_end_pct) / 100.0)
        gain.append((so - si) / 100.0 * cap)
        sensor.append(r.t)
    se["gain"] = gain
    se["t_sensor"] = sensor
    se = se.dropna(subset=["gain", "t_night"]).reset_index(drop=True)
    return se


def charging_ratio(pk, min_dsoc=30):
    """the hurried read: energy into the battery over the energy through the charger meter, pooled over the sessions"""
    se = session_frame(pk, min_dsoc)
    return float(se["gain"].sum() / se["energy_kwh"].sum())


def charging_model(pk, tcol="t_night", hcol="rel_h", T0=None, base=True, se=None):
    """the session's metered energy split into the recharge over the charger's efficiency and a steady draw while
    plugged in and released that rises below a temperature: kWh = gain / eta + hours x (c0 + c1 x max(0, T0 - T)),
    T0 profiled on a half-degree grid unless given. Returns (eta, c0, c1, T0, the draw at the design night in kW)."""
    se = session_frame(pk) if se is None else se
    y = se["energy_kwh"].values
    g = se["gain"].values
    h = se[hcol].values
    t = se[tcol].values
    best = None
    for t0 in ([T0] if T0 is not None else np.arange(-4.0, 12.01, 0.5)):
        cols = [g] + ([h] if base else []) + [h * np.maximum(0.0, t0 - t)]
        X = np.column_stack(cols)
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        sse = float(np.sum((y - X @ beta) ** 2))
        if best is None or sse < best[0]:
            best = (sse, beta, t0)
    sse, beta, t0 = best
    eta = 1.0 / beta[0]
    c0 = float(beta[1]) if base else 0.0
    c1 = float(beta[-1])
    return float(eta), c0, c1, float(t0), c0 + c1 * max(0.0, t0 - DESIGN_T), float(np.sqrt(sse / len(y)))


def charging_ratio_by_cold(pk, se=None):
    """a rival a careful run fits once it sees winter sessions take more per kWh: the meter's energy per kWh into the
    battery as a line in the night's cold, read at the design night (a multiplicative loss, no hours term)"""
    se = session_frame(pk) if se is None else se
    y = (se["energy_kwh"] / se["gain"]).values
    best = None
    for t0 in np.arange(-4.0, 12.01, 0.5):
        X = np.column_stack([np.ones(len(y)), np.maximum(0.0, t0 - se["t_night"].values)])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        sse = float(np.sum((y - X @ beta) ** 2))
        if best is None or sse < best[0]:
            best = (sse, beta, t0)
    _, beta, t0 = best
    k15 = float(beta[0] + beta[1] * max(0.0, t0 - DESIGN_T))
    # the fit's error on the metered energy itself, comparable with the split's
    pred = se["gain"].values * (beta[0] + beta[1] * np.maximum(0.0, t0 - se["t_night"].values))
    return 1.0 / k15, float(np.sqrt(np.mean((se["energy_kwh"].values - pred) ** 2)))


# ----------------------------------------------------------------------------------------------- R4: the energies
def bridge(pk, e_block, days, rates, min_days=1, with_climb=False, with_hours=False):
    """block energy per km outside HVAC on diesel litres per 100 km over the blocks an electric bus ran, weighted by
    days; rivals add the climb or the hours per km"""
    xs, ys, ws, cl, hk = [], [], [], [], []
    for c, e in e_block.items():
        if c in rates and days.get(c, 0) >= min_days:
            xs.append(rates[c])
            ys.append(e)
            ws.append(days[c])
            cl.append(pk.blocks[c]["climb"])
            hk.append(pk.blocks[c]["hours"] / pk.blocks[c]["km"])
    xs, ys, ws, cl, hk = map(np.array, (xs, ys, ws, cl, hk))
    W = np.sqrt(ws)
    cols = [np.ones_like(xs), xs] + ([cl] if with_climb else []) + ([hk] if with_hours else [])
    X = np.column_stack(cols)
    beta, *_ = np.linalg.lstsq(X * W[:, None], ys * W, rcond=None)
    pred = X @ beta
    rmse = float(np.sqrt(np.average((ys - pred) ** 2, weights=ws)))
    return beta, rmse, len(xs)


def covariate_model(pk, e_block, days):
    """the hurried transfer: block rate on climb and hours per kilometre (the timetable's speed) over the blocks an
    electric bus ran, weighted by days"""
    xs, ys, ws = [], [], []
    for c, e in e_block.items():
        b = pk.blocks[c]
        xs.append([1.0, b["climb"], b["hours"] / b["km"]])
        ys.append(e)
        ws.append(days[c])
    xs, ys, ws = np.array(xs), np.array(ys), np.array(ws, float)
    W = np.sqrt(ws)
    beta, *_ = np.linalg.lstsq(xs * W[:, None], ys * W, rcond=None)
    return beta


def design_energies(pk, how="golden", rates=None, own_min_days=30, bridge_hours=False):
    """the 48 weekday blocks' battery energy on the design day for the 2027 model, kWh, by the named route"""
    e_block, days, table = ebus_model(pk)
    if rates is None:
        rates = diesel_rates(pk)
    h_pilot = hvac_at(table, DESIGN_T)
    k, T0, lph, _ = heater_fuel(pk)
    heat_new = h_pilot + lph * HEATER_KWH_PER_L / 1.0        # below the heat pump's range the boosters supply it 1:1
    if how in ("golden", "j2_wrong"):
        beta, _, _ = bridge(pk, e_block, days, rates, with_hours=bridge_hours)
        def e_of(b):
            c = b["code"]
            if days.get(c, 0) >= own_min_days:
                return e_block[c]
            x = [1.0, rates[c]] + ([b["hours"] / b["km"]] if bridge_hours else [])
            return float(np.array(x) @ beta)
    else:
        cb = covariate_model(pk, e_block, days)
        def e_of(b):
            c = b["code"]
            if c in e_block:
                return e_block[c]
            return float(cb[0] + cb[1] * b["climb"] + cb[2] * b["hours"] / b["km"])
    heat = heat_new if how in ("golden", "j1_wrong") else (hvac_fit(pk)(DESIGN_T) if how == "careful" else h_pilot)
    out = {}
    for c in pk.weekday:
        b = pk.blocks[c]
        out[c] = b["km"] * e_of(b) + b["hours"] * heat
    return out, {"e_block": e_block, "days": days, "h_pilot": h_pilot, "heater_lph": lph, "heater_k": k,
                 "heater_T0": T0, "heat_new": heat_new, "heat_used": heat}


def quick_energies(pk):
    eb = pk.ebus
    cold = eb[eb["t"] <= -5]
    rate = float(cold["energy_used_kwh"].sum() / cold["distance_km"].sum())
    return {c: pk.blocks[c]["km"] * rate for c in pk.weekday}, rate


# ----------------------------------------------------------------------------------------------- R5 to R8
def limit(pk, loss):
    return SHARE * pk.usable_2027 * (1 - loss)


def window(pk, c, pad=0):
    """block c's charging window on the design night: its return to its next departure inside the night period (the
    standard's 3.2 and 4.2 read literally: pad 0); pad minutes at each end are a rival reading"""
    return max(pk.blocks[c]["ret"] + pad, NIGHT_FROM), min(pk.blocks[c]["dep"] + 1440 - pad, NIGHT_TO + 1440)


def windows(pk, codes, energies, eta, cond_kw=0.0, pad=0):
    """each block's charging job: the recharge at the connection point (battery energy over the charger's efficiency)
    and the steady draw beside it over the whole window"""
    out = []
    for c in codes:
        a, b = window(pk, c, pad)
        out.append((c, energies[c] / eta, a, b, cond_kw))
    return out


def night_draw(pk, codes, energies, eta, cond_kw=0.0, pad=0):
    """what the installation takes at the connection point on the design night for these blocks' buses, kWh"""
    return sum(j[1] + j[4] * (j[3] - j[2]) / 60.0 for j in windows(pk, codes, energies, eta, cond_kw, pad))


def night_cut(pk, energies, lim, eta, cond_kw=0.0, supply=None, pad=0):
    """the standard's 4.2: qualifying blocks in priority order, cut at the first the night cannot recharge with those
    above it; returns (taken codes, refused code, shortfall kWh, the taken set's draw at the connection point, the
    qualifying codes)"""
    supply = pk.supply if supply is None else supply
    q = [c for c in sorted(pk.weekday, key=lambda c: pk.priority[c]) if energies[c] <= lim]
    cands = windows(pk, q, energies, eta, cond_kw, pad)
    taken, refused, short = night.cut_by_priority(cands, CHARGER_KW, supply)
    grid = night_draw(pk, taken, energies, eta, cond_kw, pad)
    return taken, refused, short, grid, q


def capacity_for(pk, codes, energies, eta, cond_kw=0.0, pad=0):
    """the least night-period capacity at the connection point at which these blocks can all be recharged, kW"""
    return night.least_supply(windows(pk, codes, energies, eta, cond_kw, pad), CHARGER_KW)


def golden(pk):
    rates = diesel_rates(pk)
    loss, rmse, lvl = capacity_loss(pk)
    eta, c0, c1, t0, cond, cm_rmse = charging_model(pk)
    E, parts = design_energies(pk, "golden", rates)
    lim = limit(pk, loss)
    taken, refused, short, grid, q = night_cut(pk, E, lim, eta, cond)
    verdict = {c: E[c] <= lim for c in pk.weekday}
    faults = heater_from_faults(pk)
    return {"rates": rates, "loss": loss, "eta": eta, "cond_kw": cond, "cond_fit": (c0, c1, t0, cm_rmse), "E": E, "limit": lim,
            "taken": taken, "refused": refused, "short": short, "grid_kwh": grid, "qualifying": q,
            "demand_kwh": night_draw(pk, q, E, eta, cond), "capacity_kw": capacity_for(pk, q, E, eta, cond),
            "verdict": verdict, "parts": parts, "faults": faults, "cap_rmse": rmse, "heater_kw": parts["heater_lph"] * HEATER_KWH_PER_L,
            "ratio_pooled": charging_ratio(pk)}


def careful(pk, energies="j1_wrong", conditioning=False):
    """the careful but hurried pass: every file cleaned and joined, the diesel figures tank to tank, the pilot's heaters
    read from the HVO fills, the pilot's fit carried to the blocks it never ran on climb and hours per km, the loss on a
    curved age form, the charging losses as the sessions' pooled ratio, the night scheduled exactly on those figures"""
    rates = diesel_rates(pk)
    loss, _, _ = capacity_loss(pk)
    if conditioning:
        eta, _, _, _, cond, _ = charging_model(pk)
    else:
        eta, cond = charging_ratio(pk), 0.0
    E, parts = design_energies(pk, energies, rates)
    lim = limit(pk, loss)
    taken, refused, short, grid, q = night_cut(pk, E, lim, eta, cond)
    return {"rates": rates, "loss": loss, "eta": eta, "cond_kw": cond, "E": E, "limit": lim, "taken": taken, "grid_kwh": grid,
            "qualifying": q, "demand_kwh": night_draw(pk, q, E, eta, cond), "capacity_kw": capacity_for(pk, q, E, eta, cond),
            "verdict": {c: E[c] <= lim for c in pk.weekday}, "parts": parts}


def quick(pk):
    """ten minutes: the pilot's cold-day energy per km times each block's kilometres against 85 per cent of the quoted
    battery, every block that passes ordered, the night's draw as the battery energy and its capacity as that energy
    over the night period's ten hours"""
    E, rate = quick_energies(pk)
    lim = SHARE * pk.usable_2027
    q = [c for c in sorted(pk.weekday, key=lambda c: pk.priority[c]) if E[c] <= lim]
    dem = sum(E[c] for c in q)
    return {"E": E, "limit": lim, "taken": q, "rate": rate, "verdict": {c: E[c] <= lim for c in pk.weekday},
            "grid_kwh": dem, "demand_kwh": dem, "capacity_kw": dem / 10.0}


def routes(pk, g=None):
    """every route's count and set: the golden, the two passes, and each estimate left out on the golden's path"""
    g = g or golden(pk)
    out = {}
    out["golden"] = g["taken"]
    out["careful but hurried"] = careful(pk)["taken"]
    out["quick"] = quick(pk)["taken"]
    E1, _ = design_energies(pk, "j1_wrong", g["rates"])
    out["the pilot's fit carried on kilometres, climb and speed (the diesel bridge left out)"] = night_cut(pk, E1, g["limit"], g["eta"], g["cond_kw"])[0]
    E2, _ = design_energies(pk, "j2_wrong", g["rates"])
    out["the pilot's cold response read as the new buses' (the fuel heaters' share left out)"] = night_cut(pk, E2, g["limit"], g["eta"], g["cond_kw"])[0]
    out["the sessions' pooled ratio for the night (the battery's conditioning left out)"] = night_cut(pk, g["E"], g["limit"], g["ratio_pooled"])[0]
    Ec, _ = design_energies(pk, "careful", g["rates"])
    out["the pilot's own record carried as it stands (no bridge, no heaters' share, the pooled ratio)"] = night_cut(pk, Ec, g["limit"], g["ratio_pooled"])[0]
    out["the per-block verdicts summed, the night's supply ignored"] = [c for c in sorted(pk.weekday, key=lambda c: pk.priority[c]) if g["E"][c] <= g["limit"]]
    out["the night scheduled on battery energy (charging losses and conditioning ignored)"] = night_cut(pk, g["E"], g["limit"], 1.0)[0]
    out["the careful pass without the night's supply"] = [c for c in sorted(pk.weekday, key=lambda c: pk.priority[c]) if E1[c] <= g["limit"]]
    return out
