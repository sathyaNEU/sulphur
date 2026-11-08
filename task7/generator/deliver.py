"""task7 architecture 6: the golden deliverables (the committee's briefing deck and the round's workbook) and
figures.json, every figure computed from the cut pack by golden.py and checks.py."""
import json
import math
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import golden as GD
import postprocess

MEAS = GD.MEASURES
LABEL = {"insulation": "Insulation", "heating optimisation": "Heating optimisation", "heating controls": "Heating controls"}


def rnd(v, u):
    return math.floor(v / u + 0.5) * u


def thousands(v):
    return format(int(rnd(v, 1)), ",")


def figures(C):
    P, G, Gw, A = C["P"], C["rates"], C["rates_whole"], C["A"]
    lot, lotw, lotA = C["lottery"]["rates"], C["lottery"]["rates_whole"], C["lottery"]["A"]
    ba = C["before_after"]
    rd = C["round"]
    ac = C["at_close"]["by measure"]
    ss = C["season_saving"]["golden"]
    ev_a, ev_c = C["event_all"], C["event_clean"]
    hm = "heating optimisation"
    clean = [ev_c[(hm, s)] for s in range(2020, 2027)]
    by_m = {m: sum(1 for a in C["apps"] if a["measure"] == m) for m in MEAS}
    day = (GD.RECEIVED_TO - GD.NOTICE[GD.PIPELINE]).days
    lot_ac = C["at_close_rivals"]["the lottery's funded set"]
    F = {
        "call": {"funded": list(C["funded"]), "not_funded": [m for m in MEAS if m not in C["funded"]],
                 "received_funded_applications": rd["n"], "received_funded_grant_eur": rnd(rd["grant"], 10000),
                 "received_funded_tonnes": rnd(rd["tonnes"], 10),
                 "at_close_grant_million": int(rnd(ac["grant"], 1e6) / 1e6), "at_close_grant_unrounded": round(ac["grant"]),
                 "at_close_tonnes": int(rnd(ac["tonnes"], 10000)), "at_close_tonnes_unrounded": round(ac["tonnes"])},
        "rates_pct": {m: int(round(100 * Gw[m])) for m in MEAS},
        "rates_1dp": {m: "%.1f" % (100 * G[m]) for m in MEAS},
        "eur_per_tonne": {m: int(rnd(A[m]["eur_t"], 10)) for m in MEAS},
        "eur_per_tonne_unrounded": {m: round(A[m]["eur_t"], 1) for m in MEAS},
        "break_even_pct": {m: "%.1f" % (100 * A[m]["break_even_rate"]) for m in MEAS},
        "applications_by_measure": by_m,
        "grant_by_measure_eur": {m: int(rnd(A[m]["grant"], 10000)) for m in MEAS},
        "tonnes_by_measure": {m: int(rnd(A[m]["tonnes"], 10)) for m in MEAS},
        "answered_by_day_2019_pct": {m: int(round(100 * GD.answered_share(P, day, [m]))) for m in MEAS},
        "answered_by_day_2019_all_pct": int(round(100 * GD.answered_share(P, day))),
        "season_saving_2026": {"tonnes": int(rnd(ss, 500)), "tonnes_unrounded": round(ss),
                               "static_2019_use_tonnes": round(C["season_saving_rivals"][
                                   "the rate on the 2019 use, buildings still connected"]),
                               "static_2019_use_display": int(rnd(C["season_saving_rivals"][
                                   "the rate on the 2019 use, buildings still connected"], 500)),
                               "lottery_tonnes": round(C["season_saving_rivals"]["the lottery's rates"])},
        "at_close_rivals": {h: {"grant_million": int(rnd(v["grant"], 1e6) / 1e6), "tonnes": int(rnd(v["tonnes"], 10000)),
                                "grant_unrounded": round(v["grant"]), "tonnes_unrounded": round(v["tonnes"])}
                            for h, v in C["at_close_rivals"].items()},
        "default_path": {"rates_pct": {m: int(round(100 * lotw[m])) for m in MEAS},
                         "rates_1dp": {m: "%.1f" % (100 * lot[m]) for m in MEAS},
                         "eur_per_tonne": {m: (int(rnd(lotA[m]["eur_t"], 10)) if lotA[m]["tonnes"] > 0 else None) for m in MEAS},
                         "funded": list(C["lottery"]["funded"]),
                         "at_close_grant_million": int(rnd(lot_ac["grant"], 1e6) / 1e6),
                         "at_close_tonnes": int(rnd(lot_ac["tonnes"], 10000)),
                         "season_saving_2026_tonnes": int(rnd(C["season_saving_rivals"]["the lottery's rates"], 500))},
        "before_after_pct": {m: int(rnd(100 * ba[m], 1)) for m in MEAS},
        "evidence": {"answers": int(P.answered.sum()), "drawn": int(P.drawn.sum()), "works": int(P.works.sum()),
                     "passed_over": C["losers"], "passed_over_visited": C["losers_visited"],
                     "works_visited": int((P.works & (P.tune_season > 0)).sum()),
                     "visit_step_pct": "%.0f" % (100 * C["visit_effect"]),
                     "visit_step_1dp": "%.1f" % (100 * C["visit_effect"]),
                     "lottery_gap_2020_whole": int(rnd(100 * ev_a[(hm, 2020)], 1)),
                     "lottery_gap_2026_under": int(math.floor(100 * ev_a[(hm, 2026)]) + 1),
                     "clean_gap_whole": int(rnd(100 * float(np.mean(clean)), 1)),
                     "lottery_gap_2020_pts": "%.1f" % (100 * ev_a[(hm, 2020)]),
                     "lottery_gap_2026_pts": "%.1f" % (100 * ev_a[(hm, 2026)]),
                     "clean_gap_min_pts": "%.1f" % (100 * min(clean)), "clean_gap_max_pts": "%.1f" % (100 * max(clean)),
                     "draw_balance_pct": "%.1f" % C["balance_bound_pct"],
                     "visit_season_step_lo": C["visit_season_range"][0],
                     "visit_season_step_hi": C["visit_season_range"][1],
                     "season_after_step_pct": "%.0f" % (100 * C["visit_steps"]["season after"]),
                     "applications": len(C["apps"])},
        "constants": {"limit_eur_per_tonne": 120, "factor_t_per_mwh": 0.201, "lives": GD.LIFE,
                      "grant_share_pct": 30, "grant_cap_eur": 40000, "as_of": "2026-06-15", "meeting": "9 July 2026",
                      "offer_closes": "2026-06-30", "received_to": "2026-06-12",
                      "rounding_units": [10, 500, 10000, 1000000], "plan_sections": ["4.2", "4.4"], "standard": "VDI 3807",
                      "standard_number": 3807},
    }
    return F


