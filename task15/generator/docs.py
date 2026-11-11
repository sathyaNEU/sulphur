"""Fjordkob's own documents: the pilot agreement with Kornblomst Analytics (signed in February, its price annex
updated in September), exported to PDF by the house word-processor writer, and business intelligence's pilot
dashboard workbook for week 35, computed from the shipped daily extract and order proposal log."""
import datetime as dt
import os

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import pack as PK
import postprocess as PP
import world as W

CET = dt.timezone(dt.timedelta(hours=1))
CEST = dt.timezone(dt.timedelta(hours=2))


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=14,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


AGREEMENT = [
    ("1. Parties and purpose", [
        "Fjordkøb A/S, Aarhus (Fjordkøb) and Kornblomst Analytics ApS, Copenhagen (Kornblomst) agree a trial of "
        "Kornblomst Fresh Forecast in Fjordkøb's ordering of fresh goods, so that Fjordkøb's board of directors can "
        "decide at its meeting on 6 October 2026 whether to license the forecast for 2027."]),
    ("2. The pilot", [
        "2.1 From the order proposals for delivery on Monday 2 March 2026 to those for delivery on Sunday 30 August "
        "2026 (26 weeks), Kornblomst's forecast replaces AutoOrdre's forecast in the fresh order proposals of the "
        "pilot stores listed in Annex 1. The pilot stores were chosen by Fjordkøb's regional managers.",
        "2.2 Every other part of the ordering is unchanged in the pilot stores: the ERP's order-up-to rule, the case "
        "packs, the delivery schedule from the fresh warehouse in Aarhus, the promotion plan and the stores' own "
        "counting of stock and write-offs.",
        "2.3 The pilot stores set their safety stock with Kornblomst's recommended service factor of 0.75. The other "
        "stores keep the ERP's standard factor of 1.05.",
        "2.4 From 2 March 2026 Kornblomst computes its forecast every evening for every Fjordkøb store and fresh "
        "item, and the ERP logs it in the order proposal log beside AutoOrdre's forecast. Only the pilot stores "
        "order on it during the pilot."]),
    ("3. Data", [
        "Fjordkøb gives Kornblomst read access to its daily store and item extract, its promotion plan and its "
        "weather service for the term of the pilot. Kornblomst uses the data for the pilot only and deletes it "
        "within 60 days of the pilot's end unless a licence is signed."]),
    ("4. The 2027 decision", [
        "4.1 Fjordkøb takes Kornblomst Fresh Forecast for a store format from 1 January 2027 if, and only if, the "
        "expected saving per store and year in that format is greater than the format's licence price in Annex 2. A "
        "format is taken for all of its stores or for none of them.",
        "4.2 The saving of a store is the change in its fresh result from ordering on Kornblomst's forecast at the "
        "recommended setting instead of on AutoOrdre. An order changes what is on a store's shelves, not what its "
        "customers come in for, so the saving has two parts: the fresh waste the store avoids, valued at cost price, "
        "and the change in its out-of-stock sales, the fresh units its customers would have bought after a shelf had "
        "run empty, valued at their gross margin. Fewer out-of-stock sales add to the saving and more take from it. "
        "Gross margin is the sales value excluding VAT less the cost price of the units.",
        "4.3 A year is 52 weeks, taken as twice the 26 weeks of the pilot. A format's expected saving per store is "
        "the average over every store of that format in Fjordkøb's store register, pilot stores and other stores "
        "alike.",
        "4.4 Fjordkøb signs or declines the licence for each format by 1 November 2026. A format not taken stays on "
        "AutoOrdre for 2027."]),
    ("5. Fees", [
        "The pilot is free of charge. The licence prices in Annex 2 hold for 2027 if Fjordkøb signs by 1 November "
        "2026, are stated excluding VAT and are invoiced quarterly in advance."]),
]


def agreement(path, R):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("Fjordkøb A/S and Kornblomst Analytics ApS", small),
         Paragraph("Pilot agreement: Kornblomst Fresh Forecast in Fjordkøb's fresh ordering", h1),
         Paragraph("Agreement FK-2026-014, signed 19 February 2026. Annex 2 replaced on 1 September 2026 with "
                   "Kornblomst's 2027 price list.", small), Spacer(1, 4)]
    for head, paras in AGREEMENT:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    s.append(Paragraph("Annex 1. The pilot stores", h2))
    rows = [["Store", "Name", "Format"]]
    for k in np.argsort(W.SNO):
        if W.ISPILOT[k]:
            rows.append([str(int(W.SNO[k])), W.SNAME[k].replace("Fjordkob", "Fjordkøb"), W.FMT[k]])
    s.append(_grid(rows, [22 * 2.83, 80 * 2.83, 30 * 2.83], cell))
    s.append(Paragraph("Annex 2. Kornblomst Fresh Forecast, licence prices for 2027", h2))
    rows = [["Store format", "Licence per store and year, DKK excluding VAT"]]
    for f, nm in [("Super", "Super"), ("Kvarter", "Kvarter (neighbourhood stores)"), ("To Go", "To Go")]:
        rows.append([nm, "{:,}".format(int(W.LICENCE[f]))])
    s.append(_grid(rows, [60 * 2.83, 80 * 2.83], cell))
    s.append(Spacer(1, 4))
    s.append(Paragraph("The licence covers the nightly forecast for every fresh item of a store, the service factor "
                       "recommendation and Kornblomst's support desk on weekdays from 07 to 17.", body))
    s.append(Spacer(1, 8))
    s.append(Paragraph("For Fjordkøb A/S: Jakob Lauritsen, head of supply chain planning. For Kornblomst Analytics "
                       "ApS: Ludvig Bertelsen, account manager.", small))
    O.build(path, s, "Pilot agreement FK-2026-014", "Jakob Lauritsen", "Pilot agreement",
            "Fjordkøb A/S · Kornblomst Analytics ApS · Agreement FK-2026-014", dt.datetime(2026, 9, 1, 14, 2, tzinfo=CEST),
            dt.datetime(2026, 9, 1, 14, 6, tzinfo=CEST), page_of=True, producer="LibreOffice 25.2")


