"""task7 architecture 10: the golden deliverables, the board memo (Word) and the workbook the renewals are priced in,
with figures.json and effort.json; every figure from checks.results on the cut pack."""
import datetime as dt
import json
import os

import numpy as np
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Mm, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import checks as CK
import golden as GD
import postprocess
import verify as V

INK, KEEP, DROP = "#22415E", "#2E7D5B", "#B5543C"


def head_row(ws, widths, row=1):
    for c in ws[row]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="22415E")
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for k, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = wd
    ws.freeze_panes = ws.cell(row=row + 1, column=1).coordinate


def fmt(ws, cols, f, start=2):
    for col in cols:
        for r in range(start, ws.max_row + 1):
            c = ws.cell(row=r, column=col)
            if isinstance(c.value, (int, float)):
                c.number_format = f


def details(C):
    P = C["P"]
    slopes = GD.cooling_slopes(P)
    pred = GD.home_model(P, slopes, "log")
    out = {}
    for p in P.providers:
        d = {}
        GD.value(P, p, True, True, True, slope_pred=pred, detail=d)
        out[p] = d
    return out


def write_xlsx(path, C, F, D):
    P = C["P"]
    wb = Workbook()
    ws = wb.active
    ws.title = "providers"
    ws.append(["provider", "quoted price per enrolled device, summer 2027 (USD)", "kW per device the price needs",
               "kW per 2027 device at the 4CP intervals", "price at which renewing breaks even (USD)",
               "devices enrolled 1 July 2027", "what the quote costs (USD)", "renew"])
    for p in P.providers:
        ws.append([p, F["price"][p], F["bar_kw"][p], F["kw"][p], F["breakeven_price"][p], F["n27"][p], F["cost"][p],
                   "yes" if p in F["renewed"] else "no"])
    ws.append([])
    ws.append(["renewed providers, in all", None, None, None, None, sum(F["n27"][p] for p in F["renewed"]), F["paid_usd"]])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    ws.append(["their reduction of the 4CP load (MW)", F["mw"]])
    ws.append(["the transmission cost it saves (USD)", F["saving_usd"]])
    ws.append(["net of what the co-op pays them (USD)", F["net_usd"]])
    head_row(ws, [34, 16, 14, 16, 16, 14, 14, 8])
    fmt(ws, (2, 5), "0.00")
    fmt(ws, (3, 4), "0.000")
    fmt(ws, (6, 7), "#,##0")
    for r in range(ws.max_row - 2, ws.max_row + 1):
        ws.cell(row=r, column=2).number_format = "0.00" if r == ws.max_row - 2 else "#,##0"
    ws2 = wb.create_sheet("4CP intervals")
    ws2.append(["4CP date", "interval ending", "co-op alert called"] + ["%s (kW per 2027 device)" % p for p in P.providers])
    for cp in P.cps:
        row = [cp["date"], "%02d:%02d" % divmod(cp["start"] + 15, 60), "yes" if cp["called"] else "no"]
        for p in P.providers:
            x = D[p].get(cp["date"])
            row.append(round(x["kw"], 3) if x else 0.0)
        ws2.append(row)
    ws2.append([])
    ws2.append(["average over the twelve intervals", None, None] + [F["kw"][p] for p in P.providers])
    head_row(ws2, [12, 10, 10] + [14] * len(P.providers))
    for r in range(2, ws2.max_row + 1):
        ws2.cell(row=r, column=1).number_format = "yyyy-mm-dd"
    fmt(ws2, range(4, 4 + len(P.providers)), "0.000")
    ws3 = wb.create_sheet("in the event")
    ws3.append(["provider", "share of called devices in the event at 17:30, test events",
                "share of enrolled devices in the event at the 4CP intervals, 4CP days",
                "share for the 2027 fleet at the 4CP intervals"])
    for p in P.providers:
        s27 = float(np.mean([D[p][d]["share"] for d in D[p]])) if D[p] else None
        ws3.append([p, F["share_test"][p], F["share_cp"][p], round(s27, 2) if s27 is not None else None])
    ws3.append([])
    ws3.append(["A device is in the event while it is reached and its member has not left the event; a device a provider "
                "did not reach (offline at dispatch, or left out of its report) counts as not in the event. Ondera's "
                "window ends at %s, so its share is the share that ran to the end of the window." % F["window_end"]["Ondera"]])
    head_row(ws3, [16, 22, 24, 20])
    fmt(ws3, (2, 3, 4), "0.00")
    ws4 = wb.create_sheet("2027 fleets")
    ws4.append(["provider", "enrolled 30 Oct 2026", "of which retail instant rebate", "new enrolments planned 2027",
                "devices enrolled 1 July 2027", "retail share 2027", "quoted price (USD)", "what the quote costs (USD)"])
    for p in P.providers:
        now = [v for v in GD.provider_devices(P, p) if V.active(v, GD.ASOF)]
        ws4.append([p, len(now), sum(1 for v in now if v["ch"] == "retail"), sum(P.quote[p]["new"].values()), F["n27"][p],
                    F["retail_share27"][p], F["price"][p], F["cost"][p]])
    ws4.append([])
    ws4.append(["Each device enrolled on 30 October 2026 is carried to 1 July 2027 at its channel's leaving rate since "
                "2021 (devices leaving a year per device-year enrolled); the quotes' new enrolments are taken as enrolled "
                "by 1 July, like each provider's 2025 and 2026 enrolments through the same channel."])
    head_row(ws4, [16, 12, 14, 14, 14, 11, 11, 14])
    fmt(ws4, (2, 3, 4, 5, 8), "#,##0")
    fmt(ws4, (6,), "0.00")
    fmt(ws4, (7,), "0.00")
    ws5 = wb.create_sheet("homes")
    ws5.append(["provider", "research-sample devices", "the 2027 fleet's cooling slope over the research sample's"])
    for p in P.providers:
        ws5.append([p, len(GD.ami_devices(P, p)), F["transport"][p]])
    ws5.append([])
    ws5.append(["A home's cooling slope (kW of afternoon load per degree of heat) is read off each research-sample home's "
                "quiet days and held-back test events, then predicted for every home from its living area and year built "
                "in the appraisal roll; a device in the event sheds in proportion to its home's slope."])
    head_row(ws5, [16, 12, 22])
    fmt(ws5, (3,), "0.00")
    ws6 = wb.create_sheet("other routes")
    ws6.append(["route", "renews"] + ["%s (kW per device)" % p for p in P.providers])
    labels = {"the golden": "this appraisal"}
    for name, st in F["routes"].items():
        kw = F["kw"] if name == "the golden" else F["routes_kw"][name]
        ws6.append([labels.get(name, name), ", ".join(st) or "none"] + [kw[p] for p in P.providers])
    head_row(ws6, [58, 44] + [12] * len(P.providers))
    fmt(ws6, range(3, 3 + len(P.providers)), "0.000")
    ws7 = wb.create_sheet("notes")
    for line in [
            ("Source", "Cedar Brake's Peak Partners roster, test assignments, event log and research-sample 15-minute reads; "
                       "the six providers' event reports; ERCOT's 4CP intervals; the KCDR weather station; the Calder "
                       "appraisal district's residential roll; the providers' quotes for summer 2027"),
            ("Reduction", "what the co-op's load would have been in a 4CP interval without the provider's event, less what "
                          "it was, per device enrolled on 1 July 2027 (Board Policy 412, section 4)"),
            ("Summer", "a summer like 2024 to 2026: the twelve 4CP intervals of those summers, the co-op's alerts as called "
                       "(none on %s), each provider's quoted event settings" % " or ".join(F["missed_cp"])),
            ("Rate", "USD %.2f per kW of 4CP load a year (the 2027 transmission charge notice)" % P.rate),
            ("Precision", "kW to the thousandth, shares to the hundredth, money to the dollar (totals to the hundred), "
                          "devices whole")]:
        ws7.append(list(line))
    ws7.column_dimensions["A"].width = 12
    ws7.column_dimensions["B"].width = 112
    for c in ws7["A"]:
        c.font = Font(bold=True)
    wb.save(path)
    postprocess.normalize_ooxml(path, "Renee Henry", "Renee Henry", "2026-11-03T15:10:00Z", "2026-11-09T22:41:00Z",
                                "Peak Partners provider renewals, summer 2027", excel=True,
                                company="Cedar Brake Electric Cooperative")


