"""task22 architecture 2: the pack under target/, written from the simulated world as each Brandvold system would
export it, with the mess each system really makes."""
import datetime as dt
import os

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Font

import docs as DC
import params as P
import postprocess
import records as RC

ORG = P.ORG
F = P.FILES
# workbook creators and their own created and saved times (UTC)
OFFICE = {
    "register": ("2016-03-08T15:12:00Z", "2026-11-02T14:41:00Z", "GIS and Records"),
    "damage": ("2023-02-14T16:30:00Z", "2026-10-29T19:12:00Z", "Gas Operations"),
    "own_use": ("2021-11-03T14:05:00Z", "2026-10-08T15:47:00Z", "Measurement and Regulation"),
    "plan2027": ("2026-08-19T13:22:00Z", "2026-09-30T20:05:00Z", "Gas Engineering"),
    "rp_cases": ("2021-04-12T18:40:00Z", "2026-01-21T16:18:00Z", "Customer Service"),
    "lauf_report": ("2019-11-22T15:01:00Z", "2026-10-26T21:33:00Z", "Utilities Finance"),
    "invoices": ("2023-10-11T14:20:00Z", "2026-10-15T16:44:00Z", "Utilities Finance"),
}
WRITTEN = {
    F["reads"]: "2026-11-02T11:14:00Z", F["accounts"]: "2026-11-02T11:20:00Z", F["drs"]: "2026-11-03T14:02:00Z",
    F["gate"]: "2026-11-03T14:05:00Z", F["evc"]: "2026-11-03T14:31:00Z", F["airport"]: "2026-11-04T16:10:00Z",
    F["soil"]: "2026-11-04T16:22:00Z", F["loggers"]: "2025-05-09T19:41:00Z", F["workorders"]: "2026-11-05T13:08:00Z",
    F["rebates"]: "2026-11-05T13:40:00Z", F["cng"]: "2026-11-04T20:52:00Z",
}
WRITTEN = {k: dt.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc) for k, v in WRITTEN.items()}


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


# --------------------------------------------------------------------------------------------------- the frames
def register_frames(w, rng):
    pr = w.pr
    rows = []
    for _, p in pr.iterrows():
        tc = "Y" if p["tc"] else "N"
        if rng.random() < 0.006:
            tc = None
        loc = "Outside" if p["outdoor"] else "Inside"
        ex = p["exch_date"] if isinstance(p["exch_date"], dt.date) else None
        rows.append(dict(PremiseID=int(p["premise"]), PressureDistrict=P.DNAME[p["district"]],
                         ServiceClass="Residential" if p["cls"] == "RES" else "Commercial", Cycle=int(p["cycle"]),
                         MeterID=p["meter"], MeterModel=p["model"], TempComp=tc, MeterLocation=loc,
                         MeterSetDate=p["installed"], Multiplier=int(p["multiplier"]),
                         PreviousMeterID=p["old_meter"] if ex else None, PreviousModel=p["old_model"] if ex else None,
                         PreviousSetDate=p["old_installed"] if ex else None, ExchangeDate=ex))
    prem = pd.DataFrame(rows)
    models = pd.DataFrame([
        dict(Model="S175", Type="Diaphragm, 175 cfh", TempComp="N", InService="1979 to 1996"),
        dict(Model="D250", Type="Diaphragm, 250 cfh", TempComp="N", InService="1988 to 2008"),
        dict(Model="D275", Type="Diaphragm, 275 cfh", TempComp="N", InService="1996 to 2008"),
        dict(Model="D250TC", Type="Diaphragm, 250 cfh, temperature compensated", TempComp="Y", InService="2009 on"),
        dict(Model="D275TC", Type="Diaphragm, 275 cfh, temperature compensated", TempComp="Y", InService="2009 on"),
        dict(Model="D425", Type="Diaphragm, 425 cfh", TempComp="N", InService="1985 to 2008"),
        dict(Model="D630", Type="Diaphragm, 630 cfh", TempComp="N", InService="1985 to 2008"),
        dict(Model="D425TC", Type="Diaphragm, 425 cfh, temperature compensated", TempComp="Y", InService="2009 on"),
        dict(Model="D630TC", Type="Diaphragm, 630 cfh, temperature compensated", TempComp="Y", InService="2009 on")])
    st = []
    for d in P.DISTRICTS:
        for s in d["drs"]:
            st.append(dict(Station=s, PressureDistrict=d["name"], OutletPressurePsig=int(round(w.press_nom[s])),
                           Corrector="EVC-I" if s in P.PT_ONLY_STATIONS else "EVC-II", MeteringSince="2021"))
    stations = pd.DataFrame(st)
    ev = w.evc
    corr = pd.DataFrame(dict(Account=ev["account"], PressureDistrict=ev["district"].map(P.DNAME),
                             DeliveryPressurePsig=ev["press"], MeterLocation=np.where(ev["outdoor"], "Outside", "Inside"),
                             Corrector="EVC-I"))
    return prem, models, stations, corr


