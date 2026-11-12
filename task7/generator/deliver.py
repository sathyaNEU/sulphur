"""task7 architecture 9: the golden deliverables (a one-page note for the committee's paper and the appraisal workbook
the office issues the grants from), figures.json and effort.json, every figure computed from the cut pack by golden.py
and checks.py."""
import datetime as dt
import json
import math
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Image, Paragraph, Spacer, Table

import checks as CK
import golden as GD
import officepdf
import postprocess

MEAS = GD.MEASURES
HM, IM, CM = "heating optimisation", "insulation", "heating controls"
LABEL = {IM: "Insulation", HM: "Heating optimisation", CM: "Heating controls"}
USE = {"office": "office", "retail": "shop", "hotel": "hotel", "workshop": "workshop", "care home": "care home",
       "restaurant": "restaurant"}
GREEN, RED, GREY, INK = "#2E7D6B", "#B5543C", "#8A8A8A", "#333333"
CEST = dt.timezone(dt.timedelta(hours=2))
ROUTE_LABEL = {  # the routes as the workbook names them
    "the golden: the works' own saving, ranges at the owner": "this appraisal: optimisation's works alone, owners drawn again",
    "the measured seasons carried, ranges at the building": "optimisation's seasons as measured, buildings drawn again",
    "the works' own saving, ranges at the building": "optimisation's works alone, buildings drawn again",
    "the measured seasons carried, ranges at the owner": "optimisation's seasons as measured, owners drawn again",
    "the point estimate against the limit, no range": "each grant per tonne against the limit, no range",
    "each use's saving, the measured seasons, ranges at the building":
        "each use's own pilot saving, optimisation as measured, buildings drawn again"}


def rnd(v, u):
    return math.floor(v / u + 0.5) * u


def eur(v):
    return "€" + format(int(rnd(v, 1)), ",")


def eur2(v):
    return "€%s" % format(v, ",.2f")


def head_row(ws, widths, row=1):
    for c in ws[row]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E46")
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for k, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = wd
    ws.freeze_panes = ws.cell(row=row + 1, column=1).coordinate


def num_fmt(ws, cols, fmt="0.00", start=2):
    for r in ws.iter_rows(min_row=start):
        for cell in r:
            if cell.column in cols and isinstance(cell.value, (int, float)):
                cell.number_format = fmt


