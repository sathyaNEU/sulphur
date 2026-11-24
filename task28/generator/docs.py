#!/usr/bin/env python3
"""Export the two authentic PDF documents in task28/target/ via LibreOffice Writer (officepdf.build):
1. swro_integrity_standard_q27.pdf - Governing Engineering Protocol SWRO-Q27 (WHAT only: 400.0-hour
   overhaul criterion, four physical excursion/fault mode definitions Clauses 2.1 to 2.4, excess
   desalination energy rates 420/360/540/300 kWh/h in MWh, Annex A 2027 projection rules, Annex B
   exact 9-column CSV and workbook schemas).
2. lims_qa_certificate_2026.pdf - Accredited 2026 LIMS & inline process-instrument QA certificate
   (0.004 mg/L ICP-OES boron repeatability SD, 3.5 mg/L inline bay permeate collector TDS probe
   repeatability SD, North/South bench units and date formats, QA revision precedence, carousel cadences).

Zero hints on solute mass-flux heteroscedasticity, composite variance deconvolution, Lagrangian flow
coordinates, two-path short-circuiting, continuous post-CIP re-growth kinetics, latent-class EM,
shared-bay variance-component deconvolution, or raw-alarm bias (no Clause 4.4).
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
        "body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.2, leading=12.6, spaceAfter=4.5
    )
    h1 = ParagraphStyle(
        "h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.5, leading=15.5, spaceAfter=4
    )
    h2 = ParagraphStyle(
        "h2",
        parent=ss["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.0,
        leading=13.0,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=1,
    )
    meta = ParagraphStyle(
        "meta",
        parent=ss["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=11.2,
        textColor=colors.HexColor("#444444"),
        spaceAfter=5,
    )
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.2, leading=10.4)
    hdr = ParagraphStyle("hdr", fontName="Helvetica-Bold", fontSize=8.2, leading=10.4)
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
            "Engineering Protocol SWRO-Q27: Seawater Reverse-Osmosis Membrane Reliability Diagnostics and 2027 Overhaul Criteria",
            h1,
        ),
        Paragraph(
            "Document Ref: BDM-ENG-Q27-2026 | Effective: 14 September 2026 | Operating Horizon: 2027 Production Campaign",
            meta,
        ),
        Spacer(1, 3),
        Paragraph("1. Scope and Desalination Process Systems", h2),
        Paragraph(
            "1.1 This process-engineering protocol defines the annual membrane-train reliability evaluation, physical "
            "excursion definitions, excess desalination energy accounting, and 2027 pressure-vessel overhaul criteria "
            "for Estacao Dessalinizadora de Alvor, operated by Barlavento Dessalinizacao Municipal, E.M. in the "
            "western Algarve. Diagnostic estimates are finalized ahead of the spring maintenance outage window.",
            body,
        ),
        Paragraph(
            "1.2 Scope comprises all eight active parallel seawater reverse-osmosis trains designated TR01 through TR08 "
            "across North Bay (TR01 through TR04) and South Bay (TR05 through TR08), recorded in legacy maintenance "
            "software under tags LINE-A through LINE-H. The historical observation period covers full calendar year 2026 "
            "(1 January 2026 00:00 UTC through 31 December 2026 23:59 UTC, 365 days, 8,760 operating hours). The "
            "forecast horizon covers full calendar year 2027.",
            body,
        ),
        Paragraph("2. Physical Excursion and Membrane Integrity Fault Definitions", h2),
        Paragraph(
            "2.1 Permeate Boron Excursion (Clause 2.1): A permeate boron excursion occurs during any single 1-hour "
            "operating block in which a train's hourly permeate boron concentration strictly exceeds 0.50 mg/L. "
            "Routine plant laboratory monitoring employs automated flow-proportional composite carousels rather than "
            "hourly grab bottles; process reliability analysis evaluates each train's underlying 1-hour operating block "
            "exceedance rate by quarter.",
            body,
        ),
        Paragraph(
            "2.2 Pretreatment-to-RO Scaling Excursion (Clause 2.2): A scaling excursion occurs during any 15-minute "
            "operating interval (0.25 hours) in which the pretreated seawater arriving at a train's reverse-osmosis "
            "feed header carries a standardized algal-TEP precursor index strictly exceeding 1.50 (relative to the "
            "2020-2025 coastal baseline, following transit through that train's dissolved-air-flotation and dual-media "
            "filtration stage) AND an RO-feed supersaturation-oxidant stress index strictly exceeding 1.50. Because "
            "seawater arriving at the RO feed header during the opening hours of 1 January 2026 entered the intake "
            "prior to midnight on 31 December 2025, the initial 8 hours (32 fifteen-minute intervals from "
            "2026-01-01T00:00Z through 2026-01-01T07:45Z) are outside the 2026 scaling excursion count.",
            body,
        ),
        Paragraph(
            "2.3 Persistent Structural Membrane Integrity Fault (Clause 2.3): A structural integrity fault occurs during "
            "any 1-hour operating block in which a train operates with a persistent mechanical membrane or vessel breach "
            "(such as O-ring bypass, interconnector seal failure, or element delamination). Reversible membrane fouling "
            "and surface deposits cleared during routine Clean-in-Place (CIP) chemical washes are normal operational "
            "cycles outside Clause 2.3 and do not count toward vessel overhaul hours. During the operating year, trains "
            "are monitored non-destructively via three continuous inline 1-hour shift alarm channels (salt-passage "
            "indicator, stage differential-pressure indicator, and acoustic-bypass indicator) without intrusive vessel "
            "probing.",
            body,
        ),
        Paragraph(
            "2.4 Permeate Salinity / TDS Breakthrough (Clause 2.4): A permeate salinity breakthrough occurs during any "
            "single 1-hour operating block in which an individual train's hourly permeate total dissolved solids (TDS) "
            "concentration strictly exceeds 450 mg/L. Inline permeate TDS probes at Alvor are installed exclusively on "
            "the two shared bay common permeate collectors (North Bay collecting TR01 through TR04; South Bay collecting "
            "TR05 through TR08) rather than on individual train outlets. All four trains in each bay operate at the same "
            "45% nominal permeate recovery, so each train's hourly volume share entering its bay collector equals its "
            "hourly feed-flow share within that bay.",
            body,
        ),
        Paragraph("3. 2027 Vessel Overhaul Engineering Criterion", h2),
        KeepTogether(
            [
                Paragraph(
                    "3.1 Each train's projected 2027 total anomalous operating hours equals the sum of its forecasted 2027 "
                    "permeate boron excursion hours, pretreatment-to-RO scaling excursion hours, persistent structural "
                    "fault hours, and individual train permeate TDS breakthrough hours across all four quarters of 2027. "
                    "Every train is evaluated independently against the 400.0-hour engineering overhaul limit with no "
                    "plant-wide quota:",
                    body,
                ),
                _grid(
                    [
                        ["Designation", "Projected 2027 Anomalous Hours", "2027 Maintenance Action"],
                        [
                            "OVERHAUL",
                            ">= 400.0 hours",
                            "Schedule 2027 pressure-vessel opening, seal inspection, and membrane element replacement",
                        ],
                        [
                            "MONITOR",
                            "< 400.0 hours",
                            "Retain on routine CIP maintenance and continuous inline process monitoring",
                        ],
                    ],
                    [34, 48, 92],
                    cell,
                    hdr,
                ),
            ]
        ),
        PageBreak(),
        Paragraph("4. Calendar Quarters, Clocks, and Excess Desalination Energy Penalties", h2),
        Paragraph(
            "4.1 Operational Calendar Quarters: Quarterly aggregations follow exact UTC operational quarter boundaries "
            "for non-leap year 2026: Q1 (1 January through 31 March, 90 days, 2,160 hours), Q2 (1 April through 30 June, "
            "91 days, 2,184 hours), Q3 (1 July through 30 September, 92 days, 2,208 hours), and Q4 (1 October through "
            "31 December, 92 days, 2,208 hours).",
            body,
        ),
        Paragraph(
            "4.2 Clocks, Engineering Units, and QA Precedence: Historian and bay-collector telemetry carry UTC "
            "timestamps. Shift diagnostics and CIP chemical-wash logs carry explicit Europe/Lisbon timestamps "
            "(+00:00 WET winter / +01:00 WEST summer) anchored to the 1-hour UTC operating block grid (including "
            "late-December 2025 prior-campaign carryover washes in the maintenance export). Standard engineering units "
            "are mg/L for permeate boron (1 mg/L = 1,000 ug/L) and permeate TDS, m3/h for feed and permeate flow "
            "(1 L/s = 3.6 m3/h), mS/cm for seawater conductivity, m3 for basin volumes, and MWh for aggregate excess "
            "desalination energy (1 MWh = 1,000 kWh). Where laboratory data carry multiple QA revisions for a single "
            "sample identifier, the latest QA revision supersedes preliminary releases. Exact re-transmitted telemetry "
            "frames sharing timestamp and train or bay identifier represent a single interval reading.",
            body,
        ),
        KeepTogether(
            [
                Paragraph(
                    "4.3 Mode-Specific Excess Desalination Energy Penalty: Operating under physical excursion or membrane "
                    "fault conditions imposes incremental electrical energy demand for second-pass permeate polishing, "
                    "elevated feed transmembrane-pressure pumping drag, high-salinity permeate bypass recirculation, or "
                    "brackish post-treatment remineralization blending. Validated 2027 plant energy penalties per "
                    "forecasted anomalous operating hour are:",
                    body,
                ),
                _grid(
                    [
                        ["Physical Failure Mode", "Protocol Clause", "Excess Energy Rate (kWh / anomalous hour)"],
                        ["Permeate Boron (> 0.50 mg/L, 1-hour basis; 2nd-pass polishing)", "Clause 2.1", "420 kWh/h"],
                        ["Pretreatment-to-RO Scaling (RO header > 1.50 & > 1.50; TMP drag)", "Clause 2.2", "360 kWh/h"],
                        ["Persistent Structural Membrane Fault (bypass recirculation)", "Clause 2.3", "540 kWh/h"],
                        ["Permeate Salinity / TDS Breakthrough (> 450 mg/L, 1-hour basis)", "Clause 2.4", "300 kWh/h"],
                    ],
                    [86, 30, 58],
                    cell,
                    hdr,
                ),
            ]
        ),
        Paragraph(
            "Total 2027 excess desalination energy penalty (reported in MWh, dividing kWh by 1,000) sums across all "
            "eight trains and all four failure modes. Overhaul-train subtotals for projected 2027 anomalous hours "
            "and excess desalination energy (MWh) sum strictly over trains designated OVERHAUL under Clause 3.1. "
            "Summer Q3 anomalous hours sum projected 2027 Q3 hours across all eight trains and four modes.",
            body,
        ),
        Paragraph("Annex A. Uniform 2027 Operating Regime Physical Projection Rules", h2),
        Paragraph(
            "A.1 Forecasted 2027 anomalous hours carry each train's estimated 2026 quarterly physical mode hours "
            "forward into the 2027 operating regime uniformly across all eight trains, where R_duty(u, q) is train "
            "u's planned 2027-to-2026 quarterly potable dispatch duty ratio, F_thermal(q) is the quarterly seawater "
            "thermal boron-passage factor, F_recovery(q) is the quarterly scaling recovery factor, and F_salinity(q) "
            "is the quarterly thermal salinity-passage factor:",
            body,
        ),
        Paragraph("H_boron_2027(u, q) = H_boron_2026(u, q) * F_thermal(q) * R_duty(u, q)", body),
        Paragraph("H_scaling_2027(u, q) = H_scaling_2026(u, q) * F_recovery(q) * R_duty(u, q)", body),
        Paragraph("H_struct_2027(u, q) = H_struct_2026(u, q) * R_duty(u, q)", body),
        Paragraph("H_tds_2027(u, q) = H_tds_2026(u, q) * F_salinity(q) * R_duty(u, q)", body),
        KeepTogether(
            [
                Paragraph(
                    "A.2 Planned 2027 seasonal seawater-temperature, recovery-rate, and salinity-passage process "
                    "factors are identical across all eight trains:",
                    body,
                ),
                _grid(
                    [
                        [
                            "2027 Quarter",
                            "Boron Temp Factor",
                            "Scaling Rec Factor",
                            "Salinity Temp Factor",
                        ],
                        ["2027-Q1", "1.05", "1.03", "1.04"],
                        ["2027-Q2", "1.14", "1.12", "1.12"],
                        ["2027-Q3", "1.32", "1.28", "1.26"],
                        ["2027-Q4", "1.09", "1.07", "1.08"],
                    ],
                    [42, 44, 44, 44],
                    cell,
                    hdr,
                ),
            ]
        ),
        Paragraph("Annex B. 2027 Membrane Reliability Diagnostics Output Schema", h2),
        Paragraph(
            "B.1 Annual reliability diagnostics deliverables for Barlavento process engineering consist of two matched "
            "files: (1) an engineering diagnostics workbook opening on an executive overhaul summary sheet showing "
            "every train's forecasted 2027 permeate boron, scaling, structural, permeate TDS, total, and Q3 anomalous "
            "hours, excess desalination energy penalty in MWh, overhaul designation, plant-wide and overhaul subtotals, "
            "estimation uncertainty ranges across modeling assumptions, and a train comparison chart against the "
            "400.0-hour criterion, supported by 2026-to-2027 physical model backup sheets; and (2) a train-level "
            "diagnostics CSV for the plant maintenance historian sorted by projected 2027 total anomalous hours "
            "descending.",
            body,
        ),
        KeepTogether(
            [
                Paragraph("B.2 Required column layout for the train-level plant historian diagnostics CSV:", body),
                _grid(
                    [
                        ["Column Name", "Unit / Format", "Definition"],
                        ["train_id", "TR01..TR08", "Canonical Barlavento SWRO train identifier"],
                        ["boron_2027_h", "hours", "Forecasted 2027 permeate boron excursion hours (Clause 2.1 + Annex A)"],
                        ["scaling_2027_h", "hours", "Forecasted 2027 pretreatment-to-RO scaling hours (Clause 2.2 + Annex A)"],
                        ["struct_2027_h", "hours", "Forecasted 2027 persistent structural fault hours (Clause 2.3 + Annex A)"],
                        ["tds_2027_h", "hours", "Forecasted 2027 individual train permeate TDS breakthrough hours (Clause 2.4 + Annex A)"],
                        ["total_2027_h", "hours", "Sum of boron_2027_h + scaling_2027_h + struct_2027_h + tds_2027_h"],
                        ["q3_2027_h", "hours", "Forecasted 2027 summer Q3 total anomalous hours (all 4 modes)"],
                        ["energy_2027_mwh", "MWh", "Forecasted 2027 excess desalination process energy penalty (Clause 4.3)"],
                        ["designation", "OVERHAUL / MONITOR", "Clause 3.1 engineering classification (>= 400.0 h = OVERHAUL)"],
                    ],
                    [36, 36, 102],
                    cell,
                    hdr,
                ),
            ]
        ),
        Spacer(1, 5),
        Paragraph(
            "Issued by: "
            + PK.PEOPLE["compliance"]
            + ", Membrane Reliability Engineering Lead, "
            + PK.ORG
            + " Reviewed by: "
            + PK.PEOPLE["inspector"]
            + ", Chief Desalination Process Engineer.",
            meta,
        ),
    ]
    created = dt.datetime(2026, 9, 14, 10, 18, 42, tzinfo=WEST)
    modified = dt.datetime(2026, 9, 14, 15, 34, 11, tzinfo=WEST)
    O.build(
        os.path.join(out_dir, PK.FILES["standard_pdf"]),
        story,
        title="Engineering Protocol SWRO-Q27: Membrane Reliability Diagnostics and 2027 Overhaul Criteria",
        author=PK.PEOPLE["compliance"],
        subject="SWRO Membrane Train Physical Reliability Diagnostics, Energy Burden, and 2027 Overhaul Protocol",
        footer="Barlavento Dessalinizacao Municipal, E.M. | Engineering Protocol SWRO-Q27",
        created=created,
        modified=modified,
        producer="LibreOffice 24.2",
        header="Engineering Protocol SWRO-Q27 (BDM-ENG-Q27-2026)",
        page_of=True,
    )


def _write_lims_qa_certificate(out_dir):
    body, h1, h2, meta, cell, hdr = _styles()
    story = [
        Paragraph("LABORATORIO DE QUIMICA ANALITICA - ESTACAO DESSALINIZADORA DE ALVOR", h2),
        Paragraph("2026 Annual ICP-OES Boron and Inline Permeate TDS Quality Assurance Certificate", h1),
        Paragraph(
            "Certificate Ref: LAB-QA-2026-B08 | Issued: 8 January 2027 | Accreditation: IPAC ISO/IEC 17025 (L0482)",
            meta,
        ),
        Spacer(1, 4),
        Paragraph("1. Analytical Methods and Calibration Verification", h2),
        Paragraph(
            "1.1 Routine permeate boron determinations for Barlavento SWRO trains TR01 through TR08 during calendar "
            "year 2026 were executed by inductively coupled plasma optical emission spectrometry (EN ISO 11885, "
            "wavelength 249.772 nm) across dual laboratory benches ICP-OES-B1 (North Bay) and ICP-OES-B2 (South Bay). "
            "Certified reference check standards (0.25 mg/L, 0.50 mg/L, and 0.75 mg/L NIST-traceable boron) remained "
            "within +/-1.5% recovery across all 52 weekly analytical batches. Inline toroidal conductivity-derived "
            "permeate TDS transmitters on the North Bay (COLL-N-TDS01) and South Bay (COLL-S-TDS01) common permeate "
            "collectors were verified bi-weekly against gravimetric residue-on-evaporation check standards (SM 2540 C).",
            body,
        ),
        KeepTogether(
            [
                Paragraph("1.2 Validated 2026 Analytical and Inline Sensor Performance Summary:", body),
                _grid(
                    [
                        ["Performance Parameter", "Validated Value", "Basis"],
                        ["ICP-OES Boron Analytical Repeatability SD", "0.004 mg/L", "Pooled duplicate injections across 2026 batches"],
                        ["Boron Relative Standard Deviation at 0.50 mg/L", "0.80%", "Process excursion limit check standard"],
                        ["Boron Limit of Quantification (LOQ)", "0.020 mg/L", "10x procedural blank standard deviation"],
                        ["Inline Bay Collector TDS Probe Repeatability SD", "3.5 mg/L", "Bi-weekly gravimetric calibration checks (COLL-N/S-TDS01)"],
                    ],
                    [70, 36, 68],
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
        Paragraph("3. Automated Composite Sampling and Permeate Header Instrumentation", h2),
        Paragraph(
            "3.1 Permeate boron samples are drawn continuously from each train's permeate takeoff by refrigerated "
            "flow-proportional autosampler carousels. Under Barlavento's 2026 laboratory schedule, carousels run the "
            "standard 6-bottle daily program (4-hour composite bottles, PROG_4H_STD) from Thursday through Monday and "
            "switch to the extended 3-bottle daily program (8-hour composite bottles, PROG_8H_EXT) on Tuesdays and "
            "Wednesdays to accommodate scheduled municipal potable-water trace-metals runs and ICP-OES torch maintenance. "
            "No routine single-hour permeate boron grab sampling program was operated during 2026. Continuous inline TDS "
            "transmitters operate only on the North Bay and South Bay shared permeate collectors.",
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
        title="2026 Annual ICP-OES Boron and Inline Permeate TDS Quality Assurance Certificate",
        author=PK.PEOPLE["lims"],
        subject="ISO/IEC 17025 Permeate Boron and Bay Collector TDS Analytical Repeatability Verification",
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