def airport(w, rng):
    tavg = w.air + rng.normal(0, 0.7, w.D)
    df = pd.DataFrame(dict(NAME="BRANDVOLD REGIONAL AIRPORT, MN US", DATE=w.dates,
                           PRCP=np.round(w.precip, 2), SNOW=np.round(w.snowfall, 1), SNWD=w.snow_depth.astype(int),
                           TAVG=np.round(tavg).astype(int), TMAX=np.round(w.tmax).astype(int),
                           TMIN=np.round(w.tmin).astype(int)))
    df = df.astype(object)
    miss = rng.random(w.D) < 0.006
    df.loc[miss, "TAVG"] = None
    df.loc[rng.random(w.D) < 0.01, "SNWD"] = None
    return df


def soil(w, rng):
    out = []
    for i in range(w.D):
        r = dict(Date=w.dates[i], AirMaxF=round(float(w.tmax[i] + rng.normal(0, 1.0)), 1),
                 AirMinF=round(float(w.tmin[i] + rng.normal(0, 1.0)), 1), PrecipIn=round(float(w.precip[i]), 2),
                 SnowDepthIn=int(max(0, round(w.snow_depth[i] + rng.normal(0, 0.8)))))
        for lab, arr in (("Soil2in", w.s2), ("Soil4in", w.s4), ("Soil8in", w.s8), ("Soil20in", w.s20),
                         ("Soil40in", w.s40)):
            v = float(arr[i] + rng.normal(0, 0.25))
            r[lab + "F"] = "M" if rng.random() < 0.01 else round(v, 1)
        out.append(r)
    return pd.DataFrame(out)


def damage(w, rng):
    rows = []
    no = 23001
    for e in sorted(w.damage, key=lambda e: e["day"]):
        d = w.dates[e["day"]]
        rows.append(dict(ReportNo="DMG-%d" % no, Date=d, PressureDistrict=P.DNAME[e["district"]],
                         Facility=str(rng.choice(["Service line", "Service line", "Main"])),
                         Material=str(rng.choice(["PE", "PE", "Coated steel", "Bare steel"])),
                         Excavator=str(rng.choice(["Contractor", "Contractor", "Homeowner", "Municipal"])),
                         LocateTicket=bool(rng.random() < 0.7),
                         MinutesToControl=int(rng.integers(25, 160)),
                         EstimatedGasLostMcf=int(e["reported"])))
        no += 1
    return pd.DataFrame(rows)