def write_xlsx(path, C, F):
    P, A = C["P"], C["A"]
    wb = Workbook()
    ws = wb.active
    ws.title = "measures"
    ws.append(["measure", "saving rate over its life on the applications received (%)", "applications received",
               "grant asked (EUR)", "lifetime tonnes CO2", "grant per tonne (EUR)", "90% range, low (EUR)",
               "90% range, high (EUR)", "fund", "applications once the offer closes", "grant asked once the offer "
               "closes (EUR)"])
    for m in MEAS:
        ws.append([LABEL[m], F["rates"][m], F["n_apps"][m], F["grant_received"][m], F["tonnes"][m], F["eur_t"][m],
                   F["range"][m][0], F["range"][m][1], "yes" if m in F["funded"] else "no", F["close"][m]["n"],
                   F["close"][m]["grant"]])
    ws.append([])
    ws.append(["lifetime tonnes the funded measures' applications received so far buy", None, None, None,
               F["funded_tonnes"]])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    head_row(ws, [26, 18, 12, 14, 13, 13, 12, 12, 7, 14, 16])
    num_fmt(ws, (2, 6, 7, 8))
    num_fmt(ws, (3, 4, 5, 10, 11), "#,##0")
    ws2 = wb.create_sheet("savings by season")
    ws2.append(["measure"] + F["seasons"])
    for m in MEAS:
        ws2.append([LABEL[m]] + F["R1"][m])
    ws2.append(["Heating optimisation, its works alone"] + F["R2_own"])
    ws2.append([])
    ws2.append(["Saving against the owners the 2019 draw passed over, % of the gas the works buildings would have used, "
                "normal weather; heating optimisation's works alone from each works building's seasons before its "
                "campaign check (sheet 'heating optimisation')"])
    head_row(ws2, [34] + [10] * 7)
    num_fmt(ws2, range(2, 9))
    ws3 = wb.create_sheet("heating optimisation")
    ws3.append(["season", "saving as measured (%)", "saving its works alone keep (%)", "the campaign's checks (points)",
                "works buildings before their check", "works buildings in all"])
    tot = len(GD._arms(P, HM)[0])
    for j, s in enumerate(F["seasons"]):
        ws3.append([s, F["R1"][HM][j], F["R2_own"][j], F["R2_campaign_points"][j], F["R2_n_works_clean"][j], tot])
    ws3.append([])
    life = F["R3_life_profile"]
    ws3.append(["year of the 2026 works' life"] + list(range(1, len(life) + 1)))
    ws3.append(["saving its works keep, pilot's works buildings (%)"] + life)
    ws3.append([])
    ws3.append(["The state campaign's heating checks (September 2022 to March 2026, closed) set each taker's heating curve "
                "back down; a works building's seasons from its own check carry the campaign, so its works' own saving "
                "is read off the seasons before it. Over the life: the seasons as observed, then the level of the last "
                "three, weighted by the gas of the works buildings each rests on (%.2f%%)." % F["R3_settled_level"]])
    head_row(ws3, [30, 16, 16, 16, 18, 14])
    num_fmt(ws3, (2, 3, 4))
    ws4 = wb.create_sheet("controls by empty week")
    ws4.append(["band of the pilot's controls answers", "share of the week empty, gas-weighted (%)",
                "saving, seven seasons (%)", "fitted (%)"])
    k = 0
    for x, v, _ in C["R4_pts"]:
        if x <= 0:
            lab = "lived in round the clock"
        else:
            k += 1
            lab = "closes, band %d" % k
        ws4.append([lab, round(100 * x, 2), round(100 * v, 2), round(100 * float(GD.dose_at(C["R4_fit"], x)[0]), 2)])
    ws4.append([])
    ws4.append(["share of the week empty, this year's controls applications, by reference consumption (%)",
                round(100 * F["drivers"][CM]["2026"], 2)])
    head_row(ws4, [34, 18, 16, 12])
    ws5 = wb.create_sheet("insulation by roof")
    ws5.append(["band of the pilot's insulation answers", "roof per square metre of floor, gas-weighted",
                "saving of the heating, seven seasons (%)", "fitted (%)"])
    for k, (x, v, _) in enumerate(C["R5_pts"], 1):
        ws5.append(["band %d" % k, round(math.exp(x), 3), round(100 * v, 2),
                    round(100 * float(GD.dose_at(C["R5_fit"], x)[0]), 2)])
    ws5.append([])
    ws5.append(["roof per floor, this year's insulation applications, by reference consumption",
                round(F["drivers"][IM]["2026"], 3)])
    head_row(ws5, [34, 18, 18, 12])
    ws6 = wb.create_sheet("ranges")
    ws6.append(["measure", "grant per tonne (EUR)", "90% range, low (EUR)", "90% range, high (EUR)",
                "share of fresh draws within EUR 120 (%)", "fund"])
    for m in MEAS:
        ws6.append([LABEL[m], F["eur_t"][m], F["range"][m][0], F["range"][m][1], F["share_under_limit"][m],
                    "yes" if m in F["funded"] else "no"])
    ws6.append([])
    ws6.append(["Each range is the spread of the grant per tonne over %s fresh draws of the pilot as it was drawn: the "
                "owners who answered, drawn again within each measure's drawn and passed-over owners with all their "
                "buildings, and every step repeated (the seasons, the campaign's seasons set aside, the bands and their "
                "fit, the pricing of every application); a draw whose works save nothing buys no tonnes and counts over "
                "the limit." % format(CK.B_BOOT, ",")])
    head_row(ws6, [24, 14, 14, 14, 18, 7])
    num_fmt(ws6, (2, 3, 4))
    num_fmt(ws6, (5,), "0.0")
    ws7 = wb.create_sheet("other routes")
    ws7.append(["route", "funds", "heating optimisation, grant per tonne (EUR)", "its 90% range, high (EUR)",
                "heating controls, 90% range, high (EUR)"])
    for name, rt in F["routes_table"]:
        ws7.append([ROUTE_LABEL[name], ", ".join(LABEL[m].lower() for m in rt["set"]) or "nothing", rt["opt_eur_t"],
                    rt["opt_hi"],
                    rt["ctrl_hi"]])
    head_row(ws7, [60, 44, 18, 16, 16])
    num_fmt(ws7, (3, 4, 5))
    ws8 = wb.create_sheet("applications")
    ws8.append(["application_no", "building_id", "owner_number", "received", "use", "measure", "share_of_week_empty_pct",
                "roof_per_floor", "grant_eur", "reference_consumption_kwh", "saving rate over its life (%)",
                "lifetime_tonnes", "funded"])
    for a in C["apps"]:
        ws8.append([a["no"], a["bid"], a["owner"], a["date"].strftime("%Y-%m-%d"), USE[a["use"]], a["measure"],
                    round(100 * a["empty"], 1) if a["measure"] == CM else None,
                    round(a["roof"], 2) if a["measure"] == IM else None,
                    int(round(a["grant"])), int(round(a["ref_kwh"])), round(100 * a["rate"], 2),
                    round(a["life_t"], 1), "yes" if a["funded"] else "no"])
    ws8.append([])
    ws8.append(["all applications", None, None, None, None, None, None, None, F["grant_total"], None, None,
                F["tonnes_total"], None])
    ws8.cell(row=ws8.max_row, column=1).font = Font(bold=True)
    head_row(ws8, [14, 12, 13, 11, 11, 20, 14, 12, 11, 16, 14, 13, 8])
    num_fmt(ws8, (7,), "0.0")
    num_fmt(ws8, (8, 11))
    num_fmt(ws8, (9, 10), "#,##0")
    num_fmt(ws8, (12,), "#,##0.0")
    ws9 = wb.create_sheet("round at close")
    ws9.append(["measure", "applications received by 12 June", "grant received (EUR)", "2019 share in by the same day (%)",
                "2019 late answers' grant against the early ones'", "applications once the offer closes",
                "grant asked once the offer closes (EUR)"])
    for m in MEAS:
        R = C["R9"][m]
        ws9.append([LABEL[m], R["n"], round(R["grant"]), round(100 * R["share"], 2), round(R["size"], 4),
                    round(R["n_close"]), round(R["grant_close"])])
    head_row(ws9, [22, 14, 14, 14, 16, 14, 16])
    num_fmt(ws9, (2, 3, 6, 7), "#,##0")
    num_fmt(ws9, (4,))
    num_fmt(ws9, (5,), "0.000")
    ws10 = wb.create_sheet("funded applications")
    ws10.append(["application_no", "building_id", "owner_number", "received", "use", "measure", "grant_eur",
                 "lifetime_tonnes"])
    fa = [a for a in C["apps"] if a["funded"]]
    for a in fa:
        ws10.append([a["no"], a["bid"], a["owner"], a["date"].strftime("%Y-%m-%d"), USE[a["use"]], a["measure"],
                     int(round(a["grant"])), round(a["life_t"], 1)])
    ws10.append([])
    ws10.append(["%d applications" % len(fa), None, None, None, None, None, F["funded_grant"], F["funded_tonnes"]])
    ws10.cell(row=ws10.max_row, column=1).font = Font(bold=True)
    head_row(ws10, [16, 12, 13, 11, 11, 14, 11, 13])
    num_fmt(ws10, (7,), "#,##0")
    num_fmt(ws10, (8,), "#,##0.0")
    ws11 = wb.create_sheet("notes")
    for line in [
            ("Source", "Stadtwerke Haldenau's meter reads, meter points, register, notices and 2025 typical weeks; the "
                       "council's 2019 pilot responses and draw, 2026 applications and documents; the state solar "
                       "cadastre; the Haldenau weather station"),
            ("Saving", "the gas the works save as a share of the gas the works buildings would have used, normal "
                       "weather, against the owners the 2019 draw passed over, each against its own 2018/19 season"),
            ("Life", "heating optimisation's works alone (the seasons before each works building's campaign check), "
                     "controls' fade as measured, insulation flat; lives as plan 4.4 sets them"),
            ("Range", "owners drawn again within each measure's drawn and passed-over owners, every step repeated; the "
                      "committee funds a measure only where the range's upper end is within EUR 120"),
            ("Grant per tonne", "a round's grant over its lifetime tonnes, on the applications received by 12 June "
                                "(climate action plan 4.4; the committee's request of 15 June)"),
            ("As of", "applications received by 12 June 2026, a revised application replacing the earlier one; the offer "
                      "closes on 30 June 2026"),
            ("Precision", "savings and rates to two decimals, grant per tonne to the cent, money to the euro, counts "
                          "and totals whole, an application's lifetime tonnes to a tenth")]:
        ws11.append(list(line))
    ws11.column_dimensions["A"].width = 12
    ws11.column_dimensions["B"].width = 110
    for c in ws11["A"]:
        c.font = Font(bold=True)
    wb.save(path)
    postprocess.normalize_ooxml(path, "Torben Römer", "Torben Römer", "2026-06-19T08:02:00Z", "2026-06-24T16:47:00Z",
                                "The 2026 efficiency grant round", excel=True, company="Stadtwerke Haldenau")


