"""Generate Weserfrucht Cold-Chain Remediation Charter RC-2027 PDF via house officepdf.py.

Strictly pins the WHAT only (chargeable excess container-day scope, stage free-time allowances,
eight canonical operational causes, exhaustive 2026 conservation, >= 2,500 Mandatory Remediation
threshold, Schedule B daily EUR tariffs, Annex C uniform cause-level 2027 projection rules, and
Section 5 CSV register schema). Zero analytical methods, zero stump vocabulary, zero em dashes.
"""
import datetime as dt
import os
import sys

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, ".agents", "skills", "reduce-house-fixes", "scripts", "writers"))
import officepdf  # noqa: E402
import core  # noqa: E402
import pack as PK  # noqa: E402

UTC = dt.timezone.utc

NAVY = colors.HexColor("#1E3A5F")
SLATE = colors.HexColor("#3A4B63")
MUTED = colors.HexColor("#555555")
ROW_ALT = colors.HexColor("#F3F6FA")
BORDER = colors.HexColor("#C5CDD8")

S_TITLE = ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=NAVY, spaceAfter=4)
S_SUB = ParagraphStyle("Sub", fontName="Helvetica-Oblique", fontSize=9.5, leading=13, textColor=MUTED, spaceAfter=10)
S_H1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=NAVY, spaceBefore=12, spaceAfter=4)
S_H2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=SLATE, spaceBefore=8, spaceAfter=3)
S_BODY = ParagraphStyle("Body", fontName="Helvetica", fontSize=9.2, leading=13.2, textColor=colors.black, spaceAfter=5)
S_SMALL = ParagraphStyle("Small", fontName="Helvetica", fontSize=8.3, leading=11.5, textColor=MUTED, spaceAfter=4)


