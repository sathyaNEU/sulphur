"""task14: every file under target/, written from the simulated world as each system or office exports it."""
import datetime as dt
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font

import panelfile as PF
import params as P
import postprocess
import registry as RG
import world as WD

ORG_TBB = "Tenancy Bond Board"
ORG_PSO = "Penmarra Statistics Office"
FILES = {
    "legacy": "tbb_legacy_register_extract_2023-03-05.csv",
    "online": "tbb_bond_events_2023-03-06_to_2026-11-27.csv",
    "xwalk": "tbb_landlord_id_crosswalk_2023-03-06.csv",
    "codes": "tbb_code_lists.xlsx",
    "conc": "pso_suburb_region_concordance_2024.csv",
    "panel": "pso_rent_survey_2018q1_2026q3.csv",
    "pcodes": "pso_rent_survey_codes.csv",
    "series": "pso_private_rents_index_survey_2026q3.xlsx",
    "cpi": "pso_cpi_2026q3.xlsx",
    "method": "pso_private_rents_measure_definition.pdf",
    "hpi": "pso_house_price_index_2026q3.xlsx",
    "consents": "pso_building_consents_2019-01_2026-09.csv",
}
DISTRACTORS = ["hpi", "consents"]
NZT = dt.timezone(dt.timedelta(hours=13))
WRITTEN = {   # each file's own last save, in the producing office's local time
    "legacy": dt.datetime(2026, 9, 14, 10, 42, 17, tzinfo=NZT),
    "online": dt.datetime(2026, 11, 30, 7, 18, 52, tzinfo=NZT),
    "xwalk": dt.datetime(2023, 3, 6, 5, 51, 9, tzinfo=dt.timezone(dt.timedelta(hours=13))),
    "conc": dt.datetime(2024, 7, 1, 9, 12, 44, tzinfo=dt.timezone(dt.timedelta(hours=12))),
    "panel": dt.datetime(2026, 10, 2, 14, 7, 31, tzinfo=NZT),
    "pcodes": dt.datetime(2018, 2, 6, 11, 25, 3, tzinfo=NZT),
    "consents": dt.datetime(2026, 11, 2, 10, 55, 40, tzinfo=NZT),
}
OFFICE = {   # created, modified (UTC), last saved by
    "codes": ("2023-02-20T21:14:00Z", "2024-07-02T22:31:00Z", "Kim Chandler", ORG_TBB),
    "series": ("2018-07-30T22:05:00Z", "2026-10-27T20:48:00Z", "Christine Buckley", ORG_PSO),
    "cpi": ("2018-04-22T21:30:00Z", "2026-10-20T19:12:00Z", "Prices Statistics", ORG_PSO),
    "hpi": ("2019-02-11T20:40:00Z", "2026-11-04T21:03:00Z", "Housing Statistics", ORG_PSO),
}


def _csv(path, df, float_cols=None):
    float_cols = float_cols or {}
    df = df.copy()
    for c, f in float_cols.items():
        df[c] = df[c].map(lambda v: (f % v) if isinstance(v, (int, float, np.floating)) and v == v else v)
    df.to_csv(path, index=False, lineterminator="\r\n")
    return len(df)