def chart(F, scratch):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "task7"})
    fig, ax = plt.subplots(figsize=(6.6, 1.9), dpi=200)
    order = [IM, CM, HM]
    for y, m in enumerate(order):
        lo, hi = F["range"][m]
        col = GREEN if m in F["funded"] else RED
        ax.plot([lo, hi], [y, y], color=col, lw=5, solid_capstyle="butt", alpha=0.85)
        ax.plot([F["eur_t"][m]], [y], "o", color="white", mec=INK, ms=5, zorder=3)
        ax.text(hi + 4, y, "%s to %s" % (eur(lo), eur(hi)), va="center", fontsize=7.5, color=INK)
    ax.axvline(GD.LIMIT, color=INK, lw=1, ls="--")
    ax.text(GD.LIMIT + 1.5, len(order) - 0.45, "€120 limit", fontsize=7.5, color=INK)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([LABEL[m] for m in order])
    ax.set_xlabel("grant per lifetime tonne of CO2 (EUR), point and 90% range")
    ax.set_xlim(0, max(F["range"][m][1] for m in order) + 60)
    ax.set_ylim(-0.6, len(order) - 0.3)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    path = os.path.join(scratch, "ranges.png")
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)
    return path


def write_note(path, F, png):
    H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=12.5, spaceAfter=3)
    B = ParagraphStyle("b", fontName="Helvetica", fontSize=8.6, spaceAfter=3)
    SB = ParagraphStyle("sb", fontName="Helvetica-Bold", fontSize=8.6, spaceAfter=2)
    SM = ParagraphStyle("s", fontName="Helvetica", fontSize=7.4, spaceAfter=1, textColor="#555555")
    rows = [["Measure", "Grant per tonne", "90% range", "Fund", "At close: applications", "grant asked"]]
    for m in (IM, HM, CM):
        rows.append([LABEL[m], eur2(F["eur_t"][m]), "%s to %s" % (eur2(F["range"][m][0]), eur2(F["range"][m][1])),
                     "yes" if m in F["funded"] else "no", format(F["close"][m]["n"], ","), eur(F["close"][m]["grant"])])
    opt_meas = F["measured_opt_eur_t"]
    s = [Paragraph("Stadtwerke Haldenau, Energy Services, for the Committee for Climate and Environment, 9 July 2026", SM),
         Paragraph("The 2026 efficiency grant round", H1),
         Paragraph("<b>Fund roof insulation in the 2026 round, and neither heating optimisation nor heating controls.</b> "
                   "Insulation costs %s of grant per lifetime tonne of CO2 on the %d applications received by 12 June, and "
                   "its 90%% range (%s to %s) is within the €120 limit. Heating optimisation (%s, range up to %s) and "
                   "heating controls (%s, range up to %s) do not meet the committee's rule."
                   % (eur2(F["eur_t"][IM]), F["n_apps"][IM], eur2(F["range"][IM][0]), eur2(F["range"][IM][1]),
                      eur2(F["eur_t"][HM]), eur2(F["range"][HM][1]), eur2(F["eur_t"][CM]), eur2(F["range"][CM][1])), B),
         Table(rows, colWidths=[110, 70, 120, 32, 92, 70]),
         Paragraph("Grant per tonne on the applications received by 12 June (climate action plan 4.4). Range: the "
                   "pilot's owners drawn again %s times, every step repeated; the committee funds a measure where its "
                   "upper end is €120 or less. At close: the offer closes on 30 June." % format(CK.B_BOOT, ","), SM),
         Spacer(1, 4),
         Image(png, width=470, height=470 * 1.9 / 6.6),
         Paragraph("Why not heating optimisation", SB),
         Paragraph("The pilot's measured saving levels at about %.1f per cent from 2022/23, which would price it at %s a tonne. "
                   "But from September 2022 the state campaign's heating checks set every taker's heating curve back "
                   "down, and the pilot's works buildings, balanced by their works, held what the check gave them while "
                   "the passed-over owners' systems lost it within a winter. Read off each works building's seasons "
                   "before its own check, the works alone keep %.2f per cent by 2025/26. The campaign closed in March "
                   "2026, so the 2026 works will save %.2f per cent of their reference use over their fifteen years, not "
                   "%.2f. The 2022 price shock moved works and passed-over buildings alike and explains none of the gap."
                   % (sum(F["R1"][HM][-3:]) / 3, eur2(opt_meas), F["R2_own"][-1], F["R3_rate"], F["R3_measured_rate"]), B),
         Paragraph("Why not heating controls", SB),
         Paragraph("Controls save more the longer a building stands empty, and this year's controls buildings stand empty "
                   "%.0f per cent of the week, so they price at %s a tonne. But the pilot was drawn by owner, and an "
                   "owner's facility manager runs every one of its buildings' timers the same way: the pilot's evidence "
                   "for controls rests on a few large owners. Drawn again owner by owner, its range runs to %s; drawn "
                   "building by building it would stop at %s and look safe."
                   % (100 * F["drivers"][CM]["2026"], eur2(F["eur_t"][CM]), eur2(F["range"][CM][1]),
                      eur2(F["range_building"][CM][1])), B),
         Paragraph("The round", SB),
         Paragraph("The %d insulation applications received by 12 June ask %s and buy %s lifetime tonnes of CO2; the "
                   "workbook lists each with its grant and lifetime tonnes, the office's basis for issuing the grants. "
                   "Once the offer closes on 30 June, insulation will have about %s applications asking %s, heating "
                   "optimisation %s and heating controls %s."
                   % (F["n_apps"][IM], eur(F["funded_grant"]), format(F["funded_tonnes"], ","),
                      format(F["close"][IM]["n"], ","), eur(F["close"][IM]["grant"]), format(F["close"][HM]["n"], ","),
                      format(F["close"][CM]["n"], ",")), B),
         Paragraph("Torben Römer, head of Energy Services", SM)]
    officepdf.build(path, s, "The 2026 efficiency grant round", "Torben Römer", "Grant round 2026: note",
                    "Stadtwerke Haldenau | Energy Services | Note for the committee's paper",
                    dt.datetime(2026, 6, 24, 15, 58, tzinfo=CEST), dt.datetime(2026, 6, 24, 16, 40, tzinfo=CEST),
                    producer="LibreOffice 25.2", font="Carlito", body_pt=8.6, margin_mm=16, top_mm=13, bottom_mm=12)


