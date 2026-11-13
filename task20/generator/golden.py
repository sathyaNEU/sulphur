"""The golden deliverables: the treasury workbook with the stress year's daily path, and the note."""
import datetime as dt
from docx import Document
from docx.shared import Pt, Mm
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import common as C
from common import mi, mi_date, month_hours, year_months

XLSX = "hallingvass_margin_facility_2027.xlsx"
NOTE = "margin_facility_2027_note.docx"


def workbook(F, R, path):
    g = R["golden_path"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    bold = Font(bold=True)
    rows = [("Stress requirement 2027 (EUR m)", F["peak_m"]), ("Date of the peak", F["peak_date"]),
            ("Facility required (EUR m, next EUR 50 m)", F["facility_m"]), ("Facility committed for 2026 (EUR m)", F["facility_2026_m"]),
            ("", ""), ("At the peak", ""),
            ("Exchange book still to deliver, 2027 (TWh)", F["book_peak_2027_twh"]),
            ("Exchange book, 2028 (TWh)", F["book_peak_2028_twh"]), ("Exchange book, 2029 (TWh)", F["book_peak_2029_twh"]),
            ("Exchange book, 2030 (TWh)", F["book_peak_2030_twh"]), ("Initial margin (EUR m)", F["im_peak_m"]),
            ("", ""), ("1 January to the peak", ""),
            ("Variation margin paid (EUR m)", F["vm_m"]), ("Delivery settlement paid (EUR m)", F["dlv_m"]),
            ("Initial margin added (EUR m)", F["dim_m"]), ("Day-ahead purchases less sales (EUR m)", F["da_net_m"]),
            ("Customer payments received (EUR m)", F["rec_m"]), ("Output (GWh)", F["out_gwh"]),
            ("", ""), ("Hedge ratio at 31 December 2026 (policy basis)", ""),
            ("2027 (%)", F["ratio_2027_pct"]), ("2028 (%)", F["ratio_2028_pct"]), ("2029 (%)", F["ratio_2029_pct"]),
            ("", ""), ("2022 check (end-2021 book through 2022)", ""),
            ("Records: largest cumulative net outflow (EUR m)", F["c22_actual_m"]), ("Records: date", F["c22_actual_date"]),
            ("This method on the end-2021 book (EUR m)", F["c22_method_m"]), ("This method: date", F["c22_method_date"])]
    for a, b in rows:
        ws.append([a, b])
        if b == "" and a:
            ws.cell(row=ws.max_row, column=1).font = bold
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 16
    p = wb.create_sheet("Daily path")
    p.append(["Date", "Variation margin", "Delivery settlement", "Initial margin", "Initial margin change",
              "Day-ahead purchases less sales", "Customer payments", "Net outflow", "Cumulative net outflow"])
    for c in p[1]:
        c.font = bold
    cum = 0.0
    for i, d in enumerate(g["days"]):
        net = g["vm"][i] + g["dlv"][i] + g["dim"][i] - g["da"][i] - g["rec"][i]
        cum += net
        p.append([d, round(g["vm"][i] / 1e6, 3), round(g["dlv"][i] / 1e6, 3), round(g["im"][i] / 1e6, 3),
                  round(g["dim"][i] / 1e6, 3), round(-g["da"][i] / 1e6, 3), round(g["rec"][i] / 1e6, 3),
                  round(net / 1e6, 3), round(cum / 1e6, 3)])
        p.cell(row=p.max_row, column=1).number_format = "yyyy-mm-dd"
    p.column_dimensions["A"].width = 12
    for col in "BCDEFGHI":
        p.column_dimensions[col].width = 15
    b = wb.create_sheet("Book")
    b.append(["Month end", "2027 (MW)", "2028 (MW)", "2029 (MW)", "2030 (MW)"])
    for c in b[1]:
        c.font = bold
    last = {}
    for i, d in enumerate(g["days"]):
        last[d.month] = i
    for m in range(1, 13):
        i = last[m]
        mw = g["book"]["mw_by_day"][i]
        b.append([g["days"][i]] + [round(-sum(mw.get(k, 0.0) for k in year_months(y) if mi_date(k + 1) > g["days"][i])
                                         / max(1, sum(1 for k in year_months(y) if mi_date(k + 1) > g["days"][i])), 1)
                                   for y in (2027, 2028, 2029, 2030)])
        b.cell(row=b.max_row, column=1).number_format = "yyyy-mm-dd"
    r = wb.create_sheet("Margin rates")
    r.append(["Date", "Base Month (EUR/MWh)", "Base Quarter (EUR/MWh)", "Base Year (EUR/MWh)"])
    for c in r[1]:
        c.font = bold
    for i, d in enumerate(g["days"]):
        r.append([d] + [round(float(g["rates"][t][i]), 2) for t in "MQY"])
        r.cell(row=r.max_row, column=1).number_format = "yyyy-mm-dd"
    o = wb.create_sheet("Output")
    o.append(["Month", "Output (GWh)"])
    for c in o[1]:
        c.font = bold
    acc = {}
    for c_, v in g["out_day"].items():
        if c_.year == 2027:
            acc[c_.month] = acc.get(c_.month, 0.0) + v
    for m in range(1, 13):
        o.append([dt.date(2027, m, 1).strftime("%b %Y"), round(acc[m] / 1e3, 1)])
    wb.save(path)


def note(F, R, path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(22)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    doc.add_heading("Margin facility for 2027", 1)
    doc.add_paragraph(
        "Commit EUR %d million for 2027, up from EUR %d million. In a year whose prices and inflows repeat 2022, the "
        "hedge program's cumulative net cash outflow peaks at EUR %.1f million on %s; the standard rounds that up to "
        "the next EUR 50 million." % (F["facility_m"], F["facility_2026_m"], F["peak_m"], F["peak_date"]))
    doc.add_paragraph(
        "By the peak we would have paid EUR %.1f million of variation margin, EUR %.1f million of delivery settlement "
        "and EUR %.1f million of extra initial margin, and bought EUR %.1f million more power day-ahead than we sold, "
        "against EUR %.1f million received from customers." % (F["vm_m"], F["dlv_m"], F["dim_m"], F["da_net_m"], F["rec_m"]))
    doc.add_paragraph(
        "Five things set the size. The desk keeps selling: once a year contract trades a quarter above its budget "
        "price it moves that year to the policy maximum, three points a week, so at the peak the exchange book holds "
        "%.2f TWh of 2028, %.2f TWh of 2029 and %.2f TWh of 2030. The Fjordal contract is fixed-price and counts "
        "towards the ratio, so the exchange book is the ratio less that contract (2027 stood at %.1f per cent at the "
        "year end, %.1f per cent of it on the exchange)." % (F["book_peak_2028_twh"], F["book_peak_2029_twh"],
                                                              F["book_peak_2030_twh"], F["ratio_2027_pct"], F["ratio_ex_2027_pct"]))
    doc.add_paragraph(
        "NEX sets each class's rate at the %dth percentile of the front contract's two-day moves over the last %d "
        "business days, reviewed on Thursdays and changed when more than %d per cent off; initial margin at the peak "
        "is EUR %.1f million. Replaying 2022's own rates as a share of price would put it at EUR %.1f million, "
        "because 2022's look-back still held December 2021." % (F["rule_q_pct"], F["rule_look"], F["rule_band_pct"],
                                                               F["im_peak_m"], F["pct2022_im_m"]))
    doc.add_paragraph(
        "Storage opens the year at %d GWh, close to the licence floor of %d GWh, so the dry spring holds output to "
        "%s GWh by the peak and we buy the shortfall against our supply contracts at the spring's prices. Hallingvass "
        "Straum pays the average system price of the %d months ending %d months before delivery, so its payments lag "
        "the spike." % (F["storage_open_gwh"], F["floor_gwh"], F["out_gwh_txt"], F["aff_window"], F["aff_lag"]))
    doc.add_paragraph(
        "Check: the same method on the end-2021 book through 2022 gives EUR %.1f million on %s; the 2022 records show "
        "EUR %.1f million on %s." % (F["c22_method_m"], F["c22_method_date"], F["c22_actual_m"], F["c22_actual_date"]))
    doc.save(path)
