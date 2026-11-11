"""task10 architecture 7: the golden deliverables, as Wealdmoor's DSO planning team would hand them to the December
capital expenditure review: the assessment workbook (the primaries with a chart, whether more flexibility could stand in,
the demand side, the customers, the sites still to come, what each shortcut would have committed) and six slides."""
import datetime as dt
import os

import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Emu, Pt

import postprocess as PP

ORG = "Wealdmoor Power Networks plc"
F_XLSX = "halverton_primary_assessment_2027-28.xlsx"
F_PPTX = "capex_review_2027-28.pptx"
# the workbook was started the Monday after the asset register was extracted and last saved two days later; the
# deck was built from it next
BOOK_CREATED = dt.datetime(2026, 11, 5, 10, 22, 0, tzinfo=dt.timezone.utc)
BOOK_SAVED = dt.datetime(2026, 11, 9, 11, 41, 9, tzinfo=dt.timezone.utc)
DECK_CREATED = dt.datetime(2026, 11, 6, 13, 48, 0, tzinfo=dt.timezone.utc)
DECK_SAVED = dt.datetime(2026, 11, 9, 15, 12, 44, tzinfo=dt.timezone.utc)
HEAD_FONT = Font(name="Calibri", bold=True, size=11)
HEAD_FILL = PatternFill("solid", fgColor="DDEBF7")
# demand before flexibility, expected peak, nine design days in ten, firm capacity (a fixed order, checked for
# colour-blind separation; every bar carries its value)
PALETTE = ("2A78D6", "EB6834", "1BAF7A", "EDA100")
TOTAL = 6     # slides in the deck


def _z(t):
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _head(ws, hdr, widths, height=48):
    ws.append(hdr)
    for c in ws[1]:
        c.font = HEAD_FONT
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, wd in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    ws.row_dimensions[1].height = height
    ws.freeze_panes = "A2"


def _formats(ws, fmts, first=2):
    """Number formats by column letter, from row `first` down."""
    for col, fmt in fmts.items():
        for cell in ws[col][first - 1:]:
            if isinstance(cell.value, (int, float)):
                cell.number_format = fmt
                cell.alignment = Alignment(horizontal="right")


