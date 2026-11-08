"""task2 architecture 5: the golden deliverables and figures.json. The memo is a Word document exported by
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
BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.4, spaceAfter=4)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8, spaceAfter=2, textColor="#444444")
QN = ["first", "second", "third", "fourth"]


def rnd(v, u=1.0):
    return math.floor(v / u + 0.5) * u


def pc(x):
    return int(rnd(100 * x))


def figures(C):
    G = C["G"]
    q = [G["q"][k] for k in GD.Q27]
    lad = C["ladder"]
    fp = G["first_past"]
    rec = C["record"]
    F = {
        "call": {"ceiling_pct": G["ceiling"], "first_quarter_past_10": fp.get(10), "first_quarter_past_12": fp.get(12)},
        "quarters_2027": {
            "lowest_ceiling": G["bands"],
            "p90_q4_pct": pc(q[3]["p90"]),
            "share_1dp": ["%.1f" % (100 * f["share"]) for f in q],
            "share_whole": [pc(f["share"]) for f in q],
            "voluntary_share_of_dictations_pct": [pc(f["wV"]) for f in q],
        },
        "record": {"shares_1dp": ["%.1f" % (100 * x) for x in rec],
                   "late_min_1dp": "%.1f" % (100 * min(rec[6:])), "late_max_1dp": "%.1f" % (100 * max(rec[6:])),
                   "late_floor": int(math.floor(100 * min(rec[6:]))), "late_ceil": int(math.ceil(100 * max(rec[6:]))),
                   "gap_from_1dp": "%.1f" % (100 * C["gap"][0]), "gap_to_1dp": "%.1f" % (100 * C["gap"][1])},
        "evidence": {
            "heavy_share_frozen_pct": {"voluntary": "%.1f" % (100 * G["share"]["V"]),
                                       "compulsory": "%.1f" % (100 * G["share"]["M"])},
            "heavy_share_frozen_whole": {"voluntary": pc(G["share"]["V"]), "compulsory": pc(G["share"]["M"])},
            "release_steps_pct": {r: "%.0f" % (100 * (math.exp(G["steps"][r]) - 1)) for r in G["steps"]},
            "release_cuts_pct": {r: "%.0f" % (100 * (1 - math.exp(G["steps"][r] - G["steps"][p])))
                                 for p, r in zip(["3.4", "4.0", "5.0", "5.2"], ["4.0", "5.0", "5.2", "6.0"])},
            "golive_levels_pct": ["%.1f" % (100 * x) for x in C["golive_levels"]],
            "turnover_pct_year": "%.0f" % (100 * (1 - math.exp(-12 * G["lam"]))),
            "ramp_pct": ["%.0f" % (100 * x) for x in G["ramp"][:3]],
            "steady_volume_month": int(rnd(G["vM"])),
            "staff_in_post": C["P"].staff_in_post,
            "dictating_dec_2026": {h: sum(1 for p, d in G["per"].items() if d["last"] == GD.DEC and d["site_last"] == h)
                                   for h in ("SSU", "BKU")},
            "dictating_dec_2026_total": sum(1 for p, d in G["per"].items() if d["last"] == GD.DEC and d["site_last"] in
                                            ("SSU", "BKU")),
            "voluntary_share_2026_pct": pc(C["record_wV_2026"]),
            "staff_in_post_total": sum(C["P"].staff_in_post.values()),
        },
        "ladder": {k: {"shares_1dp": ["%.1f" % (100 * x) for x in v[0]], "ceiling": v[1]} for k, v in lad.items()},
        "no_ramp": {"p90_q4_pct": pc(C["no_ramp"]["q"][(2027, 4)]["p90"]), "first_past": C["no_ramp"]["first_past"],
                    "lowest_ceiling": C["no_ramp"]["bands"]},
        "constants": {"line_pct": 15, "ceilings_pct": list(GD.CEILINGS), "audit_rate_pct": "2.5",
                      "quarters": [1, 2, 3, 4], "year": 2027, "as_of": "2027-01-11", "frozen_release": "6.0",
                      "compulsory": {h[0]: GD.months_label(h[4]) for h in W.HOSPITALS if h[0] in ("SSU", "BKU")},
                      "rounding_units": [10000],
                      "nine_in_ten": 90, "record_years": [2023, 2026], "releases": ["3.4", "4.0", "5.0", "5.2", "6.0"]},
    }
    return F


def chart(C, F, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rec = [100 * x for x in C["record"]]
    fut = [100 * C["G"]["q"][k]["share"] for k in GD.Q27]
    xr = list(range(16))
    xf = list(range(16, 20))
    fig, ax = plt.subplots(figsize=(7.6, 3.6), dpi=150)
    ax.plot(xr, rec, color="#1D3557", marker="o", ms=3.5, lw=1.6, label="audited, 2023 to 2026")
    ax.plot([15] + xf, [rec[-1]] + fut, color="#C8553D", marker="o", ms=4, lw=1.8, ls="--", label="expected, 2027")
    for c in GD.CEILINGS:
        ax.axhline(c, color="#888888", lw=0.7, ls=":")
        ax.text(19.6, c + 0.12, "%d%%" % c, fontsize=7, color="#555555", ha="right")
    labels = ["%d Q%d" % (y, q) for y in (2023, 2024, 2025, 2026, 2027) for q in (1, 2, 3, 4)]
    ax.set_xticks(range(20))
    ax.set_xticklabels([l if l.endswith("Q1") or l.startswith("2027") else "" for l in labels], fontsize=7, rotation=0)
    ax.set_ylim(4, 17)
    ax.set_ylabel("share above 15% WER (%)", fontsize=8)
    ax.tick_params(axis="y", labelsize=7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(path, format="png", metadata={"Software": None})
    plt.close(fig)


def write_pdf(path, C, F, png):
    c, q, ev = F["call"], F["quarters_2027"], F["evidence"]
    sh = ev["heavy_share_frozen_pct"]
    rows = [["2027", "Expected share above 15%", "Lowest ceiling it stays under", "Voluntary clinicians' share of dictation"]]
    for i in range(4):
        rows.append(["Q%d" % (i + 1), "%s%%" % q["share_1dp"][i], "%d%%" % q["lowest_ceiling"][i],
                     "about %d%%" % q["voluntary_share_of_dictations_pct"][i]])
    s = [Paragraph("Larkmoor Speech: Recognition Quality", SMALL),
         Paragraph("Shannonside 2027 quality schedule: the heavy-correction ceiling", H1),
         Paragraph("12 January 2027. Jody Cahir, Head of Recognition Quality, for the account team.", SMALL),
         Paragraph("We should commit to Ceiling C, %d per cent." % c["ceiling_pct"], H2),
         Paragraph("A 10 per cent ceiling would be passed in the %s quarter of 2027 and a 12 per cent ceiling in the %s; "
                   "no quarter is expected to pass 14 per cent." % (QN[c["first_quarter_past_10"] - 1],
                                                                    QN[c["first_quarter_past_12"] - 1])),
         Image(png, width=480, height=227),
         Paragraph("The audited share has held between about %s and %s per cent since the middle of 2024, but that is two "
                   "movements cancelling. Each release has lowered every clinician's error rate (5.0 alone by about %s "
                   "per cent), while more and more of Shannonside's dictation has come from clinicians who began only once "
                   "their hospital made dictation compulsory: under release %s about %s per cent of their dictations "
                   "need heavy correction, against %s per cent for clinicians who chose to dictate. When no release came "
                   "between February 2023 and June 2024 the share rose from about %s per cent in the first half of 2023 to about %s "
                   "at the turn of the year."
                   % (F["record"]["late_floor"], F["record"]["late_ceil"], ev["release_cuts_pct"]["5.0"],
                      F["constants"]["frozen_release"],
                      sh["compulsory"], sh["voluntary"], F["record"]["gap_from_1dp"], F["record"]["gap_to_1dp"])),
         Paragraph("In 2027 recognition stays on release 6.0 for the Dublin migration, and Shannonside University "
                   "(%s) and Ballykeel University (%s) make dictation compulsory for about %s clinicians in "
                   "post, of whom only %s dictate today. Their rows read low now because only those who chose to "
                   "dictate appear in them. With the clinicians who leave replaced by compulsory starters at the record's "
                   "rate and the go-lives ramping up as the six earlier ones did, the voluntary clinicians' share of "
                   "dictation falls from about %s per cent in December 2026 to under two fifths by the fourth quarter."
                   % (F["constants"]["compulsory"]["SSU"], F["constants"]["compulsory"]["BKU"],
                      format(sum(ev["staff_in_post"].values()), ","), format(sum(ev["dictating_dec_2026"].values()), ","),
                      ev["voluntary_share_2026_pct"])),
         Table(rows, colWidths=[50, 130, 150, 160]),
         Paragraph("Nine in ten of the fourth quarter's dictations are expected to stay under %d per cent word error "
                   "rate." % q["p90_q4_pct"]),
         Paragraph("Reweighting today's audited shares to 2027's hospitals would put every quarter under %d per cent, "
                   "and giving 2027's new dictators the level of the clinicians who began in 2025 and 2026 would stop at "
                   "%d; the first reads the teaching hospitals' clinicians as the few who dictate there now, the second "
                   "mixes those who chose to dictate with those who had to."
                   % (F["ladder"]["R1 each hospital's 2026 share at 2027's hospital mix"]["ceiling"],
                      F["ladder"]["R2 starters at the 2025 and 2026 starters' level"]["ceiling"]), SMALL)]
    officepdf.build(path, s, "Shannonside 2027 quality schedule: the heavy-correction ceiling", "Jody Cahir",
                    "Heavy-correction ceiling 2027", "Larkmoor Speech | Recognition Quality | Shannonside 2027",
                    dt.datetime(2027, 1, 11, 15, 20, tzinfo=GMT), dt.datetime(2027, 1, 12, 10, 5, tzinfo=GMT),
                    producer="LibreOffice 24.8")


def write_xlsx(path, C, F):
    q = F["quarters_2027"]
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 quarters"
    ws.append(["quarter", "expected_share_above_15pct", "lowest_ceiling_pct", "voluntary_share_of_dictations_pct"])
    for i in range(4):
        ws.append(["2027 Q%d" % (i + 1), float(q["share_1dp"][i]) / 100, q["lowest_ceiling"][i],
                   q["voluntary_share_of_dictations_pct"][i]])
        ws.cell(ws.max_row, 2).number_format = "0.0%"
    ws.append([])
    ws.append(["word error rate nine in ten fourth-quarter dictations stay under (per cent)", q["p90_q4_pct"]])
    ws.append(["ceiling committed (per cent)", F["call"]["ceiling_pct"]])
    ws2 = wb.create_sheet("record")
    ws2.append(["quarter", "audited_share_above_15pct"])
    for (y, qq), x in zip([(y, qq) for y in (2023, 2024, 2025, 2026) for qq in (1, 2, 3, 4)], C["record"]):
        ws2.append(["%d Q%d" % (y, qq), x])
        ws2.cell(ws2.max_row, 2).number_format = "0.0%"
    ws3 = wb.create_sheet("basis")
    ev = F["evidence"]
    for row in [["heavy share under release 6.0, clinicians who began before their hospital's compulsory date",
                 float(ev["heavy_share_frozen_pct"]["voluntary"]) / 100],
                ["heavy share under release 6.0, clinicians who began on or after it",
                 float(ev["heavy_share_frozen_pct"]["compulsory"]) / 100],
                ["clinicians leaving a year", float(ev["turnover_pct_year"]) / 100],
                ["go-live ramp, first three months against later months",
                 ", ".join("%s%%" % x for x in ev["ramp_pct"])],
                ["dictations a month, a compulsory starter after the ramp", ev["steady_volume_month"]]]:
        ws3.append(row)
        if isinstance(row[1], float):
            ws3.cell(ws3.max_row, 2).number_format = "0.0%"
    for sh_ in (ws, ws2, ws3):
        for cell in sh_[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="1D3557")
            cell.alignment = Alignment(wrap_text=True, vertical="center")
    for k, wd in enumerate([62, 26, 20, 30], 1):
        ws.column_dimensions[get_column_letter(k)].width = wd
    ws2.column_dimensions["A"].width = 12
    ws2.column_dimensions["B"].width = 26
    ws3.column_dimensions["A"].width = 88
    ws3.column_dimensions["B"].width = 18
    wb.save(path)
    postprocess.normalize_ooxml(path, "Jody Cahir", "Jody Cahir", "2027-01-11T09:12:00Z", "2027-01-12T09:48:00Z",
                                "Heavy correction 2027", excel=True, company="Larkmoor Speech")


def write_all(C, golden_dir, gen_dir, scratch):
    F = figures(C)
    os.makedirs(golden_dir, exist_ok=True)
    write_xlsx(os.path.join(golden_dir, "heavy_correction_2027.xlsx"), C, F)
    png = os.path.join(scratch, "ceiling.png")
    chart(C, F, png)
    write_pdf(os.path.join(golden_dir, "quality_schedule_2027_ceiling.pdf"), C, F, png)
    with open(os.path.join(gen_dir, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False)
    return F
