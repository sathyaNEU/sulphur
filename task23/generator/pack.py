"""task23 architecture 1: the pack's data files under target/, each written the way its system exports it (CSV
from the operational systems, workbooks from the people who keep them, through the house container writer)."""
import datetime as dt
import math
import os

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Font

import params as P
import postprocess
import records as RC
import world as WD

TONS = 1.0 / 0.90718474


def history(W):
    r = W.streams["docs"]
    rows = []
    for y in range(1986, 2021):
        for c in P.CELLS:
            i0 = WD.month_index(y, 1)
            vals = {mat: float(W.tonnes[c][mat][i0:i0 + 12].sum()) * TONS for mat in P.SHARE}
            if sum(vals.values()) <= 0:
                continue
            basis = "scale records"
            if y in (1991, 1992):
                basis = "estimated (scale replaced)"
                vals = {k: v * (1 + r.normal(0, 0.03)) for k, v in vals.items()}
            rows.append([y, c, round(vals["MSW"]), round(vals["CD"]), round(vals["BIO"]), round(vals["SOIL"]),
                         round(vals["SPEC"]), basis])
    return pd.DataFrame(rows, columns=["year", "cell", "msw_tons", "cd_tons", "biosolids_tons", "soil_tons",
                                       "special_tons", "basis"])


def cells_sheet(W):
    rows = []
    liners = {1: dt.date(1985, 10, 15), 2: dt.date(1995, 3, 30), 3: dt.date(2004, 7, 22), 4: dt.date(2012, 11, 9),
              5: dt.date(2024, 10, 31)}
    first = {c: dt.date(*P.CELLS[c]["open"], 1) + dt.timedelta(days=d) for c, d in zip(P.CELLS, (6, 3, 4, 1, 2))}
    last = {1: dt.date(1995, 6, 28), 2: dt.date(2004, 9, 29), 3: dt.date(2013, 3, 27), 4: dt.date(2025, 1, 31),
            5: None}
    for c, d in P.CELLS.items():
        cap = d["capped"]
        rows.append([c, liners[c], first[c], last[c] if last[c] else "filling", round(d["area"] / 4046.86, 1),
                     dt.date(cap[0], cap[1], 1) if cap else "",
                     {1: "final cover, 40-mil LLDPE geomembrane", 2: "final cover, 40-mil LLDPE geomembrane",
                      3: "final cover, 40-mil LLDPE geomembrane", 4: "intermediate cover, 18 in soil",
                      5: "active; daily and interim cover"}[c]])
    df = pd.DataFrame(rows, columns=["cell", "liner_constructed", "first_waste", "last_waste", "footprint_acres",
                                     "final_cover_completed", "cover_2026"])
    # the last-waste date of cell 5 stays open while it fills
    return df


def fill_plan(W):
    rows = []
    for i in range(WD.month_index(2026, 11), WD.month_index(2028, 1)):
        y, m = WD.month_of_index(i)
        v = {mat: float(W.tonnes[5][mat][i]) * TONS for mat in P.SHARE}
        lift = "5-L%d" % RC.lift_of(dt.date(y, m, 15))
        rows.append(["%04d-%02d" % (y, m), int(round(v["MSW"], -1)), int(round(v["CD"], -1)), int(round(v["BIO"], -1)),
                     int(round(v["SOIL"], -1)), int(round(v["SPEC"], -1)), lift])
    return pd.DataFrame(rows, columns=["month", "msw_tons", "cd_tons", "biosolids_tons", "soil_tons", "special_tons",
                                       "lift"])


def frames(W):
    F = {}
    F["tickets"] = RC.tickets(W)
    F["history"] = history(W)
    F["cells"] = cells_sheet(W)
    F["dailylog"] = RC.daily_log(W)
    F["scada"] = RC.scada(W)
    F["wells"] = RC.readings(W)
    F["register"] = RC.register(W)
    F["workorders"] = RC.work_orders(W)
    F["recirc"] = RC.recirc_log(W)
    F["weather"] = RC.weather(W)
    F["chambers"] = RC.chambers(W)
    F["campaigns"] = RC.campaigns(W)
    F["drone"] = RC.drone(W)
    F["oxplots"] = RC.ox_plots(W)
    F["fillplan"] = fill_plan(W)
    F["groundwater"] = RC.groundwater(W)
    F["leachate"] = RC.leachate(W)
    F["sem"] = RC.sem(W)
    F["odor"] = RC.odor(W)
    return F