def _join(names):
    names = list(names)
    if not names:
        return "none"
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def write_workbook(G, F, path):
    names = F["order"]
    Z = F["zones"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Primaries"
    _head(ws, ["Constraint managed zone", "Primary substation", "Provider", "Design-day demand, winter 2025/26 (MW)",
               "Customers on the growth register add by 15 January 2028 (MW)",
               "Design-day demand before flexibility, winter 2027/28 (MW)", "Contracted 2027/28 (MW)",
               "In service on 15 January 2028 (MW)", "Share of MW in service available on the design day",
               "Delivered 17:00 to 18:00, design day (MW)", "Half-hour of the day's peak with flexibility (ending)",
               "Expected peak with flexibility (MW)", "Peak not exceeded on nine design days in ten (MW)",
               "Firm capacity (MW)", "Design days over firm capacity (%)", "Reinforce",
               "Further flexibility on the 2027/28 award's terms that would hold it within one design day in ten (MW)"],
          [24, 18, 26, 13, 15, 15, 12, 13, 13, 13, 13, 13, 14, 10, 12, 10, 20], height=76)
    for n in names:
        z = Z[n]
        prov = [p for p in F["providers"] if n in F["providers"][p]["zones"]][0]
        fu = F["r12_further"].get(n)
        ws.append(["%s CMZ" % n, n, z["provider"], F["r1_demand_2526"][n], F["r2_connections"][n], F["r3_before"][n],
                   z["contracted"], F["r4_in_service"][n], F["r5_share"][prov], F["r6_delivered"][n], z["peak_hh"],
                   F["r8_peak"][n], F["r9_one_in_ten"][n], z["firm"], F["r10_share_over"][n], "Yes" if z["commit"] else "No",
                   "Not needed" if fu is None else ("No amount" if fu == "none" else fu)])
    k = len(names)
    _formats(ws, {"D": "0.0", "E": "0.0", "F": "0.0", "G": "0.0", "H": "0.0", "I": "0.00", "J": "0.0", "L": "0.0", "M": "0.0",
                  "N": "0.0", "O": "0", "Q": "0.0"})
    notes = [
        "Design day: a working weekday at a daily mean of minus 3.0 C at Halverton weather station, assessed as at "
        "15 January, with the 2027/28 contract instructed in full for the service window (WPN-NP-G-014, issue 5).",
        "Reinforce where the day's highest half-hour would exceed firm capacity on more than one design day in ten "
        "(guideline 7).",
        "In service on 15 January 2028: the megawatts in service on the asset register's extract of %s plus what the sites "
        "still to come can be expected to add by then, each on its asset class's record." % F["conventions"]["register_extract"],
        "Megawatts are rounded to one decimal after the arithmetic, so a figure can differ by 0.1 from the sum or "
        "difference of its rounded parts.",
    ]
    for i, t in enumerate(notes):
        ws.cell(row=k + 3 + i, column=1, value=t)
    ch = BarChart()
    ch.type = "col"
    ch.grouping = "clustered"
    ch.title = "%s exceed firm capacity on more than one design day in ten" % _join(F["call"])
    ch.y_axis.title = "MW, winter 2027/28 design day"
    ch.y_axis.number_format = "0"
    ch.y_axis.scaling.min = 0
    cats = Reference(ws, min_col=2, min_row=2, max_row=k + 1)
    for col in (6, 12, 13, 14):
        ch.add_data(Reference(ws, min_col=col, min_row=1, max_row=k + 1), titles_from_data=True)
    ch.set_categories(cats)
    for ser, colour in zip(ch.series, PALETTE):
        ser.graphicalProperties.solidFill = colour
        ser.graphicalProperties.line.solidFill = colour
    ch.legend.position = "b"
    ch.height, ch.width = 10.5, 24
    ws.add_chart(ch, "A%d" % (k + 9))

    fx = wb.create_sheet("Flexibility")
    call = F["call"]
    _head(fx, ["Primary substation", "Provider", "Contracted 2027/28 (MW)", "2027/28 award, of which the step over 2026/27 (MW)",
               "In service by 15 January 2028 per MW of that step", "Delivered at 17:00 to 18:00 per further MW",
               "Further MW on the award's terms for one design day in ten or fewer",
               "Lowest share of design days over firm any further contract reaches (%)", "Reached with a further (MW)"],
          [18, 26, 12, 14, 14, 14, 18, 18, 12], height=76)
    for n in call:
        z = Z[n]
        prov = [p for p in F["providers"] if n in F["providers"][p]["zones"]][0]
        fu, lo = F["r12_further"][n], F["r12_lowest"].get(n)
        fx.append([n, z["provider"], z["contracted"], z["award_step"], F["r12_per_mw"][n],
                   round(F["r12_per_mw"][n] * F["r5_share"][prov], 2), "No amount" if fu == "none" else fu,
                   lo["share_pct"] if lo else None, lo["at_mw"] if lo else None])
    _formats(fx, {"C": "0.0", "D": "0.0", "E": "0.00", "F": "0.00", "G": "0.0", "H": "0", "I": "0.0"})
    r0 = fx.max_row + 2
    fx.cell(row=r0, column=1, value="Each further megawatt is signed as the 2027/28 award was: the same kinds of site in the "
                                    "same proportions, planned for the same dates. The load that comes back after the window "
                                    "grows with every megawatt delivered, so beyond a point a larger contract raises the "
                                    "day's peak instead of lowering it.")
    sd = F["r13_detail"]
    r0 += 2
    fx.cell(row=r0, column=1, value="%s scheduled short of its contract for the whole window" % sd["primary"]).font = HEAD_FONT
    rows = [("Schedule giving the fewest design days over firm capacity (MW)", F["r13_schedule"]["schedule"], "0.0"),
            ("Expected peak at that schedule (MW)", sd["mean_peak"], "0.0"),
            ("Peak not exceeded on nine design days in ten at that schedule (MW)", F["r13_schedule"]["one_in_ten"], "0.0"),
            ("Design days over firm capacity at that schedule (%)", sd["share_pct"], "0"),
            ("Firm capacity (MW)", sd["firm"], "0.0"),
            ("Within one design day in ten at that schedule", "Yes" if sd["holds"] else "No", None),
            ("Contracted 2027/28 (MW), delivered when instructed in full (MW)", "%.1f, %.1f" % (sd["contracted"], sd["delivered_in_full"]), None)]
    for i, (label, val, fmt) in enumerate(rows):
        fx.cell(row=r0 + 1 + i, column=1, value=label)
        c = fx.cell(row=r0 + 1 + i, column=4, value=val)
        if fmt:
            c.number_format = fmt
            c.alignment = Alignment(horizontal="right")
    cd_ = F["r14_detail"]
    r0 += len(rows) + 3
    fx.cell(row=r0, column=1, value="%s with a %s kVA %s energised %s" % (cd_["primary"], "{:,}".format(cd_["kva"]),
                                                                          cd_["type"].lower(), cd_["energised"])).font = HEAD_FONT
    rows = [("Adds to the evening peak by 15 January 2028 (MW)", F["r14_customer"]["adds"], "0.0"),
            ("Of its type's established draw reached by then (%)", cd_["build_up_pct"], "0"),
            ("Type's established draw (kW per kVA of agreed capacity)", cd_["established_share"], "0.00"),
            ("Peak not exceeded on nine design days in ten with it (MW)", F["r14_customer"]["one_in_ten"], "0.0"),
            ("Firm capacity (MW)", cd_["firm"], "0.0"),
            ("Design days over firm capacity with it (%)", cd_["share_pct"], "0"),
            ("Within one design day in ten", "Yes" if cd_["holds"] else "No", None)]
    for i, (label, val, fmt) in enumerate(rows):
        fx.cell(row=r0 + 1 + i, column=1, value=label)
        c = fx.cell(row=r0 + 1 + i, column=4, value=val)
        if fmt:
            c.number_format = fmt
            c.alignment = Alignment(horizontal="right")

    dm = wb.create_sheet("Demand")
    _head(dm, ["Primary substation", "Working weekdays on record, three winters", "Of which at or below 0 C",
               "Working weekdays with no service, winter 2025/26", "Coldest of those (C)",
               "Morning demand rises per degree colder, above the knee (MW)",
               "Morning demand rises per degree colder, below the knee (MW)", "Knee (C)",
               "Design-day demand, winter 2025/26 (MW)", "Underlying growth to 2027/28 (%)",
               "Customers on the growth register add (MW)", "Design-day demand before flexibility, winter 2027/28 (MW)"],
          [18, 14, 12, 14, 11, 15, 15, 9, 13, 12, 13, 15], height=76)
    for n in names:
        z, c = Z[n], F["cold_end"][n]
        dm.append([n, z["working_weekdays"], z["at_or_below_freezing"], z["days_without_service_2526"],
                   z["coldest_without_service_2526"], c["per_degree_above"], c["per_degree_below"], c["knee_c"],
                   F["r1_demand_2526"][n], z["growth_pct"], F["r2_connections"][n], F["r3_before"][n]])
    _formats(dm, {"E": "0.0", "F": "0.00", "G": "0.00", "H": "0.0", "I": "0.0", "J": "0.0", "K": "0.0", "L": "0.0"})
    dm.cell(row=k + 3, column=1, value="Morning: the mean of the half-hours ending 07:00 to 15:30, before any service window. "
                                       "The evening is carried from the morning by the relation the days with no service show.")

    cu = wb.create_sheet("Customers")
    _head(cu, ["Primary substation", "Reference", "Customer type", "Agreed supply capacity (kVA)",
               "Energisation date (planned if not yet energised)", "On supply at the register's save",
               "Adds between 15 January 2026 and 15 January 2028 (MW)"], [18, 16, 22, 14, 16, 12, 16], height=62)
    for n in names:
        for r in F["customers"][n]:
            cu.append([n, r["reference"], r["type"], r["kva"], r["energised"], "Yes" if r["on_supply"] else "No", r["adds_mw"]])
    _formats(cu, {"D": "#,##0", "G": "0.00"})
    cu.auto_filter.ref = "A1:G%d" % cu.max_row

    st = wb.create_sheet("Sites")
    _head(st, ["Primary substation", "Asset class", "Sites still to come", "Registered (MW)",
               "Expected in service by 15 January 2028 (MW)", "Expected in service (%)"], [18, 30, 11, 12, 16, 12], height=62)
    for n in names:
        for cls, v in F["sites"][n].items():
            st.append([n, cls, v["sites"], v["mw"], v["expected_mw"], v["chance_pct"]])
    _formats(st, {"D": "0.00", "E": "0.00", "F": "0"})
    r0 = st.max_row + 3
    st.cell(row=r0 - 1, column=1, value="Every site on the register whose planned commissioning date has passed, by asset class")
    hdr = ["Asset class", "Sites", "Commissioned", "Withdrawn before commissioning", "Median days late, commissioned sites",
           "In service 150 days after the planned date (%)"]
    for j, h in enumerate(hdr):
        c = st.cell(row=r0, column=j + 1, value=h)
        c.font = HEAD_FONT
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, (cls, v) in enumerate(F["classes"].items()):
        for j, val in enumerate([cls, v["sites"], v["commissioned"], v["withdrawn"], v["median_days_late"],
                                 v["in_service_by_150_days_pct"]]):
            st.cell(row=r0 + 1 + i, column=j + 1, value=val)

    rt = wb.create_sheet("Routes")
    _head(rt, ["Route", "Would commit", "Primary substation", "Demand before flexibility (MW)",
               "Delivered 17:00 to 18:00 (MW)", "Expected peak (MW)", "Nine days in ten (MW)", "Firm capacity (MW)",
               "Design days over firm capacity (%)", "Reinforce"], [66, 40, 18, 13, 13, 11, 11, 10, 12, 10], height=62)
    gold_rows = {n: dict(before=F["r3_before"][n], delivered=F["r6_delivered"][n], peak=F["r8_peak"][n],
                         one_in_ten=F["r9_one_in_ten"][n], share_over=F["r10_share_over"][n], commit=Z[n]["commit"])
                 for n in names}
    shown = lambda s: s.replace("careful but hurried: ", "three of them together: ").replace("quick: ", "a first pass: ")
    for name, tab in [("Every result of this assessment", gold_rows)] + [(shown(k), v) for k, v in F["route_figures"].items()]:
        commit = _join(n for n in names if tab[n]["commit"])
        for n in names:
            t = tab[n]
            rt.append([name, commit, n, t["before"], t["delivered"], t["peak"], t["one_in_ten"], Z[n]["firm"], t["share_over"],
                       "Yes" if t["commit"] else "No"])
    _formats(rt, {"D": "0.0", "E": "0.0", "F": "0.0", "G": "0.0", "H": "0.0", "I": "0"})
    rt.auto_filter.ref = "A1:J%d" % rt.max_row
    wb.save(path)
    PP.normalize_ooxml(path, "Marion Todd", "Marion Todd", _z(BOOK_CREATED), _z(BOOK_SAVED), excel=True, company=ORG)


def _text(slide, left, top, width, height, lines, size=16, color=None):
    tb = slide.shapes.add_textbox(Emu(left), Emu(top), Emu(width), Emu(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        if color:
            p.font.color.rgb = RGBColor.from_string(color)
        p.space_after = Pt(6)
    return tb


def _title(slide, text, size, color="1F3864", top=300000, height=700000):
    t = slide.shapes.title
    t.left, t.top, t.width, t.height = Emu(600000), Emu(top), Emu(12192000 - 1200000), Emu(height)
    t.text = text
    tf = t.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = 1
    p.font.size = Pt(size)
    p.font.bold = True
    p.font.color.rgb = RGBColor.from_string(color)
    return t


def _strip(slide, n, total):
    _text(slide, 600000, 6420000, 12192000 - 1200000, 300000,
          ["Source: Halverton primary assessment workbook, DSO planning. WPN-NP-G-014 issue 5.   %d of %d" % (n, total)],
          size=10, color="7F7F7F")


def write_deck(G, F, path):
    names = F["order"]
    Z = F["zones"]
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[5]
    W_ = 12192000
    commit, hold = F["call"], F["hold"]
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}

    s = prs.slides.add_slide(blank)
    _title(s, "Halverton zone: commit %s reinforcements for winter 2027/28" % words.get(len(commit), str(len(commit))), 28,
           top=420000, height=900000)
    _text(s, 600000, 1500000, W_ - 1200000, 4600000, [
        "Commit reinforcement now at %s." % _join(commit),
        "%s within firm capacity on nine design days in ten with the flexibility contracted for 2027/28."
        % (_join(hold) + (" stays" if len(hold) == 1 else " stay")),
        "With each contract instructed in full on a minus 3 C working weekday, nine days in ten the peaks stay under %s."
        % _join("%.1f MW at %s (firm %.1f)" % (F["r9_one_in_ten"][n], n, Z[n]["firm"]) for n in commit),
        "%s: %.1f MW against %.1f MW firm." % (_join(hold), F["r9_one_in_ten"][hold[0]], Z[hold[0]]["firm"]) if len(hold) == 1
        else "The others stay under firm capacity.",
        "More flexibility is no substitute at %s; %s would need %.1f MW more on its 2027/28 award's terms."
        % (_join(n for n in commit if F["r12_further"][n] == "none"),
           _join(n for n in commit if F["r12_further"][n] != "none"),
           sum(F["r12_further"][n] for n in commit if F["r12_further"][n] != "none")),
        "DSO capital expenditure review, December 2026. Prepared by the Halverton DSO planning team."], size=18)
    _strip(s, 1, TOTAL)

    s = prs.slides.add_slide(blank)
    _title(s, "%s go over firm capacity on more than one design day in ten" % _join(commit), 22)
    cd = CategoryChartData()
    cd.categories = names
    cd.add_series("Demand before flexibility", [F["r3_before"][n] for n in names])
    cd.add_series("Expected peak with flexibility", [F["r8_peak"][n] for n in names])
    cd.add_series("Nine design days in ten", [F["r9_one_in_ten"][n] for n in names])
    cd.add_series("Firm capacity", [Z[n]["firm"] for n in names])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(700000), Emu(1100000), Emu(W_ - 1400000), Emu(5150000), cd)
    ch = gf.chart
    ch.value_axis.has_title = True
    ch.value_axis.axis_title.text_frame.text = "MW, winter 2027/28 design day"
    ch.value_axis.axis_title.text_frame.paragraphs[0].font.size = Pt(11)
    ch.value_axis.tick_labels.number_format = "0"
    ch.value_axis.tick_labels.number_format_is_linked = False
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    for ser, colour in zip(ch.plots[0].series, PALETTE):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = RGBColor.from_string(colour)
        ser.data_labels.show_value = True
        ser.data_labels.number_format = "0.0"
        ser.data_labels.number_format_is_linked = False
        ser.data_labels.font.size = Pt(9)
    _strip(s, 2, TOTAL)

    s = prs.slides.add_slide(blank)
    _title(s, "Demand: the cold end and the customers still building up carry %s" % _join(
        [n for n in ("Dunmore Street", "Charlecote Way") if n in commit]), 22)
    lines = []
    for n in names:
        z, c = Z[n], F["cold_end"][n]
        lines.append("%s: %.1f MW in 2025/26, %.1f MW before flexibility in 2027/28 (customers add %.1f MW)."
                     % (n, F["r1_demand_2526"][n], F["r3_before"][n], F["r2_connections"][n]))
    lines.append("No evening without a service in 2025/26 was colder than %s; the design day is at minus 3.0 C, so the cold "
                 "end is read from the mornings of all %d working weekdays on its record, which the service never touches."
                 % (_join("%.1f C at %s" % (Z[n]["coldest_without_service_2526"], n) for n in ("Dunmore Street",) if n in Z),
                    Z["Dunmore Street"]["working_weekdays"]))
    _text(s, 600000, 1150000, W_ - 1200000, 5200000, lines, size=16)
    _strip(s, 3, TOTAL)

    s = prs.slides.add_slide(blank)
    _title(s, "Flexibility: %.1f MW contracted, %.1f MW in service by 15 January 2028, %.1f MW delivered at the peak"
           % (F["totals"]["contracted"], F["totals"]["in_service"], F["totals"]["delivered"]), 22)
    lines = []
    for n in names:
        z = Z[n]
        t = "%s: %.1f MW contracted, %.1f MW in service, %.1f MW delivered at 17:00 to 18:00" % (
            n, z["contracted"], F["r4_in_service"][n], F["r6_delivered"][n])
        if z["peak_hh"] not in ("17:30", "18:00"):
            t += "; the day then peaks in the half-hour to %s at %.1f MW" % (z["peak_hh"], F["r8_peak"][n])
        lines.append(t + ".")
    slow = sorted(F["classes"].items(), key=lambda kv: -kv[1]["median_days_late"])[:2]
    lines.append("%s commission a median of %s days after the planned date; the Fenwick Street and Ashcombe Road awards are "
                 "made of them." % (_join(c for c, _ in slow).replace("Process load", "Process load sites").replace(
                     "Battery storage", "battery sites"), _join(str(v["median_days_late"]) for _, v in slow)))
    _text(s, 600000, 1150000, W_ - 1200000, 5200000, lines, size=16)
    _strip(s, 4, TOTAL)

    s = prs.slides.add_slide(blank)
    none_ = [n for n in commit if F["r12_further"][n] == "none"]
    some = [n for n in commit if F["r12_further"][n] != "none"]
    _title(s, "More flexibility would not hold %s: the load that comes back after the window caps it" % _join(none_), 22)
    sd, cd_ = F["r13_detail"], F["r14_detail"]
    lines = []
    for n in none_:
        lo = F["r12_lowest"][n]
        if lo["at_mw"] > 0:
            lines.append("%s: no further contract on its 2027/28 terms brings it within one design day in ten; the best any "
                         "size does is %d per cent of design days over firm (at %.1f MW more)." % (n, lo["share_pct"], lo["at_mw"]))
        else:
            lines.append("%s: every further MW on its 2027/28 terms only raises the peak after the window; as awarded it is "
                         "over firm on %d per cent of design days." % (n, lo["share_pct"]))
    for n in some:
        lines.append("%s: %.1f MW more on its 2027/28 terms would hold it within one design day in ten; about %.2f MW of "
                     "each further MW would be in service by 15 January 2028." % (n, F["r12_further"][n], F["r12_per_mw"][n]))
    lines.append("%s scheduled at %.1f MW for the whole window, not its %.1f MW in full, gives its lowest peak; nine days "
                 "in ten it still reaches %.1f MW against %.1f MW firm." % (
                     sd["primary"], F["r13_schedule"]["schedule"], sd["contracted"], F["r13_schedule"]["one_in_ten"], sd["firm"]))
    lines.append("%s would stay within firm capacity with a %s kVA %s energised %s: it adds %.1f MW by 15 January "
                 "2028 (%.1f MW nine days in ten against %.1f)." % (
                     cd_["primary"], "{:,}".format(cd_["kva"]), cd_["type"].lower(), cd_["energised"],
                     F["r14_customer"]["adds"], F["r14_customer"]["one_in_ten"], cd_["firm"]))
    _text(s, 600000, 1150000, W_ - 1200000, 5200000, lines, size=16)
    _strip(s, 5, TOTAL)

    s = prs.slides.add_slide(blank)
    _title(s, "Commit %s; keep %s on its flexibility contract" % (_join(commit), _join(hold)), 22)
    _text(s, 600000, 1150000, W_ - 1200000, 5200000, [
        "Commit the reinforcement of %s at this review, for energisation before November 2027." % _join(commit),
        "Keep the 2027/28 flexibility contract at %s; no reinforcement there this year." % _join(hold),
        "Share of design days over firm capacity: %s." % _join("%s %d per cent" % (n, F["r10_share_over"][n]) for n in names),
        "Re-run after winter 2026/27, with the 2027/28 sites' commissioning tests and another winter of customer "
        "readings on record."], size=18)
    _strip(s, 6, TOTAL)
    prs.save(path)
    PP.normalize_pptx(path, "Marion Todd", "Marion Todd", _z(DECK_CREATED), _z(DECK_SAVED),
                      "Halverton zone: reinforcement for winter 2027/28", ORG, revision=11, total_time=134)


def write(G, F, golden_dir):
    os.makedirs(golden_dir, exist_ok=True)
    write_workbook(G, F, os.path.join(golden_dir, F_XLSX))
    write_deck(G, F, os.path.join(golden_dir, F_PPTX))