def own_use(w):
    rows = []
    months = pd.period_range(P.MON0, P.SIM1, freq="M")
    for d in P.DISTRICTS:
        for s in d["drs"]:
            for m in months:
                msk = (w.days.year == m.year) & (w.days.month == m.month)
                hdd = float(w.hdd60[msk].sum())
                est = (0.15 * msk.sum() + 0.012 * hdd) if m.month in (10, 11, 12, 1, 2, 3, 4) else 0.0
                rows.append(dict(Month=str(m), Facility="Regulator station heater %s" % s,
                                 PressureDistrict=d["name"], EstimatedMcf=round(est, 1)))
    for m in months:
        msk = (w.days.year == m.year) & (w.days.month == m.month)
        rows.append(dict(Month=str(m), Facility="City gate line heater", PressureDistrict=None,
                         EstimatedMcf=round(float(w.gate_heater[msk].sum()), 0)))
    return pd.DataFrame(rows)


def rp_cases(w, rng):
    pr = w.pr
    rows = []
    for k, c in enumerate(sorted(w.bypass_hist, key=lambda c: c["found"])):
        i = c["i"]
        d1 = (c["found"] - P.SIM0).days
        months = c["months"]
        if d1 > 0:
            d0 = max(0, d1 - months * 30)
            unreg = float((w.U[i, d0:d1].sum() - w.R[i, d0:d1].sum() * P.PF / 10.0) * 10)
        else:
            unreg = float(rng.uniform(300, 900))
        rows.append(dict(CaseNo="RP-%04d" % (311 + k), PremiseID=int(pr.at[i, "premise"]),
                         PressureDistrict=P.DNAME[pr.at[i, "district"]], FoundDate=c["found"],
                         Finding="Bypass pipe around meter" if c["kind"] == "full" else
                         "Furnace supply tapped ahead of meter",
                         EstimatedMonths=months, BackBilledCcf=int(round(max(unreg, 0) / 10) * 10),
                         Notes="Meter reset and sealed" if c["kind"] == "full" else
                         "Water heater and range stayed on the meter; tap removed"))
    return pd.DataFrame(rows)


def lauf_report(w, reads, F0):
    rows = [["FY2019", 1755230, 1704980, 13820, 36430, 2.08], ["FY2020", 1728410, 1681020, 13510, 33880, 1.96],
            ["FY2021", 1790650, 1741770, 14100, 34780, 1.94], ["FY2022", 1831940, 1774630, 14390, 42920, 2.34],
            ["FY2023", 1712280, 1660240, 13660, 38380, 2.24]]
    gate = w.gate
    own = F0["own_use"]
    for fy, (a, b) in P.FY.items():
        g = float(gate[(gate["GasDay"] >= a) & (gate["GasDay"] <= b)]["CorrectedMcf"].sum())
        r = reads[(reads["ReadDate"] >= a) & (reads["ReadDate"] <= b)]
        sales = float(r["ConsumptionCcf"].sum()) * P.PF / 10.0
        ev = w.evc_rec
        sales += float(ev[(ev["GasDay"] >= a) & (ev["GasDay"] <= b)]["CorrectedMcf"].sum())
        ow = own[(own["Month"] >= "%d-%02d" % (a.year, a.month)) & (own["Month"] <= "%d-%02d" % (b.year, b.month))]
        cu = float(ow["EstimatedMcf"].sum())
        lauf = g - sales - cu
        rows.append([fy, round(g), round(sales), round(cu), round(lauf), round(100 * lauf / g, 2)])
    return rows


