"""task5 architecture 3: the golden deliverables, computed from the pack as written to disk.

ctf_certification_december_2026.xlsx: the certification, each county's December 2026 jobs from the reports in hand,
the jobs estimated for employers whose report had not arrived, the December 2026 total and the change on December 2025,
the designated counties, a chart of the changes against the line, and how the outstanding reports were estimated.
ctf_employer_jobs_december_2026.csv: every liable employer, a row for each county it employs in."""
import csv
import os

import numpy as np
import pandas as pd

import methods as M
import world as W

KIND_TEXT = {
    "reported": "reported",
    "batch": "estimated: its usual transmission had not arrived",
    "habitual": "estimated: reports after the cutoff every quarter",
    "alone": "estimated: missing from a transmission that arrived, or late for the first time",
    "two_q": "estimated: no report for the third quarter either",
    "new": "estimated: new employer, no report yet",
}


def load_pack(folder):
    rd = lambda k, **kw: pd.read_csv(os.path.join(folder, W.FILES[k]), dtype=str, keep_default_na=False, **kw)
    rep = rd("reports")
    for c in ("year", "quarter", "month1_employment", "month2_employment", "month3_employment"):
        rep[c] = rep[c].astype(int)
    ws = rd("worksites")
    for c in ("year", "quarter", "m1_emp", "m2_emp", "m3_emp"):
        ws[c] = ws[c].astype(int)
    return M.Pack(rep, rd("accounts"), rd("status"), ws, rd("counties"), rd("naics"))


def compute(pk):
    """the golden: every county's figures, the designated set, the outcome shares and the employer rows"""
    g = M.county_change(pk, {})
    ratios = pk.route_ratios(dict(M.GOLDEN))
    v = pk.view(W.FLASH_Q)
    rec = v["rec"]
    reported = {c: 0.0 for c in pk.codes}
    for a_, c, e in g["rows"]:
        if g["kind"][a_] == "reported":
            reported[c] += e
    counts = pd.Series(g["kind"]).value_counts().to_dict()
    by_county_kind = {}
    for a_, c, e in g["rows"]:
        k = g["kind"][a_]
        by_county_kind.setdefault((c, k), [0, 0.0])
        by_county_kind[(c, k)][0] += 1
        by_county_kind[(c, k)][1] += e
    out = dict(change=g["change"], total=g["total"], imputed=g["imputed"], base=g["base"], reported=reported,
               designated=M.designated(g["change"]), ratios={str(k): float(x) for k, x in ratios.items() if np.isfinite(x)},
               kind=g["kind"], rows=g["rows"], counts=counts, by_county_kind=by_county_kind,
               n_liable=len(v["liable"]), n_received=len(rec), n_missing=len(v["missing"]))
    return out


def round_jobs(x):
    return int(round(x / 100.0)) * 100


