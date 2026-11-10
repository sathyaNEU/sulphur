"""task10 architecture 7: reads the pack back into clean tables, cleaning each Layer 1 item the way a careful analyst
does (both SCADA point names mapped through the register, S and B quality rows and the re-sent overlap dropped, the
latest revision of each dispatch instruction kept, UK local dates parsed, the growth register's live rows kept and
its feeders mapped through both their codes, the monthly summary joined on the meter point, the asset register's
superseded entries dropped and its provider and class spellings brought to one)."""
import datetime as dt
import os
import re
import subprocess

import openpyxl
import pandas as pd

UTC = dt.timezone.utc
F_ASSET = "flexibility_asset_register_2026-11-04.csv"
F_MON = "hh_customer_demand_monthly_2021-2026.csv"


def _book(path, sheet):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    return [dict(zip(hdr, r)) for r in rows[1:] if r and r[0] is not None and any(v is not None for v in r)]


def _day(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date() if isinstance(s, str) and s.strip() else None


def provider_key(s):
    """One spelling per provider: upper case, without the company suffix."""
    return re.sub(r"\s+LTD\.?$", "", str(s).upper().strip())


def register(target):
    prim = _book(os.path.join(target, "primary_substation_register.xlsx"), "Primaries")
    dfes = _book(os.path.join(target, "primary_substation_register.xlsx"), "DFES 2026")
    pmap = {}
    for r in prim:
        pmap[r["SCADA point (to 13/05/2024)"]] = r["Asset code"]
        pmap[r["SCADA point (from 14/05/2024)"]] = r["Asset code"]
    names = {r["Asset code"]: r["Primary substation"] for r in prim}
    rates = {r["Asset code"]: (float(r["Underlying peak growth 2026/27 (%)"]), float(r["Underlying peak growth 2027/28 (%)"]))
             for r in dfes if isinstance(r.get("Asset code"), str) and r["Asset code"].startswith("PS")}
    return pmap, names, rates


def scada(target, pmap, mis=()):
    d = pd.read_csv(os.path.join(target, "primary_demand_halfhourly_2023-2026.csv"), dtype={"quality": str})
    d = d.drop_duplicates()
    if "held_values_kept" not in mis:
        d = d[d["quality"] == "G"].copy()
    d["code"] = d["point"].map(pmap)
    d["t_utc"] = pd.to_datetime(d["interval_end_uk_local"]).dt.tz_localize("Europe/London").dt.tz_convert("UTC")
    d = d.rename(columns={"value_mw": "mw"})[["code", "t_utc", "mw"]]
    d = d.drop_duplicates(subset=["code", "t_utc"])
    return d.sort_values(["code", "t_utc"]).reset_index(drop=True)


def events(target, mis=()):
    e = pd.read_csv(os.path.join(target, "flexibility_events_2023-2026.csv"), dtype=str)
    e["revision"] = e["revision"].astype(int)
    e = e.sort_values(["instruction_ref", "revision"]).groupby("instruction_ref", as_index=False)
    if "first_megawatts" in mis:      # the megawatts first issued, at the instruction's final status
        first, last = e.first(), e.last()
        last["scheduled_mw"] = [a if s == "Completed" else b for a, b, s in
                                zip(first["scheduled_mw"], last["scheduled_mw"], last["status"])]
        e = last
    else:
        e = e.last()
    out = pd.DataFrame({
        "zone": e["primary_asset"],
        "provider": [provider_key(s) for s in e["provider"]],
        "date": [_day(s) for s in e["service_date"]],
        "scheduled_mw": e["scheduled_mw"].astype(float),
        "status": e["status"]})
    return out.sort_values(["zone", "date"]).reset_index(drop=True)


def weather(target, mis=()):
    w = pd.read_csv(os.path.join(target, "halverton_weather_hourly_2023-2026.csv"))
    # an hour checked by the station carries its raw reading (version 0) and its quality-controlled one (version 1)
    w = w.sort_values(["ob_end_time", "version_num"]).drop_duplicates(subset=["ob_end_time"],
                                                                      keep="first" if "raw_weather" in mis else "last")
    w["t_utc"] = pd.to_datetime(w["ob_end_time"], utc=True)
    return w.rename(columns={"air_temperature": "temp_c"})[["t_utc", "temp_c"]]


def feeders(target):
    path = os.path.join(target, "network_feeders_11kv.xlsx")
    f = _book(path, "Feeders")
    nops = _book(path, "Open points")
    fmap = {}
    for r in f:
        fmap[r["Feeder ID"]] = r["Primary asset code"]
        fmap[r["Circuit (legacy)"]] = r["Primary asset code"]
    links = {}
    for r in nops:
        a, b = r["Primary (side 1)"], r["Primary (side 2)"]
        links.setdefault(a, set()).add(b)
        links.setdefault(b, set()).add(a)
    return fmap, links


def growth(target, fmap):
    """The register's live rows (accepted or energised; withdrawn, superseded and quoted rows are not counted): one
    row per customer, its primary through the feeder schedule, its agreed capacity and its energisation date."""
    rows = _book(os.path.join(target, "load_growth_register_2026-27.xlsx"), "Register")
    out = []
    for r in rows:
        if r["Status"] not in ("Accepted", "Energised"):
            continue
        when = _day(r["Energisation date (planned if not yet energised)"])
        if when is None:
            continue
        out.append(dict(conn=r["Reference"], code=fmap[r["11 kV feeder"]], type=r["Customer type"],
                        kva=float(r["Agreed supply capacity (kVA)"]), accepted=_day(r["Offer accepted"]), planned=when,
                        energised=when if r["Status"] == "Energised" else None,
                        mpan=str(r["MPAN core"]).strip() if r["MPAN core"] else None))
    return pd.DataFrame(out)


def monitor(target, conns):
    """The monthly summary's rows for the register's customers, by meter point."""
    m = pd.read_csv(os.path.join(target, F_MON), dtype={"mpan_core": str})
    by = {r.mpan: r.conn for r in conns.itertuples() if r.mpan}
    m = m[m["mpan_core"].isin(by)].copy()
    m["conn"] = m["mpan_core"].map(by)
    m["month"] = [dt.date(int(s[:4]), int(s[5:7]), 1) for s in m["month"]]
    m = m.rename(columns={"mean_kw_1700_1800_working_days": "evening_kw"})
    return m[["conn", "month", "evening_kw"]].sort_values(["conn", "month"]).reset_index(drop=True)


CLASSES = ["Domestic heat pump aggregation", "Battery storage", "EV charging aggregation", "Commercial refrigeration",
           "HVAC", "Process load"]


def assets(target, mis=()):
    """The asset register's current entries: one row per site, with the date it passed its commissioning test, the
    date it was withdrawn before that (lost) and the date it left the service after it."""
    a = pd.read_csv(os.path.join(target, F_ASSET), dtype=str, keep_default_na=False)
    if "superseded_sites_kept" not in mis:
        a = a[a["status"] != "Superseded"].copy()
    canon = {c.lower(): c for c in CLASSES}
    # the class as typed keeps the register's two capitalisations of a class apart
    cls = [s.strip() if "classes_as_typed" in mis else canon[s.strip().lower()] for s in a["asset_class"]]
    out = pd.DataFrame({
        "site": a["site_ref"].values,
        "zone": a["primary_asset"].values,
        "provider": [provider_key(s) for s in a["provider"]],
        "cls": cls,
        "kw": a["registered_kw"].astype(float).values,
        "winter": a["service_year"].values,
        "signed": [_day(s) for s in a["site_signed"]],
        "planned": [_day(s) for s in a["planned_commissioning"]],
    })
    comm = [_day(s) for s in a["commissioning_test_passed"]]
    sd = [_day(s) for s in a["status_date"]]
    st = list(a["status"])
    out["commissioned"] = pd.Series(comm, dtype=object)
    out["lost"] = pd.Series([d if s == "Withdrawn" else None for d, s in zip(sd, st)], dtype=object)
    out["left"] = pd.Series([d if s == "Left service" else None for d, s in zip(sd, st)], dtype=object)
    return out.reset_index(drop=True)


def firm_capacity(target):
    """Appendix A of the guideline, read with pdftotext."""
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(target, "capacity_assessment_guideline_2026.pdf"), "-"],
                         capture_output=True, text=True, check=True).stdout
    out = {}
    for m in re.finditer(r"(PS\d{5})\s+\d+\s*\+\s*\d+\s+(\d+\.\d)", txt):
        out[m.group(1)] = float(m.group(2))
    return out, txt