def distractors(w, rng):
    pr = w.pr
    reb = []
    for (i, d, f) in w.rebates:
        reb.append(dict(RebateNo="R%05d" % (4100 + len(reb)), PremiseID=int(pr.at[i, "premise"]),
                        InstallDate=d, Equipment=str(rng.choice(["Furnace 96% AFUE", "Furnace 97% AFUE",
                                                                  "Boiler 95% AFUE"])),
                        RebateUSD=int(rng.choice([300, 400, 400, 500]))))
    for _ in range(140):
        i = int(rng.integers(0, len(pr)))
        reb.append(dict(RebateNo="R%05d" % (4100 + len(reb)), PremiseID=int(pr.at[i, "premise"]),
                        InstallDate=w.dates[int(rng.integers(100, w.D - 10))],
                        Equipment=str(rng.choice(["Water heater 0.67 UEF", "Smart thermostat", "Water heater 0.70 UEF"])),
                        RebateUSD=int(rng.choice([50, 75, 100]))))
    for c in w.dualfuel:
        if c["rebated"]:
            reb.append(dict(RebateNo="R%05d" % (4100 + len(reb)), PremiseID=int(pr.at[c["i"], "premise"]),
                            InstallDate=c["conv"], Equipment="Dual-fuel heat pump controls",
                            RebateUSD=int(rng.choice([250, 300]))))
    reb = pd.DataFrame(reb).sort_values(["InstallDate", "PremiseID"], kind="mergesort").reset_index(drop=True)
    reb["RebateNo"] = ["R%05d" % (4100 + k) for k in range(len(reb))]    # numbered in the order applications closed
    cng = []
    for i in range(w.D):
        if w.dates[i] < dt.date(2024, 1, 2) or w.days[i].dayofweek >= 6:
            continue
        for _ in range(int(rng.integers(3, 11))):
            cng.append(dict(Date=w.dates[i], Fleet=str(rng.choice(["City refuse", "Transit", "School district",
                                                                     "Parks"])),
                            GGE=round(float(rng.uniform(8, 36)), 2), Dispenser=int(rng.integers(1, 3))))
    cng = pd.DataFrame(cng)
    inv = []
    g = w.gate
    for m in pd.period_range("2023-09", "2026-09", freq="M"):
        msk = pd.to_datetime(g["GasDay"]).dt.to_period("M") == m
        dth = float(g.loc[msk, "Dth"].sum())
        inv.append(dict(Month=str(m), DeliveredDth=round(dth), CommodityUSD=round(dth * float(rng.uniform(2.4, 4.6)), 2),
                        ReservationUSD=184250.00, FuelRetainedDth=round(dth * 0.0081)))
    return reb, cng, pd.DataFrame(inv)


