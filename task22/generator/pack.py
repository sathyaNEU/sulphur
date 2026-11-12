"""task22 pack: the shipped tables built from the records (frames()), then written under target/ in the formats each
system exports (write()). The golden and the passes run on frames() for calibration and on the files read back
(golden.load) for the figures, and the two must agree."""
import datetime as dt
import math
from collections import defaultdict

import numpy as np
import pandas as pd

import params as P
import records as R
import world as WD


def burn_hours(w):
    """Monthly burning hours of a photocell-controlled light at Delmont: the month's dark hours on average."""
    g = w.g
    dark = (w.elev < -0.8).astype(float)
    tot = defaultdict(float)
    n = defaultdict(int)
    seen = set()
    for h in range(g.H):
        d = g.loc[h].date()
        tot[(d.year, d.month)] += dark[h]
        if (d.year, d.month) not in seen:
            seen.add((d.year, d.month))
    by_m = defaultdict(list)
    for (y, m), v in tot.items():
        if (y, m) in ((2026, 11),):
            continue
        by_m[m].append(v)
    return {m: round(float(np.mean(v))) for m, v in sorted(by_m.items())}


def frames(w, seed=P.SEED + 7):
    rng = np.random.default_rng(seed)
    R.customer_metered(w)
    F = {}
    reads = R.meter_reads(w, rng) + R.lp_reads(w, rng)
    rows = []
    for r in reads:
        bill = R.add_business(r["read_date"], int(rng.integers(1, 4)))
        rows.append(dict(ServicePointID=r["sp"], AccountNo=r["account"], MeterNo=r["meter"], RateCode=r["rate"],
                         Cycle=r["cycle"], ReadDate=r["read_date"].isoformat(), ReadType=r["read_type"],
                         Register=round(r["register"], 0) if r["register"] is not None else None,
                         kWh=round(r["kwh"], 0) if r["kwh"] is not None else None,
                         RegisterRcv=round(r["register_rcv"], 0) if r["register_rcv"] is not None else None,
                         kWhRcv=round(r["kwh_rcv"], 0) if r["kwh_rcv"] is not None else None,
                         Multiplier=r["mult"], MeterType=r["meter_type"], BillDate=bill.isoformat()))
    F["reads"] = pd.DataFrame(rows)
    w.read_rows = reads
    dp = R.delivery_points(w, rng)
    F["dp"] = pd.DataFrame(dp, columns=["DeliveryPoint", "Date", "HourEnding", "kWh", "kVArh"])
    sc = R.scada(w, rng)
    F["scada"] = pd.DataFrame(sc, columns=["Timestamp", "Point", "MW", "MVAR", "Quality"])
    F["station_service"] = pd.DataFrame(R.station_service(w))
    F["subxf"] = pd.DataFrame([dict(Substation=v["name"], Rating_MVA=v["mva"], NoLoad_kW=v["nl_kw"],
                                    LoadLoss_kW=v["ll_kw"], Impedance_pct=round(7.6 + 0.3 * k, 1))
                               for k, v in enumerate(P.SUBSTATIONS.values())])
    segs, sws, xfs, sps = R.gis_export(w, rng)
    F["gis_segments"] = pd.DataFrame(segs)
    F["gis_switches"] = pd.DataFrame(sws)
    F["gis_xf"] = pd.DataFrame(xfs)
    F["gis_sp"] = pd.DataFrame(sps)
    reg = R.xfmr_register(w)
    F["xfmr_register"] = pd.DataFrame([dict(AssetID=r["AssetID"], kVA=r["kVA"], MfgYear=r["MfgYear"],
                                            InstallDate=r["InstallDate"].isoformat(),
                                            RemovedDate=r["RemovedDate"].isoformat() if r["RemovedDate"] else "",
                                            Location=r["Location"], Mount=r["Mount"]) for r in reg])
    F["oms_log"] = pd.DataFrame(R.oms_log(w, rng))
    F["oms_xref"] = pd.DataFrame(R.oms_xref(w, rng))
    F["conductors"] = pd.DataFrame([dict(Conductor=k, R25_ohm_per_mile=v[1], R50_ohm_per_mile=v[0],
                                         X_ohm_per_mile=v[2]) for k, v in P.CONDUCTORS.items()])
    xl = []
    for kva, (nl, ll) in P.XFMR_LOSS.items():
        xl.append(dict(kVA=kva, Vintage="2010 and later", NoLoad_W=nl, LoadLoss_W=ll))
        xl.append(dict(kVA=kva, Vintage="before 2010", NoLoad_W=round(nl * P.OLD_NL), LoadLoss_W=round(ll * P.OLD_LL)))
    F["xfmr_losses"] = pd.DataFrame(xl)
    nominal = {"HPS100": 100, "HPS150": 150, "HPS250": 250, "MV175": 175, "LED40": 40, "LED70": 70, "LED110": 110}
    F["lamp_watts"] = pd.DataFrame([dict(LampCode=k, Nominal_W=nominal[k], Input_W=v) for k, v in P.INPUT_W.items()])
    bh = burn_hours(w)
    F["burn_hours"] = pd.DataFrame([dict(Month=m, BurningHours=v) for m, v in bh.items()])
    R.light_accounts(w, rng)
    inv = []
    for L in w.lights:
        inv.append(dict(LightID=L["id"], Account=L["account"], Type=L["kind"], PoleNode=L["node"],
                        LampCode=L["lamp"], InstallDate=L["install"].isoformat(),
                        LEDConversion=L["led"].isoformat() if L["led"] else "",
                        LEDLampCode=P.LED_FOR[L["lamp"]] if L["led"] else "",
                        WorkOrder="WO-%06d" % int(rng.integers(100000, 999999)) if L["led"] else ""))
    F["lights_inventory"] = pd.DataFrame(inv)
    lb = R.lights_billing(w)
    F["lights_billing"] = pd.DataFrame([dict(Account=r["account"], Month=r["month"].isoformat(), Type=r["kind"],
                                             LampCode=r["lamp"], Lamps=r["lamps"], DeemedkWh=r["kwh"]) for r in lb])
    F["lp_interval"] = pd.DataFrame(R.lp_interval(w), columns=["ServicePointID", "MeterNo", "IntervalEnd", "kWh"])
    apps = R.applications(w, rng)
    F["applications"] = pd.DataFrame([{k: (v.isoformat() if isinstance(v, dt.date) else v) for k, v in a.items()}
                                      for a in apps])
    st = WD.study_2019(w)
    w.study = st
    F["study2019"] = pd.DataFrame([dict(Feeder=f, Peak_MW=round(s["peak_mw"], 2), Energy_MWh=round(s["energy_mwh"]),
                                        LoadFactor=round(s["lf"], 3), Req_ohm=round(s["req"], 3),
                                        PeakLoss_kW=round(s["peak_loss_kw"], 1), LossFactor=round(s["lsf"], 3),
                                        Primary_MWh=round(s["prim_mwh"]), NoLoad_MWh=round(s["nl_mwh"]),
                                        LoadLoss_MWh=round(s["ll_mwh"]), Secondary_MWh=round(s["sec_mwh"]),
                                        Technical_MWh=round(s["tech_mwh"]), Technical_pct=round(s["tech_pct"], 2))
                                   for f, s in st.items()])
    # the 2027 reconductor: APT-3's trunk segments from the breaker out to 9.8 miles
    tr = w.net.trunk[P.RECONDUCTOR["feeder"]]
    segs_rc = []
    for s in w.net.seg:
        if s["feeder"] == P.RECONDUCTOR["feeder"] and s["phasing"] == "ABC" and s["b"] in tr and \
                w.net.node_pos[s["b"]] <= P.RECONDUCTOR["miles"] + 0.05:
            segs_rc.append(s["id"])
    w.reconductor_segments = segs_rc
    F["cwp"] = dict(segments=segs_rc, new=P.RECONDUCTOR["new"], in_service=P.RECONDUCTOR["in_service"].isoformat())
    F["outages"] = pd.DataFrame(R.outage_log(w, rng))
    F["weather"] = pd.DataFrame(R.weather_daily(w))
    return F