def contracts(target, zone_names):
    """The award notice: megawatts contracted for the winter assessed, zone by zone, and the megawatts contracted in
    the winters before."""
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(target, "flexibility_contract_awards_2027-28.pdf"), "-"],
                         capture_output=True, text=True, check=True).stdout
    zs = "|".join(re.escape(z) for z in zone_names)
    out, prev = {}, {}
    # the awards table, one line per zone: zone, primary, provider, contracted MW, availability (two decimals),
    # utilisation (whole pounds); the previous winters' table carries one-decimal MW figures instead
    for line in txt.splitlines():
        m = re.match(r"\s*(%s) CMZ\s.*?\s(\d+\.\d)\s+(\d+\.\d\d)\s+(\d+)\s*$" % zs, line)
        if m:
            out[m.group(1)] = float(m.group(2))
    # the previous winters' table: its header line names the winters in order
    past = []
    for line in txt.split("Previous winters")[-1].splitlines():
        ws = re.findall(r"20\d\d/\d\d", line)
        if len(ws) >= 2:
            past = ws
            break
    for line in txt.splitlines():
        m = re.match(r"\s*(%s) CMZ\s.*?((?:\s+\d+\.\d){%d})\s*$" % (zs, max(len(past), 1)), line)
        if m and past and m.group(1) not in prev:
            vals = [float(v) for v in m.group(2).split()]
            if len(vals) == len(past):
                prev[m.group(1)] = dict(zip(past, vals))
    return out, txt, prev