def write_xlsx(path, C, F):
    wb = Workbook()
    ws = wb.active
    ws.title = "measures"
    head = ["measure", "saving_rate_pct", "applications", "grant_eur", "lifetime_tonnes", "grant_per_tonne_eur", "fund"]
    ws.append(head)
    A = C["A"]
    for m in MEAS:
        ws.append([m, F["rates_pct"][m], A[m]["n"], int(rnd(A[m]["grant"], 10000)), int(rnd(A[m]["tonnes"], 10)),
                   F["eur_per_tonne"][m], "yes" if m in C["funded"] else "no"])
    ws.append([])
    c = F["call"]
    ws.append(["funded, received by 12 June", None, c["received_funded_applications"], c["received_funded_grant_eur"],
               c["received_funded_tonnes"], None, None])
    ws.append(["funded, once the offer closes on 30 June", None, None, c["at_close_grant_million"] * 1000000,
               c["at_close_tonnes"], None, None])
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E46")
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    for r in (ws.max_row - 1, ws.max_row):
        ws.cell(row=r, column=1).font = Font(bold=True)
    for k, wd in enumerate([38, 15, 13, 13, 15, 19, 7], 1):
        ws.column_dimensions[get_column_letter(k)].width = wd
    for r in ws.iter_rows(min_row=2, min_col=4, max_col=5):
        for cell in r:
            cell.number_format = "#,##0"
    ws2 = wb.create_sheet("funded applications")
    ws2.append(["application_no", "building_id", "received", "measure", "grant_eur", "reference_consumption_kwh",
                "expected_annual_saving_mwh", "lifetime_tonnes"])
    for a in C["apps"]:
        if a["funded"]:
            ws2.append([a["no"], a["bid"], a["date"].strftime("%Y-%m-%d"), a["measure"], int(round(a["grant"])),
                        int(round(a["ref_kwh"])), int(rnd(a["annual_mwh"], 1)), int(rnd(a["life_t"], 10))])
    for cell in ws2[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E46")
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    for k, wd in enumerate([15, 12, 11, 21, 11, 16, 16, 13], 1):
        ws2.column_dimensions[get_column_letter(k)].width = wd
    ws2.freeze_panes = "A2"
    for r in ws2.iter_rows(min_row=2, min_col=5, max_col=6):
        for cell in r:
            cell.number_format = "#,##0"
    wb.save(path)
    postprocess.normalize_ooxml(path, "Torben Römer", "Torben Römer", "2026-06-19T08:02:00Z", "2026-06-24T16:47:00Z",
                                "The 2026 efficiency grant round", excel=True, company="Stadtwerke Haldenau")


def charts(C, F, scratch):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "svg.hashsalt": "task7", "path.simplify": False})
    out = {}
    fig, ax = plt.subplots(figsize=(8.2, 4.4), dpi=150)
    vals = [C["A"][m]["eur_t"] for m in MEAS]
    cols = ["#2E7D6B" if m in C["funded"] else "#B5543C" for m in MEAS]
    bars = ax.bar([LABEL[m] for m in MEAS], vals, color=cols, width=0.55)
    for b, m in zip(bars, MEAS):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 4, "€%d" % F["eur_per_tonne"][m], ha="center", fontsize=11)
    ax.axhline(120, color="#333333", lw=1.2, ls="--")
    ax.text(2.45, 124, "limit €120", ha="right", fontsize=10, color="#333333")
    ax.set_ylabel("Grant per tonne of CO2, euro")
    ax.set_ylim(0, max(vals) * 1.18)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#E5E5E5", lw=0.6)
    fig.tight_layout()
    out["eur"] = os.path.join(scratch, "grant_per_tonne.png")
    fig.savefig(out["eur"], format="png", metadata={"Software": None})
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8.2, 4.2), dpi=150)
    hm = "heating optimisation"
    xs = list(range(2020, 2027))
    ax.plot(xs, [100 * C["event_clean"][(hm, s)] for s in xs], color="#2E7D6B", lw=2.2, marker="o",
            label="against owners passed over, before their service visit")
    ax.plot(xs, [100 * C["event_all"][(hm, s)] for s in xs], color="#9A9A9A", lw=2.0, marker="o",
            label="against every owner passed over")
    ax.set_xticks(xs)
    ax.set_xticklabels(["%d/%02d" % (s - 1, s % 100) for s in xs])
    ax.set_ylabel("Saving, % of normal-weather gas use")
    ax.set_ylim(0, 9)
    ax.legend(frameon=False, fontsize=10, loc="lower left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#E5E5E5", lw=0.6)
    fig.tight_layout()
    out["gap"] = os.path.join(scratch, "heating_optimisation_by_season.png")
    fig.savefig(out["gap"], format="png", metadata={"Software": None})
    plt.close(fig)
    return out