def _sheet(ws, df, widths=None, title=None):
    r0 = 1
    if title:
        ws.cell(row=1, column=1, value=title).font = Font(bold=True)
        r0 = 3
    for j, col in enumerate(df.columns, 1):
        c = ws.cell(row=r0, column=j, value=col)
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, row in enumerate(df.itertuples(index=False), r0 + 1):
        for j, v in enumerate(row, 1):
            if isinstance(v, float) and math.isnan(v):
                v = None
            if isinstance(v, (np.integer,)):
                v = int(v)
            if isinstance(v, (np.floating,)):
                v = float(v)
            if isinstance(v, pd.Timestamp):
                v = v.date()
            ws.cell(row=i, column=j, value=v)
            if isinstance(v, dt.date):
                ws.cell(row=i, column=j).number_format = "yyyy-mm-dd"
    for j, col in enumerate(df.columns, 1):
        wd = (widths or {}).get(col, max(10, min(40, len(str(col)) + 2)))
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = wd
    ws.freeze_panes = ws.cell(row=r0 + 1, column=1)


# each export's own save time (CSV files carry no stamp of their own: the time their system wrote them)
CSV_STAMPS = {
    "tickets": dt.datetime(2026, 11, 3, 16, 41, 12, tzinfo=P.UTC),
    "dailylog": dt.datetime(2026, 11, 3, 17, 2, 47, tzinfo=P.UTC),
    "scada": dt.datetime(2026, 11, 3, 15, 18, 5, tzinfo=P.UTC),
    "wells": dt.datetime(2026, 11, 4, 18, 27, 33, tzinfo=P.UTC),
    "workorders": dt.datetime(2026, 11, 4, 19, 55, 9, tzinfo=P.UTC),
    "recirc": dt.datetime(2026, 11, 4, 16, 6, 51, tzinfo=P.UTC),
    "weather": dt.datetime(2026, 11, 2, 22, 13, 40, tzinfo=P.UTC),
    "chambers": dt.datetime(2026, 11, 2, 23, 48, 2, tzinfo=P.UTC),
    "campaigns": dt.datetime(2026, 9, 18, 20, 31, 26, tzinfo=P.UTC),
    "oxplots": dt.datetime(2020, 1, 29, 23, 11, 54, tzinfo=P.UTC),
    "groundwater": dt.datetime(2026, 10, 21, 17, 44, 30, tzinfo=P.UTC),
    "leachate": dt.datetime(2026, 11, 4, 21, 3, 17, tzinfo=P.UTC),
    "sem": dt.datetime(2026, 10, 6, 18, 39, 58, tzinfo=P.UTC),
    "odor": dt.datetime(2026, 11, 3, 18, 21, 4, tzinfo=P.UTC),
}


def write(W, F, target):
    os.makedirs(target, exist_ok=True)
    f = {k: os.path.join(target, v) for k, v in P.FILES.items()}
    counts = {}

    def csv(key, df):
        df.to_csv(f[key], index=False, date_format="%Y-%m-%d", lineterminator="\r\n" if key in ("tickets", "dailylog") else "\n")
        counts[P.FILES[key]] = len(df)

    t = F["tickets"].copy()
    csv("tickets", t)
    csv("dailylog", F["dailylog"])
    csv("scada", F["scada"])
    csv("wells", F["wells"])
    csv("workorders", F["workorders"])
    csv("recirc", F["recirc"])
    csv("weather", F["weather"])
    csv("chambers", F["chambers"])
    camp = F["campaigns"].drop(columns=["_i0", "_i1"])
    csv("campaigns", camp)
    csv("oxplots", F["oxplots"])
    csv("groundwater", F["groundwater"])
    csv("leachate", F["leachate"])
    csv("sem", F["sem"])
    csv("odor", F["odor"])

    # workbooks
    books = {}
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tonnage by cell"
    _sheet(ws, F["history"])
    ws2 = wb.create_sheet("Cells")
    _sheet(ws2, F["cells"], widths={"cover_2026": 38})
    wb.save(f["history"])
    books["history"] = ("Patrice Lindgren", "2015-02-17T18:20:00Z", "2021-03-02T23:41:16Z", P.ORG)
    counts[P.FILES["history"]] = len(F["history"])

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Wells"
    _sheet(ws, F["register"], widths={"notes": 44})
    wb.save(f["register"])
    books["register"] = (P.ENGINEER, "2016-06-03T20:12:44Z", "2026-10-29T22:07:51Z", P.ORG)
    counts[P.FILES["register"]] = len(F["register"])

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Flights"
    dr = F["drone"].drop(columns=["_i0", "_i1"])
    _sheet(ws, dr)
    wb.save(f["drone"])
    books["drone"] = (P.ENGINEER, "2024-05-16T00:31:09Z", "2026-08-11T19:46:22Z", P.ORG)
    counts[P.FILES["drone"]] = len(dr)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cell 5 receipts"
    _sheet(ws, F["fillplan"])
    wb.save(f["fillplan"])
    books["fillplan"] = ("Carla Ibsen", "2026-10-06T16:58:37Z", "2026-10-27T21:14:05Z", P.ORG)
    counts[P.FILES["fillplan"]] = len(F["fillplan"])
    for k, (who, c0, c1, org) in books.items():
        postprocess.normalize_ooxml(f[k], who, who, c0, c1, excel=True, company=org)
    return counts, {P.FILES[k]: v for k, v in CSV_STAMPS.items()}
