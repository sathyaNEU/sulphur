"""The golden deliverables, every figure computed from the pack by analysis.py: district_handover_2027.xlsx (the
districts in Owenduff's offer, going or staying, and each run's 2027 van-hours saved, with the year's net saving) and
handover_2027.png (each of those runs' 2027 van-hours before and after the hand-over)."""
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import analysis as A

XLSX = "district_handover_2027.xlsx"
PNG = "handover_2027.png"
RUN_NAMES = {"R01": "Castlebar town", "R02": "Claremorris", "R03": "Westport and Louisburgh", "R04": "Newport and Achill",
             "R05": "Connemara", "R06": "Ballinrobe and Cong", "R07": "Crossmolina and Erris",
             "R08": "Ballina and the north coast", "R09": "East Mayo"}


def r50(x):
    return int(50 * math.floor(x / 50.0 + 0.5))


def r5000(x):
    return int(5000 * math.floor(x / 5000.0 + 0.5))


def compute(target):
    pk = A.Pack(target)
    res = A.golden(pk)
    offer = A.offered(pk)
    runs = [r for r in pk.runs if res["runs"][r]["cand"]]
    fig = {"set": sorted(res["set"], key=offer.index), "net_saving": res["saving"],
           "net_saving_rounded": r5000(res["saving"]), "price": A.PRICE, "rate": pk.rate, "runs": {}, "districts": {}}
    for r in runs:
        rr = res["runs"][r]
        fig["runs"][r] = {"name": RUN_NAMES[r], "before_h": rr["base_h"], "after_h": rr["after_h"],
                          "saved_h": rr["hours"], "saved_h_rounded": r50(rr["hours"]), "before_rounded": r50(rr["base_h"]),
                          "after_rounded": r50(rr["after_h"]), "charge": rr["charge"], "net": rr["net"],
                          "districts": rr["set"]}
    for c in offer:
        fig["districts"][c] = {"name": pk.reg[c]["name"], "run": pk.reg[c]["run"], "goes": c in res["set"],
                               "parcels_2027": sum(pk.plan[c]), "charge_2027": sum(pk.plan[c]) * A.PRICE}
    return pk, res, fig


THIN = Side(style="thin", color="B7BEC9")
HEAD = Font(bold=True, color="FFFFFF")
HFILL = PatternFill("solid", fgColor="2F4A66")
YES = PatternFill("solid", fgColor="E3EFE0")


def _head(ws, row, vals, widths=None):
    for j, v in enumerate(vals, 1):
        c = ws.cell(row=row, column=j, value=v)
        c.font, c.fill = HEAD, HFILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = w