def _sheet(ws, header, rows, widths=None, title=None, note=None):
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
    for j, w in enumerate(widths or [], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    ws.freeze_panes = ws.cell(row=r0 + 1, column=2)


def write(W, target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    counts = {}
    L, O, X = RG.build(W)
    W.legacy_df, W.online_df, W.xwalk_df = L, O, X
    counts["legacy"] = _csv(F["legacy"], L)
    counts["online"] = _csv(F["online"], O, {"weekly_rent": "%.2f"})
    counts["xwalk"] = _csv(F["xwalk"], X)
    # code lists
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Legacy record types"
    _sheet(ws, ["REC_TYPE", "Description"], [["L", "Lodgement"], ["A", "Additional bond"], ["T", "Transfer to new landlord"],
                                            ["P", "Change of tenant parties"], ["R", "Refund"]], [12, 34])
    ws = wb.create_sheet("Online event types")
    _sheet(ws, ["event", "Description"], [["LODGE", "Bond lodged"], ["MIGRATED", "Bond migrated from the legacy register"],
                                         ["TOPUP", "Additional bond lodged"], ["TRANSFER", "Bond transferred to new landlord"],
                                         ["PARTIES", "Change of tenant parties"], ["REFUND", "Bond refunded"]], [12, 40])
    ws = wb.create_sheet("Rent frequency")
    _sheet(ws, ["RENT_FREQ", "Description"], [["W", "Weekly"], ["F", "Fortnightly"], ["M", "Calendar monthly"]], [12, 24])
    ws = wb.create_sheet("Dwelling types")
    _sheet(ws, ["Legacy DWELLING", "Online dwelling_type", "Description"],
           [["H", "house", "House"], ["T", "townhouse", "Townhouse or unit"], ["F", "apartment", "Flat or apartment"],
            ["R", "room", "Room let under its own agreement"]], [16, 20, 34])
    ws = wb.create_sheet("Rental areas")
    _sheet(ws, ["AREA_CODE", "Rental area"], [[a[0], a[1]] for a in WD.OLD_AREAS], [12, 26])
    ws = wb.create_sheet("Regions")
    _sheet(ws, ["Region code", "Region", "In use from"], [[r[0], r[1], "2024-07-01"] for r in P.REGIONS], [12, 20, 12])
    wb.save(F["codes"])
    # concordance
    import pandas as pd
    conc = pd.DataFrame([[s["name"], s["postcode"], s["area"], dict((a[0], a[1]) for a in WD.OLD_AREAS)[s["area"]],
                          s["region"], dict((r[0], r[1]) for r in P.REGIONS)[s["region"]]] for s in W.suburbs],
                        columns=["suburb", "postcode", "rental_area_code", "rental_area", "region_code", "region"])
    conc = conc.sort_values(["region_code", "suburb"]).reset_index(drop=True)
    counts["conc"] = _csv(F["conc"], conc)
    # rent survey
    PNL = PF.build(W)
    W.panel_df = PNL
    counts["panel"] = _csv(F["panel"], PNL, {"weekly_rent": "%.2f"})
    pc = pd.DataFrame([["response", "R", "Rent reported"], ["response", "N", "No response"],
                       ["response", "V", "Vacant on the reference date"],
                       ["response", "O", "Out of scope: no longer let as a private rental"],
                       ["landlord_type", "I", "Individual or trust"], ["landlord_type", "C", "Company"],
                       ["agent_managed", "Y", "Managed by a letting agent"], ["agent_managed", "N", "Managed by the landlord"]],
                      columns=["field", "code", "label"])
    counts["pcodes"] = _csv(F["pcodes"], pc)
    # the published survey-based index
    quarters, idx = PF.published_series(PNL)
    W.published = idx
    W.published_quarters = quarters
    names = ["Penmarra"] + [r[1] for r in P.REGIONS]
    keys = ["NAT"] + P.REGION_CODES
    pubq = [q for q in quarters if (int(q[:4]), int(q[-1])) >= (2018, 2)]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Index"
    _sheet(ws, ["Quarter"] + names, [[q] + [round(idx[k][q], 1) for k in keys] for q in pubq], [10] + [15] * 8,
           title="Private rents index (rent survey), June 2018 quarter = 1000",
           note="Source: Penmarra Statistics Office, Rent Survey. Published 28 October 2026.")
    ws = wb.create_sheet("Annual change")
    anq = [q for q in pubq if (int(q[:4]), int(q[-1])) >= (2019, 2)]
    prev = {q: "%dQ%d" % (int(q[:4]) - 1, int(q[-1])) for q in anq}
    _sheet(ws, ["Quarter"] + names, [[q] + [round(100 * (idx[k][q] / idx[k][prev[q]] - 1), 1) for k in keys]
                                    for q in anq], [10] + [15] * 8,
           title="Private rents index (rent survey): annual change, per cent",
           note="Change from the same quarter of the previous year. Source: Penmarra Statistics Office, Rent Survey.")
    wb.save(F["series"])
    W.published_annual = {k: {q: round(100 * (idx[k][q] / idx[k][prev[q]] - 1), 1) for q in anq} for k in keys}
    # CPI release
    cpiq = sorted(P.CPI_YOY)
    lvl = {}
    base = {(2017, i): 1000.0 * (1 + 0.0045 * (i - 1)) for i in range(1, 5)}
    lvl.update(base)
    for (y, q) in cpiq:
        lvl[(y, q)] = lvl[(y - 1, q)] * (1 + P.CPI_YOY[(y, q)] / 100.0)
    rng = np.random.default_rng(P.SEED + 31)
    grp = {"Food": 0.9, "Housing and household utilities": 1.25, "Transport": 1.05, "Communication": 0.35}
    gl = {g: {(2017, i): 1000.0 for i in range(1, 5)} for g in grp}
    for (y, q) in cpiq:
        for g, m in grp.items():
            gl[g][(y, q)] = gl[g][(y - 1, q)] * (1 + (m * P.CPI_YOY[(y, q)] + rng.normal(0, 0.6)) / 100.0)
    rows = [["%dQ%d" % k, round(lvl[k], 1), P.CPI_YOY[k]] + [round(gl[g][k], 1) for g in grp] for k in cpiq]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "CPI"
    _sheet(ws, ["Quarter", "All groups index", "All groups annual change (%)"] + ["%s index" % g for g in grp], rows,
           [10, 16, 18, 12, 22, 14, 16], title="Consumers price index, 2017 = 1000",
           note="September 2026 quarter released 21 October 2026. Source: Penmarra Statistics Office.")
    wb.save(F["cpi"])
    # distractors: house prices and building consents
    hp = {}
    for ri, r in enumerate(P.REGIONS):
        lv = 1000.0
        hp[r[0]] = {}
        for y in range(2018, 2027):
            for q in range(1, 5):
                if (y, q) > (2026, 3):
                    break
                g = {2018: 0.05, 2019: 0.04, 2020: 0.09, 2021: 0.19, 2022: -0.06, 2023: -0.04, 2024: 0.01, 2025: 0.02,
                     2026: 0.015}[y] * (0.7 + 0.15 * (6 - ri) / 3)
                lv *= (1 + g / 4 + rng.normal(0, 0.006))
                hp[r[0]][(y, q)] = lv
    hq = sorted(hp["HC"])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "House prices"
    _sheet(ws, ["Quarter"] + [r[1] for r in P.REGIONS], [["%dQ%d" % k] + [round(hp[c][k], 1) for c in P.REGION_CODES]
                                                        for k in hq], [10] + [15] * 7,
           title="House price index (sales of dwellings), March 2018 quarter = 1000",
           note="Source: Penmarra Statistics Office, from settled sales recorded by the land registry.")
    wb.save(F["hpi"])
    rows = []
    for y in range(2019, 2027):
        for m in range(1, 13):
            if (y, m) > (2026, 9):
                break
            for ri, r in enumerate(P.REGIONS):
                for typ, base_ in (("house", 38), ("townhouse or unit", 22), ("apartment", 14)):
                    lam = base_ * r[2] * 7 * (1.3 if 2021 <= y <= 2023 else 1.0) * (1.6 if (typ == "apartment" and
                                                                                         r[0] in ("HC", "HE")) else 1.0)
                    rows.append(["%d-%02d" % (y, m), r[0], typ, int(rng.poisson(lam))])
    cons = pd.DataFrame(rows, columns=["month", "region_code", "dwelling_type", "dwellings_consented"])
    counts["consents"] = _csv(F["consents"], cons)
    import docs as DC
    DC.write_method(F["method"])
    for k, (created, modified, who, org) in OFFICE.items():
        postprocess.normalize_ooxml(F[k], who, who, created, modified, excel=True, company=org)
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in WRITTEN.items()})
    return counts