def switching(target):
    """The control room's switching log: each transfer from the operation that closed the open point to the one that
    put the network back to normal."""
    s = pd.read_csv(os.path.join(target, "control_room_switching_log_2023-2026.csv"), dtype=str)
    s["t"] = pd.to_datetime(s["operation_time_uk_local"]).dt.tz_localize("Europe/London").dt.tz_convert("UTC")
    s = s.sort_values("t").reset_index(drop=True)
    rows, open_at = [], {}
    for r in s.itertuples():
        if r.operation == "Closed":
            open_at[r.open_point] = r
        elif r.open_point in open_at:
            a = open_at.pop(r.open_point)
            rows.append(dict(nop=r.open_point, frm=a.section_from_primary, to=a.section_to_primary, start=a.t, end=r.t,
                             mw=float(a.load_transferred_mw)))
    return pd.DataFrame(rows).sort_values(["start", "nop"]).reset_index(drop=True)


def load(target, mis=()):
    """The analyst's inputs (estim.analyse reads these keys). `mis` names Layer 1 items read the careless way, for
    the generator's own neutrality checks: held_values_kept, first_megawatts, raw_weather, superseded_sites_kept,
    classes_as_typed."""
    pmap, names, rates = register(target)
    fmap, links = feeders(target)
    firm, guide_txt = firm_capacity(target)
    awards, award_txt, prev = contracts(target, sorted(names.values()))
    code_of = {v: k for k, v in names.items()}
    conns = growth(target, fmap)
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", F_ASSET)
    for z in awards:
        prev[z]["2027/28"] = awards[z]
    ev = events(target, mis)
    # each zone's provider, as its instructions name it
    prov = {z: g.sort_values("date")["provider"].iloc[-1] for z, g in ev.groupby("zone")}
    return dict(demand=scada(target, pmap, mis), events=ev, weather=weather(target, mis), switching=switching(target),
                names=names, rates=rates, links=links, firm=firm,
                contracts_code={code_of[z]: mw for z, mw in awards.items()},
                provider_of={code_of[z]: prov[code_of[z]] for z in awards},
                previous=prev, assets=assets(target, mis), connections=conns.drop(columns=["mpan"]),
                monitor=monitor(target, conns),
                register_date=dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))),
                guideline_text=guide_txt, award_text=award_txt)