def write_xlsx(path, pk, res, fig):
    wb = Workbook()
    ws = wb.active
    ws.title = "Districts"
    ws["A1"] = "Owenduff offer OC-2027-114: districts going and staying from 1 January 2027"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "EUR %.2f a parcel delivered (Owenduff, 2027); plan parcels from the commercial plan of 19 October 2026" % A.PRICE
    _head(ws, 4, ["Code", "District", "Run", "2027 plan parcels", "Owenduff charge 2027 (EUR)", "Decision"],
          [8, 20, 26, 16, 22, 12])
    i = 5
    for c, d in fig["districts"].items():
        vals = [c, d["name"], "%s %s" % (d["run"], RUN_NAMES[d["run"]]), d["parcels_2027"], round(d["charge_2027"], -2),
                "Goes" if d["goes"] else "Stays"]
        for j, v in enumerate(vals, 1):
            cell = ws.cell(row=i, column=j, value=v)
            cell.border = Border(bottom=THIN)
            if j in (4, 5):
                cell.number_format = "#,##0"
            if d["goes"]:
                cell.fill = YES
        i += 1
    ws.freeze_panes = "A5"

    ws2 = wb.create_sheet("Runs")
    ws2["A1"] = "2027 van-hours on the runs that serve an offered district, before and after the hand-over"
    ws2["A1"].font = Font(bold=True, size=12)
    ws2["A2"] = "Van-hours depot out to depot in, to the nearest 50; all-in rate EUR %.2f a van-hour (fleet rate card 2027)" % pk.rate
    _head(ws2, 4, ["Run", "Districts handed over", "Van-hours 2027 as things stand", "Van-hours 2027 after the hand-over",
                   "Van-hours saved", "Cost of the hours saved (EUR)", "Owenduff charges (EUR)", "Net saving (EUR)"],
          [26, 30, 16, 16, 12, 18, 16, 14])
    i = 5
    for r, d in fig["runs"].items():
        names = ", ".join(pk.reg[c]["name"] for c in d["districts"]) or "none"
        vals = ["%s %s" % (r, d["name"]), names, d["before_rounded"], d["after_rounded"], d["saved_h_rounded"],
                round(d["saved_h"] * pk.rate, -2), round(d["charge"], -2), round(d["net"], -2)]
        for j, v in enumerate(vals, 1):
            cell = ws2.cell(row=i, column=j, value=v)
            cell.border = Border(bottom=THIN)
            if j >= 3:
                cell.number_format = "#,##0"
        i += 1
    ws2.cell(row=i + 1, column=1, value="Net saving 2027, to the nearest EUR 5,000").font = Font(bold=True)
    c = ws2.cell(row=i + 1, column=8, value=fig["net_saving_rounded"])
    c.font, c.number_format = Font(bold=True), "#,##0"
    ws2.cell(row=i + 2, column=1, value="Net saving 2027 before rounding")
    ws2.cell(row=i + 2, column=8, value=round(fig["net_saving"], -2)).number_format = "#,##0"

    ws2.print_title_rows = "4:4"
    ws.print_title_rows = "4:4"
    ws4 = wb.create_sheet("Notes")
    notes = [
        ("Basis", "NPS-3 version 2, section 4: the saving is the cost at the 2027 all-in van-hour rate of the van-hours "
                  "the hand-over takes off our runs, less Owenduff's charges for the districts' 2027 plan parcels."),
        ("Van-hours", "Depot out to depot in as the van run log records them (NPS-3 2.3), the driver's break included; "
                      "the break is taken on every run-day and is not saved by a hand-over."),
        ("Data", "Stop log and van run log 2 January 2025 to 30 October 2026; re-synced stop rows counted once; Castlebar "
                 "north and south counted as Castlebar town (register code change of 1 April 2026)."),
        ("2027", "Commercial plan of 19 October 2026, 251 delivery days in the 2027 calendar, EUR 58.00 a van-hour, "
                 "Owenduff EUR 12.60 a parcel delivered."),
        ("Rounding", "Van-hours to the nearest 50 and the net saving to the nearest EUR 5,000, each rounded once from the "
                     "unrounded total; euro columns on the Runs sheet to the nearest EUR 100."),
        ("Prepared", "Aislinn Duffin, transport planning, 6 November 2026, for the 2027 budget committee.")]
    for i, (k, v) in enumerate(notes, 1):
        ws4.cell(row=i, column=1, value=k).font = Font(bold=True)
        c4 = ws4.cell(row=i, column=2, value=v)
        c4.alignment = Alignment(wrap_text=True, vertical="top")
    ws4.column_dimensions["A"].width = 12
    ws4.column_dimensions["B"].width = 100
    ws3 = wb.create_sheet("Workings")
    ws3["A1"] = "Road sections and district times fitted on the 2025 and 2026 stop log (hours)"
    ws3["A1"].font = Font(bold=True)
    _head(ws3, 3, ["Run", "District", "Section from the district before (h)", "District access (h)",
                   "Door time a stop (h)", "Drive between its stops (h)", "Stops a parcel", "2027 stops a delivery day (Jan)",
                   "2027 stops a delivery day (Jul)"], [8, 18, 16, 12, 12, 14, 10, 14, 14])
    i = 4
    model, per, mus = res["model"], res["per"], res["mus"]
    for r in pk.runs:
        for c in model[r]["chain"]:
            vals = [r, pk.reg.get(c, {"name": c})["name"] if c in pk.reg else "Castlebar town", round(model[r]["e"][c], 3),
                    round(model[r]["a"][c], 3), round(per[c]["door"], 3), round(per[c]["local"], 3),
                    round(per[c]["stops_per_parcel"], 3), round(mus[c][0], 2), round(mus[c][6], 2)]
            for j, v in enumerate(vals, 1):
                ws3.cell(row=i, column=j, value=v)
            i += 1
    ws3.cell(row=i + 1, column=1, value="A section is driven on a delivery day when any district beyond it on the run "
                                        "has a stop; the 2027 day counts each district's month of plan stops.")
    wb.properties.creator = "Aislinn Duffin"
    wb.save(path)


def write_png(path, pk, res, fig):
    runs = list(fig["runs"])
    labels = ["%s\n%s" % (r, RUN_NAMES[r].replace(" and ", " &\n").replace("Ballina &\nthe north coast", "Ballina &\nnorth coast")) for r in runs]
    before = [fig["runs"][r]["before_rounded"] for r in runs]
    after = [fig["runs"][r]["after_rounded"] for r in runs]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    figr, ax = plt.subplots(figsize=(9.2, 4.8), dpi=150)
    x = range(len(runs))
    b1 = ax.bar([i - 0.2 for i in x], before, 0.38, color="#9AA8B8", label="2027 as things stand")
    b2 = ax.bar([i + 0.2 for i in x], after, 0.38, color="#2F6B4F", label="2027 after the hand-over")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 15, "{:,}".format(int(b.get_height())),
                    ha="center", va="bottom", fontsize=7.5)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=7.8)
    ax.set_ylabel("Van-hours in 2027 (nearest 50)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, max(before) * 1.15)
    nm = [pk.reg[c]["name"] for c in fig["set"]]
    names = ", ".join(nm[:-1]) + " and " + nm[-1]
    from matplotlib.ticker import FuncFormatter
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: "{:,}".format(int(v))))
    figr.text(0.01, 0.01, "Source: Brackloon stop log and van run log 2025 to October 2026; 2027 plan, calendar and rate card; "
              "Owenduff offer OC-2027-114. Van-hours depot out to depot in (NPS-3 2.3).", fontsize=6.8, color="#555555")
    ax.set_title("Handing %s to Owenduff saves about EUR {:,} net in 2027".format(fig["net_saving_rounded"]) % names,
                 fontsize=9.5, loc="left", wrap=True)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    figr.tight_layout(rect=(0, 0.03, 1, 1))
    figr.savefig(path, dpi=150, metadata={"Software": None})
    plt.close(figr)


def write(target, outdir):
    pk, res, fig = compute(target)
    os.makedirs(outdir, exist_ok=True)
    write_xlsx(os.path.join(outdir, XLSX), pk, res, fig)
    write_png(os.path.join(outdir, PNG), pk, res, fig)
    return pk, res, fig