# ---------------------------------------------------------------------------------------------------------------
# the files under target/
# ---------------------------------------------------------------------------------------------------------------

import os  # noqa: E402

import openpyxl  # noqa: E402
from openpyxl.styles import Alignment, Font  # noqa: E402

import docs as DC  # noqa: E402
import postprocess  # noqa: E402

ORG = "City of Delmont"
FILES = {
    "dp": "bmpa_delivery_point_interval_2023-09_2026-10.csv",
    "scada": "historian_feeder_breakers_hourly_2023-09-01_2026-10-31.csv",
    "reads": "cis_meter_reads_2023-08-01_2026-11-01.csv",
    "lp_interval": "idr_large_power_interval_2025-10_2026-09.csv",
    "gis": "gis_electric_network_2026-10-27.xlsx",
    "register": "transformer_asset_register_2026-10-27.xlsx",
    "oms_log": "oms_switching_orders_2023-09_2026-10.csv",
    "xref": "oms_gis_device_crosswalk_2024-07.xlsx",
    "eng": "distribution_engineering_tables.xlsx",
    "subs": "substations_and_station_service.xlsx",
    "lights_inv": "street_area_lighting_inventory_2026-10-27.xlsx",
    "lights_bill": "unmetered_lighting_billing_2023-09_2026-10.csv",
    "rates": "dpl_electric_rate_schedules_2025-10.pdf",
    "study": "loss_evaluation_study_2019_hester.pdf",
    "apps": "large_load_service_applications_2019-2027.xlsx",
    "cwp": "cwp_2027-2028_approved_projects_excerpt.pdf",
    "budget": "fy2027_budget_instructions_electric_fund.pdf",
    "scope": "rfp_2026-14_revenue_protection_scope.pdf",
    "lineloss": "annual_line_loss_report_2019-2026.xlsx",
    "outages": "oms_outage_events_2023-09_2026-10.csv",
    "wholesale": "bmpa_wholesale_rate_schedule_w1_2026.pdf",
    "weather": "delmont_municipal_airport_daily_2023-09_2026-10.csv",
}
DISTRACTORS = ["outages", "wholesale", "weather"]
CDT = dt.timezone(dt.timedelta(hours=-5))
CST = dt.timezone(dt.timedelta(hours=-6))
WRITTEN = {   # each export's own save time
    "dp": dt.datetime(2026, 11, 2, 7, 41, 3, tzinfo=CST),
    "scada": dt.datetime(2026, 11, 3, 8, 12, 51, tzinfo=CST),
    "reads": dt.datetime(2026, 11, 5, 9, 3, 27, tzinfo=CST),
    "lp_interval": dt.datetime(2026, 10, 5, 10, 22, 8, tzinfo=CDT),
    "oms_log": dt.datetime(2026, 11, 3, 8, 47, 14, tzinfo=CST),
    "lights_bill": dt.datetime(2026, 11, 3, 9, 18, 40, tzinfo=CST),
    "outages": dt.datetime(2026, 11, 3, 8, 51, 2, tzinfo=CST),
    "weather": dt.datetime(2026, 11, 2, 6, 5, 33, tzinfo=CST),
}
OFFICE = {   # workbooks: created, modified (UTC), last saved by
    "gis": ("2024-02-05T15:20:00Z", "2026-10-27T16:41:00Z", "GIS Services"),
    "register": ("2019-03-11T14:02:00Z", "2026-10-27T17:05:00Z", "Asset Management"),
    "xref": ("2024-07-12T19:44:00Z", "2024-07-12T21:16:00Z", "Systems Integration"),
    "eng": ("2017-05-22T13:30:00Z", "2025-03-04T15:52:00Z", "Electric Engineering"),
    "subs": ("2018-01-15T16:12:00Z", "2026-11-02T15:27:00Z", "Substations"),
    "lights_inv": ("2020-08-03T14:45:00Z", "2026-10-27T18:20:00Z", "Electric Distribution"),
    "apps": ("2019-06-04T15:01:00Z", "2026-10-20T20:33:00Z", "Customer Engineering"),
    "lineloss": ("2020-01-27T16:10:00Z", "2026-10-14T19:48:00Z", "Utilities Finance"),
}