def _tbl(data, widths):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 8.4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT]),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def write_charter(out_path):
    story = []

    story.append(Paragraph("WESERFRUCHT IMPORT GMBH", S_SMALL))
    story.append(Paragraph("Cold-Chain Detention, Demurrage and Remediation Charter (RC-2027)", S_TITLE))
    story.append(Paragraph(
        "Document Reference: WF-SCG-RC2027-Rev2 | Effective Date: 18 November 2026 | "
        "Issued by: Supply Chain Governance Committee (Bremen / Hannover) | "
        f"Owner: {PK.PEOPLE['procurement']} (Head of Transport Procurement)",
        S_SUB,
    ))

    story.append(Paragraph("1. Purpose and Network Scope", S_H1))
    story.append(Paragraph(
        "Charter RC-2027 governs Weserfrucht Import GmbH's annual cold-chain delay attribution, "
        "carrier close-out settlement review, and 2027 Mandatory Remediation funding allocation across "
        "all 40-foot high-cube refrigerated import containers entering Northern Germany through "
        "Bremerhaven (BHV), Hamburg (HAM), and Wilhelmshaven (WHV) and serving the four inland cold-storage "
        "distribution centers at Hannover (HAN), Osnabrueck (OSN), Kassel (KAS), and Magdeburg (MAG).",
        S_BODY,
    ))
    story.append(Paragraph(
        "All volume counts, delay durations, and tariff schedules in this Charter apply to standardized "
        "40-foot high-cube refrigerated containers (1 container = 1 physical 40-foot reefer unit) across "
        "all three commercial produce temperature classes: +2C chilled berry and stonefruit (Z02), "
        "+7C citrus and pome fruit (Z07), and +13C tropical produce (Z13).",
        S_BODY,
    ))

    story.append(Paragraph("2. Chargeable Excess Container-Days and Operational Cause Taxonomy", S_H1))
    story.append(Paragraph("2.1 Definition of Chargeable Excess Container-Days and Record Scope", S_H2))
    story.append(Paragraph(
        "For each settled import container lifecycle in calendar year 2026 (excluding cancelled or void "
        "EDI test transmissions), chargeable excess container-days equal elapsed hours beyond the "
        "contractual stage free-time allowance divided by 24. Where operational extracts contain multiple "
        "nightly EDI revisions for the same container, warehouse movement, or depot gate event, the "
        "highest revision version supersedes earlier preliminary transmissions. Port and rail operational "
        "timestamps are logged in Coordinated Universal Time (UTC), whereas inland cold-store and depot "
        "gate timestamps are logged in Europe/Berlin civil time (CET/CEST). Legacy retail store and "
        "drayage carrier codes resolve to canonical partner codes via the active entity crosswalk.",
        S_BODY,
    ))

    ft_tbl = [
        ["Lifecycle Stage", "Elapsed Operational Window", "Contractual Free Time", "Primary TMS Exception Bucket"],
        ["1. Vessel Berth Arrival", "Scheduled vessel ETA to vessel discharge", "0 hours", "VESSEL_LATE"],
        ["2. Customs / EDI Release", "Vessel discharge to customs document release", "6 hours", "EDI_DOC_HOLD"],
        ["3. Port Terminal Yard Dwell", "Customs release to port gate readiness", "24 hours", "TERM_YARD_HOLD"],
        ["4. Border Phytosanitary Exam", "Port gate readiness to border exam release", "0 hours", "PHYTO_HOLD"],
        ["5. Hinterland Rail Handoff", "Border release to intermodal rail departure (RAIL)", "6 hours", "RAIL_CAP_ROLL"],
        ["6. Inland Cold-Store Dock", "Inland DC gate-in to unload completion", "4 hours", "DC_DOCK_WAIT"],
        ["7. Empty Drayage Return", "Unload completion to empty depot gate arrival", "24 hours", "DRAY_EMPTY_HOLD"],
        ["8. Empty Depot Physical Gate", "Depot gate arrival to empty gate acceptance", "0 hours", "DEPOT_TURN_AWAY"],
    ]
    story.append(KeepTogether([
        Paragraph("Table 1. Contractual Stage Free-Time Allowances under Charter RC-2027", S_SMALL),
        _tbl(ft_tbl, [118, 165, 86, 108]),
    ]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.2 Canonical Operational Cause Partition", S_H2))
    story.append(Paragraph(
        "Attribution of 2026 settled excess container-days uses an exhaustive, mutually exclusive "
        "partition across the eight operational cause identifiers listed in Table 2. The sum of "
        "attributed 2026 container-days across all eight causes equals 100 percent of settled 2026 "
        "network excess container-days with zero unallocated residual. Operational cause attribution "
        "reflects the originating operational bottleneck responsible for each container-day of excess "
        "dwell, regardless of which lifecycle stage timer was running when the delay accrued.",
        S_BODY,
    ))

    cause_tbl = [
        ["Cause ID", "Operational Bottleneck Definition"],
        ["vessel_berth", "Late ocean vessel arrival, anchorage wait, or berth-window slippage prior to container discharge."],
        ["edi_docs", "Commercial invoice, bill-of-lading, or customs clearance holds after vessel discharge."],
        ["reefer_plug", "Port terminal power plug congestion, yard crane queues, and terminal gate congestion."],
        ["coldstore_dock", "Inland distribution center receiving constraints, dock scheduling limits, or inland receiving holdbacks."],
        ["rail_handoff", "Intermodal rail operator locomotive shortages, short-consist capacity cuts, or rail terminal transfer delays."],
        ["phyto_insp", "EU Border Inspection Post (BIP) phytosanitary examinations, consignment holds, and directly caused border clearances."],
        ["drayage_carrier", "Inland trucking fleet driver shortages, chassis availability, and carrier turnaround backlogs."],
        ["empty_depot", "Ocean carrier empty-container return depot intake restrictions, gate turn-aways, and empty-return acceptance limits."],
    ]
    story.append(KeepTogether([
        Paragraph("Table 2. Canonical Operational Cause Identifiers (Charter Clause 2.2)", S_SMALL),
        _tbl(cause_tbl, [98, 379]),
    ]))

    story.append(PageBreak())
    story.append(Paragraph("3. 2027 Mandatory Remediation Threshold and Designation Rule", S_H1))
    story.append(Paragraph(
        "Under Clause 3.1 of Charter RC-2027, Weserfrucht allocates dedicated 2027 capital and carrier "
        "remediation budgets exclusively to operational causes whose projected 2027 attributable excess "
        "container-days under the 2027 Import Schedule Plan equal or exceed 2,500 container-days:",
        S_BODY,
    ))
    story.append(Paragraph(
        "<b>REMEDIATE (Mandatory Remediation):</b> Projected 2027 attributable excess container-days >= 2,500.0.<br/>"
        "<b>MONITOR (Routine Monitoring):</b> Projected 2027 attributable excess container-days < 2,500.0.",
        S_BODY,
    ))
    story.append(Paragraph(
        "The 2,500 container-day designation threshold applies strictly to projected 2027 attributable "
        "excess container-days under the approved 2027 Import Schedule Plan (Annex C), not to unprojected "
        "2026 actuals. Commercial dispute credit settlements in 2026 reflect documentary invoice proofs "
        "exchanged under existing carrier service level agreements and do not govern operational root-cause "
        "designations under Clause 3.1.",
        S_BODY,
    ))

    story.append(Paragraph("4. Financial Valuation (Schedule B) and Corridor / Quarter Reporting", S_H1))
    story.append(Paragraph("4.1 Contractual Daily Detention, Demurrage and Cold-Chain Exposure Tariffs", S_H2))
    story.append(Paragraph(
        "Projected 2027 financial exposure is valued in nominal euros (EUR) using the fixed contractual "
        "per-cause daily detention, demurrage, power, and spoilage-risk tariffs set out in "
        "Schedule B below. Total 2027 network expenditure equals the sum of (projected 2027 container-days "
        "x Schedule B daily EUR tariff) across all eight causes. Avoidable 2027 expenditure for designated "
        "causes equals 100 percent of projected 2027 EUR exposure summed across all causes designated "
        "REMEDIATE under Clause 3.1. Bunker fuel indices and federal highway LKW-Maut toll schedules are "
        "budgeted under ocean freight and line-haul contracts and are outside Schedule B detention and "
        "demurrage tariffs.",
        S_BODY,
    ))

    tar_tbl = [
        ["Cause ID", "2027 Daily Tariff (EUR / day)", "Contractual Cost Scope"],
        ["vessel_berth", "195", "Port berth-window rescheduling, vessel feeder standby, shelf-life shrink"],
        ["edi_docs", "140", "Customs brokerage handling, terminal storage surcharge"],
        ["reefer_plug", "210", "Port terminal demurrage, daily container power plug fee"],
        ["coldstore_dock", "285", "Extended container power, inland dock detention, perishable produce shrink"],
        ["rail_handoff", "175", "Intermodal terminal storage, shuttle rebooking penalty"],
        ["phyto_insp", "260", "BIP inspection handling, quarantine storage, perishable shelf-life loss"],
        ["drayage_carrier", "160", "Equipment detention, chassis standby charge"],
        ["empty_depot", "230", "Ocean-line equipment detention escalation, yard storage and redelivery handling"],
    ]
    story.append(KeepTogether([
        Paragraph("Schedule B. Contractual 2027 Daily Detention and Demurrage Tariffs (Nominal EUR)", S_SMALL),
        _tbl(tar_tbl, [100, 128, 249]),
    ]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.2 Port Corridor and Calendar Quarter Definitions", S_H2))
    story.append(Paragraph(
        "Calendar quarters follow standard non-leap calendar boundaries: Q1 = 1 January to 31 March, "
        "Q2 = 1 April to 30 June, Q3 = 1 July to 30 September, and Q4 = 1 October to 31 December, "
        "assigned by container discharge date (or planned shuttle date for corridor-level rail transfers). "
        "Reported 2027 excess container-days for Bremerhaven (BHV), Hamburg (HAM), and Q3 include all "
        "eight operational causes combined across the full settled network (BHV, HAM, and WHV).",
        S_BODY,
    ))

    story.append(PageBreak())
    story.append(Paragraph("Annex C. 2027 Import Schedule Projection Specification", S_H1))
    story.append(Paragraph(
        "To translate 2026 attributed excess container-days by operational cause onto the 2027 operating "
        "plan, each cause's 2026 attributable container-days are scaled uniformly using the approved "
        "2027 operating-plan schedule parameters as specified in Table 3. Every container-day "
        "attributed to a given cause uses that cause's single Annex C projection formula.",
        S_BODY,
    ))

    annex_tbl = [
        ["Cause ID", "2027 Uniform Projection Formula (applied to 2026 attributed container-days)"],
        ["vessel_berth", "2026 days by port x 2027 port volume growth"],
        ["edi_docs", "2026 days by port x 2027 port volume growth"],
        ["reefer_plug", "2026 days by port x 2027 port volume growth x 2027 port plug capacity factor"],
        ["coldstore_dock", "2026 days by temperature class x 2027 DC zone load factor"],
        ["rail_handoff", "2026 days by port x 2027 port volume growth x 2027 rail fleet factor"],
        ["phyto_insp", "2026 days by port x 2027 port volume growth x 2027 port BIP sampling factor"],
        ["drayage_carrier", "2026 days by port x 2027 port volume growth x 2027 road contract factor"],
        ["empty_depot", "2026 days by port and ocean line x 2027 port volume growth x (2027 / 2026 line share) x 2027 depot load factor"],
    ]
    story.append(KeepTogether([
        Paragraph("Table 3. Uniform Cause-Level 2027 Projection Equations (Annex C)", S_SMALL),
        _tbl(annex_tbl, [98, 379]),
    ]))
    story.append(Spacer(1, 6))

    p_tbl = [
        ["Plan Dimension", "Entity", "2026 Base", "2027 Plan / Factor", "Operational Context"],
        ["Port volume growth", "BHV / HAM / WHV", "1.00", "1.10 / 1.12 / 1.06", "Contracted 2027 North Sea import volume plan"],
        ["Berth 4 plug upgrade", "BHV / HAM / WHV", "1.00", "0.78 / 1.00 / 1.00", "Bremerhaven Berth 4 additional power racks commissioned Q1 2027"],
        ["Inland DC zone load", "Z02 / Z07 / Z13", "1.00", "1.48 / 1.06 / 1.08", "Expanded 2027 +2C chilled berry program on fixed DC footprint"],
        ["EU BIP exam schedule", "BHV / HAM / WHV", "1.00", "1.25 / 1.23 / 1.20", "2027 EU Priority-Pest border sampling frequency schedule"],
        ["Nordbahn rail fleet", "NETWORK", "1.00", "0.84", "Two additional Nordbahn BR-193 locomotives entering service Jan 2027"],
        ["Road carrier contract", "NETWORK", "1.00", "0.88", "Dedicated regional chassis pool effective Jan 2027"],
        ["Ocean line share", "LINE_A / B / C / D", "26/25/26/23%", "34/32/20/14%", "2027 Ocean Alliance vessel-sharing consolidation"],
        ["Empty depot load", "LINE_A / B / C / D", "1.00", "1.22 / 1.20 / 1.00 / 1.00", "2027 carrier container-pool rebalancing at North Sea depots"],
    ]
    story.append(KeepTogether([
        Paragraph("Table 4. Summary of Approved 2027 Operating Plan Parameters", S_SMALL),
        _tbl(p_tbl, [92, 80, 62, 100, 143]),
    ]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5. Annual Carrier Close-Out Register Filing Specification", S_H1))
    story.append(Paragraph(
        "For the annual carrier close-out review, the cause-level register CSV contains exactly eight "
        "rows (one per canonical cause_id from Table 2), sorted descending by projected 2027 excess "
        "container-days, with columns: cause_id, cdays_2026, cdays_2027, share_2027_pct, eur_2027, "
        "and designation (REMEDIATE or MONITOR).",
        S_BODY,
    ))
    story.append(Paragraph(
        f"Approved by Supply Chain Governance Committee: {PK.PEOPLE['procurement']} (Procurement), "
        f"{PK.PEOPLE['logistics']} (Logistics Operations), and {PK.PEOPLE['controlling']} (Financial Controlling). "
        "Bremen, 18 November 2026.",
        S_SMALL,
    ))

    created = dt.datetime(2026, 11, 16, 9, 24, 10, tzinfo=UTC)
    modified = dt.datetime(2026, 11, 18, 15, 42, 33, tzinfo=UTC)
    officepdf.build(
        path=out_path,
        story=story,
        title="Weserfrucht Cold-Chain Detention, Demurrage and Remediation Charter (RC-2027)",
        author=PK.PEOPLE["procurement"],
        subject="Cold-chain delay attribution definitions, Schedule B tariffs, and 2027 remediation threshold",
        footer="Weserfrucht Import GmbH  |  Charter RC-2027 (WF-SCG-RC2027-Rev2)",
        created=created,
        modified=modified,
        producer="LibreOffice 25.8",
        header="Weserfrucht Import GmbH - Supply Chain Governance Charter RC-2027",
        page_of=True,
    )


def write_all(target_dir):
    write_charter(os.path.join(target_dir, PK.FILES["charter"]))
