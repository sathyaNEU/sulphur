"""task19: every file under target/, written from the simulated world as each system or office exports it."""
import datetime as dt
import os

import openpyxl
from openpyxl.styles import Alignment, Font

import docs as DC
import params as PR
import postprocess
import records as RC

ORG = {"KHS": "Kilvarra Health Service", "KSO": "Kilvarra Statistics Office", "KBA": "Kilvarra Border Agency",
       "DF": "Defence Forces", "HEA": "Higher Education Authority", "LGGC": "Local Government Grants Commission"}
FILES = {
    "register": "KHS_register_extract_2026-06-30.csv",
    "practices": "KHS_practices_2026-06.csv",
    "postcodes": "KSO_postcode_directory_2026-06.csv",
    "blocks": "CS26_blocks.csv",
    "persons": "CS26_persons.csv",
    "followup": "CS26_register_followup.csv",
    "review": "CS26_clerical_review.csv",
    "vital": "KSO_vital_statistics_2026.xlsx",
    "border": "KBA_permit_holder_movements_2021-07_to_2026-06.csv",
    "defence": "DF_personnel_by_location_2026-06-30.csv",
    "accounts": "KSO_population_accounts_2021-2026.xlsx",
    "census": "KSO_census2021_usual_residents.xlsx",
    "link": "KHS_census2021_link_study.csv",
    "listsize": "KHS_list_size_quarterly_2021-2026.csv",
    "he": "HEA_enrolments_2025-26.csv",
    "circular": "LGGC_2026-14_grant_determination_population_basis.pdf",
}
DISTRACTORS = ["census", "link", "listsize", "he"]
IST = dt.timezone(dt.timedelta(hours=1))
GMT = dt.timezone.utc
WRITTEN = {   # each export's own last save, in the producing office's local time
    "register": dt.datetime(2026, 7, 3, 6, 12, 41, tzinfo=IST),
    "practices": dt.datetime(2026, 7, 3, 6, 13, 9, tzinfo=IST),
    "postcodes": dt.datetime(2026, 6, 26, 15, 48, 3, tzinfo=IST),
    "blocks": dt.datetime(2026, 5, 22, 11, 31, 56, tzinfo=IST),
    "persons": dt.datetime(2026, 9, 29, 16, 4, 27, tzinfo=IST),
    "followup": dt.datetime(2026, 10, 14, 10, 22, 35, tzinfo=IST),
    "review": dt.datetime(2026, 10, 27, 14, 57, 18, tzinfo=GMT),
    "border": dt.datetime(2026, 7, 8, 8, 2, 50, tzinfo=IST),
    "defence": dt.datetime(2026, 7, 14, 12, 40, 11, tzinfo=IST),
    "link": dt.datetime(2023, 11, 20, 17, 15, 6, tzinfo=GMT),
    "listsize": dt.datetime(2026, 7, 9, 9, 26, 38, tzinfo=IST),
    "he": dt.datetime(2026, 3, 13, 13, 44, 2, tzinfo=GMT),
}
OFFICE = {   # created, modified (UTC), last saved by, organisation
    "vital": ("2019-03-11T10:02:00Z", "2026-08-19T13:47:00Z", "Vital Statistics", "KSO"),
    "accounts": ("2022-08-24T09:12:00Z", "2026-08-27T15:21:00Z", "Population Statistics", "KSO"),
    "census": ("2022-06-14T08:40:00Z", "2022-11-02T16:05:00Z", "Census Division", "KSO"),
}


def _csv(path, df):
    df.to_csv(path, index=False, lineterminator="\r\n", encoding="utf-8")
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
    ws.freeze_panes = ws.cell(row=r0 + 1, column=1)


def write(W, target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    O = W["other"]
    counts = {}
    counts["register"] = _csv(F["register"], W["register_df"])
    counts["practices"] = _csv(F["practices"], W["practice_df"])
    counts["postcodes"] = _csv(F["postcodes"], W["postcodes"])
    counts["blocks"] = _csv(F["blocks"], W["blocks_df"])
    counts["persons"] = _csv(F["persons"], W["survey_df"])
    counts["followup"] = _csv(F["followup"], W["followup_df"])
    counts["review"] = _csv(F["review"], W["gold_df"])
    counts["border"] = _csv(F["border"], O["border"])
    counts["defence"] = _csv(F["defence"], O["defence"])
    counts["link"] = _csv(F["link"], O["link2021"])
    counts["listsize"] = _csv(F["listsize"], O["listsize"])
    counts["he"] = _csv(F["he"], O["he"])

    # vital statistics
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Births"
    b = O["births"]
    _sheet(ws, list(b.columns), b.values.tolist(), [24, 10, 10, 10], title="Live births registered in Kilvarra, by sex",
           note="2026: births registered January to June, provisional. Source: Kilvarra Statistics Office, civil registration.")
    ws = wb.create_sheet("Deaths")
    d = O["deaths"]
    _sheet(ws, list(d.columns), d.values.tolist(), [16, 14, 10, 10],
           title="Deaths registered in Kilvarra, by sex and age at death, years to 30 June",
           note="Source: Kilvarra Statistics Office, civil registration.")
    ws = wb.create_sheet("Life table 2019-21")
    lt = O["lifetable"]
    _sheet(ws, list(lt.columns), lt.values.tolist(), [8, 12, 12, 12, 12],
           title="National life table 2019-2021: probability of dying within a year (qx) and survivors (lx)",
           note="Source: Kilvarra Statistics Office. Published 4 October 2022.")
    wb.save(F["vital"])
    counts["vital"] = len(b) + len(d) + len(lt)

    # population accounts: the rolled-forward national series
    a = O["accounts"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "National"
    _sheet(ws, list(a.columns), a.values.tolist(), [16, 14, 10, 10, 16, 18, 12, 14],
           title="Kilvarra population accounts: usual residents at 30 June, rolled forward from the 2021 Census",
           note="Population at 30 June 2021 from the 2021 Census. Components from civil registration, health register "
                "and border records. Source: Kilvarra Statistics Office, 27 August 2026.")
    wb.save(F["accounts"])
    counts["accounts"] = len(a)

    # 2021 Census usual residents
    c = O["census"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Usual residents 2021"
    _sheet(ws, ["District code", "District", "Age group", "Males", "Females"], c.values.tolist(), [12, 16, 10, 10, 10],
           title="2021 Census: usual residents by district, age group and sex (estimates after coverage adjustment)",
           note="Census day 21 March 2021. Source: Kilvarra Statistics Office.")
    wb.save(F["census"])
    counts["census"] = len(c)

    DC.write(F["circular"])
    for k, (created, modified, who, org) in OFFICE.items():
        postprocess.normalize_ooxml(F[k], who, who, created, modified, excel=True, company=ORG[org])
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in WRITTEN.items()})
    return counts