def chart(F, scratch):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "task7"})
    ps = F["providers"]
    fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=200)
    y = np.arange(len(ps))[::-1]
    for yy, p in zip(y, ps):
        col = KEEP if p in F["renewed"] else DROP
        ax.barh(yy, F["kw"][p], color=col, height=0.55)
        ax.plot([F["bar_kw"][p]] * 2, [yy - 0.38, yy + 0.38], color=INK, lw=1.6)
        ax.text(max(F["kw"][p], F["bar_kw"][p]) + 0.03, yy, "%.2f kW against %.2f" % (F["kw"][p], F["bar_kw"][p]),
                va="center", fontsize=7.4, color=INK)
    ax.axvline(0, color="#888888", lw=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels(ps)
    ax.set_xlabel("kW per 2027 device off the co-op's load at the 4CP intervals (bar); the kW its price needs (line)")
    ax.set_xlim(min(-0.25, min(F["kw"].values()) - 0.05), max(F["kw"].values()) + 0.45)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    path = os.path.join(scratch, "providers.png")
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)
    return path


def write_memo(path, F, png):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(215.9), Mm(279.4)
    for side in ("left_margin", "right_margin"):
        setattr(sec, side, Mm(22))
    sec.top_margin, sec.bottom_margin = Mm(18), Mm(18)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)

    def para(text, bold=False, size=None, color=None, space=4):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color.lstrip("#"))
        p.paragraph_format.space_after = Pt(space)
        return p
    para("Cedar Brake Electric Cooperative, Energy Programs", size=8.5, color="#555555", space=1)
    para("To: the board of directors    From: Renee Henry, manager of energy programs    Date: 9 November 2026",
         size=8.5, color="#555555", space=1)
    para("Peak Partners provider renewals for summer 2027", bold=True, size=14, color=INK, space=6)
    keep, drop = F["renewed"], [p for p in F["providers"] if p not in F["renewed"]]
    para("Renew %s and %s; do not renew %s." % (", ".join(keep[:-1]), keep[-1], ", ".join(drop[:-1]) + " or " + drop[-1]),
         bold=True, space=4)
    para("Under Board Policy 412 a provider is worth renewing when its devices take enough off our load in ERCOT's four "
         "coincident-peak intervals to save more transmission cost, at $%.2f per kW, than its quote costs us. In a summer "
         "like 2024 to 2026 the three renewed providers' devices would take %.2f MW off our 4CP load and save $%s, "
         "$%s more than we would pay them." % (F["rate"], F["mw"], format(F["saving_usd"], ","), format(F["net_usd"], ",")))
    t = doc.add_table(rows=1, cols=6)
    t.style = "Table Grid"
    hdr = ["Provider", "kW per 2027 device at the 4CP intervals", "kW its price needs", "Devices on 1 July 2027",
           "Quote's cost", "Renew"]
    for c, h in zip(t.rows[0].cells, hdr):
        c.text = h
        for r in c.paragraphs[0].runs:
            r.bold = True
            r.font.size = Pt(8.5)
    for p in F["providers"]:
        cells = t.add_row().cells
        vals = [p, "%.3f" % F["kw"][p], "%.3f" % F["bar_kw"][p], format(F["n27"][p], ","), "$" + format(F["cost"][p], ","),
                "yes" if p in keep else "no"]
        for c, v in zip(cells, vals):
            c.text = v
            for r in c.paragraphs[0].runs:
                r.font.size = Pt(8.5)
    para("Each figure is per device enrolled on 1 July 2027, averaged over the twelve 4CP intervals of 2024 to 2026 with "
         "our alerts as we called them (none on %s)." % " or ".join(F["missed_cp"]), size=8, color="#555555", space=6)
    doc.add_picture(png, width=Mm(160))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    para("Why the test events overstate Lumivale and Pinecrest Home, and understate Kitebrook", bold=True, color=INK, space=2)
    para("Our test events are single hot days. The 4CP intervals fall on the hottest day of a heat wave, after two or more "
         "alert days in a row, when members leave events: on those days %.0f%% of Lumivale's enrolled devices were still "
         "in its long, deep event at the 4CP interval, against %.0f%% on the test events at 17:30. Pinecrest Home's 2027 "
         "fleet will be %.0f%% retail-rebate devices, which are often offline and leave events: its fleet would keep %.0f%% "
         "in the event at the 4CP intervals against today's %.0f%%. The research sample's homes are in the north and "
         "newer; Kitebrook's fleet is mostly in larger, older homes in the south, which shed %.0f%% more than its sample "
         "devices." % (100 * F["share_cp"]["Lumivale"], 100 * F["share_test"]["Lumivale"],
                       100 * F["retail_share27"]["Pinecrest Home"], 100 * F["share27"]["Pinecrest Home"][0],
                       100 * F["share27"]["Pinecrest Home"][1], 100 * (F["transport"]["Kitebrook"] - 1)))
    para("Ondera's event ends at %s, before %d of the twelve 4CP intervals, and its homes are recovering then: its "
         "devices add load at the 4CP intervals." % (F["window_end"]["Ondera"], F["after_window"]["Ondera"]))
    para("Read straight off the test events, Lumivale and Pinecrest Home would be renewed and Kitebrook dropped. The "
         "workbook carries the twelve intervals, the shares in the event, the 2027 fleets, the homes and the other routes.",
         space=2)
    doc.save(path)
    postprocess.normalize_docx(path, "Renee Henry", "Renee Henry", "2026-11-04T14:02:00Z", "2026-11-09T22:18:00Z", 9, 214,
                               "task7-memo", title="Peak Partners provider renewals for summer 2027",
                               company="Cedar Brake Electric Cooperative")


def write_all(C, golden_dir, gen_dir, scratch):
    F = CK.figures(C)
    D = details(C)
    write_xlsx(os.path.join(golden_dir, "provider_renewals_2027_workbook.xlsx"), C, F, D)
    png = chart(F, scratch)
    write_memo(os.path.join(golden_dir, "provider_renewals_2027_memo.docx"), F, png)
    with open(os.path.join(gen_dir, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False, default=str)
    E = CK.effort(C, F)
    with open(os.path.join(gen_dir, "effort.json"), "w", encoding="utf-8") as fh:
        json.dump(E, fh, indent=1, ensure_ascii=False, default=str)
    return F
