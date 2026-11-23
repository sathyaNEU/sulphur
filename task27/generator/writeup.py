"""Emit task27/submission.md strictly from task27/generator/figures.json (Arch 2, v4-hardened).

Carries exact platform blocks in order:
  0. ## Tags
  1. ## Final Recommendation
  2. ## Supplementary Questions (3 multi-faceted asks grouped by deliverable)
  3. ## Critical Components (3 independent decisive steps: answer + unit + band + deliverable ONLY, zero method clauses)
  4. ## Step-by-Step (numbered path + closing passage naming every rival and lattice independence)

Note: ## How is each model stumped? is added only after the platform's two model runs arrive (/triage-runs).
Zero em/en dashes, zero typed golden numbers outside figures.json, zero custom composite indices.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)


def render(fig=None):
    if fig is None:
        fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))

    corrs = fig["corridors"]
    by_c = {r["corridor_id"]: r for r in corrs}
    bands = fig["bands"]
    diag = fig["diagnostics"]
    rt = fig["routes"]
    cl = fig["cleaning"]

    funded = [r for r in corrs if r["decision"] == "FUND"]
    deferred = [r for r in corrs if r["decision"] == "DEFER"]

    def _band_bcr(cid):
        lo, hi = bands["BCR_" + cid.replace("-", "_")]
        return f"{lo:.3f} to {hi:.3f}"

    lines = []
    lines.append("## Tags")
    lines.append("")
    lines.append("**Domain:** Supply Chain & Logistics, Trade Flows (mapped to Machine Learning Research, General Statistics & Data Science: interpretability).")
    lines.append("**Analytical objective:** Root-Cause Analysis.")
    lines.append("")

    # 1. Final Recommendation
    lines.append("## Final Recommendation")
    lines.append("")
    lines.append(
        f"**Fund three North Sea import corridors under Charter RC-2027's EUR {fig['budget_cap_eur']:,.0f} "
        f"2027 carrier-remediation capital budget: "
        f"{funded[0]['corridor_id']} (Rank #1, BCR {funded[0]['bcr_2027']:.3f}, EUR {funded[0]['avoidable_eur_2027']:,.2f} avoidable / EUR {funded[0]['budget_eur']:,.0f} budget), "
        f"{funded[1]['corridor_id']} (Rank #2, BCR {funded[1]['bcr_2027']:.3f}, EUR {funded[1]['avoidable_eur_2027']:,.2f} / EUR {funded[1]['budget_eur']:,.0f}), and "
        f"{funded[2]['corridor_id']} (Rank #3, BCR {funded[2]['bcr_2027']:.3f}, EUR {funded[2]['avoidable_eur_2027']:,.2f} / EUR {funded[2]['budget_eur']:,.0f}), "
        f"deploying EUR {fig['funded_budget_eur']:,.2f} (leaving EUR {fig['unspent_budget_eur']:,.2f} in Contingency Reserve) "
        f"for EUR {fig['funded_avoidable_eur_2027']:,.2f} in projected 2027 avoidable carrier-controllable detention and demurrage "
        f"(funded portfolio BCR {fig['funded_portfolio_bcr']:.3f}), and defer "
        f"{deferred[0]['corridor_id']} (Rank #4, BCR {deferred[0]['bcr_2027']:.3f}), "
        f"{deferred[1]['corridor_id']} (Rank #5, BCR {deferred[1]['bcr_2027']:.3f}), and "
        f"{deferred[2]['corridor_id']} (Rank #6, BCR {deferred[2]['bcr_2027']:.3f}).** "
        f"This completely reverses the naive TMS and rigorous single-system ranking, which fund the exact wrong three corridors "
        f"(BHV-KAS at {rt['direct']['bcrs']['BHV-KAS']:.3f}, HAM-MAG at {rt['direct']['bcrs']['HAM-MAG']:.3f}, and "
        f"BHV-HAN at {rt['direct']['bcrs']['BHV-HAN']:.3f}) because unseparated non-carrier delays inflate all three deferred lanes "
        f"(cold-store chamber pull-back C1 = {fig['C1_coldstore_pullback_2026']:,.1f} c-days, BIP rail rollover bump C2 = "
        f"{fig['C2_phyto_rail_roll_2026']:,.1f} c-days, and ocean-line empty-depot portal backlog C3 = "
        f"{fig['C3_depot_backlog_2026']:,.1f} c-days). "
        f"The funded slate matches the exact integer knapsack optimum, holds across all 21 honest modeling specifications "
        f"(zero overlap between #3 HAM-HAN [{_band_bcr('HAM-HAN')}] and #4 HAM-MAG [{_band_bcr('HAM-MAG')}]), and survives "
        f"all eight +/-15% parameter stress tests."
    )
    lines.append("")

    # 2. Supplementary Questions
    lines.append("## Supplementary Questions")
    lines.append("")
    lines.append(
        f"1. **2027 corridor remediation funding slate and projected Benefit-Cost Ratios** "
        f"(in `weserfrucht_corridor_allocation_2027.csv`, `weserfrucht_corridor_capital_model_2027.xlsx` tabs "
        f"`Executive_Allocation` and `2027_Corridor_Economics`, and `weserfrucht_remediation_allocation_2027.pptx` slides 2-3 and 9-10): "
        f"Ranking all six corridors descending by projected 2027 BCR (avoidable carrier-controllable EUR / corridor budget EUR) under the "
        f"EUR {fig['budget_cap_eur']:,.0f} fixed capital cap yields: "
        f"#1 **WHV-OSN** BCR **{by_c['WHV-OSN']['bcr_2027']:.3f}** (band {_band_bcr('WHV-OSN')}; "
        f"EUR {by_c['WHV-OSN']['avoidable_eur_2027']:,.2f} avoidable / EUR {by_c['WHV-OSN']['budget_eur']:,.0f} budget; "
        f"{by_c['WHV-OSN']['carrier_ctrl_cdays_2027']:,.1f} carrier c-days; **FUND**); "
        f"#2 **BHV-OSN** BCR **{by_c['BHV-OSN']['bcr_2027']:.3f}** (band {_band_bcr('BHV-OSN')}; "
        f"EUR {by_c['BHV-OSN']['avoidable_eur_2027']:,.2f} / EUR {by_c['BHV-OSN']['budget_eur']:,.0f}; "
        f"{by_c['BHV-OSN']['carrier_ctrl_cdays_2027']:,.1f} carrier c-days; **FUND**); "
        f"#3 **HAM-HAN** BCR **{by_c['HAM-HAN']['bcr_2027']:.3f}** (band {_band_bcr('HAM-HAN')}; "
        f"EUR {by_c['HAM-HAN']['avoidable_eur_2027']:,.2f} / EUR {by_c['HAM-HAN']['budget_eur']:,.0f}; "
        f"{by_c['HAM-HAN']['carrier_ctrl_cdays_2027']:,.1f} carrier c-days; **FUND**); "
        f"#4 **HAM-MAG** BCR **{by_c['HAM-MAG']['bcr_2027']:.3f}** (band {_band_bcr('HAM-MAG')}; "
        f"EUR {by_c['HAM-MAG']['avoidable_eur_2027']:,.2f} / EUR {by_c['HAM-MAG']['budget_eur']:,.0f}; "
        f"{by_c['HAM-MAG']['carrier_ctrl_cdays_2027']:,.1f} carrier c-days; **DEFER**); "
        f"#5 **BHV-HAN** BCR **{by_c['BHV-HAN']['bcr_2027']:.3f}** (band {_band_bcr('BHV-HAN')}; "
        f"EUR {by_c['BHV-HAN']['avoidable_eur_2027']:,.2f} / EUR {by_c['BHV-HAN']['budget_eur']:,.0f}; "
        f"{by_c['BHV-HAN']['carrier_ctrl_cdays_2027']:,.1f} carrier c-days; **DEFER**); "
        f"#6 **BHV-KAS** BCR **{by_c['BHV-KAS']['bcr_2027']:.3f}** (band {_band_bcr('BHV-KAS')}; "
        f"EUR {by_c['BHV-KAS']['avoidable_eur_2027']:,.2f} / EUR {by_c['BHV-KAS']['budget_eur']:,.0f}; "
        f"{by_c['BHV-KAS']['carrier_ctrl_cdays_2027']:,.1f} carrier c-days; **DEFER**). "
        f"Total funded capital is EUR {fig['funded_budget_eur']:,.2f} (EUR {fig['unspent_budget_eur']:,.2f} unspent), "
        f"capturing EUR {fig['funded_avoidable_eur_2027']:,.2f} of EUR {fig['all6_avoidable_eur_2027']:,.2f} network-wide "
        f"2027 avoidable carrier-controllable exposure (funded portfolio BCR {fig['funded_portfolio_bcr']:.3f})."
    )
    lines.append("")
    lines.append(
        f"2. **2026 non-carrier delay volumes removed from carrier-controllable channels** "
        f"(in `weserfrucht_corridor_allocation_2027.csv`, `weserfrucht_corridor_capital_model_2027.xlsx` tab "
        f"`2026_Attribution_Bridge`, and `weserfrucht_remediation_allocation_2027.pptx` slides 4-7): "
        f"Across {cl['milestones_settled_containers']:,} reconciled settled 2026 import containers, separating the three "
        f"disclosed non-carrier overlap processes removes **{fig['total_non_carrier_removed_2026']:,.1f} container-days** (plus {fig['phyto_sibling_rail_2026']:,.1f} c-days "
        f"of direct CHED rail sibling holds) from raw TMS Stage 3, Stage 5, and Stage 7 timers, leaving "
        f"{fig['all6_carrier_ctrl_cdays_2026']:,.1f} attributed 2026 carrier-controllable container-days "
        f"({fig['all6_carrier_ctrl_cdays_2027']:,.1f} projected 2027 carrier-controllable container-days): "
        f"(a) inland cold-store thermal-chamber pull-back **C1 = {fig['C1_coldstore_pullback_2026']:,.1f} c-days** "
        f"(21-variant band {bands['C1_coldstore_pullback_2026'][0]:,.1f} to {bands['C1_coldstore_pullback_2026'][1]:,.1f}), "
        f"reassigned from `reefer_plug` to `coldstore_dock` (heaviest on BHV-KAS at {by_c['BHV-KAS']['c1_coldstore_pullback_2026']:,.1f} c-days); "
        f"(b) border-inspection rail booking-lock rollovers **C2 = {fig['C2_phyto_rail_roll_2026']:,.1f} c-days** "
        f"(21-variant band {bands['C2_phyto_rail_roll_2026'][0]:,.1f} to {bands['C2_phyto_rail_roll_2026'][1]:,.1f}, separate from "
        f"{fig['phyto_sibling_rail_2026']:,.1f} direct CHED rail sibling days), reassigned from `rail_handoff` to `phyto_insp` "
        f"(heaviest on HAM-MAG at {by_c['HAM-MAG']['c2_phyto_rail_roll_2026']:,.1f} c-days); and "
        f"(c) ocean-line empty-depot booking-portal queue backlogs **C3 = {fig['C3_depot_backlog_2026']:,.1f} c-days** "
        f"(21-variant band {bands['C3_depot_backlog_2026'][0]:,.1f} to {bands['C3_depot_backlog_2026'][1]:,.1f}), "
        f"reassigned from `drayage_carrier` to `empty_depot` (heaviest on BHV-HAN at {by_c['BHV-HAN']['c3_depot_backlog_2026']:,.1f} c-days, "
        f"with {diag['s3_open_day_backlog_share_pct']:.1f}% occurring on open-portal drain days)."
    )
    lines.append("")
    lines.append(
        f"3. **Deliverables, observable validation, and robustness audit** "
        f"(in `weserfrucht_remediation_allocation_2027.pptx` slides 8-10 and `weserfrucht_corridor_capital_model_2027.xlsx` "
        f"tabs `Validation_and_Routes` and `Robustness_and_Forcing`): "
        f"All three requested deliverables reconcile identically from one controlling calculation: "
        f"(i) the 10-slide committee deck (`weserfrucht_remediation_allocation_2027.pptx`) presenting the funding slate, "
        f"complete 3-for-3 ranking reversal, S1/S2/S3 empirical evidence, validation diagnostics, and 2027 SLA execution gates; "
        f"(ii) the 5-tab live-formula controlling workbook (`weserfrucht_corridor_capital_model_2027.xlsx`) carrying zero formula "
        f"recalculation errors; and (iii) the 6-row tracker CSV (`weserfrucht_corridor_allocation_2027.csv`) conforming to Charter "
        f"Section 5. Two-sided observable residual validation confirms non-carrier orthogonality and genuine carrier-slope "
        f"preservation (`fal_err` = {diag['golden_fal_err']:.1f} vs {diag['s1_one_fact_fal_err']:.1f} to {diag['cutoff_fal_err']:,.1f} "
        f"across all rivals), while 21/21 honest modeling specifications and 8/8 +/-15% parameter stresses hold the identical funding slate."
    )
    lines.append("")

    # 3. Critical Components (strictly answer + unit + band + deliverable, ZERO method!)
    lines.append("## Critical Components")
    lines.append("")
    lines.append(
        f"- **2026 inland cold-store thermal-chamber pull-back attribution (C1):** "
        f"**{fig['C1_coldstore_pullback_2026']:,.1f} container-days** "
        f"(21-variant band {bands['C1_coldstore_pullback_2026'][0]:,.1f} to {bands['C1_coldstore_pullback_2026'][1]:,.1f} c-days), "
        f"reported in `weserfrucht_corridor_allocation_2027.csv` (sum of `c1_coldstore_pullback_2026`), "
        f"`weserfrucht_corridor_capital_model_2027.xlsx` (`Executive_Allocation!G15` and `2026_Attribution_Bridge!G12`), "
        f"and `weserfrucht_remediation_allocation_2027.pptx` (slides 2, 4, and 5)."
    )
    lines.append(
        f"- **2026 border-inspection rail rollover attribution (C2):** "
        f"**{fig['C2_phyto_rail_roll_2026']:,.1f} container-days** "
        f"(21-variant band {bands['C2_phyto_rail_roll_2026'][0]:,.1f} to {bands['C2_phyto_rail_roll_2026'][1]:,.1f} c-days), "
        f"reported in `weserfrucht_corridor_allocation_2027.csv` (sum of `c2_phyto_rail_roll_2026`), "
        f"`weserfrucht_corridor_capital_model_2027.xlsx` (`Executive_Allocation!G16` and `2026_Attribution_Bridge!H12`), "
        f"and `weserfrucht_remediation_allocation_2027.pptx` (slides 2, 4, and 6)."
    )
    lines.append(
        f"- **2026 ocean-line empty-depot booking-portal backlog attribution (C3):** "
        f"**{fig['C3_depot_backlog_2026']:,.1f} container-days** "
        f"(21-variant band {bands['C3_depot_backlog_2026'][0]:,.1f} to {bands['C3_depot_backlog_2026'][1]:,.1f} c-days), "
        f"reported in `weserfrucht_corridor_allocation_2027.csv` (sum of `c3_depot_backlog_2026`), "
        f"`weserfrucht_corridor_capital_model_2027.xlsx` (`Executive_Allocation!G17` and `2026_Attribution_Bridge!I12`), "
        f"and `weserfrucht_remediation_allocation_2027.pptx` (slides 2, 4, and 7)."
    )
    lines.append("")

    ref = fig["reference"]
    # 4. Step-by-Step
    lines.append("## Step-by-Step")
    lines.append("")
    lines.append(
        f"1. **Operational data cleaning, reconciliation, and physical stock-flow assembly (Layer 1):** "
        f"Load all operational logs from `target.zip` under Charter RC-2027 Rev 3 Section 1.3 and Annex A. "
        f"In `container_milestones_2026.csv` ({cl['milestones_raw_rows']:,} raw rows), exclude {cl['milestones_void_removed']:,} "
        f"`record_status = VOID` EDI test transmissions and retain the maximum `extract_version` per `container_id` "
        f"(removing {cl['milestones_superseded_removed']:,} superseded rows) to establish the exact "
        f"{cl['milestones_settled_containers']:,} settled 2026 container lifecycles across {ref['n_vessels']} vessels, 6 corridors, and 4 ocean lines "
        f"(total all-8-cause excess = {fig['total_2026_all8_cdays']:,.2f} c-days). "
        f"In `warehouse_pallet_movements_2026.csv` ({cl['pallets_raw_rows']:,} raw rows), retain the latest `extract_version` "
        f"per `movement_id` (removing {cl['pallets_superseded_removed']:,} superseded revisions), parse mixed `DD.MM.YYYY` "
        f"({cl['pallets_de_date_rows']:,} rows) and ISO dates, convert {cl['pallets_case_converted_rows']:,} `CASE` rows to exact "
        f"integer Euro-pallets via `sku_thermal_catalog.csv`, and map {cl['pallets_legacy_store_mapped']:,} legacy retail store codes "
        f"via `entity_crosswalk_2026.csv`. Reconstruct daily closing stock and net flow (`IN - OUT`) for all 12 sealed thermal "
        f"chambers (`4 DCs x 3 zones`) from `dc_chamber_register_2026.csv`, verifying exact zero-residual agreement with "
        f"`coldstore_inventory_daily_2026.csv` on every DC-day (whole-DC occupancy stays flat between "
        f"{diag['s1_dc_total_util_min_pct']:.1f}% and {diag['s1_dc_total_util_max_pct']:.1f}%). "
        f"Audit `depot_turnin_log_2026.csv` ({cl['turnin_raw_rows']:,} rows; {cl['turnin_superseded_removed']:,} superseded; "
        f"{cl['turnin_legacy_carrier_mapped']:,} legacy carriers mapped) against `excess_depot_gate_cdays`, confirm "
        f"`carrier_dispute_closeout_2026.xlsx` reflects commercial invoice recovery scope only, and exclude the two contract "
        f"reference distractors (`north_sea_bunker_fuel_index_2026.csv` and `german_toll_maut_rates_2026_2027.xlsx`)."
    )
    lines.append("")
    lines.append(
        f"2. **Mechanism S1 (Inland cold-store chamber pull-back vs port reefer plug, C1 = {fig['C1_coldstore_pullback_2026']:,.1f} c-days):** "
        f"Whole-building DC occupancy stays flat ({diag['s1_dc_total_util_min_pct']:.1f}% to {diag['s1_dc_total_util_max_pct']:.1f}%) "
        f"because opposing summer Z02 (+2C) and winter Z07 (+7C) cycles offset Z13 (+13C) buffer stocks, so a whole-DC occupancy check "
        f"falsely attributes zero pull-back. Joining container discharge dates to reconstructed destination `(dc_id, thermal_zone)` "
        f"chamber occupancy and daily net pallet flow reveals a +{diag['s1_raw_asym_gap_h']:.2f}-hour raw filling-vs-draining "
        f"`excess_port_yard_cdays` gap at {ref['s1_band_lo_pct']}% to {ref['s1_band_hi_pct']}% chamber occupancy. Estimate a within-vessel fixed-effects asymmetric convex "
        f"response above {ref['s1_hinge_pct']}% chamber occupancy interacting excess utilization and squared excess utilization with filling "
        f"(`net_flow > 0`) vs draining (`net_flow <= 0`) regime indicators plus corridor controls, and split each container's "
        f"`excess_port_yard_cdays` by proportional Gamma posterior share `y * pred_pb / (pred_pb + pred_base)`. "
        f"This attributes **C1 = {fig['C1_coldstore_pullback_2026']:,.1f} c-days** (band {bands['C1_coldstore_pullback_2026'][0]:,.1f} "
        f"to {bands['C1_coldstore_pullback_2026'][1]:,.1f}) to `coldstore_dock`, collapsing the residual filling-vs-draining gap to "
        f"{diag['s1_resid_asym_gap_h']:.2f} hours while preserving genuine port reefer-rack congestion on draining-heavy BHV-OSN "
        f"(and stripping {by_c['BHV-KAS']['c1_coldstore_pullback_2026']:,.1f} non-carrier c-days out of filling-heavy BHV-KAS). "
        f"Seven alternative S1 specifications (binned non-parametric, piecewise spline, Huber robust FE, port-day FE, corridor-week FE, "
        f"hinges 0.76 and 0.80) all land inside band with zero call flips."
    )
    lines.append("")
    lines.append(
        f"3. **Mechanism S2 (Terminal-varying BIP rail booking locks vs Nordbahn short-consist cuts, C2 = {fig['C2_phyto_rail_roll_2026']:,.1f} c-days):** "
        f"Join `customs_consignment_bol_2026.csv`, `bip_inspection_notices_2026.jsonl` ({cl['bip_notice_lots']:,} BIP-selected CHED lots), "
        f"and `rail_shuttle_departures_2026.csv` ({ref['n_shuttles']} every-3-day corridor block trains). Separate direct non-sampled CHED rail sibling "
        f"holds ({fig['phyto_sibling_rail_2026']:,.1f} c-days above baseline rail dwell) directly to `phyto_insp`. For standby rail "
        f"rollovers (`departed_shuttle_id != planned_shuttle_id`), compute exact continuous notice lead hours "
        f"(`scheduled_departure_ts_utc` minus `exam_notice_ts_utc`, in hours) spanning {ref['s2_lead_min_h']}h to {ref['s2_lead_max_h']}h with zero dead zones. Profile each port's "
        f"smooth logistic booking-lock cutoff controlling jointly for correlated `consist_wagons_short` and `loco_derate_events`, "
        f"identifying distinct terminal cutoffs at BHV ({diag['s2_emp_port_cuts_h']['BHV']:.0f}h), HAM ({diag['s2_emp_port_cuts_h']['HAM']:.0f}h), "
        f"and WHV ({diag['s2_emp_port_cuts_h']['WHV']:.0f}h) with mean BIP standby pass-through slope {diag['s2_bip_slope']:.3f}. "
        f"Decompose each shuttle's observed rollover days using the exact Poisson-thinning posterior share `bip_hat / (bip_hat + rail_hat)`, "
        f"attributing **C2 = {fig['C2_phyto_rail_roll_2026']:,.1f} c-days** (band {bands['C2_phyto_rail_roll_2026'][0]:,.1f} "
        f"to {bands['C2_phyto_rail_roll_2026'][1]:,.1f}) to `phyto_insp`. This removes {by_c['HAM-MAG']['c2_phyto_rail_roll_2026']:,.1f} "
        f"c-days of late-notice BIP rollovers from HAM-MAG while preserving genuine Nordbahn consist shortfalls on HAM-HAN. "
        f"Seven alternative S2 specifications (Poisson IRLS, Huber, non-parametric lead bins, hard-step cuts, month+corridor FE, "
        f"pooled slope, and booked-slot control) all land inside band with zero call flips."
    )
    lines.append("")
    lines.append(
        f"4. **Mechanism S3 (Conserved shipping-line empty-depot portal backlogs vs carrier drayage, C3 = {fig['C3_depot_backlog_2026']:,.1f} c-days):** "
        f"Align container unload dates in `Europe/Berlin` civil time (`unload_complete_ts_cet`) and join daily `(port_id, shipping_line_id)` "
        f"inland empty unloads against `confirmed_bookings` in `depot_portal_requests_2026.csv` ({ref['n_portal_days']} days through 2027-01-18). "
        f"Compute the exact conserved unbooked return queue stock `Q_days(p, l, t) = cumsum(daily_unloads - confirmed_bookings) / mean_daily_unloads`. "
        f"Even on open-portal days (`quota_closed_rejections = 0`), high-queue containers (`Q_days >= {ref['s3_high_queue_thresh']}`) suffer a "
        f"+{diag['s3_raw_open_drain_gap_h']:.2f}-hour raw drayage delay premium over clean open days (`Q_days < {ref['s3_clean_queue_thresh']}`), confirming "
        f"that multi-day drain tails outlive portal closures ({diag['s3_open_day_backlog_share_pct']:.1f}% of total backlog delay accrues "
        f"after portal reopening). Estimate a DC-week fixed-effects regression of `excess_dray_empty_cdays` on corridor-interacted "
        f"`Q_days` (with corridor and day-of-week controls) and split each container via proportional Gamma posterior share, attributing "
        f"**C3 = {fig['C3_depot_backlog_2026']:,.1f} c-days** (band {bands['C3_depot_backlog_2026'][0]:,.1f} to "
        f"{bands['C3_depot_backlog_2026'][1]:,.1f}) to `empty_depot`. Residual open-portal drain gap collapses to "
        f"{diag['s3_resid_open_drain_gap_h']:.2f} hours, stripping {by_c['BHV-HAN']['c3_depot_backlog_2026']:,.1f} non-carrier c-days "
        f"from LINE_A/B-heavy BHV-HAN while protecting genuine drayage hub WHV-OSN ({ref['whv_osn_unconstrained_line_pct']:.1f}% unconstrained LINE_C/D). Six alternative S3 "
        f"specifications (DC-day FE, port-day FE, corridor-week FE, harmonic OLS, Huber, and distance-parametric) plus a joint "
        f"spline+Poisson+DC-day model all hold the identical call."
    )
    lines.append("")
    lines.append(
        f"5. **{ref['plan_year']} Annex C corridor projection, Schedule B valuation, and EUR {fig['budget_cap_eur']:,.0f} capital allocation:** "
        f"Scale each corridor's attributed 2026 carrier-controllable channel days (`reefer_plug`, `rail_handoff`, `drayage_carrier`) "
        f"by its corridor `vol_growth_2027` and port capacity factors from `remediation_program_budgets_2027.csv`, value at Schedule B "
        f"tariffs (EUR {ref['tariffs_eur']['reefer_plug']:.0f} / {ref['tariffs_eur']['rail_handoff']:.0f} / {ref['tariffs_eur']['drayage_carrier']:.0f} per day), multiply by `capture_rate_2027`, and divide by `remediation_budget_eur` to compute "
        f"each corridor's {ref['plan_year']} BCR: WHV-OSN {by_c['WHV-OSN']['bcr_2027']:.3f} (EUR {by_c['WHV-OSN']['avoidable_eur_2027']:,.2f} / "
        f"EUR {by_c['WHV-OSN']['budget_eur']:,.0f}), BHV-OSN {by_c['BHV-OSN']['bcr_2027']:.3f} (EUR {by_c['BHV-OSN']['avoidable_eur_2027']:,.2f} / "
        f"EUR {by_c['BHV-OSN']['budget_eur']:,.0f}), HAM-HAN {by_c['HAM-HAN']['bcr_2027']:.3f} (EUR {by_c['HAM-HAN']['avoidable_eur_2027']:,.2f} / "
        f"EUR {by_c['HAM-HAN']['budget_eur']:,.0f}), HAM-MAG {by_c['HAM-MAG']['bcr_2027']:.3f} (EUR {by_c['HAM-MAG']['avoidable_eur_2027']:,.2f} / "
        f"EUR {by_c['HAM-MAG']['budget_eur']:,.0f}), BHV-HAN {by_c['BHV-HAN']['bcr_2027']:.3f} (EUR {by_c['BHV-HAN']['avoidable_eur_2027']:,.2f} / "
        f"EUR {by_c['BHV-HAN']['budget_eur']:,.0f}), and BHV-KAS {by_c['BHV-KAS']['bcr_2027']:.3f} (EUR {by_c['BHV-KAS']['avoidable_eur_2027']:,.2f} / "
        f"EUR {by_c['BHV-KAS']['budget_eur']:,.0f}). Funding in descending BCR order within the EUR {fig['budget_cap_eur']:,.0f} cap "
        f"selects **WHV-OSN, BHV-OSN, and HAM-HAN** (EUR {fig['funded_budget_eur']:,.2f} deployed, EUR {fig['unspent_budget_eur']:,.2f} "
        f"unspent, EUR {fig['funded_avoidable_eur_2027']:,.2f} avoidable, portfolio BCR {fig['funded_portfolio_bcr']:.3f}), matching "
        f"the exact integer knapsack optimum (every 4-corridor subset requires at least EUR {ref['min_4corridor_budget_eur']:,.0f})."
    )
    lines.append("")
    lines.append(
        f"6. **Why no alternative conclusion survives (two-sided validation, lattice independence, and forcing):** "
        f"Every alternative route fails observable two-sided residual diagnostics (`fal_err` = {diag['golden_fal_err']:.1f} for the "
        f"joint golden solution vs {diag['s1_one_fact_fal_err']:.1f} to {diag['cutoff_fal_err']:,.1f} across rivals) and lands on a "
        f"wrong funding slate. Under-correcting any single mechanism opens its own false-alarm corridor: dropping S1 alone lifts "
        f"BHV-KAS to {rt['S1_drop']['bcrs']['BHV-KAS']:.3f} (funding {', '.join(rt['S1_drop']['funded_slate'])}); dropping S2 alone "
        f"lifts HAM-MAG to {rt['S2_drop']['bcrs']['HAM-MAG']:.3f} (funding {', '.join(rt['S2_drop']['funded_slate'])}); dropping S3 "
        f"alone lifts BHV-HAN to {rt['S3_drop']['bcrs']['BHV-HAN']:.3f} (funding {', '.join(rt['S3_drop']['funded_slate'])}); and "
        f"the direct TMS / rigorous single-system baselines fund BHV-HAN, BHV-KAS, and HAM-MAG (all three wrong). Partial shortcuts "
        f"fail on both sides: a binary >=92% chamber cut (`C1 = {rt['S1_one_fact']['C1_coldstore_pullback_2026']:,.1f}`) or symmetric "
        f"linear chamber FE (`BHV-KAS = {rt['S1_sym_lin']['bcrs']['BHV-KAS']:.3f}`) still mis-funds BHV-KAS; a fixed-24h bivariate "
        f"BIP regression omitting Nordbahn consist cuts over-attributes `C2 = {rt['S2_one_fact']['C2_phyto_rail_roll_2026']:,.1f}` "
        f"and crashes HAM-HAN to {rt['S2_one_fact']['bcrs']['HAM-HAN']:.3f}; a binary unload-day portal rejection flag recovers only "
        f"`C3 = {rt['S3_one_fact']['C3_depot_backlog_2026']:,.1f}` and still mis-funds BHV-HAN ({rt['S3_one_fact']['bcrs']['BHV-HAN']:.3f}); "
        f"and broad over-corrections (`S1_over`, `S2_over`, `S3_over`, `generous`, `cutoff`, `hedge`) collapse channel-dominant winners "
        f"BHV-OSN ({rt['S1_over']['bcrs']['BHV-OSN']:.3f}), HAM-HAN ({rt['S2_over']['bcrs']['HAM-HAN']:.3f}), or WHV-OSN "
        f"({rt['S3_over']['bcrs']['WHV-OSN']:.3f}). By contrast, all 21 honest modeling specifications and all 8 independent +/-15% "
        f"parameter stress tests confirm the identical funding slate: **WHV-OSN, BHV-OSN, and HAM-HAN**."
    )
    lines.append("")

    text = "\n".join(lines)
    assert "\u2014" not in text and "\u2013" not in text, "Em/en dash detected in submission.md!"
    out_path = os.path.join(TASK_DIR, "submission.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    return out_path


if __name__ == "__main__":
    p = render()
    print(f"Wrote {p} ({os.path.getsize(p)} bytes)")
