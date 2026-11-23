#!/usr/bin/env python3
"""Export the two authentic PDF documents in task28/target/ via LibreOffice Writer (officepdf.build):
1. swro_integrity_standard_q27.pdf - Governing regulatory engineering standard (WHAT only: 400-hour threshold,
   three physical excursion mode definitions, Schedule B EUR tariffs, Annex B 2027 operating-plan projection
   rules, Clause 4.1-4.4 calendar/clock/discrepancy definitions, Annex C deliverable schemas).
2. lims_qa_certificate_2026.pdf - Accredited 2026 LIMS ICP-OES boron analytical QA certificate (0.004 mg/L
   repeatability SD, North/South bench units and date formats, QA revision precedence, carousel cadences).

Zero hints on composite variance deconvolution, Lagrangian flow coordinates, baffling efficiency, effective
holdup volume, Dawid-Skene/latent-class EM, conditional alarm dependence, or CIP clearing shares.
"""
import datetime as dt
import os
import sys

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(
    os.path.dirname(os.path.dirname(HERE)),
    ".agents",
    "skills",
    "reduce-house-fixes",
    "scripts",
    "writers",
)
sys.path.insert(0, HERE)
sys.path.insert(0, WRITERS)
import officepdf as O  # noqa: E402
import pack as PK  # noqa: E402

