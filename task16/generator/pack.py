"""task16 pack: the files the conversion team holds on 4 November 2026, each written the way its system exports it,
with each file's own save time."""
import datetime as dt
import os

import openpyxl
from openpyxl.styles import Alignment, Font

import docs as DC
import params as P
import postprocess

FILES = {
    "index_a": "calder_bay_patient_index_2026-11-02.csv",
    "index_b": "rosario_patient_index_20261102.csv",
    "merges": "calder_bay_merge_history_2006-2026.csv",
    "blood": "blood_bank_type_screen_2016-2026.csv",
    "deliveries": "labor_delivery_log_2006-2026.csv",
    "deaths": "death_notices_matched_2016-2026.csv",
    "names": "halvard_name_equivalence_table.csv",
    "pilot": "halvard_pilot_review_2026.xlsx",
    "spec": "halvard_match_6_specification.pdf",
    "policy": "patient_identity_policy_him-14.pdf",
    "plan": "one_chart_empi_conversion_plan.pdf",
    "volumes": "registration_volumes_2024-2026.xlsx",
    "dupreport": "rosario_duplicate_report_summary_2025-2026.xlsx",
}
DISTRACTORS = ["volumes", "dupreport", "deaths"]
CDT = dt.timezone(dt.timedelta(hours=-5))
CST = dt.timezone(dt.timedelta(hours=-6))
WRITTEN = {
    "index_a": dt.datetime(2026, 11, 2, 6, 14, 9, tzinfo=CST),
    "index_b": dt.datetime(2026, 11, 2, 7, 2, 41, tzinfo=CST),
    "merges": dt.datetime(2026, 11, 2, 6, 31, 55, tzinfo=CST),
    "blood": dt.datetime(2026, 11, 3, 9, 47, 12, tzinfo=CST),
    "deliveries": dt.datetime(2026, 11, 3, 10, 5, 38, tzinfo=CST),
    "deaths": dt.datetime(2026, 10, 30, 15, 22, 4, tzinfo=CDT),
    "names": dt.datetime(2026, 4, 17, 11, 40, 0, tzinfo=CDT),
}
OFFICE = {
    "pilot": ("2026-05-11T14:20:00Z", "2026-07-02T19:46:00Z", "Felicia Soto", "Halvard Identity"),
    "volumes": ("2024-02-05T15:02:00Z", "2026-11-03T16:18:00Z", "Patient Access", "Calder Rosario Health"),
    "dupreport": ("2025-02-03T17:40:00Z", "2026-11-02T21:05:00Z", "HIM Data Integrity", "Calder Rosario Health"),
}


def _csv(path, df):
    df.to_csv(path, index=False, lineterminator="\r\n")
    return len(df)


def _sheet(ws, df, widths=None, title=None, note=None):
    r0 = 1
    if title:
        ws.cell(row=1, column=1, value=title).font = Font(bold=True, size=12)
        r0 = 3
    for j, h in enumerate(df.columns, 1):
        c = ws.cell(row=r0, column=j, value=h)
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, row in enumerate(df.astype(object).where(df.notna(), None).values.tolist(), r0 + 1):
        for j, v in enumerate(row, 1):
            ws.cell(row=i, column=j, value=v)
    if note:
        ws.cell(row=r0 + len(df) + 2, column=1, value=note).font = Font(italic=True, size=8)
    for j, wd in enumerate(widths or [], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = wd
    ws.freeze_panes = ws.cell(row=r0 + 1, column=1)


def write(F, target):
    os.makedirs(target, exist_ok=True)
    out = {k: os.path.join(target, v) for k, v in FILES.items()}
    counts = {}
    for k in ("index_a", "index_b", "merges", "blood", "deliveries", "deaths", "names"):
        counts[k] = _csv(out[k], F[k])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reviewed pairs"
    _sheet(ws, F["pilot"], [10, 11, 13, 7, 10, 10, 10, 7, 10, 9, 9, 18, 12, 12],
           title="Halvard Match pilot, Calder Bay and Rosario indexes: candidate pairs in the review band")
    wb.save(out["pilot"])
    counts["pilot"] = len(F["pilot"])
    wb = openpyxl.Workbook()
    wb.active.title = "New registrations"
    _sheet(wb.active, F["volumes"], [10, 14, 18], title="New patient registrations by month")
    wb.save(out["volumes"])
    wb = openpyxl.Workbook()
    wb.active.title = "Monthly report"
    _sheet(wb.active, F["dupreport"], [13, 14, 10, 15, 16], title="Rosario potential duplicate report: monthly worklist")
    wb.save(out["dupreport"])
    for k, (c0, c1, who, org) in OFFICE.items():
        postprocess.normalize_ooxml(out[k], who, who, c0, c1, excel=True, company=org)
    DC.spec(out["spec"])
    DC.policy(out["policy"])
    DC.plan(out["plan"])
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in WRITTEN.items()})
    return counts
