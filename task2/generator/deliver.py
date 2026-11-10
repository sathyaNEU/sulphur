"""task2 architecture 6: the golden deliverables and figures.json. The memo is a Word document exported by
LibreOffice Writer (officepdf.py) with its chart; the workbook passes through the house writer. Every figure is
taken from the checks' golden on the cut pack."""
import datetime as dt
import json
import math
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Image, Paragraph, Table

import golden as GD
import officepdf
import postprocess
import world as W

GMT = dt.timezone.utc
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, spaceAfter=6, textColor="#1D3557")
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8, spaceAfter=3, textColor="#1D3557")
BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.2, spaceAfter=4)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8, spaceAfter=2, textColor="#444444")
QN = ["first", "second", "third", "fourth"]
NAME = {h[0]: h[1] for h in W.HOSPITALS}


def d1(x):
    """a share as the write-up states it, in per cent to one decimal"""
    return float("%.1f" % (100 * x))


def figures(C):
    G, P = C["G"], C["P"]
    B = G["bridge"]
    q = [G["q"][k]["share"] for k in GD.Q27]
    res = {
        "r1_bridge_ends": {"start": d1(B["start"]), "end": d1(B["end"])},
        "r2_bridge_split": {"releases": d1(B["releases"]), "mix": d1(B["mix"])},
        "r3_hospital_effects": {h: round(100 * (math.exp(G["F"]["site"][h]) - 1), 1) for h in W.TEACHING},
        "r4_starters_share": {h: d1(G["U"][h]["h_ent"]) for h in W.TEACHING},
        "r5_bku_q4_dictations": int(round(G["hq"]["BKU"]["vol"], -3)),
        "r6_univ_q4_share": {h: d1(G["hq"][h]["share"]) for h in W.TEACHING},
        "r7_lowest_ceilings": list(G["bands"]),
        "r8_p90_q4": d1(G["p90"]),
        "r9_ceiling": G["ceiling"],
    }
    bands = {
        "r1_bridge_ends": {"start": [res["r1_bridge_ends"]["start"] - 0.1, res["r1_bridge_ends"]["start"] + 0.1],
                           "end": [res["r1_bridge_ends"]["end"] - 0.1, res["r1_bridge_ends"]["end"] + 0.1]},
        "r2_bridge_split": {"releases": [-4.7, -3.5], "mix": [1.2, 2.5]},
        "r3_hospital_effects": {"SSU": [3.5, 6.5], "BKU": [7.0, 10.0]},
        "r4_starters_share": {"SSU": [17.0, 19.5], "BKU": [20.5, 23.0]},
        "r5_bku_q4_dictations": {"band": [85000, 91000], "partly": [80000, 96000]},
        "r6_univ_q4_share": {"SSU": [14.3, 15.5], "BKU": [12.3, 13.5]},
        "r8_p90_q4": {"band": [15.8, 16.3], "partly": [15.5, 16.6]},
    }
    U = G["U"]
    kr = C["kinds"]
    rt = C["full_routes"]
    fam_q4 = [100 * X["q"][(2027, 4)]["share"] for X in C["family"].values()]
    ev = {
        "quarters_1dp": ["%.1f" % (100 * x) for x in q],
        "first_past": {str(k): v for k, v in G["first_past"].items()},
        "family_q4_range": ["%.1f" % min(fam_q4), "%.1f" % max(fam_q4)],
        "record_1dp": ["%.1f" % (100 * x) for x in C["record"]],
        "record_max_1dp": "%.1f" % (100 * max(C["record"])), "record_2026_1dp": "%.1f" % (100 * C["routes"]["R0 the 2026 share carried forward"][0][0]),
        "release_cuts_pct": {r: "%.1f" % (100 * (1 - math.exp(G["F"]["steps"][r] - G["F"]["steps"][p])))
                             for p, r in zip(["3.4", "4.0", "5.0", "5.2"], ["4.0", "5.0", "5.2", "6.0"])},
        "release_step_4_to_6_pct": "%.1f" % (100 * (1 - math.exp(B["step"]))),
        "bridge_change_1dp": "%.1f" % (100 * B["change"]),
        "bridge_orders_1dp": ["%.1f" % (100 * x) for x in B["releases_orders"]],
        "moved_staff_numbers": sum(1 for d in P.reg.values() if d["prev"]),
        "pairs": {h: G["F"]["into"][h] for h in W.TEACHING},
        "pairs_total": G["F"]["pairs"],
        "small_effects_pct": {h: "%.1f" % (100 * (math.exp(G["F"]["site"][h]) - 1)) for h in GD.SMALL},
        "uptake_pct": {h: int(round(100 * v)) for h, v in C["uptake"].items()},
        "kinds_pct": {k: "%.1f" % (100 * v) for k, v in kr.items()},
        "staff": {h: len(U[h]["staff"]) for h in W.TEACHING},
        "dictating": {h: len(U[h]["dictating"]) for h in W.TEACHING},
        "starters": {h: len(U[h]["entrants"]) for h in W.TEACHING},
        "whole_staff_pct": {h: "%.1f" % (100 * U[h]["h_pop"]) for h in W.TEACHING},
        "dictators_pct": {h: "%.1f" % (100 * U[h]["h_dict"]) for h in W.TEACHING},
        "ramp_pct": [int(round(100 * x)) for x in G["ramp"][:4]],
        "bku_q4_dictators": int(round(sum(v for t in GD.months(2027, 4) for h, k, v, r in G["out"][t]
                                          if h == "BKU" and k == "dictating"), -3)),
        "bku_q4_starters": int(round(sum(v for t in GD.months(2027, 4) for h, k, v, r in G["out"][t]
                                         if h == "BKU" and k == "starters"), -3)),
        "bku_q4_full_volume": int(round(rt["R4 the go-lives at full volume from the date"]["hq"]["BKU"]["vol"], -3)),
        "bku_q4_own_first": int(round(rt["R4 every clinician starting on the date at their own first months' volume"]["hq"]["BKU"]["vol"], -3)),
        "p90_levels_1dp": "%.1f" % (100 * C["p90_levels"]),
        "nosite": {"q4_1dp": "%.1f" % (100 * rt["R3 no hospital effect (the university hospitals at the smaller hospitals' level)"]["q"][(2027, 4)]["share"]),
                   "ceiling": rt["R3 no hospital effect (the university hospitals at the smaller hospitals' level)"]["ceiling"],
                   "ssu_1dp": "%.1f" % (100 * rt["R3 no hospital effect (the university hospitals at the smaller hospitals' level)"]["hq"]["SSU"]["share"]),
                   "bku_1dp": "%.1f" % (100 * rt["R3 no hospital effect (the university hospitals at the smaller hospitals' level)"]["hq"]["BKU"]["share"])},
        "compelled": {"q4_1dp": "%.1f" % (100 * rt["R2 the 2027 starters at the smaller hospitals' compelled clinicians' rate"]["q"][(2027, 4)]["share"])},
        "noramp": {"q4_1dp": "%.1f" % (100 * rt["R4 the go-lives at full volume from the date"]["q"][(2027, 4)]["share"]),
                   "q1_1dp": "%.1f" % (100 * rt["R4 the go-lives at full volume from the date"]["q"][(2027, 1)]["share"])},
        "bridge_routes_1dp": {k: {"releases": "%.1f" % (100 * v["releases"]), "mix": "%.1f" % (100 * v["mix"])}
                              for k, v in C["bridge_routes"].items()},
    }
    ev["releases_abs_1dp"] = "%.1f" % abs(res["r2_bridge_split"]["releases"])
    ev["releases_band_abs_1dp"] = ["%.1f" % abs(bands["r2_bridge_split"]["releases"][1]),
                                   "%.1f" % abs(bands["r2_bridge_split"]["releases"][0])]
    ev["bku_q4_starters_full_volume"] = int(round(ev["bku_q4_full_volume"] - ev["bku_q4_dictators"], -3))
    F = dict(res)
    F.update({"results": res, "bands": bands, "evidence": ev,
         "routes": {k: {"quarters_1dp": ["%.1f" % (100 * x) for x in v], "ceiling": c} for k, (v, c) in C["routes"].items()},
         "full_routes": {k: {"quarters_1dp": ["%.1f" % (100 * X["q"][kk]["share"]) for kk in GD.Q27],
                             "ceiling": X["ceiling"], "lowest_ceilings": X["bands"]} for k, X in rt.items()},
         "constants": {"line_pct": 15, "ceilings_pct": list(GD.CEILINGS), "audit_rate_pct": "2.5", "year": 2027,
                       "as_of": "2027-01-11", "frozen_release": "6.0", "nine_in_ten": 90,
                       "compulsory": {h: GD.months_label(W.H[h]["comp"]) for h in W.TEACHING},
                       "small_hospitals": 6, "quarters": [1, 2, 3, 4], "bridge_from": "2023 Q2", "bridge_to": "2026 Q4",
                       "releases": ["4.0", "5.0", "5.2", "6.0"]}})
    return F