def write_all(C, golden_dir, gen_dir, scratch):
    P = C["P"]
    F = CK.figures(C)
    s, sz = C["R2"], C["R2_sizes"]
    level = float(sum(a * b for a, b in zip(s[-3:], sz[-3:])) / sum(sz[-3:]))
    F["R3_settled_level"] = round(100 * level, 2)
    F["R3_life_profile"] = [round(100 * x, 2) for x in list(s) + [level] * (GD.LIFE[HM] - len(s))]
    F["share_under_limit"] = {m: round(100 * C["R7"][m]["share_under_limit"], 1) for m in MEAS}
    meas = C["R3_hurried"]["the seasons as measured, a fitted approach to a level"]
    tab = []
    for name, st in C["routes"].items():
        opt_m = "measured" in name
        opt_e = meas["eur_t"] if opt_m else C["A"][HM]["eur_t"]
        if "owner" in name or name.startswith("the golden"):
            opt_hi = C["R7_measured"]["owner"][1] if opt_m else C["R7"][HM]["hi"]
            ctrl_hi = C["R7"][CM]["hi"]
        elif "building" in name:
            opt_hi = C["R7_measured"]["building"][1] if opt_m else C["R7"][HM]["b_hi"]
            ctrl_hi = C["R7"][CM]["b_hi"]
        else:
            opt_hi = ctrl_hi = None
        tab.append((name, {"set": list(st), "opt_eur_t": round(opt_e, 2),
                           "opt_hi": round(opt_hi, 2) if opt_hi is not None else None,
                           "ctrl_hi": round(ctrl_hi, 2) if ctrl_hi is not None else None}))
    F["routes_table"] = tab
    E = CK.effort(C, F)
    os.makedirs(golden_dir, exist_ok=True)
    write_xlsx(os.path.join(golden_dir, "grant_round_2026_appraisal.xlsx"), C, F)
    png = chart(F, scratch)
    write_note(os.path.join(golden_dir, "grant_round_2026_note.pdf"), F, png)
    with open(os.path.join(gen_dir, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False, default=float)
    with open(os.path.join(gen_dir, "effort.json"), "w", encoding="utf-8") as fh:
        json.dump(E, fh, indent=1, ensure_ascii=False, default=float)
    return F
