"""The golden deliverables: niittyla_ebus_order_2027.xlsx (the order, every weekday block's diesel use, design-day
energy and verdict, the night's schedule, the model behind it) and niittyla_ebus_order_2027.pptx (three slides for
the board), both from analysis.py's figures on the shipped pack, written by the house writers."""
import datetime as dt
import io
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from pptx import Presentation
from pptx.util import Emu, Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402

import analysis as A  # noqa: E402
import night  # noqa: E402
import params as P  # noqa: E402

XLSX = "niittyla_ebus_order_2027.xlsx"
PPTX = "niittyla_ebus_order_2027.pptx"


def r10(x):
    return int(round(x / 10.0) * 10)


def hhmm(m):
    m = int(m) % 1440
    return "%02d:%02d" % (m // 60, m % 60)


def compute(target):
    pk = A.load(target)
    g = A.golden(pk)
    return pk, g


def _head(ws, row, fill="D9E1EA"):
    for c in ws[row]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(wrap_text=True, vertical="top")


def _widths(ws, widths):
    for i, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = wd


def write_xlsx(path, pk, g, figs):
    wb = Workbook()
    ws = wb.active
    ws.title = "Order"
    ws["A1"] = "Niittylä 2027: battery-electric buses for the weekday blocks (DES-1)"
    ws["A1"].font = Font(bold=True, size=12)
    rows = [("Buses to order", figs["call_count"]),
            ("Blocks assigned", ", ".join(figs["call_set"])),
            ("Blocks qualifying on the design day (DES-1 4.1)", len(g["qualifying"])),
            ("First block the night cannot recharge with those above it", g["refused"] or "none"),
            ("Usable battery after the first winter, kWh", round(figs["usable_y1"])),
            ("Limit, 85 per cent, kWh", round(g["limit"])),
            ("First-winter loss, per cent of usable", figs["loss_pct"]),
            ("Design night: draw at the connection point for the buses ordered, MWh", figs["night_mwh"]),
            ("Design night: draw at the connection point with every qualifying block on charge, MWh", figs["demand_mwh"]),
            ("   of which recharge, MWh", figs["demand_recharge_mwh"]),
            ("   of which battery conditioning while on charge, MWh", figs["demand_cond_mwh"]),
            ("Design night: at most in the night period, MWh", figs["night_capacity_mwh"]),
            ("Design night: capacity in the night period, kW (agreement 2025-ND-117)", int(pk.supply)),
            ("Charger efficiency into the battery", figs["eta"]),
            ("Conditioning draw on charge at -15 C, kW per bus", figs["cond_kw"])]
    for k, v in rows:
        ws.append([k, v])
        ws.cell(ws.max_row, 1).font = Font(bold=True)
    ws.append([])
    ws.append(["Prepared 10 November 2026 for the board meeting of 21 January 2027; records to 31 October 2026; DES-1 version 2."])
    _widths(ws, [72, 60])

    ws2 = wb.create_sheet("Blocks")
    ws2.append(["Priority", "Block", "Lines", "Zone", "Scheduled km", "Hours out", "Diesel l/100 km (11/2025 to 10/2026)",
                "Design-day energy kWh", "Qualifies (85 per cent)", "Assigned 2027", "Pilot block"])
    _head(ws2, 1)
    taken = set(g["taken"])
    for c in sorted(pk.weekday, key=lambda c: pk.priority[c]):
        b = pk.blocks[c]
        ws2.append([pk.priority[c], c, b["lines"], b["zone"], b["km"], b["hours"], figs["diesel"][c], figs["energy"][c],
                    "yes" if g["verdict"][c] else "no", "yes" if c in taken else "no", "yes" if c in figs["pilot_blocks"] else ""])
    for row in ws2.iter_rows(min_row=2, max_row=ws2.max_row):
        row[4].number_format = "0.0"
        row[5].number_format = "0.00"
        row[6].number_format = "0.0"
        row[7].number_format = "#,##0"
    ws2.append([])
    ws2.append(["Diesel: fuel-card statement 11/2025 to 10/2026 over the dispatch log, litres per 100 scheduled km (DES-1 3.3). Energy: "
                "2027 model, -15 C design day (DES-1 2.4), pilot records carried by diesel use. Limit %d kWh (DES-1 4.1)." % round(g["limit"])])
    _widths(ws2, [8, 8, 9, 6, 11, 9, 16, 14, 12, 11, 9])
    ws2.freeze_panes = "C2"
    ws2.auto_filter.ref = "A1:K49"
    ws2.print_title_rows = "1:1"

    ws3 = wb.create_sheet("Night")
    ws3.append(["Priority", "Block", "Depot return", "Depot departure", "On charge from", "On charge until", "Hours on charge",
                "Battery energy kWh", "Recharge at the connection point kWh", "Conditioning kWh", "Night draw kWh", "Assigned 2027"])
    _head(ws3, 1)
    for c in g["qualifying"]:
        a, b = A.window(pk, c)
        hrs = (b - a) / 60.0
        rech = g["E"][c] / g["eta"]
        ws3.append([pk.priority[c], c, hhmm(pk.blocks[c]["ret"]), hhmm(pk.blocks[c]["dep"]), hhmm(a), hhmm(b), round(hrs, 2),
                    round(g["E"][c], 1), round(rech, 1), round(g["cond_kw"] * hrs, 1), round(rech + g["cond_kw"] * hrs, 1),
                    "yes" if c in taken else "no"])
    ws3.append([])
    ws3.append(["", "Qualifying blocks", "", "", "", "", "", round(sum(g["E"][c] for c in g["qualifying"]), 1), "", "",
                round(g["demand_kwh"], 1), ""])
    ws3.append(["", "Assigned blocks", "", "", "", "", "", round(sum(g["E"][c] for c in g["taken"]), 1), "", "",
                round(g["grid_kwh"], 1), ""])
    for r in (ws3.max_row - 1, ws3.max_row):
        ws3.cell(r, 2).font = Font(bold=True)
    if g["refused"]:
        ws3.append(["", "Next on the list: %s; with the %d blocks above it the night's maximum flow (returns to departures, "
                    "21:00 to 07:00, %d kW, 150 kW a charger) falls about %s kWh short" %
                    (g["refused"], len(g["taken"]), int(pk.supply), figs["refused_short_kwh"])])
    ws3.append(["", "Night period 21:00 to 07:00 at %d kW (connection agreement 2025-ND-117). Recharge = battery energy / %.3f; "
                "conditioning %.1f kW a bus for every hour on charge in the night period (the sessions, -15 C night)." %
                (int(pk.supply), g["eta"], g["cond_kw"])])
    for row in ws3.iter_rows(min_row=2, max_row=ws3.max_row):
        if isinstance(row[6].value, float):
            row[6].number_format = "0.00"
        for c in row[7:11]:
            c.number_format = "#,##0.0"
    _widths(ws3, [8, 10, 11, 13, 13, 13, 10, 12, 16, 13, 12, 11])
    ws3.freeze_panes = "C2"

    ws4 = wb.create_sheet("Model")
    ws4.append(["Pilot energy per km outside heating and cooling, by block (electric bus-days)"])
    ws4["A1"].font = Font(bold=True)
    ws4.append(["Block", "Electric bus-days", "kWh per km (traction and auxiliaries)", "Diesel l/100 km", "Weekday"])
    _head(ws4, 2)
    e_block, days = g["parts"]["e_block"], g["parts"]["days"]
    for c in sorted(e_block, key=lambda c: -days[c]):
        ws4.append([c, days[c], round(e_block[c], 3), round(g["rates"].get(c, float("nan")), 1), "yes" if c in pk.weekday else "no"])
    ws4.append([])
    bb, rmse, n = A.bridge(pk, e_block, days, g["rates"])
    for k, v in (("Bridge: kWh per km = a + b x diesel l/100 km, over %d blocks weighted by days" % n, ""),
                 ("a", round(float(bb[0]), 4)), ("b", round(float(bb[1]), 5)), ("RMSE kWh per km", round(rmse, 3)),
                 ("Pilot HVAC draw at -15 C, kW per hour out", round(g["parts"]["h_pilot"], 2)),
                 ("Fuel heater at -15 C, litres per hour out", round(g["parts"]["heater_lph"], 3)),
                 ("Fuel heater at -15 C, kW of heat (35 kW at 3.9 l/h)", figs["heater_kw"]),
                 ("Heating on the 2027 model at -15 C, kW (boosters below -10 C)", round(g["parts"]["heat_new"], 2)),
                 ("Design-day energy = km x (kWh per km) + hours out x heating kW", ""),
                 ("", ""),
                 ("Charging sessions: metered kWh = gain / efficiency + hours on charge x (c0 + c1 x max(0, T0 - night mean))", ""),
                 ("Efficiency into the battery", figs["eta"]),
                 ("c0, kW", figs["cond_base_kw"]),
                 ("c1, kW per degree", figs["cond_slope_kw"]),
                 ("T0, C", figs["cond_t0"]),
                 ("Conditioning at a -15 C night, kW", figs["cond_kw"]),
                 ("Residual, kWh a session", figs["cond_rmse"]),
                 ("Pooled ratio, battery gain over metered energy (all sessions)", figs["ratio_pooled"])):
        ws4.append([k, v])
    _widths(ws4, [60, 16, 30, 14, 9])
    wb.save(path)


def chart_png(pk, g, figs):
    order = sorted(pk.weekday, key=lambda c: pk.priority[c])
    vals = [g["E"][c] for c in order]
    cols = ["#2E6F9E" if c in set(g["taken"]) else ("#8FB3CC" if g["verdict"][c] else "#C9CED6") for c in order]
    fig, ax = plt.subplots(figsize=(11, 4.2), dpi=150)
    ax.bar(range(len(order)), vals, color=cols, width=0.8)
    ax.axhline(g["limit"], color="#B03A2E", lw=1.2)
    ax.text(len(order) - 0.5, g["limit"] + 6, "limit %d kWh" % round(g["limit"]), ha="right", va="bottom", fontsize=8, color="#B03A2E")
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, rotation=90, fontsize=6.5)
    ax.set_ylabel("design-day energy, kWh")
    ax.set_xlabel("weekday blocks in the fleet plan's priority order")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, max(vals) * 1.08)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def write_pptx(path, pk, g, figs):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]

    def footer(slide, n):
        tb = slide.shapes.add_textbox(Inches(0.6), Inches(7.0), Inches(12.1), Inches(0.35))
        p = tb.text_frame.paragraphs[0]
        p.text = "%s | Niittylä 2027 order | board 21 January 2027 | %d/3" % (P.ORG, n)
        p.font.size = Pt(10)

    def text(slide, left, top, width, height, lines, size=16, bold_first=False):
        tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = ln
            p.font.size = Pt(size)
            if bold_first and i == 0:
                p.font.bold = True
        return tb

    s1 = prs.slides.add_slide(blank)
    text(s1, 0.6, 0.4, 12, 1.0, ["Niittylä: %d battery-electric buses for 2027, the night supply sets the number" % figs["call_count"]], 28, True)
    text(s1, 0.6, 1.4, 12, 5.5, [
        "Order %d %s %s buses for the weekday blocks %s." % (figs["call_count"], P.EMAKE, P.EMODEL, ", ".join(figs["call_set"])),
        "%d of the 48 weekday blocks stay within the design-day limit of %d kWh (85 per cent of %d kWh usable after the first winter); "
        "the night period's %d kW recharges %d of them, in the plan's priority order; %s, next on the list, does not fit with them." %
        (len(g["qualifying"]), round(g["limit"]), round(figs["usable_y1"]), int(pk.supply), figs["call_count"], g["refused"]),
        "The remaining blocks stay on diesel until the connection is reinforced (earliest Q4 2028).",
        "Order by 15 January 2027 for delivery in August to September 2027 (quotation 26-0931).",
    ], 18)
    footer(s1, 1)

    s2 = prs.slides.add_slide(blank)
    text(s2, 0.6, 0.3, 12, 0.8, ["%d of 48 weekday blocks stay under the design-day limit; the night recharges %d" % (len(g["qualifying"]), figs["call_count"])], 24, True)
    png = chart_png(pk, g, figs)
    s2.shapes.add_picture(png, Inches(0.6), Inches(1.2), width=Inches(12.1))
    text(s2, 0.6, 6.3, 12, 1.0, ["Dark: assigned. Light blue: within the limit but beyond the night's capacity. Grey: over the limit. "
                                 "Energies from the pilot's own records carried to every block by its diesel use, with the heating the "
                                 "2027 model takes from the battery."], 12)
    footer(s2, 2)

    s3 = prs.slides.add_slide(blank)
    text(s3, 0.6, 0.3, 12, 0.8, ["What the figures rest on"], 24, True)
    text(s3, 0.6, 1.2, 12, 5.5, [
        "Diesel use per block, tank to tank over the dispatch log, 11/2025 to 10/2026: %.1f to %.1f l/100 km; the nine pilot blocks average %.1f against %.1f for the other 39." %
        (figs["diesel_min"], figs["diesel_max"], figs["pilot_diesel_mean"], figs["others_diesel_mean"]),
        "The pilot buses' fuel heaters supplied about %.1f kW of cabin heat at -15 C; the 2027 model heats electrically, so its design-day energy carries it (%.1f kW of heating in all)." %
        (figs["heater_kw"], g["parts"]["heat_new"]),
        "First-winter loss of usable battery on our own buses: %.1f per cent; usable battery for planning %d kWh." % (figs["loss_pct"], round(figs["usable_y1"])),
        "Design night: %.1f MWh at the connection point for the %d buses (%.1f MWh with all %d qualifying blocks on charge, against %.2f MWh in the night period); on a -15 C night each bus also takes about %.1f kW on charge to keep its battery warm." % (figs["night_mwh"], figs["call_count"], figs["demand_mwh"], figs["qualifying_count"], figs["night_capacity_mwh"], figs["cond_kw"]),
        "Business case: the %d blocks burn about %s litres of diesel a year." % (figs["call_count"], format(figs["diesel_litres_assigned"], ",d")),
    ], 16)
    footer(s3, 3)
    prs.save(path)


def write(target, gold):
    import writeup as WU
    os.makedirs(gold, exist_ok=True)
    pk, g = compute(target)
    figs = WU.figures(pk, g)
    write_xlsx(os.path.join(gold, XLSX), pk, g, figs)
    write_pptx(os.path.join(gold, PPTX), pk, g, figs)
    return pk, g, figs