def chart(C, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rec = [100 * x for x in C["record"]]
    fut = [100 * C["G"]["q"][k]["share"] for k in GD.Q27]
    xr = list(range(16))
    xf = list(range(16, 20))
    fig, ax = plt.subplots(figsize=(7.6, 3.5), dpi=150)
    ax.plot(xr, rec, color="#1D3557", marker="o", ms=3.4, lw=1.5, label="audited, 2023 to 2026")
    ax.plot([15] + xf, [rec[-1]] + fut, color="#C8553D", marker="o", ms=4, lw=1.8, ls="--", label="expected, 2027")
    for c in GD.CEILINGS:
        ax.axhline(c, color="#888888", lw=0.7, ls=":")
        ax.text(19.6, c + 0.12, "%d%%" % c, fontsize=7, color="#555555", ha="right")
    ax.set_xticks(range(20))
    ax.set_xticklabels([str(2023 + i // 4) if i % 4 == 0 else "" for i in range(20)], fontsize=7)
    for x, y in zip(xf, fut):
        ax.annotate("%.1f" % y, (x, y), textcoords="offset points", xytext=(-4, 6), fontsize=6.5, color="#C8553D", ha="right")
    ax.set_ylim(6, 17)
    ax.set_ylabel("audited dictations above 15% WER (%)", fontsize=8)
    ax.tick_params(axis="y", labelsize=7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(path, format="png", metadata={"Software": None})
    plt.close(fig)


def write_pdf(path, C, F, png):
    r, ev, k = F["results"], F["evidence"], F["constants"]
    fp = ev["first_past"]
    rows = [["2027", "Expected share above 15%", "Lowest ceiling it stays under"]]
    for i in range(4):
        rows.append(["Q%d" % (i + 1), "%s%%" % ev["quarters_1dp"][i], "%d%%" % r["r7_lowest_ceilings"][i]])
    univ = [["", "Shannonside University", "Ballykeel University"],
            ["In post, 31 December 2026", format(ev["staff"]["SSU"], ","), format(ev["staff"]["BKU"], ",")],
            ["Dictating in late 2026", "%d" % ev["dictating"]["SSU"], "%d" % ev["dictating"]["BKU"]],
            ["Starting once compulsory", "%d" % ev["starters"]["SSU"], "%d" % ev["starters"]["BKU"]],
            ["The hospital's own effect on error", "+%s%%" % r["r3_hospital_effects"]["SSU"], "+%s%%" % r["r3_hospital_effects"]["BKU"]],
            ["Heavy-correction share, 2027 starters", "%s%%" % r["r4_starters_share"]["SSU"], "%s%%" % r["r4_starters_share"]["BKU"]],
            ["Expected share, 2027 Q4", "%s%%" % r["r6_univ_q4_share"]["SSU"], "%s%%" % r["r6_univ_q4_share"]["BKU"]]]
    s = [Paragraph("Larkmoor Speech: Recognition Quality", SMALL),
         Paragraph("Shannonside 2027 quality schedule: the heavy-correction ceiling", H1),
         Paragraph("12 January 2027. Jody Cahir, Head of Recognition Quality, for the account team.", SMALL),
         Paragraph("We should commit to Ceiling C, %d per cent." % r["r9_ceiling"], H2),
         Paragraph("A 10 per cent ceiling would be passed in the %s quarter of 2027 and a 12 per cent ceiling in the %s. "
                   "No quarter is expected to pass 14 per cent: the fourth, the highest, comes to about %s per cent."
                   % (QN[fp["10"] - 1], QN[fp["12"] - 1], ev["quarters_1dp"][3])),
         Image(png, width=480, height=221),
         Table(rows, colWidths=[50, 150, 170]),
         Paragraph("Audited shares to the end of 2026 from the QA-07 audits; 2027 expected from the audits, the group's HR "
                   "register and the six past go-lives, with recognition on release 6.0 through 2027 (SN-2026-14).", SMALL),
         Paragraph("Why the record does not carry forward", H2),
         Paragraph("The audited share went from %s per cent in the second quarter of 2023 to %s per cent at the end of "
                   "2026. Measured within clinicians, releases 5.0, 5.2 and 6.0 together cut a clinician's error by "
                   "about %s per cent, which on its own would have taken about %s points off the share; the changing "
                   "mix of dictations put about %s back, as the six smaller hospitals went compulsory and the "
                   "clinicians who had not chosen to dictate joined."
                   % (r["r1_bridge_ends"]["start"], r["r1_bridge_ends"]["end"], ev["release_step_4_to_6_pct"],
                      abs(r["r2_bridge_split"]["releases"]), r["r2_bridge_split"]["mix"])),
         Paragraph("2027 has no release (SN-2026-14) and brings the two university hospitals into the service: "
                   "Shannonside University from %s and Ballykeel University from %s. Most of their staff do not "
                   "dictate yet." % (k["compulsory"]["SSU"], k["compulsory"]["BKU"])),
         Paragraph("The university hospitals", H2),
         Table(univ, colWidths=[180, 130, 130]),
         Paragraph("In post: the HR register at 31 December 2026, as the rollout plan counts them. Dictating: any "
                   "dictation from October to December 2026.", SMALL),
         Paragraph("The clinicians dictating there now look excellent (%s and %s per cent heavy correction) because they "
                   "are the few who chose to. The %d moves between the group's hospitals that the register records under "
                   "a new staff number let us separate the place from the people: the same clinician's word error rate is "
                   "about %s per cent higher at Shannonside University and %s per cent higher at Ballykeel than at the six "
                   "smaller hospitals on average. The starters are most of each staff, not the hard core who held "
                   "out at the smaller hospitals (whose compelled clinicians carry %s per cent heavy correction): their "
                   "share is the whole staff's, at the smaller hospitals' levels for their grades and specialties with "
                   "the hospital's own effect, less what the volunteers already carry."
                   % (ev["dictators_pct"]["SSU"], ev["dictators_pct"]["BKU"], ev["moved_staff_numbers"],
                      r["r3_hospital_effects"]["SSU"], r["r3_hospital_effects"]["BKU"], ev["kinds_pct"]["compelled"])),
         Paragraph("The go-lives switch over department by department. At the six earlier go-lives the compelled "
                   "clinicians dictated about %d, %d and %d per cent of a settled month in the first three months, so "
                   "Ballykeel's fourth quarter holds about %s dictations, %s of them from its starters."
                   % (ev["ramp_pct"][0], ev["ramp_pct"][1], ev["ramp_pct"][2], format(r["r5_bku_q4_dictations"], ","),
                      format(ev["bku_q4_starters"], ","))),
         Paragraph("Nine in ten of the fourth quarter's dictations are expected to stay under %s per cent word error "
                   "rate." % r["r8_p90_q4"]),
         Paragraph("What we ruled out", H2),
         Paragraph("Carrying 2026's %s per cent forward points to 10 per cent. Putting the university hospitals' "
                   "starters at the smaller hospitals' compelled clinicians' rate puts the fourth quarter at %s per cent, "
                   "above every ceiling offered. Reading the university hospitals at the smaller hospitals' acoustic "
                   "level gives %s per cent and 12. Starting the go-lives at full volume gives %s per cent and 16."
                   % (ev["record_2026_1dp"], ev["compelled"]["q4_1dp"], ev["nosite"]["q4_1dp"], ev["noramp"]["q4_1dp"])),
         Paragraph("Heavy correction is an audited dictation whose word error rate is above 15 per cent, the adjudicated "
                   "score where a dictation was scored twice (draft Schedule 4.1; QA-07 4). Quarters are calendar quarters "
                   "by dictation date.", SMALL)]
    officepdf.build(path, s, "Shannonside 2027 quality schedule: the heavy-correction ceiling", "Jody Cahir",
                    "Heavy-correction ceiling 2027", "Larkmoor Speech | Recognition Quality | Shannonside 2027",
                    dt.datetime(2027, 1, 11, 15, 20, tzinfo=GMT), dt.datetime(2027, 1, 12, 10, 5, tzinfo=GMT),
                    producer="LibreOffice 24.8")


def style(ws, widths):
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1D3557")
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    for i, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = wd


def write_xlsx(path, C, F):
    r, ev = F["results"], F["evidence"]
    G = C["G"]
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 quarters"
    ws.append(["Quarter", "Expected share above 15% WER", "Lowest ceiling it stays under (%)"])
    for i, kk in enumerate(GD.Q27):
        ws.append(["2027 Q%d" % (i + 1), round(G["q"][kk]["share"], 4), r["r7_lowest_ceilings"][i]])
        ws.cell(ws.max_row, 2).number_format = "0.0%"
    ws.append([])
    ws.append(["Ceiling to commit (%)", r["r9_ceiling"]])
    ws.append(["First quarter past 10%", "Q%d" % ev["first_past"]["10"]])
    ws.append(["First quarter past 12%", "Q%d" % ev["first_past"]["12"]])
    ws.append(["Word error rate nine in ten Q4 dictations stay under", r["r8_p90_q4"] / 100])
    ws.cell(ws.max_row, 2).number_format = "0.0%"
    style(ws, [52, 30, 30])
    ws2 = wb.create_sheet("University hospitals")
    ws2.append(["", "SSU", "BKU"])
    for label, key, fmt in [("Clinicians in post, 31 Dec 2026", "staff", None), ("Dictating in Oct to Dec 2026", "dictating", None),
                            ("Starting once compulsory", "starters", None)]:
        ws2.append([label, ev[key]["SSU"], ev[key]["BKU"]])
    ws2.append(["Hospital's own effect on a clinician's word error (vs the six smaller hospitals)",
                r["r3_hospital_effects"]["SSU"] / 100, r["r3_hospital_effects"]["BKU"] / 100])
    ws2.append(["Clinicians seen at the hospital and at another", ev["pairs"]["SSU"], ev["pairs"]["BKU"]])
    ws2.append(["Heavy share, whole staff at 6.0", float(ev["whole_staff_pct"]["SSU"]) / 100, float(ev["whole_staff_pct"]["BKU"]) / 100])
    ws2.append(["Heavy share, current dictators at 6.0", float(ev["dictators_pct"]["SSU"]) / 100, float(ev["dictators_pct"]["BKU"]) / 100])
    ws2.append(["Heavy share, 2027 starters", r["r4_starters_share"]["SSU"] / 100, r["r4_starters_share"]["BKU"] / 100])
    ws2.append(["Expected share, 2027 Q4", r["r6_univ_q4_share"]["SSU"] / 100, r["r6_univ_q4_share"]["BKU"] / 100])
    ws2.append(["Dictations, 2027 Q4", int(round(G["hq"]["SSU"]["vol"], -3)), r["r5_bku_q4_dictations"]])
    for row in ws2.iter_rows(min_row=5, max_row=ws2.max_row):
        for c in row[1:]:
            if isinstance(c.value, float):
                c.number_format = "0.0%"
    style(ws2, [70, 14, 14])
    ws3 = wb.create_sheet("Go-live ramp")
    ws3.append(["Month from the compulsory date", "Share of a settled month (six past go-lives)"])
    for i, x in enumerate(G["ramp"]):
        ws3.append([i, round(x, 3)])
        ws3.cell(ws3.max_row, 2).number_format = "0%"
    style(ws3, [32, 40])
    ws4 = wb.create_sheet("Bridge 2023-26")
    ws4.append(["", "Percentage points"])
    for label, v in [("Audited share, 2023 Q2 (%)", r["r1_bridge_ends"]["start"]), ("Audited share, 2026 Q4 (%)", r["r1_bridge_ends"]["end"]),
                     ("Change", float(ev["bridge_change_1dp"])), ("Releases 5.0, 5.2 and 6.0", r["r2_bridge_split"]["releases"]),
                     ("Mix of dictations", r["r2_bridge_split"]["mix"]),
                     ("Releases, 2023 mix", float(ev["bridge_orders_1dp"][0])), ("Releases, 2026 mix", float(ev["bridge_orders_1dp"][1]))]:
        ws4.append([label, v])
    style(ws4, [36, 18])
    ws5 = wb.create_sheet("Routes")
    ws5.append(["Route", "Q1", "Q2", "Q3", "Q4", "Ceiling"])
    ws5.append(["The golden"] + [float(x) for x in ev["quarters_1dp"]] + [r["r9_ceiling"]])
    for k, v in list(F["routes"].items()) + list(F["full_routes"].items()):
        ws5.append([k.split(" ", 1)[1] if k[:1] == "R" else k] + [float(x) for x in v["quarters_1dp"]] +
                   [v["ceiling"] if v["ceiling"] is not None else "none"])
    style(ws5, [86, 8, 8, 8, 8, 9])
    ws6 = wb.create_sheet("Record")
    ws6.append(["Quarter", "Audited share above 15% WER"])
    for (y, qq), x in zip([(y, qq) for y in (2023, 2024, 2025, 2026) for qq in (1, 2, 3, 4)], C["record"]):
        ws6.append(["%d Q%d" % (y, qq), round(x, 4)])
        ws6.cell(ws6.max_row, 2).number_format = "0.0%"
    style(ws6, [12, 28])
    ws7 = wb.create_sheet("Notes")
    ws7.append(["Notes"])
    for line in ["Heavy correction: an audited dictation whose word error rate is above 15 per cent (draft Schedule 4.1), "
                 "the adjudicated score where a dictation was scored twice (QA-07 4); unscorable audio left out.",
                 "Quarters are calendar quarters by dictation date. The record runs to 31 December 2026; audits scored "
                 "after the 8 January 2027 export are not in it.",
                 "2027: recognition on release 6.0 throughout (SN-2026-14); Shannonside University compulsory from %s and "
                 "Ballykeel University from %s (Schedule 2); the staff in post held as on 31 December 2026, a leaver "
                 "replaced like for like." % (F["constants"]["compulsory"]["SSU"], F["constants"]["compulsory"]["BKU"]),
                 "A hospital's own effect is measured within the clinicians audited at two of the group's hospitals, "
                 "linked through previous_staff_no on the register, against the six smaller hospitals' average.",
                 "The Routes sheet sets each tempting shortcut beside the expected shares; only the expected shares carry "
                 "the recommendation."]:
        ws7.append([line])
    style(ws7, [140])
    for row in ws7.iter_rows(min_row=2):
        row[0].alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    postprocess.normalize_ooxml(path, "Jody Cahir", "Jody Cahir", "2027-01-11T09:12:00Z", "2027-01-12T09:48:00Z",
                                "Heavy correction 2027", excel=True, company="Larkmoor Speech")


def write_all(C, golden_dir, gen_dir, scratch):
    F = figures(C)
    C["bands_stated"] = F["bands"]
    os.makedirs(golden_dir, exist_ok=True)
    write_xlsx(os.path.join(golden_dir, "heavy_correction_2027.xlsx"), C, F)
    png = os.path.join(scratch, "ceiling.png")
    chart(C, png)
    write_pdf(os.path.join(golden_dir, "quality_schedule_2027_ceiling.pdf"), C, F, png)
    with open(os.path.join(gen_dir, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    return F