def study_stats(w, airport_df):
    lg = w.loggers.copy()
    pr = w.pr.set_index("premise")
    lg["loc"] = lg["PremiseID"].map(lambda p: "Outside" if pr.at[p, "outdoor"] else "Inside")
    ap = airport_df.set_index("DATE")["TAVG"]
    lg["air"] = lg["Date"].map(ap)
    out = lg[(lg["loc"] == "Outside") & lg["air"].notna()]
    x = out["air"].astype(float).values
    y = out["GasTempF"].values
    b, a = np.polyfit(x, y, 1)
    r2 = 1 - ((y - (a + b * x)) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    months = []
    for m in pd.period_range("2024-11", "2025-04", freq="M"):
        mm = pd.to_datetime(lg["Date"]).dt.to_period("M") == m
        am = (pd.to_datetime(airport_df["DATE"]).dt.to_period("M") == m)
        months.append([m.strftime("%B %Y"), "%.1f" % airport_df.loc[am, "TAVG"].dropna().astype(float).mean(),
                       "%.1f" % lg.loc[mm & (lg["loc"] == "Outside"), "GasTempF"].mean(),
                       "%.1f" % lg.loc[mm & (lg["loc"] == "Inside"), "GasTempF"].mean(), str(int(mm.sum()))])
    n_out = lg.loc[lg["loc"] == "Outside", "LoggerID"].nunique()
    n_in = lg.loc[lg["loc"] == "Inside", "LoggerID"].nunique()
    return dict(a=a, b=b, r2=r2, n_days=len(out), months=months, n=n_out + n_in, n_out=n_out, n_in=n_in,
                dropout="%s" % lg["LoggerID"].iloc[0].split("-")[1])


def lauf2019():
    rng = np.random.default_rng([P.SEED, 30])
    months = []
    tot_eff = 0.0
    tot_vol = 0.0
    norm = [45.1, 27.6, 12.9, 7.4, 11.8, 25.3, 42.6, 56.2, 66.0, 70.8, 68.9, 58.9]
    names = ["October 2018", "November 2018", "December 2018", "January 2019", "February 2019", "March 2019",
             "April 2019", "May 2019", "June 2019", "July 2019", "August 2019", "September 2019"]
    vols = [52100, 103400, 151800, 176900, 158300, 129600, 73400, 39800, 24100, 20400, 20900, 27300]
    for nm, t, v in zip(names, norm, vols):
        t = t + float(rng.normal(0, 1.2))
        eff = v * (P.R_BASE / (t + 459.67) - 1)
        months.append([nm, "%.1f" % t, "{:,.0f}".format(v), "{:,.0f}".format(eff)])
        tot_eff += eff
        tot_vol += v
    rec = 1755230
    lauf = 36430
    comps = [["Temperature effect, meters without compensation", "{:,.0f}".format(tot_eff), "%.2f" % (100 * tot_eff / rec)],
             ["Billing lag (bills issued against gas delivered)", "2,940", "%.2f" % (100 * 2940 / rec)],
             ["Leakage (survey leak counts at industry factors)", "4,880", "%.2f" % (100 * 4880 / rec)],
             ["Third-party damage", "610", "0.03"],
             ["Unexplained", "{:,.0f}".format(lauf - tot_eff - 2940 - 4880 - 610),
              "%.2f" % (100 * (lauf - tot_eff - 2940 - 4880 - 610) / rec)],
             ["Lost and unaccounted-for gas", "{:,.0f}".format(lauf), "%.2f" % (100 * lauf / rec)]]
    return dict(months=months, components=comps, lauf=lauf, lauf_pct=100 * lauf / rec)


def frames(w):
    rng = np.random.default_rng([P.SEED, 40])
    F0 = {}
    reads = RC.reads(w)
    F0["reads_clean"] = reads
    prem, models, stations, corr = register_frames(w, rng)
    F0.update(register=prem, models=models, stations=stations, correctors=corr)
    acc = w.accounts.copy()
    acc["AccountClass"] = acc["cls"].map({"RES": "Residential", "COM": "Commercial"})
    F0["accounts"] = acc[["AccountID", "PremiseID", "AccountClass", "StartDate", "EndDate"]]
    F0["drs"] = w.drs
    F0["gate"] = w.gate
    F0["evc"] = w.evc_rec
    F0["airport"] = airport(w, rng)
    F0["soil"] = soil(w, rng)
    F0["loggers"] = w.loggers
    F0["damage"] = damage(w, rng)
    F0["own_use"] = own_use(w)
    wo = w.workorders.copy()
    F0["workorders"] = wo
    F0["plan2027"] = w.plan2027
    F0["rp_cases"] = rp_cases(w, rng)
    F0["rebates"], F0["cng"], F0["invoices"] = distractors(w, rng)
    F0["lauf_report"] = lauf_report(w, reads, F0)
    F0["study"] = study_stats(w, F0["airport"])
    F0["lauf2019"] = lauf2019()
    return F0


def write(w, F0, target):
    os.makedirs(target, exist_ok=True)
    out = {k: os.path.join(target, v) for k, v in F.items()}
    counts = {}
    reads = F0["reads_clean"].copy()
    # the June 2025 extract was re-run and both runs' rows were kept
    dup = reads[(reads["ReadDate"] >= dt.date(2025, 6, 1)) & (reads["ReadDate"] <= dt.date(2025, 6, 30))]
    reads = pd.concat([reads, dup]).sort_values(["ReadDate", "Cycle", "PremiseID"], kind="mergesort")
    counts["reads"] = _csv(out["reads"], reads)
    counts["accounts"] = _csv(out["accounts"], F0["accounts"].sort_values(["PremiseID", "StartDate"], key=lambda s: s.map(
        lambda v: v if isinstance(v, dt.date) else dt.date(1900, 1, 1)) if s.name == "StartDate" else s))
    counts["drs"] = _csv(out["drs"], F0["drs"])
    counts["gate"] = _csv(out["gate"], F0["gate"])
    counts["evc"] = _csv(out["evc"], F0["evc"])
    counts["airport"] = _csv(out["airport"], F0["airport"])
    counts["soil"] = _csv(out["soil"], F0["soil"])
    counts["loggers"] = _csv(out["loggers"], F0["loggers"])
    wo = F0["workorders"].copy()
    counts["workorders"] = _csv(out["workorders"], wo)
    counts["rebates"] = _csv(out["rebates"], F0["rebates"])
    counts["cng"] = _csv(out["cng"], F0["cng"])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Premises"
    _df_sheet(ws, F0["register"], [11, 16, 12, 7, 11, 10, 9, 11, 12, 10, 14, 13, 14, 13])
    _df_sheet(wb.create_sheet("Meter models"), F0["models"], [10, 40, 10, 14])
    _df_sheet(wb.create_sheet("Regulator stations"), F0["stations"], [10, 16, 18, 10, 13])
    _df_sheet(wb.create_sheet("Corrector accounts"), F0["correctors"], [10, 16, 18, 14, 10])
    wb.save(out["register"])
    counts["register"] = len(F0["register"])
    wb = openpyxl.Workbook()
    _df_sheet(wb.active, F0["damage"], [12, 11, 16, 13, 13, 12, 12, 16, 18])
    wb.active.title = "Damage reports"
    wb.save(out["damage"])
    wb = openpyxl.Workbook()
    _df_sheet(wb.active, F0["own_use"], [10, 34, 16, 14], title="Utility own use, estimated",
              note="Station heaters: rated input times heating hours from the month's degree days. Gate line heater: "
                   "estimated from throughput.")
    wb.active.title = "Own use"
    wb.save(out["own_use"])
    wb = openpyxl.Workbook()
    _df_sheet(wb.active, F0["plan2027"], [9, 11, 14, 11, 10, 13, 12], title="2027 meter changeout plan",
              note="Set from the 2026 capital budget. Crews work routes in the order shown. The heating season begins "
                   "November 1.")
    wb.active.title = "Plan"
    wb.save(out["plan2027"])
    wb = openpyxl.Workbook()
    _df_sheet(wb.active, F0["rp_cases"], [10, 11, 16, 12, 34, 15, 14, 44])
    wb.active.title = "Cases"
    wb.save(out["rp_cases"])
    wb = openpyxl.Workbook()
    _sheet(wb.active, ["Fiscal year", "City gate receipts Mcf", "Sales Mcf", "Company use Mcf", "LAUF Mcf", "LAUF %"],
           F0["lauf_report"], [12, 20, 14, 16, 12, 9], title="Lost and unaccounted-for gas, fiscal years ending September 30",
           note="Sales: volume billed on bills issued in the fiscal year (registered ccf times the pressure factor) and "
                "corrector customers' corrected volume. Company use: station heaters and the gate line heater.")
    wb.active.title = "LAUF"
    wb.save(out["lauf_report"])
    wb = openpyxl.Workbook()
    _df_sheet(wb.active, F0["invoices"], [10, 14, 16, 16, 16])
    wb.active.title = "Invoices"
    wb.save(out["invoices"])
    for k, (c0, c1, who) in OFFICE.items():
        postprocess.normalize_ooxml(out[k], who, who, c0, c1, excel=True, company=ORG)
    DC.rules(out["rules"])
    DC.lauf_study(out["lauf_study"], F0["lauf2019"])
    DC.study_memo(out["study_memo"], F0["study"])
    DC.rate_schedules(out["tariff"])
    postprocess.own_mtimes(target, WRITTEN)
    return counts