def write_pptx(path, C, F, png):
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Inches, Pt
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    GREEN = RGBColor(0x1F, 0x4E, 0x46)
    GREY = RGBColor(0x40, 0x40, 0x40)

    def title(slide, text, sub=None):
        tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.1), Inches(1.1))
        tb.text_frame.word_wrap = True
        p = tb.text_frame.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.LEFT
        p.font.size, p.font.bold, p.font.color.rgb = Pt(26), True, GREEN
        if sub:
            q = tb.text_frame.add_paragraph()
            q.text = sub
            q.alignment = PP_ALIGN.LEFT
            q.font.size, q.font.color.rgb = Pt(14), GREY

    def text(slide, lines, left=0.7, top=1.8, width=11.9, size=16):
        tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(5.0))
        tf = tb.text_frame
        tf.word_wrap = True
        for k, line in enumerate(lines):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            p.text = line
            p.font.size, p.font.color.rgb = Pt(size), GREY
            p.space_after = Pt(10)
        return tb

    def table(slide, rows, top, widths, size=14):
        shp = slide.shapes.add_table(len(rows), len(rows[0]), Inches(0.7), Inches(top), Inches(sum(widths)),
                                     Inches(0.45 * len(rows)))
        t = shp.table
        for j, wdt in enumerate(widths):
            t.columns[j].width = Inches(wdt)
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                c = t.cell(i, j)
                c.text = str(v)
                for p in c.text_frame.paragraphs:
                    p.font.size = Pt(size)
                    p.font.bold = i == 0
        return t
    c, r, e, e2, ss, dp = F["call"], F["rates_pct"], F["eur_per_tonne"], F["evidence"], F["season_saving_2026"], F["default_path"]
    ab = F["answered_by_day_2019_pct"]
    s = prs.slides.add_slide(blank)
    title(s, "The 2026 efficiency grant round: which measures to fund",
          "Energy Services for the Committee for Climate and Environment, meeting of 9 July 2026")
    text(s, ["Fund insulation and heating optimisation in the 2026 round; do not fund heating controls.",
             "Insulation saved %d%% of a building's normal-weather gas use in the 2019 pilot and comes to €%d of grant a "
             "tonne of CO2 on this year's applications; heating optimisation saved %d%% at €%d a tonne. Heating controls "
             "saved %d%% and would cost €%d a tonne, over the €120 limit."
             % (r["insulation"], e["insulation"], r["heating optimisation"], e["heating optimisation"],
                r["heating controls"], e["heating controls"]),
             "Once the offer closes on 30 June the funded round should come to about €%d million of grant and %s tonnes "
             "of CO2 over the measures' lives (%d funded applications for €%s were in by 12 June)."
             % (c["at_close_grant_million"], thousands(c["at_close_tonnes"]), c["received_funded_applications"],
                thousands(c["received_funded_grant_eur"])),
             "The pilot's works saved about %s tonnes of CO2 in the 2025/26 season." % thousands(ss["tonnes"])],
         top=2.0, size=18)
    s = prs.slides.add_slide(blank)
    title(s, "Grant per tonne of CO2 on the 2026 applications", "Saving rate from the 2019 pilot; the plan's appraisal")
    s.shapes.add_picture(png["eur"], Inches(0.7), Inches(1.7), width=Inches(7.9))
    rows = [["Measure", "Saving rate", "Grant per tonne", "Fund"]] + [
        [LABEL[m], "%d%%" % r[m], "€%d" % e[m], "yes" if m in C["funded"] else "no"] for m in MEAS]
    t = s.shapes.add_table(4, 4, Inches(8.9), Inches(2.2), Inches(4.0), Inches(1.8)).table
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            cell = t.cell(i, j)
            cell.text = v
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(12)
                p.font.bold = i == 0
    for j, wdt in enumerate([1.5, 0.9, 1.0, 0.6]):
        t.columns[j].width = Inches(wdt)
    s = prs.slides.add_slide(blank)
    title(s, "What the pilot's works saved", "Heating optimisation, saving by season since the works")
    s.shapes.add_picture(png["gap"], Inches(0.7), Inches(1.7), width=Inches(7.9))
    text(s, ["The pilot's places were drawn by lot, so the owners the draw passed over show what the works buildings "
             "would have used without the works.",
             "From August 2019 most of them had a service visit, district by district (%s of %s by April 2026), and "
             "no building with pilot works had one. After a visit a building's normal-weather use stays about %s%% "
             "lower than unvisited buildings'."
             % (format(e2["passed_over_visited"], ","), format(e2["passed_over"], ","), e2["visit_step_pct"]),
             "Set against every passed-over owner, heating optimisation's saving seems to fade from about %d points to "
             "under %d. Against passed-over owners not yet visited it holds at about %d points, with no trend."
             % (e2["lottery_gap_2020_whole"], e2["lottery_gap_2026_under"], e2["clean_gap_whole"])],
         left=8.9, top=1.8, width=4.1, size=12)
    s = prs.slides.add_slide(blank)
    title(s, "The 2026 round", "Applications received by 12 June; the offer is open to 30 June")
    A = C["A"]
    rows = [["Measure", "Applications", "Grant", "Lifetime tonnes", "Grant per tonne", "Fund"]]
    for m in MEAS:
        rows.append([LABEL[m], str(A[m]["n"]), "€%s" % thousands(rnd(A[m]["grant"], 10000)),
                     thousands(rnd(A[m]["tonnes"], 10)), "€%d" % e[m], "yes" if m in C["funded"] else "no"])
    rows.append(["Funded, received by 12 June", str(c["received_funded_applications"]),
                 "€%s" % thousands(c["received_funded_grant_eur"]), thousands(c["received_funded_tonnes"]), "", ""])
    rows.append(["Funded, once the offer closes", "", "about €%d million" % c["at_close_grant_million"],
                 "about %s" % thousands(c["at_close_tonnes"]), "", ""])
    table(s, rows, 1.9, [3.4, 1.7, 2.2, 2.0, 1.8, 0.9], size=14)
    text(s, ["A response to the offer comes with a contractor's quote, and a quote for insulation needs a survey: in 2019 "
             "%d%% of the insulation responses, %d%% of the heating optimisation responses and %d%% of the heating controls "
             "responses had come in by the same day after the notice. The round once the offer closes scales each funded "
             "measure's applications by its own share."
             % (ab["insulation"], ab["heating optimisation"], ab["heating controls"]),
             "Each funded application is listed with its expected saving and lifetime tonnes in retrofit_round_2026.xlsx."],
         top=5.0, size=13)
    s = prs.slides.add_slide(blank)
    title(s, "Basis")
    text(s, ["Gas use per building and season (1 May to 30 April) from the meter reads, converted to kWh and normalised to "
             "long-term average weather as in the benchmarking notices.",
             "Saving rate as the climate action plan's 4.2 sets it: each works building's use as a share of its 2018/19 "
             "use, against the average of that share over the owners the draw passed over who had not yet had a service "
             "visit, every season from 2019/20 to 2025/26, averaged and taken in whole per cent.",
             "Appraisal as in the climate action plan, section 4.4: the saving rate times each application's reference "
             "consumption, 0.201 tonnes of CO2 per MWh, service lives of 30, 15 and 10 years; a measure is funded at €120 "
             "of grant a tonne or less.",
             "The round once the offer closes: each funded measure's applications received by 12 June, scaled by the share "
             "of the 2019 responses for that measure in by the same day after the notice.",
             "The 2025/26 saving: each measure's rate on what its works buildings would have used that season without the "
             "works (their use divided by one less the rate), at the plan's factor."], top=1.8, size=14)
    cp = prs.core_properties
    cp.author, cp.last_modified_by = "Torben Römer", "Torben Römer"
    cp.title = "The 2026 efficiency grant round"
    cp.comments, cp.subject, cp.keywords, cp.category = "", "", "", ""
    cp.revision = 3
    prs.save(path)
    postprocess.normalize_pptx(path, "Torben Römer", "Torben Römer", "2026-06-22T10:12:00Z", "2026-06-24T17:05:00Z",
                               "The 2026 efficiency grant round", "Stadtwerke Haldenau")


def write_all(C, golden_dir, gen_dir, scratch):
    F = figures(C)
    os.makedirs(golden_dir, exist_ok=True)
    write_xlsx(os.path.join(golden_dir, "retrofit_round_2026.xlsx"), C, F)
    png = charts(C, F, scratch)
    write_pptx(os.path.join(golden_dir, "committee_briefing_retrofit_round_2026.pptx"), C, F, png)
    with open(os.path.join(gen_dir, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False)
    return F