WET = dt.timezone.utc
WEST = dt.timezone(dt.timedelta(hours=1))


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle(
        "body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13.0, spaceAfter=5
    )
    h1 = ParagraphStyle(
        "h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.8, leading=16.0, spaceAfter=4
    )
    h2 = ParagraphStyle(
        "h2",
        parent=ss["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.2,
        leading=13.4,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=1,
    )
    meta = ParagraphStyle(
        "meta",
        parent=ss["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.6,
        leading=11.4,
        textColor=colors.HexColor("#444444"),
        spaceAfter=6,
    )
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.6)
    hdr = ParagraphStyle("hdr", fontName="Helvetica-Bold", fontSize=8.4, leading=10.6)
    return body, h1, h2, meta, cell, hdr


def _grid(rows, widths_mm, cell, hdr):
    styled = [[Paragraph(str(c), hdr if r_i == 0 else cell) for c in r] for r_i, r in enumerate(rows)]
    t = Table(styled, colWidths=[w * 2.8346 for w in widths_mm], repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return t


def _write_integrity_standard(out_dir):
    body, h1, h2, meta, cell, hdr = _styles()
    story = [
        Paragraph("BARLAVENTO DESSALINIZACAO MUNICIPAL, E.M.", h2),
        Paragraph(
            "Standard SWRO-Q27: Seawater Reverse-Osmosis Membrane Integrity Inspection and 2027 Overhaul Designation",
            h1,
        ),
        Paragraph(
            "Document Ref: BDM-REG-Q27-2026 | Effective: 14 September 2026 | Inspection Cycle: 2027 Operating Campaign",
            meta,
        ),
        Spacer(1, 4),
        Paragraph("1. Scope and Regulated Facility", h2),
        Paragraph(
            "1.1 This engineering standard governs the annual membrane-train integrity review and mandatory pressure-vessel "
            "overhaul designation for Estacao Dessalinizadora de Alvor, operated by Barlavento Dessalinizacao Municipal, "
            "E.M. in the western Algarve. Compliance filings are submitted to the Algarve Regional Water Inspectorate "
            "ahead of the spring-summer potable production campaign.",
            body,
        ),
        Paragraph(
            "1.2 Scope comprises all eight active parallel seawater reverse-osmosis trains designated TR01 through TR08 "
            "(commissioned across North and South treatment bays and recorded in legacy maintenance software under tags "
            "LINE-A through LINE-H). The historical observation period covers full calendar year 2026 (1 January 2026 "
            "00:00 UTC through 31 December 2026 23:59 UTC, 365 days, 8,760 operating hours). The forward designation "
            "horizon covers full calendar year 2027.",
            body,
        ),
        Paragraph("2. Physical Excursion Mode Definitions", h2),
        Paragraph(
            "2.1 Permeate Boron Excursion (Clause 2.1): A permeate boron excursion occurs during any single 1-hour "
            "operating block in which a train's hourly permeate boron concentration strictly exceeds 0.50 mg/L. "
            "Routine plant compliance sampling employs automated flow-proportional composite carousels rather than "
            "hourly grab bottles; regulatory accounting evaluates the underlying 1-hour operating block exceedance rate "
            "for each train and quarter.",
            body,
        ),
        Paragraph(
            "2.2 Pretreatment-to-RO Scaling Excursion (Clause 2.2): A scaling excursion occurs on any 15-minute seawater "
            "parcel (0.25 operating hours) that enters a train's dissolved-air-flotation and dual-media filtration "
            "(DAF/DMF) pretreatment stage with standardized intake algal-TEP precursor index strictly exceeding 1.50 "
            "(relative to the 2020-2025 coastal baseline) AND arrives at that train's reverse-osmosis feed header with "
            "supersaturation-oxidant stress index strictly exceeding 1.50. Because parcels arriving at the RO feed "
            "header during the opening hours of 1 January 2026 entered the intake prior to midnight on 31 December 2025, "
            "the initial 8 hours (32 fifteen-minute intervals from 2026-01-01T00:00Z through 2026-01-01T07:45Z) are "
            "outside the 2026 scaling excursion count.",
            body,
        ),
        Paragraph(
            "2.3 Persistent Structural Membrane Integrity Fault (Clause 2.3): A structural integrity fault occurs during "
            "any 4-hour operating block in which a train operates with a persistent mechanical membrane or vessel breach "
            "(such as O-ring bypass, interconnector seal failure, or element delamination). Reversible biological fouling "
            "removed during routine Clean-in-Place (CIP) chemical washes is an operational maintenance condition outside "
            "Clause 2.3 and does not count toward mandatory vessel overhaul hours. During the operating year, trains are "
            "screened non-destructively via three continuous inline 4-hour shift alarm channels (salt-passage indicator, "
            "stage differential-pressure indicator, and acoustic-bypass indicator) without intrusive vessel probing.",
            body,
        ),
        Paragraph("3. Mandatory 2027 Vessel Overhaul Threshold", h2),
        KeepTogether(
            [
                Paragraph(
                    "3.1 Each train's projected 2027 total anomalous operating hours equals the sum of its projected 2027 "
                    "permeate boron excursion hours, pretreatment-to-RO scaling excursion hours, and persistent structural "
                    "fault hours across all four quarters of 2027. Every train is classified independently against the "
                    "400.0-hour statutory threshold with no plant-wide quota:",
                    body,
                ),
                _grid(
                    [
                        ["Designation", "Projected 2027 Anomalous Hours", "Required 2027 Integrity Action"],
                        [
                            "OVERHAUL",
                            ">= 400.0 hours",
                            "Mandatory 2027 pressure-vessel opening, seal inspection, and element replacement",
                        ],
                        [
                            "MONITOR",
                            "< 400.0 hours",
                            "Routine scheduled CIP maintenance and continuous inline monitoring",
                        ],
                    ],
                    [34, 48, 92],
                    cell,
                    hdr,
                ),
            ]
        ),
        PageBreak(),
        Paragraph("4. Calendar Quarters, Clock Conventions, Schedule B Tariffs, and Screening Audit", h2),
        Paragraph(
            "4.1 Operational Calendar Quarters: Quarterly aggregations follow exact UTC operational quarter boundaries "
            "for non-leap year 2026: Q1 (1 January through 31 March, 90 days, 2,160 hours), Q2 (1 April through 30 June, "
            "91 days, 2,184 hours), Q3 (1 July through 30 September, 92 days, 2,208 hours), and Q4 (1 October through "
            "31 December, 92 days, 2,208 hours).",
            body,
        ),
        Paragraph(
            "4.2 Clocks, Units, and QA Precedence: Historian telemetry carries UTC timestamps. Shift diagnostics and "
            "CIP chemical-wash logs carry explicit Europe/Lisbon timestamps (+00:00 WET winter / +01:00 WEST summer) "
            "anchored to the 4-hour UTC operating block grid. Standard reporting units are mg/L for permeate boron "
            "(1 mg/L = 1,000 ug/L), m3/h for feed flow (1 L/s = 3.6 m3/h), mS/cm for seawater conductivity, m3 for "
            "basin volumes, and EUR for contractual exposure. Where laboratory data carry multiple QA revisions for "
            "a single sample identifier, the latest QA revision supersedes preliminary releases. Exact re-transmitted "
            "telemetry frames sharing timestamp and train identifier represent a single interval reading.",
            body,
        ),
        KeepTogether(
            [
                Paragraph(
                    "4.3 Schedule B Contractual Off-Spec Exposure: Under the Algarve bulk-water concession agreement, "
                    "projected 2027 off-spec compliance and integrity risk exposure is priced per projected anomalous "
                    "operating hour according to Schedule B:",
                    body,
                ),
                _grid(
                    [
                        ["Excursion Mode", "Governing Clause", "Schedule B Tariff (EUR / anomalous hour)"],
                        ["Permeate Boron (> 0.50 mg/L, 1-hour basis)", "Clause 2.1", "420 EUR/h"],
                        ["Pretreatment-to-RO Scaling (parcel > 1.50 & > 1.50 index)", "Clause 2.2", "360 EUR/h"],
                        ["Persistent Structural Membrane Fault", "Clause 2.3", "540 EUR/h"],
                    ],
                    [78, 36, 60],
                    cell,
                    hdr,
                ),
            ]
        ),
        Paragraph(
            "Total 2027 Schedule B exposure sums across all eight trains and all three modes. Overhaul-train subtotals "
            "for projected 2027 anomalous hours and Schedule B EUR sum strictly over trains designated OVERHAUL under "
            "Clause 3.1. Summer Q3 anomalous hours sum projected 2027 Q3 hours across all eight trains and three modes.",
            body,
        ),
        Paragraph(
            "4.4 Incumbent 2026 Screening Discrepancy Rate: Barlavento's legacy 2026 operational screening dashboard "
            "tallies incumbent annual anomaly hours H_inc_2026(u, m) per train u and mode m from cleaned 2026 records "
            "as: (a) for permeate boron, the fraction of clean lab composite bottles exceeding 0.50 mg/L within each "
            "quarter multiplied by quarterly operating hours; (b) for scaling, the count of 15-minute intervals "
            "(excluding the initial 32 burn-in intervals) with same-timestamp intake precursor index > 1.50 and "
            "RO-feed stress > 1.50 multiplied by 0.25 hours; and (c) for structural faults, the count of 4-hour blocks "
            "with two or more of the three inline shift alarms active multiplied by 4.0 hours. The plant-wide 2026 "
            "screening discrepancy rate (in percent) is defined as 100 * sum_{u,m} |H_est_2026(u,m) - H_inc_2026(u,m)| "
            "/ sum_{u,m} H_est_2026(u,m), summed over all 8 trains and all 3 modes, where H_est_2026(u,m) denotes each "
            "train's estimated true 2026 anomalous hours under Clauses 2.1 through 2.3.",
            body,
        ),
        Paragraph("Annex B. Uniform 2027 Operating Plan Projection Rules", h2),
        Paragraph(
            "B.1 Projected 2027 anomalous hours carry each train's estimated 2026 quarterly mode hours forward using "
            "the filed 2027 Operating Plan multipliers uniformly across all eight trains, where R_duty(u, q) is train "
            "u's filed 2027-to-2026 quarterly potable dispatch duty ratio, F_thermal(q) is the quarterly seawater "
            "thermal boron-passage factor, and F_recovery(q) is the quarterly scaling recovery factor:",
            body,
        ),
        Paragraph(
            "H_boron_2027(u, q) = H_boron_2026(u, q) * F_thermal(q) * R_duty(u, q)",
            body,
        ),
        Paragraph(
            "H_scaling_2027(u, q) = H_scaling_2026(u, q) * F_recovery(q) * R_duty(u, q)",
            body,
        ),
        Paragraph(
            "H_struct_2027(u, q) = H_struct_2026(u, q) * R_duty(u, q)",
            body,
        ),
        KeepTogether(
            [
                Paragraph(
                    "B.2 Filed 2027 seasonal seawater-temperature (boron passage) and recovery-rate (scaling stress) "
                    "process factors are identical across all eight trains:",
                    body,
                ),
                _grid(
                    [
                        ["2027 Quarter", "Boron Temperature Factor", "Scaling Recovery Factor"],
                        ["2027-Q1", "1.05", "1.03"],
                        ["2027-Q2", "1.14", "1.12"],
                        ["2027-Q3", "1.32", "1.28"],
                        ["2027-Q4", "1.09", "1.07"],
                    ],
                    [50, 62, 62],
                    cell,
                    hdr,
                ),
            ]
        ),
        Paragraph("Annex C. Annual Integrity Inspection Filing Schema", h2),
        Paragraph(
            "C.1 Inspection filings for the Algarve Regional Water Inspectorate consist of two matched deliverables: "
            "(1) an inspection workbook opening on an executive overhaul triage sheet showing every train's 2027 "
            "permeate boron, scaling, structural, total, and Q3 anomalous hours, Schedule B EUR exposure, overhaul "
            "designation, plant-wide and overhaul subtotals, 2026 screening discrepancy summary, and a train comparison "
            "chart against the 400-hour threshold, supported by 2026-to-2027 diagnostic backup sheets; and (2) a "
            "train-level CSV compliance register sorted by projected 2027 total anomalous hours descending.",
            body,
        ),
        KeepTogether(
            [
                Paragraph("C.2 Required column layout for the train-level CSV compliance register:", body),
                _grid(
                    [
                        ["Column Name", "Unit / Format", "Definition"],
                        ["train_id", "TR01..TR08", "Canonical Barlavento SWRO train identifier"],
                        ["boron_2027_h", "hours", "Projected 2027 permeate boron excursion hours (Clause 2.1 + Annex B)"],
                        ["scaling_2027_h", "hours", "Projected 2027 pretreatment-to-RO scaling hours (Clause 2.2 + Annex B)"],
                        ["struct_2027_h", "hours", "Projected 2027 persistent structural fault hours (Clause 2.3 + Annex B)"],
                        ["total_2027_h", "hours", "Sum of boron_2027_h + scaling_2027_h + struct_2027_h"],
                        ["q3_2027_h", "hours", "Projected 2027 summer Q3 total anomalous hours (all 3 modes)"],
                        ["cost_2027_eur", "EUR", "Projected 2027 Schedule B contractual off-spec exposure"],
                        ["designation", "OVERHAUL / MONITOR", "Clause 3.1 overhaul classification (>= 400.0 h = OVERHAUL)"],
                    ],
                    [38, 36, 100],
                    cell,
                    hdr,
                ),
            ]
        ),
        Spacer(1, 6),
        Paragraph(
            "Issued by: "
            + PK.PEOPLE["compliance"]
            + ", Quality and Regulatory Compliance Officer, "
            + PK.ORG
            + " Concurrence: "
            + PK.PEOPLE["inspector"]
            + ", Algarve Regional Water Inspectorate.",
            meta,
        ),
    ]
    created = dt.datetime(2026, 9, 14, 10, 18, 42, tzinfo=WEST)
    modified = dt.datetime(2026, 9, 14, 15, 34, 11, tzinfo=WEST)
    O.build(
        os.path.join(out_dir, PK.FILES["standard_pdf"]),
        story,
        title="Standard SWRO-Q27: Membrane Integrity Inspection and 2027 Overhaul Designation",
        author=PK.PEOPLE["compliance"],
        subject="SWRO Membrane Train Integrity Compliance and 2027 Overhaul Standard",
        footer="Barlavento Dessalinizacao Municipal, E.M. | Standard SWRO-Q27",
        created=created,
        modified=modified,
        producer="LibreOffice 24.2",
        header="Standard SWRO-Q27 (BDM-REG-Q27-2026)",
        page_of=True,
    )


def _write_lims_qa_certificate(out_dir):
    body, h1, h2, meta, cell, hdr = _styles()
    story = [
        Paragraph("LABORATORIO DE QUIMICA ANALITICA - ESTACAO DESSALINIZADORA DE ALVOR", h2),
        Paragraph("2026 Annual ICP-OES Permeate Boron Quality Assurance Certificate", h1),
        Paragraph(
            "Certificate Ref: LAB-QA-2026-B08 | Issued: 8 January 2027 | Accreditation: IPAC ISO/IEC 17025 (L0482)",
            meta,
        ),
        Spacer(1, 4),
        Paragraph("1. Analytical Method and Calibration Verification", h2),
        Paragraph(
            "1.1 Routine permeate boron determinations for Barlavento SWRO trains TR01 through TR08 during calendar "
            "year 2026 were executed by inductively coupled plasma optical emission spectrometry (EN ISO 11885, "
            "wavelength 249.772 nm) across dual laboratory benches ICP-OES-B1 (North Bay) and ICP-OES-B2 (South Bay). "
            "Certified reference check standards (0.25 mg/L, 0.50 mg/L, and 0.75 mg/L NIST-traceable boron) remained "
            "within +/-1.5% recovery across all 52 weekly analytical batches.",
            body,
        ),
        KeepTogether(
            [
                Paragraph("1.2 Validated 2026 ICP-OES Method Performance Summary:", body),
                _grid(
                    [
                        ["Performance Parameter", "Validated Value", "Basis"],
                        ["Analytical Repeatability SD", "0.004 mg/L", "Pooled duplicate injections across 2026 batches"],
                        ["Relative Standard Deviation at 0.50 mg/L", "0.80%", "Compliance ceiling check standard"],
                        ["Limit of Quantification (LOQ)", "0.020 mg/L", "10x procedural blank standard deviation"],
                        ["Linear Calibration Range", "0.020 to 2.50 mg/L", "Six-point matrix-matched calibration"],
                    ],
                    [68, 42, 64],
                    cell,
                    hdr,
                ),
            ]
        ),
        Paragraph("2. Bench Export Conventions and QA Revision Control", h2),
        Paragraph(
            "2.1 During 2026, Bench ICP-OES-B1 (serving North Bay trains TR01 through TR04) exported LIMS result tables "
            "in mg/L with ISO-8601 calendar dates (YYYY-MM-DD). Bench ICP-OES-B2 (serving South Bay trains TR05 through "
            "TR08) operated under the legacy regional laboratory template exporting concentrations in ug/L (1,000 ug/L "
            "= 1.000 mg/L) with Portuguese calendar dates (DD/MM/YYYY). Legacy train codes LINE-A through LINE-H "
            "remained active on selected Q1 sample import queues prior to full April LIMS tag cutover.",
            body,
        ),
        Paragraph(
            "2.2 Preliminary automated LIMS imports carry revision number 1. Whenever an internal quality-control check "
            "standard triggers drift re-quantification or blank correction, the re-processed assay is released under "
            "revision number 2 with the same sample identifier, superseding revision 1 in the laboratory archive.",
            body,
        ),
        Paragraph("3. Automated Composite Sampling Cadence", h2),
        Paragraph(
            "3.1 Permeate boron samples are drawn continuously from each train's permeate collector header by refrigerated "
            "flow-proportional autosampler carousels. Under Barlavento's 2026 laboratory schedule, carousels run the "
            "standard 6-bottle daily program (4-hour composite bottles, PROG_4H_STD) from Thursday through Monday and "
            "switch to the extended 3-bottle daily program (8-hour composite bottles, PROG_8H_EXT) on Tuesdays and "
            "Wednesdays to accommodate scheduled municipal potable-water trace-metals runs and ICP-OES torch maintenance. "
            "No routine single-hour permeate boron grab sampling program was operated during 2026.",
            body,
        ),
        Spacer(1, 8),
        Paragraph(
            "Certified by: " + PK.PEOPLE["lims"] + ", LIMS Analytical Chemistry Lead, " + PK.ORG,
            meta,
        ),
    ]
    created = dt.datetime(2027, 1, 8, 9, 41, 16, tzinfo=WET)
    modified = dt.datetime(2027, 1, 8, 14, 12, 53, tzinfo=WET)
    O.build(
        os.path.join(out_dir, PK.FILES["lims_qa_pdf"]),
        story,
        title="2026 Annual ICP-OES Permeate Boron Quality Assurance Certificate",
        author=PK.PEOPLE["lims"],
        subject="ISO/IEC 17025 Permeate Boron Analytical Repeatability and LIMS Export Verification",
        footer="Estacao Dessalinizadora de Alvor | LIMS QA Certificate LAB-QA-2026-B08",
        created=created,
        modified=modified,
        producer="LibreOffice 24.2",
        header="LIMS QA Certificate LAB-QA-2026-B08",
        page_of=True,
    )


def write_all(out_dir):
    _write_integrity_standard(out_dir)
    _write_lims_qa_certificate(out_dir)


if __name__ == "__main__":
    out_d = os.path.join(os.path.dirname(HERE), "target")
    os.makedirs(out_d, exist_ok=True)
    write_all(out_d)
    print("PDFs written:", PK.FILES["standard_pdf"], PK.FILES["lims_qa_pdf"])
