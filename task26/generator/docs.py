"""Export the two PDF documents in target/ via LibreOffice Writer (officepdf.build):
1. vesterdal_planning_standard_ns2026.pdf - governing network planning standard (pins scope, limiting-phase MVA,
   relief capacity definition, and Phase 1 / Phase 2 / Defer thresholds; never mentions estimation methods).
2. grid_tariff_schedule_2026.pdf - unlabelled domain distractor (2026 retail NOK distribution network tariffs).
"""
import datetime as dt
import os
import sys

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import KeepTogether, Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
import officepdf as O  # noqa: E402
import pack as PK  # noqa: E402

CET = dt.timezone(dt.timedelta(hours=1))
FILES = {
    "standard": "vesterdal_planning_standard_ns2026.pdf",
    "tariff": "grid_tariff_schedule_2026.pdf",
}


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.0, leading=16.4, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=13.6,
                        spaceBefore=8, spaceAfter=3, keepWithNext=1)
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.7, leading=10.8)
    hdr = ParagraphStyle("hdr", fontName="Helvetica-Bold", fontSize=8.7, leading=10.8)
    return body, h1, h2, cell, hdr


def _grid(rows, widths, cell, hdr):
    styled = [[Paragraph(str(c), hdr if r_i == 0 else cell) for c in r] for r_i, r in enumerate(rows)]
    t = Table(styled, colWidths=[w * 2.83 for w in widths], repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def _write_planning_standard(out_dir):
    body, h1, h2, cell, hdr = _styles()
    story = [
        Paragraph("VESTERDAL NETT AS", h2),
        Paragraph("Network Planning Standard NS-2026: 66/22 kV Substation Firm Capacity & Relief Scheduling", h1),
        Paragraph("Document Ref: VN-NS-2026-04 | Effective Date: 18 March 2026 | Capital Planning Cycle: 2027-2029", body),
        Spacer(1, 6),
        Paragraph("1. Purpose and Governance", h2),
        Paragraph(
            "1.1 This standard governs the triennial firm-capacity assessment and capital relief scheduling for "
            "Vesterdal Nett AS regional 66/22 kV primary distribution substations. Relief timing for the 2027-2029 "
            "capital appropriation cycle is determined strictly from observed calendar-year 2026 peak loading "
            "(1 January 2026 00:00 through 31 December 2026 23:59 Europe/Oslo time).", body),
        Paragraph(
            "1.2 Each substation in the relief pool is assessed independently against its Firm N-1 MVA rating "
            "recorded in the Substation Transformer Register. No portfolio budget cap overrides the schedule tiers "
            "established in Section 4.", body),
        Paragraph("2. Scope and 2027-2029 Capital Relief Pool", h2),
        Paragraph(
            "2.1 Vesterdal Nett AS operates nine regional 66/22 kV zone substations. Lindberg and Ostervik completed "
            "full bay modernization and continuous 15-minute three-phase revenue power-quality instrumentation in "
            "2023-2024 and are excluded from the 2027-2029 relief capital pool.", body),
        Paragraph(
            "2.2 The remaining seven regional substations form the in-scope 2027-2029 capital relief pool: "
            "Drangvik, Hestmark, Kvernholm, Malmnes, Raudfjord, Svarthaug, and Tverrli.", body),
        Paragraph("3. Firm Capacity Loading and Relief Capacity Definitions", h2),
        Paragraph(
            "3.1 Thermal capacity of a three-phase 66/22 kV substation transformer under N-1 contingency binds on "
            "its heaviest-loaded phase over a 15-minute Imbalance Settlement Period (ISP). A substation's 2026 peak "
            "15-minute limiting-phase equivalent apparent load (Lim_MVA) is defined as three times the apparent power "
            "of its heaviest-loaded phase at the annual 15-minute peak: Lim_MVA = 3 * w_max * S_15m, where S_15m = "
            "sqrt(P_15m^2 + Q_15m^2) is total three-phase apparent power in MVA and w_max is the share of total "
            "substation load carried by the heaviest phase (A, B, or C) at peak.", body),
        Paragraph(
            "3.2 Total load on each phase (A, B, or C) at peak consists of all single-phase lateral loads connected "
            "to that phase plus one-third of the substation's balanced three-phase load (total active substation load "
            "minus the sum of single-phase lateral loads).", body),
        Paragraph(
            "3.3 Firm N-1 Loading Percentage is defined as 100 * Lim_MVA / Firm_N1_MVA. Relief Capacity Needed (MVA) "
            "is defined as the 2026 peak limiting-phase load excess above the 85.0% Firm N-1 planning ceiling: "
            "Relief_MVA = max(0, Lim_MVA - 0.85 * Firm_N1_MVA). Pool total relief capacity needed is the sum of "
            "Relief_MVA across the seven in-scope substations.", body),
        Paragraph("4. Relief Schedule Tiers (2027-2029 Capital Cycle)", h2),
        KeepTogether([
            Paragraph("4.1 Each in-scope substation is assigned to one of three schedule tiers based on its 2026 "
                      "Firm N-1 Loading Percentage (inclusive at each lower threshold):", body),
            _grid([
                ["Schedule Tier", "2026 Firm N-1 Loading %", "Capital Execution Window", "Action"],
                ["Phase 1 (2027)", ">= 100.0%", "2027", "Urgent transformer bay / feeder relief in Year 1"],
                ["Phase 2 (2028-2029)", ">= 85.0% and < 100.0%", "2028-2029", "Staged capacity relief in Years 2-3"],
                ["Defer", "< 85.0%", "Post-2029", "No capital relief in 2027-2029 cycle"],
            ], [38, 42, 34, 56], cell, hdr),
        ]),
        Spacer(1, 6),
        Paragraph("5. Appropriation Filing Summary", h2),
        Paragraph(
            "5.1 For the February 2027 capital appropriation desk, each in-scope substation record reports 2026 peak "
            "15-minute active demand (MW), peak-hour reactive demand (MVAr), peak limiting-phase share (%), peak "
            "15-minute limiting-phase equivalent apparent load (MVA), Firm N-1 loading percentage, relief capacity "
            "needed (MVA), and assigned relief phase. Pool summary rollups sum active demand, reactive demand, and "
            "relief capacity across the seven in-scope substations and take the unweighted mean of their seven "
            "limiting-phase shares.", body),
        Paragraph(
            "Approved by: " + PK.PEOPLE["head"] + ", Head of Network Planning, " + PK.ORG + ".", body),
    ]
    O.build(
        os.path.join(out_dir, FILES["standard"]),
        story,
        title="Network Planning Standard NS-2026",
        author=PK.PEOPLE["head"],
        subject="66/22 kV Substation Firm Capacity and Relief Scheduling Standard",
        created=dt.datetime(2026, 3, 18, 9, 14, 0, tzinfo=CET),
        modified=dt.datetime(2026, 3, 18, 11, 22, 0, tzinfo=CET),
        header="Vesterdal Nett AS | Network Planning Standard NS-2026",
        footer="VN-NS-2026-04 | Internal Grid Planning Standard",
        producer="LibreOffice 24.2",
    )


def _write_tariff_schedule(out_dir):
    body, h1, h2, cell, hdr = _styles()
    story = [
        Paragraph("VESTERDAL NETT AS", h2),
        Paragraph("Distribution Network Tariff Schedule 2026 (Retail & Commercial Customers)", h1),
        Paragraph("Tariff Notice VN-TAR-2026-01 | Effective: 1 January 2026 | Currency: NOK (excl. VAT)", body),
        Spacer(1, 6),
        Paragraph("1. Capacity-Tier Fixed Charge (Kapasitetsledd)", h2),
        Paragraph(
            "1.1 Low-voltage residential and small commercial customers (< 100,000 kWh annual consumption) are billed "
            "a monthly capacity charge determined by the average of the three highest hourly energy draws on "
            "separate calendar days during the billing month.", body),
        KeepTogether([
            _grid([
                ["Capacity Step", "Monthly Peak Average (kW)", "Monthly Charge (NOK)", "Annual Equivalent (NOK)"],
                ["Step 1", "0 - 2 kW", "145", "1,740"],
                ["Step 2", "2 - 5 kW", "235", "2,820"],
                ["Step 3", "5 - 10 kW", "365", "4,380"],
                ["Step 4", "10 - 15 kW", "510", "6,120"],
                ["Step 5", "15 - 20 kW", "660", "7,920"],
                ["Step 6", "20 - 25 kW", "820", "9,840"],
            ], [32, 52, 42, 44], cell, hdr),
        ]),
        Spacer(1, 6),
        Paragraph("2. Volumetric Energy Charge (Energiledd)", h2),
        Paragraph(
            "2.1 Volumetric network fees apply per delivered kWh with time-of-use differentiation between daytime "
            "working hours (Monday to Friday 06:00-22:00 CET) and off-peak nights and weekends.", body),
        KeepTogether([
            _grid([
                ["Customer Segment", "Day Rate (ore/kWh)", "Night/Weekend (ore/kWh)", "Enova Levy (ore/kWh)"],
                ["Residential LV", "41.2", "29.8", "1.0"],
                ["Commercial LV (<100 MWh)", "39.5", "28.4", "1.0"],
                ["Commercial MV (22 kV)", "22.6", "17.1", "0.8"],
                ["Industrial HV (66 kV)", "11.4", "8.9", "0.8"],
            ], [52, 38, 44, 36], cell, hdr),
        ]),
        Spacer(1, 6),
        Paragraph("3. Reactive Energy Surcharge (Commercial MV/HV Metering)", h2),
        Paragraph(
            "3.1 Commercial and industrial customers connected at 22 kV or 66 kV with monthly average power factor "
            "below 0.90 are assessed a reactive energy fee of 8.5 ore (0.085 NOK) per excess kVARh above the "
            "tan(arccos(0.90)) allowance, invoiced on the monthly settlement statement.", body),
        Paragraph(
            "Issued by: " + PK.PEOPLE["metering"] + ", Metering & Revenue Data Operations, " + PK.ORG + ".", body),
    ]
    O.build(
        os.path.join(out_dir, FILES["tariff"]),
        story,
        title="Distribution Network Tariff Schedule 2026",
        author=PK.PEOPLE["metering"],
        subject="Vesterdal Nett AS 2026 Retail and Commercial Grid Tariffs",
        created=dt.datetime(2025, 11, 24, 13, 40, 0, tzinfo=CET),
        modified=dt.datetime(2025, 12, 4, 10, 18, 0, tzinfo=CET),
        header="Vesterdal Nett AS | Grid Tariff Schedule 2026",
        footer="VN-TAR-2026-01 | Published Customer Tariff Schedule",
        producer="LibreOffice 24.2",
    )


def write_all(out_dir):
    _write_planning_standard(out_dir)
    _write_tariff_schedule(out_dir)
