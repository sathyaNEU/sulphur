"""Generate Weserfrucht Cold-Chain Detention and Demurrage Charter RC-2027 (Rev 3) PDF via house officepdf.py.

Open-book governance standard (10 printed pages):
- Written strictly in Weserfrucht's corporate governance voice using domain observables (never listing
  input CSV field names verbatim and never duplicating the 2027 corridor budget table from
  remediation_program_budgets_2027.csv).
- Pins the WHAT completely: settled 2026 import lifecycles, 6 corridors, 8 stage free-time rules,
  3 carrier-controllable channels (reefer_plug, rail_handoff, drayage_carrier), EUR 1.75 million
  fixed 2027 capital cap, Schedule B daily tariffs, Annex C corridor projection equations, descending
  BCR ranking (full corridor funding only), and Section 5 output CSV register schema.
- Openly describes all three operational overlap processes (asymmetric filling-vs-draining thermal
  chamber pull-backs, terminal-varying BIP rail booking locks overlapping Nordbahn consist and
  locomotive cuts, and multi-day ocean-line empty-depot return backlogs) without prescribing
  statistical formulas, numeric cutoffs, or golden values.
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
import pack as PK  # noqa: E402

UTC = dt.timezone.utc

NAVY = colors.HexColor("#1E3A5F")
SLATE = colors.HexColor("#3A4B63")
MUTED = colors.HexColor("#555555")
ROW_ALT = colors.HexColor("#F3F6FA")
BORDER = colors.HexColor("#C5CDD8")

S_TITLE = ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=NAVY, spaceAfter=4)
S_SUB = ParagraphStyle("Sub", fontName="Helvetica-Oblique", fontSize=9.4, leading=13, textColor=MUTED, spaceAfter=10)
S_H1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=NAVY, spaceBefore=12, spaceAfter=4)
S_H2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=10.0, leading=13, textColor=SLATE, spaceBefore=8, spaceAfter=3)
S_BODY = ParagraphStyle("Body", fontName="Helvetica", fontSize=9.2, leading=13.4, textColor=colors.black, spaceAfter=5.5)
S_BULLET = ParagraphStyle("Bullet", fontName="Helvetica", fontSize=9.1, leading=13.2, textColor=colors.black, leftIndent=14, firstLineIndent=-8, spaceAfter=4)
S_SMALL = ParagraphStyle("Small", fontName="Helvetica", fontSize=8.3, leading=11.6, textColor=MUTED, spaceAfter=4)


def _tbl(data, widths):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8.4),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 8.3),
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

    # ---- PAGE 1: GOVERNANCE MANDATE & NETWORK SCOPE ----
    story.append(Paragraph("WESERFRUCHT IMPORT GMBH", S_SMALL))
    story.append(Paragraph("Cold-Chain Detention, Demurrage and Corridor Governance Charter (RC-2027)", S_TITLE))
    story.append(Paragraph(
        "Document Reference: WF-SCG-RC2027-Rev3 | Effective Date: 18 November 2026 | "
        "Issued by: Supply Chain Governance Committee (Bremen / Hannover) | "
        f"Owner: {PK.PEOPLE['procurement']} (Head of Transport Procurement)",
        S_SUB,
    ))

    story.append(Paragraph("1. Purpose, Governance Mandate, and Corridor Network Scope", S_H1))
    story.append(Paragraph(
        "Charter RC-2027 (Revision 3) governs Weserfrucht Import GmbH's annual cold-chain delay attribution "
        "review, carrier close-out reconciliation, and 2027 carrier-remediation budget allocation. "
        "For the 2027 operating cycle, the Executive Board has authorized a fixed carrier-remediation "
        "budget envelope of EUR 1.75 million to co-fund terminal power-rack allocations, intermodal rail "
        "traction and consist commitments, and dedicated inland reefer-chassis contracts across Weserfrucht's "
        "six active North Sea port-to-DC refrigerated import corridors.",
        S_BODY,
    ))
    story.append(Paragraph(
        "All volume counts, delay durations, operational attribution rules, and tariff schedules in this "
        "Charter apply to standardized 40-foot high-cube refrigerated import containers (1 container = 1 "
        "physical 40-foot reefer unit) discharging during calendar year 2026 (1 January 2026 through "
        "31 December 2026) at Bremerhaven (BHV), Hamburg (HAM), and Wilhelmshaven (WHV) and serving "
        "Weserfrucht's four inland multi-temperature cold-storage distribution centers at Hannover (HAN), "
        "Osnabrueck (OSN), Kassel (KAS), and Magdeburg (MAG).",
        S_BODY,
    ))

    corr_tbl = [
        ["Corridor", "Port Gateway", "Inland Cold-Store DC", "Primary Inland Mode Mix"],
        ["Bremerhaven - Hannover", "Bremerhaven (BHV)", "Hannover (HAN)", "Intermodal rail block train + regional road drayage"],
        ["Bremerhaven - Kassel", "Bremerhaven (BHV)", "Kassel (KAS)", "Intermodal rail block train + long-haul road drayage"],
        ["Bremerhaven - Osnabrueck", "Bremerhaven (BHV)", "Osnabrueck (OSN)", "Intermodal rail block train + regional road drayage"],
        ["Hamburg - Hannover", "Hamburg (HAM)", "Hannover (HAN)", "High-share Nordbahn rail corridor + road backup"],
        ["Hamburg - Magdeburg", "Hamburg (HAM)", "Magdeburg (MAG)", "High-share Nordbahn rail corridor + road backup"],
        ["Wilhelmshaven - Osnabrueck", "Wilhelmshaven (WHV)", "Osnabrueck (OSN)", "Intermodal rail shuttle + intensive regional drayage"],
    ]
    story.append(KeepTogether([
        Paragraph("Table 1. Active North Sea Port-to-DC Refrigerated Import Corridors (2026-2027)", S_SMALL),
        _tbl(corr_tbl, [118, 92, 96, 171]),
    ]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.2 Multi-Chamber Cold-Store Architecture and Carrier Partners", S_H2))
    story.append(Paragraph(
        "Each inland distribution center operates three physically sealed thermal chambers maintained at "
        "distinct commercial produce setpoints: Z02 (+2C chilled berries, stone fruit, and leafy greens), "
        "Z07 (+7C citrus, pome fruit, and table grapes), and Z13 (+13C bananas, avocados, mangoes, and "
        "tropical produce). Pallets cannot cross thermal chambers due to chilling-injury and ethylene "
        "segregation standards. Produce inflows follow strongly staggered annual calendars: Z07 citrus and "
        "winter stone-fruit volumes peak in Q1 and Q4, Z02 berry and summer stone-fruit volumes peak in "
        "late Q2 and Q3, and Z13 tropical buffer stock adjusts counter-seasonally across the year.",
        S_BODY,
    ))
    story.append(Paragraph(
        "Ocean transport and empty equipment pools are provided under annual contracts with four ocean "
        "carriers: Nordic Reefer Line (LINE_A), Hanseatic Ocean Alliance (LINE_B), Atlantic Fruit Carriers "
        "(LINE_C), and Baltic Cold Express (LINE_D). Hinterland rail traction is operated by Nordbahn "
        "Intermodal AG on scheduled every-3-day corridor block trains; inland road drayage and empty-box "
        "redelivery are executed by contracted regional trucking partners.",
        S_BODY,
    ))

    # ---- PAGE 2: RECORD SCOPE & STAGE FREE-TIME ALLOWANCES ----
    story.append(PageBreak())
    story.append(Paragraph("1.3 Record Scope, Revision Precedence, and Calendar Boundaries", S_H2))
    story.append(Paragraph(
        "Attribution covers all settled 2026 import container lifecycles, strictly excluding void or "
        "cancelled EDI test transmissions. Where operational extracts contain multiple nightly EDI "
        "revisions for the same container lifecycle, warehouse pallet movement, or empty-depot physical "
        "gate event, the highest revision version supersedes all earlier preliminary transmissions and "
        "constitutes the controlling record.",
        S_BODY,
    ))
    story.append(Paragraph(
        "Because late-December 2026 vessel discharges complete inland unloading and empty container "
        "redelivery during the first two weeks of January 2027, empty-return booking portal logs and "
        "depot gate logs extend cleanly into January 2027 so every 2026 discharge lifecycle closes without "
        "year-end truncation. Calendar quarters follow standard non-leap boundaries (Q1: Jan-Mar, Q2: "
        "Apr-Jun, Q3: Jul-Sep, Q4: Oct-Dec) assigned by container vessel discharge date.",
        S_BODY,
    ))

    story.append(Paragraph("1.4 Stage Free-Time Allowances and TMS Exception Buckets", S_H2))
    story.append(Paragraph(
        "For each settled container lifecycle, chargeable excess container-days in each operational stage "
        "equal elapsed hours beyond the contractual stage free-time allowance divided by 24. Table 2 "
        "records the eight sequential lifecycle stages logged by Weserfrucht's Transport Management System "
        "(TMS) and the corresponding contractual free-time windows.",
        S_BODY,
    ))

    ft_tbl = [
        ["Lifecycle Stage", "Elapsed Operational Window", "Free Time", "TMS Exception Code"],
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
        Paragraph("Table 2. Contractual Stage Free-Time Allowances and TMS Exception Buckets", S_SMALL),
        _tbl(ft_tbl, [118, 175, 68, 116]),
    ]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. Operational Cause Taxonomy and Carrier-Controllable Scope", S_H1))
    story.append(Paragraph("2.1 Exhaustive Cause Partition", S_H2))
    story.append(Paragraph(
        "All 2026 settled excess container-days partition exhaustively across eight canonical operational "
        "causes (Table 3). Operational attribution assigns every excess container-day to the originating "
        "operational constraint that caused the dwell rather than relying mechanically on whichever TMS "
        "stage clock was ticking when the delay accrued. Commercial dispute credit settlements in 2026 "
        "reflect documentary invoice proofs exchanged under existing carrier service agreements and do "
        "not govern operational cause attribution or 2027 funding eligibility.",
        S_BODY,
    ))

    cause_tbl = [
        ["Cause ID", "Funding Scope under RC-2027", "Originating Operational Constraint"],
        ["reefer_plug", "Carrier-Controllable", "Port terminal reefer power plug congestion, yard crane queues, and port gate bottlenecks."],
        ["rail_handoff", "Carrier-Controllable", "Nordbahn Intermodal locomotive derates, short-consist wagon cuts, and rail terminal transfers."],
        ["drayage_carrier", "Carrier-Controllable", "Contracted inland trucking fleet driver shortages, chassis scarcity, and road turnaround backlogs."],
        ["coldstore_dock", "Non-Carrier (Internal DC)", "Inland cold-store receiving constraints, dock scheduling limits, and thermal-chamber yard pull-backs."],
        ["phyto_insp", "Non-Carrier (Regulatory)", "EU Border Inspection Post (BIP) examinations, CHED consignment holds, and BIP-induced rail rollovers."],
        ["empty_depot", "Non-Carrier (Ocean Line)", "Ocean shipping-line empty-return depot booking-portal quota closures, backlog queues, and gate turn-aways."],
        ["vessel_berth", "Excluded (Ocean Line)", "Late ocean vessel arrival, anchorage queues, or berth-window slippage prior to discharge."],
        ["edi_docs", "Excluded (Customs/Docs)", "Commercial invoice, bill-of-lading, or customs brokerage release delays after discharge."],
    ]
    story.append(KeepTogether([
        Paragraph("Table 3. Canonical Operational Causes and Carrier-Controllable Funding Scope (Clause 2.2)", S_SMALL),
        _tbl(cause_tbl, [86, 112, 279]),
    ]))

    # ---- PAGE 3: OPEN-BOOK DISCLOSURE OF OVERLAP A ----
    story.append(PageBreak())
    story.append(Paragraph("2.2 Carrier-Controllable Corridor Scope", S_H2))
    story.append(Paragraph(
        "Under Clause 2.2, corridor carrier-remediation funds strictly address Weserfrucht's three "
        "carrier-controllable hinterland and terminal channels: <b>reefer_plug</b>, <b>rail_handoff</b>, "
        "and <b>drayage_carrier</b>. Delays originating from ocean vessel schedules (vessel_berth), "
        "customs brokerage paperwork (edi_docs), Weserfrucht's own inland cold-storage chambers "
        "(coldstore_dock), EU phytosanitary border inspections (phyto_insp), and ocean shipping line "
        "empty-return depot restrictions (empty_depot) are non-carrier or excluded causes and must be "
        "separated out of the three carrier-controllable channels before projecting 2027 corridor "
        "avoidable detention and demurrage exposure.",
        S_BODY,
    ))

    story.append(Paragraph("2.3 Multi-Stage Operational Attribution Overlaps", S_H2))
    story.append(Paragraph(
        "Joint operations reviews conducted in Q4 2026 by Weserfrucht Logistics Operations, Cold-Store "
        "Dispatch, Nordbahn Intermodal, and Drayage Procurement established three recurring operational "
        "processes whereby non-carrier bottlenecks accrue inside carrier-controllable TMS stage timers. "
        "Under this Charter, the annual review must empirically quantify and remove all three non-carrier "
        "volumes from 2026 TMS stage totals using Weserfrucht's operational system logs. Charter RC-2027 "
        "intentionally does not mandate a single econometric equation or fixed numeric cutoff for any "
        "overlap; the analytical team is responsible for estimating each process directly from the 2026 "
        "operational records and verifying that carrier-attributed delays remain consistent with observed "
        "terminal, rail, and road operating conditions.",
        S_BODY,
    ))

    story.append(Paragraph("Overlap A: Inland Cold-Store Chamber Pull-Back inside Port Terminal Yard Hold (coldstore_dock vs reefer_plug)", S_H2))
    story.append(Paragraph(
        "When an inland cold-storage distribution center's destination thermal chamber (+2C, +7C, or +13C) "
        "approaches high bay utilization, inland dispatch slows outbound port pick-up orders and holds "
        "import containers on port terminal power plugs rather than letting trucks queue at full inland "
        "receiving bays. Because the container has cleared customs but has not yet received a dispatch "
        "release, TMS accrues this inland-induced hold inside Stage 3 (TERM_YARD_HOLD) alongside genuine "
        "port terminal plug congestion.",
        S_BODY,
    ))
    story.append(Paragraph(
        "Two physical properties govern this process in Weserfrucht's network. First, because opposing "
        "seasonal produce cycles (+2C summer peak, +7C winter peak, +13C counter-seasonal buffer) offset "
        "each other within the same building, whole-warehouse aggregate occupancy reported in daily DC "
        "inventory summaries remains relatively stable even when an individual sealed chamber is under "
        "heavy pressure; chamber-level daily stock and daily pallet flow must therefore be reconstructed "
        "from SKU-level warehouse movement logs and the thermal catalog. Second, dispatch pull-backs "
        "depend strongly on whether a heavily loaded chamber is building or clearing inventory: when a "
        "near-full chamber is actively building stock (inbound pallets exceeding outbound retail "
        "shipments), receiving slots tighten sharply and yard pull-backs escalate steeply with chamber "
        "occupancy, whereas when the same chamber is drawing down stock, outbound shipments free bays "
        "steadily and port yard pull-back pressure is markedly lower at comparable occupancy levels. "
        "The total 2026 port-yard container-days attributed to inland chamber pull-back are reported as "
        "the cold-store pull-back volume (C1) and reassigned from reefer_plug to coldstore_dock.",
        S_BODY,
    ))

    # ---- PAGE 4: OPERATIONAL OVERLAPS B AND C ----
    story.append(PageBreak())
    story.append(Paragraph("Overlap B: Phytosanitary Border-Inspection Rail Booking Locks vs Nordbahn Capacity Cuts (phyto_insp vs rail_handoff)", S_H2))
    story.append(Paragraph(
        "EU Border Inspection Post (BIP) authorities issue phytosanitary examination notices at the CHED "
        "consignment-lot level (typically 2 to 6 containers sharing one health certificate). Direct "
        "physical sampling holds on the inspected container accrue under Stage 4 (PHYTO_HOLD). For "
        "rail-routed multi-container consignments, non-sampled sibling containers in the same CHED lot "
        "cannot board their train until laboratory release clears; TMS logs those direct sibling detention "
        "hours inside Stage 5 even though they belong to phyto_insp rather than rail_handoff.",
        S_BODY,
    ))
    story.append(Paragraph(
        "Beyond direct consignment holds, a second rail-level spillover occurs on scheduled every-3-day "
        "Nordbahn corridor block trains. When a BIP exam notice arrives sufficiently early prior to the "
        "port rail terminal's booking-lock deadline, Weserfrucht cancels the held containers' rail slot "
        "bookings before lock-in so standby rail containers can take those slots. When a BIP notice "
        "arrives after the port terminal's booking-lock window, the booked rail slots remain locked "
        "against the held CHED lot and depart physically unused, displacing cleared standby containers "
        "onto a subsequent block train under Stage 5 (RAIL_CAP_ROLL).",
        S_BODY,
    ))
    story.append(Paragraph(
        "Three operational realities complicate attribution on every-3-day block trains. First, the "
        "three North Sea rail gateways (Bremerhaven, Hamburg, and Wilhelmshaven) enforce distinct "
        "pre-departure booking-lock windows, and in daily terminal operations lock enforcement varies "
        "around train assembly rather than acting as a single uniform network deadline. Second, terminal "
        "planners occasionally reassign a share of late-locked slots or absorb spare capacity before "
        "departure, so locked BIP bookings do not displace standby containers on a mechanical one-for-one "
        "basis. Third, peak winter and summer produce waves simultaneously elevate BIP inspection volumes "
        "and strain Nordbahn's locomotive and wagon fleet, causing genuine carrier-controllable "
        "short-consist wagon shortfalls and locomotive derate events to occur frequently on the exact "
        "same peak shuttles as late BIP notices. Quantifying BIP-induced standby rail rollovers therefore "
        "requires joint shuttle-level analysis accounting for port-specific lock timing alongside "
        "overlapping Nordbahn consist shortages and locomotive derates. The total 2026 standby rail "
        "rollover container-days attributable to late BIP booking locks (excluding direct CHED sibling "
        "holds, which are separately classified to phyto_insp) are reported as the border-inspection rail "
        "rollover volume (C2) and reassigned from rail_handoff to phyto_insp.",
        S_BODY,
    ))

    story.append(Paragraph("Overlap C: Ocean-Line Empty-Depot Booking-Portal Backlogs inside Drayage Turnaround (empty_depot vs drayage_carrier)", S_H2))
    story.append(Paragraph(
        "After an import container completes unloading at an inland DC, the regional trucking carrier "
        "must secure an electronic empty-return appointment slot through the ocean shipping line's "
        "depot booking portal before dispatching the empty box back to the designated port depot. "
        "Physical turn-aways that occur after a truck actually arrives at the depot gate are logged "
        "separately under Stage 8 (DEPOT_TURN_AWAY) and in the physical depot gate log.",
        S_BODY,
    ))
    story.append(Paragraph(
        "However, ocean shipping lines periodically impose multi-day intake quota closures on their "
        "electronic booking portals by specific port and ocean-line pool, rejecting slot booking attempts "
        "before trucks leave the inland yard. While waiting for a confirmed portal slot, the unreturned "
        "empty container sits on chassis at the inland yard and TMS accrues the entire wait under "
        "Stage 7 (DRAY_EMPTY_HOLD) alongside genuine trucking fleet and chassis turnaround delays. "
        "Because shipping-line booking portals do not attach container identifiers to rejected appointment "
        "attempts, this restriction appears only in the daily port-by-line portal log recording daily "
        "confirmed return bookings and quota-closed booking rejections.",
        S_BODY,
    ))
    story.append(Paragraph(
        "Critically, portal-induced empty-return blocking does not end on the calendar day a shipping "
        "line reopens its booking portal. During a multi-day quota closure, inland empty unloads "
        "accumulate faster than confirmed portal return bookings, creating a physical pool of unbooked "
        "empties waiting for slots (cumulative inland empty unloads minus cumulative confirmed portal "
        "return bookings for each port and ocean shipping line). When the portal reopens (zero daily "
        "quota rejections), catch-up intake clears that backlog gradually over multiple subsequent open "
        "days, delaying containers unloaded during the drain tail while leaving unconstrained ocean lines "
        "at the same port unaffected. Turnaround scheduling sensitivity to unbooked return queues also "
        "varies across corridors because longer port-to-DC loops leave less daily dispatch slack than "
        "short regional turns. The total 2026 Stage 7 container-days attributable to ocean-line "
        "empty-depot booking backlogs are reported as the empty-depot backlog volume (C3) and reassigned "
        "from drayage_carrier to empty_depot.",
        S_BODY,
    ))

    # ---- PAGE 5: FINANCIAL VALUATION & CAPITAL ALLOCATION RULE ----
    story.append(PageBreak())
    story.append(Paragraph("3. 2027 Corridor Projection Specification and Schedule B Valuation", S_H1))
    story.append(Paragraph("3.1 Schedule B Contractual Daily Detention and Demurrage Tariffs", S_H2))
    story.append(Paragraph(
        "Projected 2027 carrier-controllable detention, demurrage, power, and rebooking exposure is "
        "valued in nominal euros (EUR) using the fixed contractual daily tariffs set out in Schedule B "
        "below. Bunker fuel indices (VLSFO/MGO, EU ETS surcharges) and German federal highway LKW-Maut "
        "toll tariffs are administered under ocean freight and line-haul transport contracts and do not "
        "enter Schedule B detention and demurrage valuation or corridor remediation budgets.",
        S_BODY,
    ))

    tar_tbl = [
        ["Cause ID", "Remediation Scope", "2027 Tariff (EUR/day)", "Contractual Cost Basis"],
        ["reefer_plug", "Carrier-Controllable", "210.00", "Port terminal demurrage, daily reefer power plug and monitoring fee"],
        ["rail_handoff", "Carrier-Controllable", "175.00", "Intermodal rail terminal storage, missed-consist rebooking penalty"],
        ["drayage_carrier", "Carrier-Controllable", "160.00", "Inland container equipment detention, standby reefer-chassis charge"],
        ["coldstore_dock", "Non-Carrier (Excluded)", "285.00", "Inland dock detention, extended power, perishable shelf-life shrink"],
        ["phyto_insp", "Non-Carrier (Excluded)", "260.00", "BIP inspection handling, quarantine storage, produce quality loss"],
        ["empty_depot", "Non-Carrier (Excluded)", "230.00", "Ocean-line equipment detention escalation, depot redelivery surcharge"],
        ["vessel_berth", "Excluded", "195.00", "Port berth-window rescheduling, feeder standby, shelf-life impact"],
        ["edi_docs", "Excluded", "140.00", "Customs brokerage administrative handling, terminal storage fee"],
    ]
    story.append(KeepTogether([
        Paragraph("Schedule B. Contractual 2027 Daily Detention and Demurrage Tariffs (Nominal EUR)", S_SMALL),
        _tbl(tar_tbl, [82, 102, 84, 209]),
    ]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.2 Annex C Corridor-Level 2027 Operating Plan Projection Equations", S_H2))
    story.append(Paragraph(
        "To project 2026 attributed carrier-controllable excess container-days for each corridor c onto "
        "the approved 2027 operating plan, each corridor's attributed 2026 container-days in each of the "
        "three carrier-controllable channels (reefer_plug, rail_handoff, drayage_carrier) are scaled by "
        "that corridor's contracted 2027 volume growth multiplier and the corresponding port gateway's "
        "2027 infrastructure capacity multiplier from the Board-approved 2027 corridor budget and "
        "operating plan schedule (Annex B):",
        S_BODY,
    ))
    story.append(Paragraph(
        "<b>(1) Projected 2027 Carrier-Controllable Days (corridor c, channel ch):</b><br/>"
        "Projected Plug Days(c) = Attributed 2026 Plug Days(c) x Corridor 2027 Volume Growth(c) x Port 2027 Plug Factor(port)<br/>"
        "Projected Rail Days(c) = Attributed 2026 Rail Days(c) x Corridor 2027 Volume Growth(c) x Port 2027 Rail Fleet Factor(port)<br/>"
        "Projected Dray Days(c) = Attributed 2026 Dray Days(c) x Corridor 2027 Volume Growth(c) x Port 2027 Dray Contract Factor(port)",
        S_BODY,
    ))
    story.append(Paragraph(
        "<b>(2) Projected 2027 Gross Carrier-Controllable Exposure (EUR):</b><br/>"
        "Gross 2027 EUR(c) = Projected Plug Days(c) x 210 + Projected Rail Days(c) x 175 + Projected Dray Days(c) x 160",
        S_BODY,
    ))
    story.append(Paragraph(
        "<b>(3) Projected 2027 Avoidable Carrier-Controllable Exposure (EUR):</b><br/>"
        "Avoidable 2027 EUR(c) = Gross 2027 EUR(c) x Corridor Engineering Capture Rate(c)",
        S_BODY,
    ))
    story.append(Paragraph(
        "where the corridor engineering capture rate is the verified share of projected 2027 "
        "carrier-controllable detention and demurrage exposure eliminated by executing corridor c's full "
        "carrier-remediation package.",
        S_BODY,
    ))

    story.append(Paragraph("4. 2027 Corridor Budget Allocation Rule (EUR 1.75 Million Fixed Cap)", S_H1))
    story.append(Paragraph("4.1 Benefit-Cost Ratio (BCR) Ranking and Full-Package Rule", S_H2))
    story.append(Paragraph(
        "Under Clause 4.1, each corridor's carrier-remediation package is an indivisible full-year "
        "commitment priced at the corridor package budget in the approved 2027 budget table (partial "
        "corridor funding is not permitted under carrier SLA minimums). Each corridor is evaluated on its "
        "projected 2027 Benefit-Cost Ratio:",
        S_BODY,
    ))
    story.append(Paragraph(
        "<b>Projected 2027 BCR(c) = Avoidable 2027 EUR(c) / Corridor Package Budget EUR(c)</b>",
        S_BODY,
    ))
    story.append(Paragraph(
        "Corridors are ranked strictly in descending order of projected 2027 BCR and funded sequentially "
        "until the fixed EUR 1.75 million budget cap prevents funding any additional corridor package. "
        "Any unspent balance below the smallest remaining corridor package budget is retained in Supply "
        "Chain Contingency Reserve. Corridors funded within the cap receive status <b>FUND</b>; corridors "
        "outside the cap receive status <b>DEFER</b>.",
        S_BODY,
    ))

    # ---- PAGE 6: ANNEX B PORT PROGRAMS & CORRIDOR PACKAGE CONTEXT ----
    story.append(PageBreak())
    story.append(Paragraph("Annex B. 2027 Port Infrastructure Baseline and Corridor Package Scope", S_H1))
    story.append(Paragraph(
        "The Board-approved numeric corridor package budgets, engineering capture rates, corridor 2027 "
        "volume growth rates, haul distances, and port gateway capacity multipliers are maintained as the "
        "single controlling electronic parameter schedule in Transport Procurement's 2027 corridor budget "
        "extract (remediation_program_budgets_2027.csv). All calculations must execute at full double "
        "precision without intermediate rounding; committee reports present container-days to one decimal "
        "place, euro values to two decimal places (or whole euros in executive summary tables), and BCRs "
        "to three decimal places.",
        S_BODY,
    ))

    story.append(Paragraph("B.1 Baseline Port Infrastructure and Carrier Fleet Changes (2027)", S_H2))
    story.append(Paragraph(
        "The port-level capacity multipliers in the 2027 operating plan schedule reflect baseline network "
        "investments already contracted independent of Weserfrucht's discretionary EUR 1.75 million "
        "corridor funding envelope:",
        S_BODY,
    ))
    story.append(Paragraph(
        "- Bremerhaven (BHV): Berth 4 shore-power upgrade commissions in Q1 2027 to relieve baseline plug "
        "congestion; Nordbahn deploys two upgraded BR-193 electric locomotives on BHV departures; "
        "regional terminal gate appointment smoothing moderately trims baseline dray turnaround.",
        S_BULLET,
    ))
    story.append(Paragraph(
        "- Hamburg (HAM): Altenwerder and Burchardkai quay civil works temporarily tighten available "
        "reefer plug density during summer peak; modest rail siding debottlenecking and Elbtunnel "
        "night-window access provide incremental relief to rail handoff and drayage.",
        S_BULLET,
    ))
    story.append(Paragraph(
        "- Wilhelmshaven (WHV): JadeWeserPort power rack capacity stays balanced at 2026 baseline levels; "
        "dedicated double-track electrification feeder improves Nordbahn shuttle reliability; A29 "
        "corridor chassis staging trims baseline drayage turnaround.",
        S_BULLET,
    ))

    story.append(Paragraph("B.2 Scope of Each Corridor's Indivisible Remediation Package", S_H2))
    story.append(Paragraph(
        "Each corridor package combines three carrier-side contractual levers tailored to that port-to-DC "
        "lane: (i) contracted priority reefer-plug allocation and peak power-monitoring SLA credits at "
        "the gateway terminal; (ii) guaranteed Nordbahn Intermodal backup locomotive call-out and minimum "
        "wagon-consist protection on scheduled every-3-day block trains; and (iii) dedicated peak-season "
        "reefer chassis and regional driver capacity commitments with Weserfrucht's drayage partners. "
        "Because port, rail, and trucking contractors bundle these guarantees at the corridor contract "
        "level, corridors must be funded or deferred as complete packages.",
        S_BODY,
    ))

    pkg_tbl = [
        ["Package Pillar", "Target Carrier Channel", "Contracted 2027 Operational Lever"],
        ["Gateway Plug SLA", "reefer_plug", "Dedicated reefer rack bays, priority crane lifts, and power-alarm response credits"],
        ["Rail Traction & Consist", "rail_handoff", "Standby BR-193 locomotive cover and guaranteed minimum reefer flat-wagon consist"],
        ["Peak Chassis & Dray", "drayage_carrier", "Dedicated peak-quarter reefer chassis pool and guaranteed regional driver turns"],
    ]
    story.append(KeepTogether([
        Paragraph("Table 4. Standard Three-Pillar Carrier Package Structure per Corridor", S_SMALL),
        _tbl(pkg_tbl, [112, 108, 257]),
    ]))

    # ---- PAGE 7: ANNEX A OPERATIONAL SYSTEM INTERFACES & CONSERVATION ----
    story.append(PageBreak())
    story.append(Paragraph("Annex A. Operational System Interfaces, Timezones, and Conservation Controls", S_H1))
    story.append(Paragraph(
        "Weserfrucht's cold-chain analytics environment consolidates operational extracts from five "
        "production IT systems: the central Transport Management System (TMS), the four-DC Warehouse "
        "Management System (WMS), Nordbahn Intermodal's Rail Dispatch System, EU TRACES-NT Border "
        "Inspection Post messaging, and ocean-carrier Empty-Depot Booking Portals. Table 5 defines the "
        "operational grain, clock convention, and reconciliation controls across these interfaces.",
        S_BODY,
    ))

    sys_tbl = [
        ["Production System", "Operational Grain", "Clock / Unit Convention", "Reconciliation Control"],
        ["Transport Management System", "One final settled record per container", "Port/rail UTC; inland DC CET/CEST; dwell in c-days", "Exclude void test records; retain highest revision"],
        ["Warehouse Management System", "Daily DC-by-SKU inbound and outbound pallets/cases", "Mixed German/ISO dates; cases or Euro-pallets", "Retain highest revision; convert cases via SKU catalog"],
        ["Cold-Store Chamber & Daily Ledger", "12 thermal chambers (4 DCs x 3 zones); daily whole-DC totals", "Euro-pallets; opening inventory on 1 January 2026", "Sum of three chamber stocks equals whole-DC total"],
        ["Nordbahn Rail Dispatch", "Scheduled every-3-day corridor block trains", "Scheduled departure UTC; wagons and gross tonnes", "Link planned shuttle IDs; track consist and loco cuts"],
        ["EU TRACES-NT BIP Feed", "One electronic notice per inspected CHED lot", "Notice and lab release timestamps in UTC", "Link via customs bill-of-lading CHED lot number"],
        ["Empty-Depot Booking Portal", "Daily port-by-ocean-line slot bookings and rejections", "Calendar dates aligned to inland CET unload day", "No container IDs; balance unloads vs confirmed bookings"],
        ["Depot Physical Gate Log", "Container physical gate arrivals and turn-aways", "Europe/Berlin civil time; legacy carrier codes", "Retain highest revision; resolve via entity crosswalk"],
    ]
    story.append(KeepTogether([
        Paragraph("Table 5. Production System Interface Specifications and Reconciliation Controls", S_SMALL),
        _tbl(sys_tbl, [96, 118, 125, 138]),
    ]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("A.1 Legacy Code Resolution and Case-to-Pallet Conversion", S_H2))
    story.append(Paragraph(
        "Following Weserfrucht's 2025 ERP migration, legacy retail store accounts and four legacy regional "
        "drayage carrier identifiers still appear in partial WMS and depot gate feeds. All legacy codes "
        "map directly to canonical identifiers via the active entity crosswalk. WMS movement lines are "
        "recorded either in Euro-pallets or in commercial produce cases; case-denominated movements "
        "convert to integer Euro-pallets using the standard cases-per-pallet factor maintained in the "
        "fresh-produce SKU thermal catalog.",
        S_BODY,
    ))

    story.append(Paragraph("A.2 Physical Stock-Flow Conservation Controls", S_H2))
    story.append(Paragraph(
        "Two physical stock-flow conservation controls govern data integrity prior to attribution modeling:",
        S_BODY,
    ))
    story.append(Paragraph(
        "1. Cold-Store Chamber Conservation: For every distribution center, thermal zone (Z02, Z07, Z13), "
        "and calendar day of 2026, closing chamber pallet stock equals 1 January 2026 opening stock plus "
        "cumulative net pallet flow (inbound minus outbound Euro-pallets). Across all three zones, "
        "reconstructed daily stocks reconcile to the daily whole-building cold-store inventory ledger "
        "with zero residual.",
        S_BULLET,
    ))
    story.append(Paragraph(
        "2. Empty-Return Portal Queue Conservation: For every gateway port, ocean shipping line, and "
        "operating day (1 January 2026 through 18 January 2027), the unbooked empty-container return "
        "queue equals cumulative daily inland container unloads (grouped by Europe/Berlin civil unload "
        "date across settled containers) minus cumulative confirmed return bookings logged by the "
        "shipping-line booking portal.",
        S_BULLET,
    ))

    # ---- PAGE 8: ANNEX C CONTROLLING VERIFICATION & SENSITIVITY GOVERNANCE ----
    story.append(PageBreak())
    story.append(Paragraph("Annex C. Attribution Verification and Sensitivity Governance Standards", S_H1))
    story.append(Paragraph(
        "Because carrier-controllable and non-carrier delays accrue inside shared TMS stage timers, "
        "Supply Chain Controlling requires every annual attribution study to satisfy internal audit "
        "governance criteria before presenting a corridor funding recommendation to the Carrier "
        "Remediation Committee.",
        S_BODY,
    ))

    story.append(Paragraph("C.1 Balanced Attribution Verification", S_H2))
    story.append(Paragraph(
        "Any separation of a shared TMS stage timer into carrier-controllable delay and non-carrier "
        "delay must demonstrate balance across both sides of operational attribution:",
        S_BODY,
    ))
    story.append(Paragraph(
        "- Completeness of Non-Carrier Removal: Attributed carrier-controllable delays must not retain "
        "material systematic spillover from the underlying non-carrier constraint after separation, "
        "ensuring that internal cold-store bottlenecks, regulatory border holds, and ocean-line depot "
        "restrictions do not distort corridor rankings.",
        S_BULLET,
    ))
    story.append(Paragraph(
        "- Preservation of Genuine Carrier Exposure: Non-carrier deductions must not over-subtract "
        "genuine terminal reefer-rack congestion, Nordbahn rail consist shortfalls, or regional trucking "
        "turnaround bottlenecks occurring during overlapping peak produce waves. Carrier-attributed "
        "channels must remain consistent with observed port, rail, and road operating conditions.",
        S_BULLET,
    ))
    story.append(Paragraph(
        "- Reconciliation Integrity: For every corridor and operational channel, attributed carrier-controllable "
        "days plus separated non-carrier days must sum exactly to settled 2026 TMS stage totals with zero "
        "unallocated residual.",
        S_BULLET,
    ))

    story.append(Paragraph("C.2 Sensitivity Documentation and Capital-Allocation Stability", S_H2))
    story.append(Paragraph(
        "Supply Chain Controlling requires the annual filing to evaluate whether the recommended funding "
        "slate remains stable under reasonable alternative estimation specifications and moderate "
        "sensitivity shifts in non-carrier attribution volumes and 2027 baseline volume growth assumptions. "
        "Where alternative defensible specifications yield modest variation in C1, C2, C3, or corridor "
        "BCR point estimates, the controlling workbook must document the sensitivity range alongside the "
        "primary recommendation.",
        S_BODY,
    ))

    story.append(Paragraph("C.3 Archive Retention and Operational Sign-Off Controls", S_H2))
    story.append(Paragraph(
        "All source operational extracts, transformation logs, reconciliation tables, and final workbook "
        "calculations supporting the RC-2027 funding recommendation must be archived under Supply Chain "
        "Controlling change control for a minimum of five calendar years. Any subsequent revision to "
        "corridor package budgets, port infrastructure factors, or Schedule B daily tariffs requires "
        "formal written amendment by the Supply Chain Governance Committee prior to SLA addendum execution.",
        S_BODY,
    ))

    # ---- PAGE 9: ANNEX D COMMERCIAL DISPUTE BOUNDARY & MILESTONES ----
    story.append(PageBreak())
    story.append(Paragraph("Annex D. Separation of Commercial Dispute Close-Out from 2027 Funding", S_H1))
    story.append(Paragraph(
        "Weserfrucht maintains two distinct financial governance workstreams at year-end close: "
        "(1) retrospective commercial invoice dispute settlement with carriers under 2026 service level "
        "agreements (summarized in the 2026 commercial dispute close-out workbook), and (2) prospective "
        "2027 corridor remediation funding allocation under Charter RC-2027.",
        S_BODY,
    ))
    story.append(Paragraph(
        "Commercial dispute settlements reconcile billed invoices against timestamped documentary "
        "proofs recognized under 2026 carrier contracts (for example, whether a terminal power bill "
        "exceeded 24 hours free time or whether a rail container departed on a later train). Because "
        "those 2026 commercial contracts did not contain cross-system clauses referencing Weserfrucht's "
        "internal WMS chamber occupancy or shipping-line electronic portal queue balances, settled "
        "invoice categories mirror raw TMS exception buckets scaled by historical commercial recovery "
        "rates. Consequently, the commercial dispute close-out workbook is an accounting "
        "reference for 2026 invoice reconciliation only and must not be substituted for empirical "
        "operational root-cause attribution when sizing 2027 corridor remediation investments.",
        S_BODY,
    ))

    story.append(Paragraph("D.1 Quarterly Governance Milestones for Funded Corridors (2027)", S_H2))
    gov_tbl = [
        ["Milestone", "Target Date", "Accountable Owner", "Governance Gate Deliverable"],
        ["Committee Funding Sign-Off", "26 Jan 2027", PK.PEOPLE["procurement"], "Approved FUND/DEFER slate, CSV register, and Controlling workbook"],
        ["Carrier SLA Addendum Execution", "19 Feb 2027", PK.PEOPLE["logistics"], "Signed port plug, Nordbahn consist, and chassis pool addenda"],
        ["Q2 Pre-Berry Readiness Audit", "15 May 2027", PK.PEOPLE["coldstore"], "Chamber intake smoothing & peak Z02/Z07 slot readiness review"],
        ["Pre-Peak Q3 Gate Review", "30 Jun 2027", PK.PEOPLE["controlling"], "Mid-year BCR tracking vs Annex C baseline across funded corridors"],
        ["Annual Close-Out Audit (2027)", "15 Jan 2028", PK.PEOPLE["analyst"], "Verified 2027 carrier-controllable D&D savings vs capture targets"],
    ]
    story.append(KeepTogether([
        Paragraph("Table 6. 2027 Carrier Remediation Governance Schedule", S_SMALL),
        _tbl(gov_tbl, [118, 72, 98, 189]),
    ]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("D.2 Non-Carrier Action Track (Outside the EUR 1.75 Million Carrier Budget)", S_H2))
    story.append(Paragraph(
        "Non-carrier delays separated out under Overlaps A, B, and C are routed to dedicated internal "
        "and commercial governance tracks outside the EUR 1.75 million carrier envelope: (i) cold-store "
        "pull-back (C1) feeds Weserfrucht's internal cold-storage dock scheduling and Z02/Z07 seasonal "
        "overflow leasing review; (ii) border-inspection rail rollovers (C2) feed Customs & Compliance "
        "pre-arrival CHED filing lead-time improvements ahead of each port's booking-lock window; and "
        "(iii) empty-depot booking-portal backlogs (C3) feed annual ocean-alliance contract negotiations "
        "for minimum guaranteed daily empty-return quotas.",
        S_BODY,
    ))

    # ---- PAGE 10: SECTION 5 FILING SPECIFICATION & SIGN-OFF ----
    story.append(PageBreak())
    story.append(Paragraph("5. Annual Carrier Remediation Committee Filing Specification", S_H1))
    story.append(Paragraph("5.1 Mandatory Deliverable Package", S_H2))
    story.append(Paragraph(
        "The annual carrier remediation committee review requires three reconciled work products "
        "derived from one controlling set of calculations:",
        S_BODY,
    ))
    story.append(Paragraph(
        "1. Committee Presentation Deck (.pptx): Executive funding recommendation, corridor BCR ranking "
        "under the EUR 1.75 million budget cap, operational evidence across all three non-carrier "
        "separation models (C1, C2, C3), attribution verification diagnostics, sensitivity checks, and "
        "Q1-Q3 2027 execution plan.",
        S_BULLET,
    ))
    story.append(Paragraph(
        "2. Controlling Financial and Attribution Workbook (.xlsx): Live-formula spreadsheet backing "
        "2026 container and stock-flow reconciliation, non-carrier attribution summaries, 2027 corridor "
        "carrier-controllable projections, Schedule B avoidable EUR, corridor BCR ranking, budget "
        "utilization under the EUR 1.75 million cap, and sensitivity checks.",
        S_BULLET,
    ))
    story.append(Paragraph(
        "3. Corridor Allocation Register (.csv): Machine-readable tracker load file conforming strictly "
        "to the column specification in Section 5 below.",
        S_BULLET,
    ))

    story.append(Paragraph("5.2 Corridor Allocation Register Output Schema", S_H2))
    story.append(Paragraph(
        "The corridor allocation register CSV contains exactly six rows (one per active North Sea import "
        "corridor in Table 1), sorted descending by projected 2027 BCR, with the exact thirteen output "
        "column headers defined in Table 7:",
        S_BODY,
    ))

    csv_tbl = [
        ["Output Column Header", "Format", "Controlling Definition"],
        ["corridor_id", "String", "Canonical corridor code (BHV-HAN, BHV-KAS, BHV-OSN, HAM-HAN, HAM-MAG, WHV-OSN)"],
        ["port_id", "String", "Gateway port code (BHV, HAM, WHV)"],
        ["dc_id", "String", "Inland distribution center code (HAN, OSN, KAS, MAG)"],
        ["budget_eur", "Numeric (2 dec)", "Board-approved 2027 corridor package budget (EUR)"],
        ["c1_coldstore_pullback_2026", "Numeric (1 dec)", "2026 port-yard container-days attributed to inland cold-store chamber pull-back"],
        ["c2_phyto_rail_roll_2026", "Numeric (1 dec)", "2026 standby rail rollover container-days attributed to late BIP booking locks"],
        ["c3_depot_backlog_2026", "Numeric (1 dec)", "2026 drayage stage container-days attributed to ocean-line empty-depot portal backlogs"],
        ["carrier_ctrl_cdays_2026", "Numeric (1 dec)", "2026 attributed carrier-controllable container-days (reefer_plug + rail_handoff + drayage_carrier)"],
        ["carrier_ctrl_cdays_2027", "Numeric (1 dec)", "Projected 2027 carrier-controllable container-days under Annex C"],
        ["avoidable_eur_2027", "Numeric (2 dec)", "Projected 2027 avoidable carrier-controllable D&D exposure (EUR, after capture rate)"],
        ["bcr_2027", "Numeric (3 dec)", "Projected 2027 Benefit-Cost Ratio (avoidable_eur_2027 / budget_eur)"],
        ["rank", "Integer (1-6)", "Descending BCR priority rank (1 = highest BCR)"],
        ["decision", "String", "Funding decision under EUR 1.75 million cap: FUND or DEFER"],
    ]
    story.append(KeepTogether([
        Paragraph("Table 7. Section 5 Output CSV Register Schema", S_SMALL),
        _tbl(csv_tbl, [126, 80, 271]),
    ]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("5.3 Governance Approval and Sign-Off", S_H2))
    story.append(Paragraph(
        f"Approved by Supply Chain Governance Committee: {PK.PEOPLE['procurement']} (Head of Transport "
        f"Procurement), {PK.PEOPLE['logistics']} (Director of Logistics Operations), "
        f"{PK.PEOPLE['coldstore']} (Head of Cold-Store Operations), {PK.PEOPLE['rail_ops']} "
        f"(Intermodal Rail Coordinator), and {PK.PEOPLE['controlling']} (Senior Supply Chain Controller). "
        "Bremen / Hannover, 18 November 2026.",
        S_SMALL,
    ))

    created = dt.datetime(2026, 11, 16, 9, 24, 10, tzinfo=UTC)
    modified = dt.datetime(2026, 11, 18, 15, 42, 33, tzinfo=UTC)
    officepdf.build(
        path=out_path,
        story=story,
        title="Weserfrucht Cold-Chain Detention, Demurrage and Corridor Governance Charter (RC-2027 Rev 3)",
        author=PK.PEOPLE["procurement"],
        subject="Cold-chain delay attribution framework, Schedule B tariffs, Annex C projections, and EUR 1.75M corridor governance",
        footer="Weserfrucht Import GmbH  |  Charter RC-2027 (WF-SCG-RC2027-Rev3)",
        created=created,
        modified=modified,
        producer="LibreOffice 25.8",
        header="Weserfrucht Import GmbH - Supply Chain Governance Charter RC-2027 (Rev 3)",
        page_of=True,
    )


def write_all(target_dir):
    write_charter(os.path.join(target_dir, PK.FILES["charter"]))