def _csv(path, df):
    df.to_csv(path, index=False, lineterminator="\r\n")
    return len(df)


def _sheet(ws, header, rows, widths=None, title=None, note=None, freeze=True):
    r0 = 1
    if title:
        ws.cell(row=1, column=1, value=title).font = Font(bold=True, size=12)
        r0 = 3
    for j, h in enumerate(header, 1):
        c = ws.cell(row=r0, column=j, value=h)
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, row in enumerate(rows, r0 + 1):
        for j, v in enumerate(row, 1):
            ws.cell(row=i, column=j, value=v)
    if note:
        ws.cell(row=r0 + len(rows) + 2, column=1, value=note).font = Font(italic=True, size=8)
    for j, wd in enumerate(widths or [], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = wd
    if freeze:
        ws.freeze_panes = ws.cell(row=r0 + 1, column=1)


def _df_sheet(ws, df, widths=None, title=None, note=None):
    _sheet(ws, list(df.columns), df.astype(object).where(df.notna(), None).values.tolist(), widths, title, note)


def line_loss_report(w, F):
    """The utility's own annual line loss: purchases less billed sales, over purchases (the Form EIA-861 basis)."""
    import analysis as A
    rows = []
    hist = {2019: (231840, 218150), 2020: (229410, 215760), 2021: (233980, 219770), 2022: (238120, 223280),
            2023: (241960, 226430)}
    for y, (p_, b_) in hist.items():
        rows.append([str(y), p_, b_, round(100 * (p_ - b_) / p_, 2)])
    for y in (2024, 2025):
        win = (dt.date(y, 1, 1), dt.date(y + 1, 1, 1))
        p_ = A.purchases(F, win) / 1000.0
        c_, l_ = A.billed_in(F, win)
        b_ = (c_ + l_) / 1000.0
        rows.append([str(y), round(p_), round(b_), round(100 * (p_ - b_) / p_, 2)])
    for lab, win in (("12 months to September 2024", A.WIN24), ("12 months to September 2026", A.WIN26)):
        p_ = A.purchases(F, win) / 1000.0
        c_, l_ = A.billed_in(F, win)
        b_ = (c_ + l_) / 1000.0
        rows.append([lab, round(p_), round(b_), round(100 * (p_ - b_) / p_, 2)])
    return rows


def write(w, F, target):
    os.makedirs(target, exist_ok=True)
    out = {k: os.path.join(target, v) for k, v in FILES.items()}
    counts = {}
    rng = np.random.default_rng(P.SEED + 41)
    # the CIS extract was pulled in two runs that overlap by a day; the overlap's rows appear twice
    reads = F["reads"].copy()
    dup = reads[(reads["ReadDate"] >= "2025-06-30") & (reads["ReadDate"] <= "2025-07-01")]
    reads = pd.concat([reads, dup]).sort_values(["ReadDate", "ServicePointID", "ReadType"], kind="mergesort")
    counts["reads"] = _csv(out["reads"], reads)
    counts["dp"] = _csv(out["dp"], F["dp"])
    counts["scada"] = _csv(out["scada"], F["scada"])
    counts["lp_interval"] = _csv(out["lp_interval"], F["lp_interval"])
    counts["oms_log"] = _csv(out["oms_log"], F["oms_log"])
    counts["lights_bill"] = _csv(out["lights_bill"], F["lights_billing"])
    counts["outages"] = _csv(out["outages"], F["outages"])
    wx = F["weather"].copy()
    wx.insert(0, "NAME", "DELMONT MUNICIPAL AIRPORT, OK US")
    wx.insert(0, "STATION", "USC00342207")
    counts["weather"] = _csv(out["weather"], wx)
    # the GIS export
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Primary segments"
    _df_sheet(ws, F["gis_segments"], [12, 8, 12, 12, 10, 12, 9, 11])
    _df_sheet(wb.create_sheet("Switches"), F["gis_switches"], [10, 14, 12, 12, 12, 10, 8])
    _df_sheet(wb.create_sheet("Transformers"), F["gis_xf"], [10, 12, 8, 8, 9, 12, 8])
    _df_sheet(wb.create_sheet("Service points"), F["gis_sp"], [14, 10, 8, 10, 10])
    wb.save(out["gis"])
    counts["gis"] = len(F["gis_segments"])
    wb = openpyxl.Workbook()
    _df_sheet(wb.active, F["xfmr_register"], [10, 8, 9, 12, 12, 12, 8])
    wb.active.title = "Distribution transformers"
    wb.save(out["register"])
    wb = openpyxl.Workbook()
    _df_sheet(wb.active, F["oms_xref"], [14, 14, 12])
    wb.active.title = "Device map"
    wb.save(out["xref"])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Conductors"
    _df_sheet(ws, F["conductors"], [14, 16, 16, 16], title="Overhead and underground primary conductors")
    _df_sheet(wb.create_sheet("Transformer losses"), F["xfmr_losses"], [8, 16, 12, 14],
              title="Distribution transformer losses, manufacturers' test data")
    _df_sheet(wb.create_sheet("Lamp input watts"), F["lamp_watts"], [12, 12, 12],
              title="Lighting: lamp and ballast input watts")
    _df_sheet(wb.create_sheet("Burning hours"), F["burn_hours"], [8, 16],
              title="Photocell-controlled lighting, burning hours by month, Delmont")
    wb.save(out["eng"])
    wb = openpyxl.Workbook()
    _df_sheet(wb.active, F["subxf"], [18, 12, 12, 14, 14], title="Substation power transformers, 69/12.47 kV")
    wb.active.title = "Power transformers"
    _df_sheet(wb.create_sheet("Station service"), F["station_service"], [18, 10, 10],
              title="Station service meters, monthly kWh")
    wb.save(out["subs"])
    wb = openpyxl.Workbook()
    _df_sheet(wb.active, F["lights_inventory"], [9, 11, 8, 11, 9, 12, 13, 12, 11])
    wb.active.title = "Lights"
    wb.save(out["lights_inv"])
    wb = openpyxl.Workbook()
    _df_sheet(wb.active, F["applications"], [12, 34, 20, 8, 22, 9, 10, 9, 10, 12, 12, 10, 12, 14])
    wb.active.title = "Applications"
    wb.save(out["apps"])
    wb = openpyxl.Workbook()
    rows = line_loss_report(w, F)
    _sheet(wb.active, ["Period", "Purchased MWh", "Billed MWh", "Line loss %"], rows, [26, 16, 14, 12],
           title="Delmont Power and Light: line loss",
           note="Purchased: Bluestem Municipal Power Agency delivery point invoices. Billed: kWh on bills issued in "
                "the period, all rate schedules including lighting.")
    wb.active.title = "Line loss"
    wb.save(out["lineloss"])
    for k, (c0, c1, who) in OFFICE.items():
        postprocess.normalize_ooxml(out[k], who, who, c0, c1, excel=True, company=ORG)
    DC.study(out["study"], w.study)
    DC.cwp(out["cwp"], w.reconductor_segments)
    DC.rates(out["rates"])
    DC.budget(out["budget"])
    DC.scope(out["scope"])
    DC.wholesale(out["wholesale"])
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in WRITTEN.items()})
    w.line_loss_rows = rows
    return counts