# ---------------------------------------------------------------------------------------------------- the dashboard
def dashboard_rows(target):
    """The dashboard's figures from the shipped files: the deduplicated daily extracts and the order proposal log."""
    import golden as GD
    T = GD.load(target)
    d = T["daily"]
    isp = d["store"].isin(T["pilot"])
    out = []
    fc = T["fc"]
    fc = fc[fc["date"] >= "2026-03-02"].copy()
    fc["used"] = np.where(fc["basis"] == "Kornblomst", fc["f_korn"], fc["f_auto"])
    m = fc.merge(d[["date", "store", "item", "sold"]], on=["date", "store", "item"], how="inner")
    iso = m["date"].dt.isocalendar()
    m["week"] = iso["week"].astype(int)
    m["pilot"] = m["store"].isin(T["pilot"])
    m["abs"] = (m["used"] - m["sold"]).abs()
    for wk in range(10, 36):
        for grp, g in [("Pilotbutikker", isp), ("Øvrige butikker", ~isp)]:
            x26 = d[(d["year"] == 2026) & (d["week"] == wk) & g]
            x25 = d[(d["year"] == 2025) & (d["week"] == wk) & g]
            mm = m[(m["week"] == wk) & (m["pilot"] == (grp == "Pilotbutikker"))]
            out.append(dict(week=wk, group=grp, sales26=float(x26["sales"].sum()), waste26=float(x26["waste_val"].sum()),
                            sales25=float(x25["sales"].sum()), waste25=float(x25["waste_val"].sum()),
                            avail26=float((x26["close"] > 0).mean()), avail25=float((x25["close"] > 0).mean()),
                            acc26=float(1 - mm["abs"].sum() / mm["sold"].sum())))
    return out


def dashboard(path, target, stamp):
    rows = dashboard_rows(target)
    wb = Workbook()
    ws = wb.active
    ws.title = "Uge for uge"
    ws["A1"] = "Kornblomst-pilot, friskvarer: ugerapport til og med uge 35"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Spørgsmål: hvordan udvikler svind og tilgængelighed ved lukning sig i pilotbutikkerne mod de øvrige "
                "butikker, uge 10 til 35 2026 mod samme uger 2025?")
    ws["A3"] = "Version 26 · opdateret 7. september 2026 · ejer: BI, Elna Johnsen · kilde: dagligt butiks- og vareudtræk, ordreforslag"
    ws.append([])
    hdr = ["Uge", "Gruppe", "Friskomsætning 2026 kr", "Friskomsætning 2025 kr", "Svind kostpris 2026 kr",
           "Svind kostpris 2025 kr", "Svind % af omsætning 2026", "Svind % af omsætning 2025",
           "Tilgængelighed ved lukning 2026 %", "Tilgængelighed ved lukning 2025 %", "Prognosetræfsikkerhed 2026 %"]
    ws.append(hdr)
    for c in ws[5]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE3EA")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append([r["week"], r["group"], round(r["sales26"], 2), round(r["sales25"], 2), round(r["waste26"], 2),
                   round(r["waste25"], 2), round(100 * r["waste26"] / r["sales26"], 2),
                   round(100 * r["waste25"] / r["sales25"], 2), round(100 * r["avail26"], 2),
                   round(100 * r["avail25"], 2), round(100 * r["acc26"], 2)])
    for row in ws.iter_rows(min_row=6, min_col=3, max_col=6):
        for c in row:
            c.number_format = "#,##0"
    for row in ws.iter_rows(min_row=6, min_col=7, max_col=11):
        for c in row:
            c.number_format = "0.00"
    for col, wd in zip("ABCDEFGHIJK", [6, 16, 15, 15, 14, 14, 12, 12, 13, 13, 13]):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "C6"
    # the pilot period in one table
    ws2 = wb.create_sheet("Pilotperioden")
    ws2["A1"] = "Pilotperioden i alt, uge 10 til 35"
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append([])
    ws2.append(["Gruppe", "Friskomsætning 2026 kr", "Friskomsætning 2025 kr", "Svind kostpris 2026 kr",
                "Svind kostpris 2025 kr", "Svind % af omsætning 2026", "Svind % af omsætning 2025"])
    for c in ws2[3]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE3EA")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for grp in ["Pilotbutikker", "Øvrige butikker"]:
        g = [r for r in rows if r["group"] == grp]
        s26, s25 = sum(r["sales26"] for r in g), sum(r["sales25"] for r in g)
        w26, w25 = sum(r["waste26"] for r in g), sum(r["waste25"] for r in g)
        ws2.append([grp, round(s26, 2), round(s25, 2), round(w26, 2), round(w25, 2), round(100 * w26 / s26, 2),
                    round(100 * w25 / s25, 2)])
    for row in ws2.iter_rows(min_row=4, min_col=2, max_col=5):
        for c in row:
            c.number_format = "#,##0"
    for col, wd in zip("ABCDEFG", [16, 15, 15, 14, 14, 12, 12]):
        ws2.column_dimensions[col].width = wd
    wb.save(path)
    PP.normalize_ooxml(path, "Elna Johnsen", "Elna Johnsen", stamp[0], stamp[1], excel=True, company=PK.ORG)
    return rows


def write_docs(target, R):
    agreement(os.path.join(target, PK.F_PILOT), R)
    return dashboard(os.path.join(target, PK.F_DASH), target, PK.STAMPS[PK.F_DASH])
