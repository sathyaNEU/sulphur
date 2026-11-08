"""task10 architecture 5: reads the pack back into clean tables, cleaning each Layer 1 item the way a careful analyst
does (both SCADA point names mapped through the register, S and B quality rows and the re-sent overlap dropped, the
latest revision of each dispatch instruction kept, UK local dates parsed, the growth register filtered and
de-duplicated by reference, feeder IDs mapped through both their codes)."""
import datetime as dt
import os
import re
import subprocess

import openpyxl
import pandas as pd

UTC = dt.timezone.utc


def _book(path, sheet):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    return [dict(zip(hdr, r)) for r in rows[1:] if r and r[0] is not None and any(v is not None for v in r)]


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


def scada(target, pmap):
    d = pd.read_csv(os.path.join(target, "primary_demand_halfhourly_2023-2026.csv"), dtype={"quality": str})
    d = d.drop_duplicates()
    d = d[d["quality"] == "G"].copy()
    d["code"] = d["point"].map(pmap)
    d["t_utc"] = pd.to_datetime(d["interval_end_uk_local"]).dt.tz_localize("Europe/London").dt.tz_convert("UTC")
    d = d.rename(columns={"value_mw": "mw"})[["code", "t_utc", "mw"]]
    d = d.drop_duplicates(subset=["code", "t_utc"])
    return d.sort_values(["code", "t_utc"]).reset_index(drop=True)


def events(target):
    e = pd.read_csv(os.path.join(target, "flexibility_events_2024-2026.csv"), dtype=str)
    e["revision"] = e["revision"].astype(int)
    e = e.sort_values(["instruction_ref", "revision"]).groupby("instruction_ref", as_index=False).last()
    out = pd.DataFrame({
        "zone": e["primary_asset"],
        "provider": e["provider"].str.upper().str.replace(" LTD", "", regex=False).str.strip(),
        "date": [dt.datetime.strptime(s, "%d/%m/%Y").date() for s in e["service_date"]],
        "scheduled_mw": e["scheduled_mw"].astype(float),
        "status": e["status"]})
    return out.sort_values(["zone", "date"]).reset_index(drop=True)


def weather(target):
    w = pd.read_csv(os.path.join(target, "halverton_weather_hourly_2023-2026.csv"))
    # an hour checked by the station carries its raw reading (version 0) and its quality-controlled one (version 1)
    w = w.sort_values(["ob_end_time", "version_num"]).drop_duplicates(subset=["ob_end_time"], keep="last")
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
    rows = _book(os.path.join(target, "load_growth_register_2026-27.xlsx"), "Register")
    keep = {}
    lo, hi = dt.date(2026, 4, 1), dt.date(2027, 10, 31)
    for r in rows:
        if r["Status"] not in ("Accepted", "Energised"):
            continue
        pe = r["Planned energisation"]
        if not pe:
            continue
        en = dt.datetime.strptime(r["Energised on"], "%d/%m/%Y").date() if r["Energised on"] else None
        day = en or dt.datetime.strptime(pe, "%d/%m/%Y").date()
        if not (lo <= day <= hi):
            continue
        keep[r["Reference"]] = (fmap[r["11 kV feeder"]], float(r["Design demand (kW)"]))
    out = {}
    for code, kw in keep.values():
        out[code] = out.get(code, 0.0) + kw / 1000.0
    return out


def firm_capacity(target):
    """Appendix A of the guideline, read with pdftotext."""
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(target, "capacity_assessment_guideline_2026.pdf"), "-"],
                         capture_output=True, text=True, check=True).stdout
    out = {}
    for m in re.finditer(r"(PS\d{5})\s+\d+\s*\+\s*\d+\s+(\d+\.\d)", txt):
        out[m.group(1)] = float(m.group(2))
    return out


def contracts(target):
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(target, "flexibility_contract_awards_2027-28.pdf"), "-"],
                         capture_output=True, text=True, check=True).stdout
    out = {}
    # the awards table, one line per zone: zone, primary, provider, contracted MW, availability (two decimals),
    # utilisation (whole pounds); the previous winters' table carries two one-decimal MW figures instead
    for line in txt.splitlines():
        m = re.match(r"\s*(Ashcombe Road|Charlecote Way|Fenwick Street|Hartwell Common) CMZ\s.*?\s(\d+\.\d)\s+(\d+\.\d\d)\s+(\d+)\s*$", line)
        if m:
            out[m.group(1)] = float(m.group(2))
    return out, txt


def load(target):
    pmap, names, rates = register(target)
    fmap, links = feeders(target)
    return dict(demand=scada(target, pmap), events=events(target), weather=weather(target), names=names,
                rates=rates, links=links, growth=growth(target, fmap), firm=firm_capacity(target),
                contracts=contracts(target)[0])