def write_employers(pk, G, path):
    rows = []
    acc = pk.a
    for a_, c, e in sorted(G["rows"], key=lambda r: (r[0], r[1])):
        k = G["kind"][a_]
        rows.append((acc.loc[a_, "account_no"], acc.loc[a_, "legal_name"], c, W.NAMES[c],
                     "Y" if k == "reported" else "N",
                     "%.1f" % e,
                     KIND_TEXT[k]))
    with open(path, "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, lineterminator="\r\n")
        wr.writerow(["account_no", "legal_name", "county_code", "county", "report_received", "december_2026_jobs", "basis"])
        wr.writerows(rows)
    return len(rows)


def write_certification(pk, G, path):
    import openpyxl
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.chart.label import DataLabelList
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Certification"
    bold = Font(bold=True)
    ws["A1"] = "Community Transition Fund: December covered employment, fund year 2027"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Franklin Department of Labor, Labor Market Information. Certified to the Community Transition Fund Board under section 5 of the Act."
    ws["A3"] = "From the quarterly contribution reports received by February 15, 2027. Covered employment for the pay period including the 12th of the month, by worksite county."
    des = [W.NAMES[c] for c in G["designated"]]
    ws["A5"] = "Counties designated under section 4 (December 2026 at least 2.0 percent below December 2025): " + (", ".join(des) if des else "none")
    ws["A5"].font = bold
    head = ["County code", "County", "December 2025 jobs", "December 2026 jobs, reports received",
            "December 2026 jobs, estimated for employers whose report had not arrived", "December 2026 jobs",
            "Change on December 2025 (%)", "Designated"]
    hr = 7
    for k, h in enumerate(head):
        cell = ws.cell(row=hr, column=k + 1, value=h)
        cell.font = bold
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.border = Border(bottom=Side(style="thin"))
        cell.fill = PatternFill("solid", fgColor="E7EEF5")
    r = hr + 1
    for c in W.CODES:
        ch = round(G["change"][c] + 1e-9, 1) + 0.0
        vals = [c, W.NAMES[c], round_jobs(G["base"][c]), round_jobs(G["reported"][c]), round_jobs(G["imputed"][c]),
                round_jobs(G["total"][c]), ch, "Yes" if c in G["designated"] else "No"]
        for k, v in enumerate(vals):
            cell = ws.cell(row=r, column=k + 1, value=v)
            if k in (2, 3, 4, 5):
                cell.number_format = "#,##0"
            if k == 6:
                cell.number_format = "0.0"
        if c in G["designated"]:
            for k in range(8):
                ws.cell(row=r, column=k + 1).font = bold
        r += 1
    last = r - 1
    st = sum(G["base"].values()), sum(G["reported"].values()), sum(G["imputed"].values()), sum(G["total"].values())
    ws.cell(row=r, column=2, value="State").font = bold
    for k, v in enumerate(st):
        cell = ws.cell(row=r, column=3 + k, value=round_jobs(v))
        cell.number_format = "#,##0"
        cell.font = bold
    cell = ws.cell(row=r, column=7, value=round(100 * (st[3] / st[0] - 1) + 1e-9, 1))
    cell.number_format = "0.0"
    cell.font = bold
    ws.cell(row=r + 2, column=1, value="Jobs are rounded to the nearest hundred, so a county's two parts may not add to its "
                                        "total; the change is computed before rounding.")
    ws.cell(row=r + 3, column=1, value="Prepared by %s, %s, February 26, 2027." % W.PEOPLE["lmi_director"][:2])
    # chart data: county and change, with the line, beside the table
    ws.cell(row=hr, column=11, value="County").font = bold
    ws.cell(row=hr, column=12, value="Change on December 2025 (%)").font = bold
    ws.cell(row=hr, column=13, value="Designation line, -2.0%").font = bold
    for k_ in (11, 12, 13):
        ws.cell(row=hr, column=k_).alignment = Alignment(wrap_text=True, vertical="top")
    for i, c in enumerate(W.CODES):
        ws.cell(row=hr + 1 + i, column=11, value=W.NAMES[c])
        ws.cell(row=hr + 1 + i, column=12, value=round(G["change"][c] + 1e-9, 1) + 0.0).number_format = "0.0"
        ws.cell(row=hr + 1 + i, column=13, value=W.THRESHOLD).number_format = "0.0"
    bar = BarChart()
    bar.type = "col"
    bar.title = "Garrow and Ostrom are the only counties below the -2.0% line"
    bar.y_axis.title = "Change in covered jobs, December 2026 on December 2025 (%)"
    bar.y_axis.number_format = "0.0"
    data = Reference(ws, min_col=12, min_row=hr, max_row=hr + len(W.CODES))
    cats = Reference(ws, min_col=11, min_row=hr + 1, max_row=hr + len(W.CODES))
    bar.add_data(data, titles_from_data=True)
    bar.set_categories(cats)
    bar.dataLabels = DataLabelList()
    bar.dataLabels.showVal = True
    line = LineChart()
    line.add_data(Reference(ws, min_col=13, min_row=hr, max_row=hr + len(W.CODES)), titles_from_data=True)
    line.series[0].graphicalProperties.line.solidFill = "C00000"
    line.series[0].graphicalProperties.line.dashStyle = "dash"
    # the designated counties' columns in their own colour, every other county's in one quiet one
    from openpyxl.chart.marker import DataPoint
    ser = bar.series[0]
    ser.graphicalProperties.solidFill = "8497B0"
    ser.graphicalProperties.line.solidFill = "8497B0"
    for i, c in enumerate(W.CODES):
        if c in G["designated"]:
            pt = DataPoint(idx=i)
            pt.graphicalProperties.solidFill = "A9332B"
            pt.graphicalProperties.line.solidFill = "A9332B"
            ser.dPt.append(pt)
    bar += line
    bar.legend.position = "b"
    bar.height, bar.width = 9.5, 22
    ws.add_chart(bar, "A%d" % (r + 6))
    ws.freeze_panes = "A%d" % (hr + 1)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_area = "A1:H%d" % (r + 26)
    for k, wdt in enumerate([11, 13, 13, 16, 22, 13, 13, 11, 3, 3, 13, 11, 9]):
        ws.column_dimensions[openpyxl.utils.get_column_letter(k + 1)].width = wdt
    ws.row_dimensions[hr].height = 62
    # how the outstanding reports were estimated
    es = wb.create_sheet("Estimation")
    es["A1"] = "December 2026 jobs for employers whose report had not arrived by February 15, 2027"
    es["A1"].font = Font(bold=True, size=12)
    rr = G["ratios"]
    lines = [
        ("Liable employer accounts, fourth quarter 2026", G["n_liable"]),
        ("Reports received by the cutoff", G["n_received"]),
        ("Reports outstanding", G["n_missing"]),
    ]
    for i, (a, b) in enumerate(lines):
        es.cell(row=3 + i, column=1, value=a)
        es.cell(row=3 + i, column=2, value=b).number_format = "#,##0"
    es["A7"] = "Outstanding report"
    es["B7"] = "Employers"
    es["C7"] = "Estimated December jobs"
    es["D7"] = "How estimated"
    for c_ in ("A7", "B7", "C7", "D7"):
        es[c_].font = bold
    how = {
        "batch": "September 2026 jobs moved by the change of the reporting employers in the county and supersector "
                 "(an employer's own December-to-September pattern where it runs a seasonal business)",
        "habitual": "as above",
        "alone": "September 2026 jobs times %.2f, the share of September jobs kept in December by employers in the same "
                 "position at the 2024Q1 to 2025Q3 cutoffs, every one of them since resolved" % rr.get("('alone', 'all')", float("nan")),
        "two_q": "last reported jobs times %.3f, measured the same way" % rr.get("('two_q', 'all')", float("nan")),
        "new": "the average December jobs of the quarter's new employers that did report",
    }
    present = [k for k in ("batch", "habitual", "alone", "two_q", "new")
               if sum(v[0] for (c, kk), v in G["by_county_kind"].items() if kk == k)]
    for i, k in enumerate(present):
        n_ = int(G["counts"].get(k, 0))                 # accounts, each counted once whatever its counties
        j_ = sum(v[1] for (c, kk), v in G["by_county_kind"].items() if kk == k)
        es.cell(row=8 + i, column=1, value=KIND_TEXT[k].replace("estimated: ", "").capitalize())
        es.cell(row=8 + i, column=2, value=n_).number_format = "#,##0"
        es.cell(row=8 + i, column=3, value=round_jobs(j_)).number_format = "#,##0"
        es.cell(row=8 + i, column=4, value=how[k])
        es.cell(row=8 + i, column=4).alignment = Alignment(wrap_text=True, vertical="top")
    tr = 8 + len(present)
    es.cell(row=tr, column=1, value="Total").font = bold
    es.cell(row=tr, column=2, value=int(sum(int(G["counts"].get(k, 0)) for k in present))).number_format = "#,##0"
    es.cell(row=tr, column=3, value=round_jobs(sum(v[1] for (c, kk), v in G["by_county_kind"].items()
                                                   if kk in present))).number_format = "#,##0"
    for k_ in (2, 3):
        es.cell(row=tr, column=k_).font = bold
    es.cell(row=tr + 2, column=1, value="An employer with worksites in more than one county is counted once here and listed "
                                        "once for each of its counties in %s." % W.DELIVERABLES["employers"])
    es.column_dimensions["A"].width = 46
    es.column_dimensions["B"].width = 11
    es.column_dimensions["C"].width = 14
    es.column_dimensions["D"].width = 80
    wb.save(path)


def build(pack_dir, out_dir):
    pk = load_pack(pack_dir)
    G = compute(pk)
    os.makedirs(out_dir, exist_ok=True)
    write_certification(pk, G, os.path.join(out_dir, W.DELIVERABLES["cert"]))
    n = write_employers(pk, G, os.path.join(out_dir, W.DELIVERABLES["employers"]))
    G["n_employer_rows"] = n
    return pk, G
