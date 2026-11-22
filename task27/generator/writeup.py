"""Emit task27/submission.md strictly from task27/generator/figures.json.

Carries exact platform blocks in order:
  0. ## Tags
  1. ## Final Recommendation
  2. ## Supplementary Questions (4 multi-faceted asks grouped by file)
  3. ## Critical Components (3 independent one-liners: answer + unit + band ONLY, zero method clauses)
  4. ## Step-by-Step (numbered path + closing passage naming every rival and lattice independence)

Zero em/en dashes, zero typed numbers outside figures.json, zero custom composite indices.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)


def render(fig=None):
    if fig is None:
        fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))

    by_id = {r["cause_id"]: r for r in fig["causes"]}
    d = fig["R5_diagnostics"]
    cl = fig["cleaning"]
    cs = fig["chamber_stats"]
    ab = fig["agg_bands"]
    mb = fig["member_bands"]
    rt = fig["routes"]
    lat = fig["lattice"]

    vb = by_id["vessel_berth"]
    cs_d = by_id["coldstore_dock"]
    ed = by_id["empty_depot"]
    rp = by_id["reefer_plug"]
    dr = by_id["drayage_carrier"]
    ph = by_id["phyto_insp"]
    rh = by_id["rail_handoff"]
    edi = by_id["edi_docs"]

    lines = []
    lines.append("## Tags")
    lines.append("")
    lines.append("**Domain:** Supply Chain & Logistics, Trade Flows (mapped to Machine Learning Research, General Statistics & Data Science: interpretability).")
    lines.append("**Analytical objective:** Root-Cause Analysis.")
    lines.append("")

    # 1. Final Recommendation
    rem_rows = [r for r in fig["causes"] if r["designation"] == "REMEDIATE"]
    mon_rows = [r for r in fig["causes"] if r["designation"] == "MONITOR"]
    rem_str = ", ".join(
        f"{r['cause_id']} ({r['cdays_2027_int']:,}" + (" c-days)" if idx == 0 else ")")
        for idx, r in enumerate(rem_rows[:-1])
    ) + f", and {rem_rows[-1]['cause_id']} ({rem_rows[-1]['cdays_2027_int']:,})"
    mon_str = ", ".join(
        f"{r['cause_id']} ({r['cdays_2027_int']:,})" for r in mon_rows[:-1]
    ) + f", and {mon_rows[-1]['cause_id']} ({mon_rows[-1]['cdays_2027_int']:,})"
    lines.append("## Final Recommendation")
    lines.append("")
    lines.append(
        f"**Release 2027 Mandatory Remediation funding under Charter RC-2027 (>= 2,500 container-days) for five causes: "
        f"{rem_str}, totaling {fig['A_remed_days']:,} remediation container-days "
        f"(EUR {fig['A_avoidable_eur_m']:.3f}M of EUR {fig['A_cost_eur_m']:.3f}M total 2027 detention and demurrage exposure), "
        f"and keep {mon_str} on Routine Monitoring.** "
        f"This rejects the direct TMS and rigorous single-system slates (vessel_berth, reefer_plug, drayage_carrier, and "
        f"rail_handoff at {rt['rigorous']['members']['rail_handoff']:,.0f} to {rt['direct']['members']['rail_handoff']:,.0f} c-days), "
        f"which omit coldstore_dock ({rt['direct']['members']['coldstore_dock']:,.0f} to {rt['rigorous']['members']['coldstore_dock']:,.0f}) "
        f"and empty_depot ({rt['direct']['members']['empty_depot']:,.0f}) by missing sealed thermal-chamber pull-backs, "
        f"post-T-24h CHED-locked empty rail wagons, and ocean-line empty-depot portal closures."
    )
    lines.append("")

    # 2. Supplementary Questions (4 multi-faceted asks grouped by file)
    lines.append("## Supplementary Questions")
    lines.append("")
    lines.append("### weserfrucht_delay_attribution_2027.csv")
    lines.append(
        "Eight rows, one per canonical operational cause sorted descending by projected 2027 excess container-days; "
        "columns cause_id, cdays_2026, cdays_2027, share_2027_pct, eur_2027, and designation (REMEDIATE or MONITOR)."
    )
    lines.append("1. Ranked 2027 projected excess container-days and 2026 attributed container-days for all eight operational causes (with 22-variant 2027 bands and Charter RC-2027 designations):")
    letters = "abcdefgh"
    for ltr, row in zip(letters, fig["causes"]):
        cid = row["cause_id"]
        b_lo, b_hi = mb[cid]
        if b_lo == b_hi:
            band_str = "exact"
        else:
            band_str = f"band {b_lo:,} to {b_hi:,}"
        lines.append(
            f"   {ltr}. {cid}: {row['cdays_2027_int']:,} c-days in 2027 ({band_str}; {row['share_2027_pct']:.2f} percent share; "
            f"EUR {row['eur_2027_m']:.3f}M), {row['cdays_2026_int']:,} c-days in 2026, {row['designation']}."
        )
    lines.append("")

    lines.append("### weserfrucht_coldchain_remediation_2027.xlsx")
    lines.append(
        "Multi-sheet formula-driven workbook opening on Remediation_Summary with the headline recommendation, live 2026-to-2027 "
        "attribution table, embedded bar chart, Critical_Components, Corridor_Q3_Breakdown, Conservation_Diagnostics, "
        "Routes_Comparison, Variant_Battery, and Inputs_Plan_2027 tabs."
    )
    lines.append("2. Total 2027 network excess container-days and designated Mandatory Remediation container-days:")
    lines.append(
        f"   a. Total 2027 network excess container-days: {fig['A_total_2027']:,} c-days "
        f"(band {ab['total_2027'][0]:,} to {ab['total_2027'][1]:,}; vs {fig['total_2026_cdays_int']:,} settled c-days in 2026)."
    )
    lines.append(
        f"   b. Total 2027 designated Mandatory Remediation container-days (five REMEDIATE causes combined): "
        f"{fig['A_remed_days']:,} c-days (band {ab['remed_days'][0]:,} to {ab['remed_days'][1]:,})."
    )
    lines.append("3. Projected 2027 detention and demurrage financial exposure under Charter RC-2027 Schedule B tariffs:")
    lines.append(
        f"   a. Total 2027 network expenditure across all eight causes: EUR {fig['A_cost_eur_m']:.3f}M "
        f"(band EUR {ab['cost_eur_m'][0]:.3f}M to EUR {ab['cost_eur_m'][1]:.3f}M)."
    )
    lines.append(
        f"   b. Avoidable 2027 expenditure across the five designated REMEDIATE causes: EUR {fig['A_avoidable_eur_m']:.3f}M "
        f"(band EUR {ab['avoidable_eur_m'][0]:.3f}M to EUR {ab['avoidable_eur_m'][1]:.3f}M)."
    )
    lines.append("4. Projected 2027 excess container-days across key port corridors and the peak third quarter (all eight causes combined):")
    lines.append(
        f"   a. Bremerhaven (BHV): {fig['A_bhv_2027']:,} c-days (band {ab['bhv_2027'][0]:,} to {ab['bhv_2027'][1]:,})."
    )
    lines.append(
        f"   b. Hamburg (HAM): {fig['A_ham_2027']:,} c-days (band {ab['ham_2027'][0]:,} to {ab['ham_2027'][1]:,})."
    )
    lines.append(
        f"   c. Third quarter (Q3, 1 July to 30 September): {fig['A_q3_2027']:,} c-days "
        f"(band {ab['q3_2027'][0]:,} to {ab['q3_2027'][1]:,})."
    )
    lines.append("")

    lines.append("### weserfrucht_remediation_review_2027.pptx")
    lines.append(
        "Seven-slide widescreen close-out review deck carrying the headline funding call, ranked 2027 cause chart against the "
        "2,500 threshold, the three native-unit physical conservation proofs, port/Q3 exposure charts, and the 2027 partner remediation plan."
    )
    lines.append("")

    # 3. Critical Components (EXACTLY 3 independent answers, NO method clause!)
    lines.append("## Critical Components")
    lines.append("")
    lines.append(
        f"1. Projected 2027 excess container-days attributable to coldstore_dock: **{cs_d['cdays_2027_int']:,} container-days** "
        f"(band **{mb['coldstore_dock'][0]:,} to {mb['coldstore_dock'][1]:,}**, designation **REMEDIATE**)."
    )
    lines.append(
        f"2. Projected 2027 excess container-days attributable to rail_handoff: **{rh['cdays_2027_int']:,} container-days** "
        f"(band **{mb['rail_handoff'][0]:,} to {mb['rail_handoff'][1]:,}**, designation **MONITOR**)."
    )
    lines.append(
        f"3. Projected 2027 excess container-days attributable to empty_depot: **{ed['cdays_2027_int']:,} container-days** "
        f"(band **{mb['empty_depot'][0]:,} to {mb['empty_depot'][1]:,}**, designation **REMEDIATE**)."
    )
    lines.append("")

    # 4. Step-by-Step
    lines.append("## Step-by-Step")
    lines.append("")
    lines.append(
        f"1. Reconciled the 2026 container lifecycle in `container_milestones_2026.csv` per Charter RC-2027 Section 2: "
        f"excluded {cl['milestones_void_dropped']} VOID test rows and {cl['milestones_superseded_dropped']} superseded version-1 rows "
        f"to obtain {cl['milestones_settled_containers']:,} settled import containers and {fig['total_2026_cdays']:,.2f} conserved excess "
        f"container-days (verified against UTC and Europe/Berlin timestamps across all eight stages to within {cl['max_timestamp_excess_err_cdays']:.5f} c-days), "
        f"setting aside unlabelled distractors `north_sea_bunker_fuel_index_2026.csv` and `german_toll_maut_rates_2026_2027.xlsx`."
    )
    lines.append(
        f"2. Evaluated the direct TMS primary stage read (`container_milestones_2026.csv`) and settled commercial credits (`carrier_dispute_closeout_2026.xlsx`) "
        f"projected via `import_plan_2027.csv`: the hurried read designates vessel_berth ({rt['direct']['members']['vessel_berth']:,.0f}), "
        f"reefer_plug ({rt['direct']['members']['reefer_plug']:,.0f}), drayage_carrier ({rt['direct']['members']['drayage_carrier']:,.0f}), "
        f"and rail_handoff ({rt['direct']['members']['rail_handoff']:,.0f}), while leaving coldstore_dock at {rt['direct']['members']['coldstore_dock']:,.0f} "
        f"and empty_depot at {rt['direct']['members']['empty_depot']:,.0f}."
    )
    lines.append(
        f"3. Cleaned `warehouse_pallet_movements_2026.csv` ({cl['pallets_raw_rows']:,} raw rows; dropped {cl['pallets_superseded_dropped']:,} "
        f"superseded EDI revisions, parsed {cl['pallets_de_date_rows']:,} European DD.MM.YYYY dates, mapped {cl['pallets_legacy_store_rows']:,} "
        f"legacy store codes via `entity_crosswalk_2026.csv`, converted {cl['pallets_case_unit_rows']:,} CASE lines via `sku_thermal_catalog.csv`) "
        f"and reconstructed daily stock-flow per (DC, thermal chamber) from `dc_chamber_register_2026.csv`, tying to `coldstore_inventory_daily_2026.csv` "
        f"with {cl['stock_flow_max_diff_pallets']} pallets error across all {cl['dc_days_total']:,} DC-days."
    )
    lines.append(
        f"4. Tested inland chamber saturation against port dwell: opposing seasonal chambers keep total DC utilization flat ({cs['total_dc_util_min_pct']:.1f} "
        f"to {cs['total_dc_util_max_pct']:.1f} percent), so a rigorous total-DC regression finds only +{d['F1_rigorous_h']:.2f} h inland effect and leaves "
        f"coldstore_dock at {rt['rigorous']['members']['coldstore_dock']:,.0f}; comparing {cs['capped_boxes_count']:,} containers facing >= 95 percent "
        f"end-of-day (EOD) destination chamber utilization on container discharge date against same-vessel unsaturated twins (< 92 percent utilization; "
        f"< 95 percent yields {d['s1_lt95_cdays_26']:,.2f} c-days and identical rounded 2027 outputs) reveals a +{d['F1_twin_gap_h']:.2f} h port-dwell jump, "
        f"reallocating {d['cs_pb_26']:,.2f} c-days in 2026 from reefer_plug to coldstore_dock (2027: coldstore_dock {cs_d['cdays_2027_int']:,}, reefer_plug {rp['cdays_2027_int']:,})."
    )
    lines.append(
        f"5. Linked `customs_consignment_bol_2026.csv` to the {cl['bip_notices_count']} CHED-lot notices in `bip_inspection_notices_2026.jsonl` "
        f"and the {fig['n_shuttles']:,} daily corridor shuttle blocks in `rail_shuttle_departures_2026.csv`: direct unsampled CHED rail sibling attribution "
        f"(netted against same-shuttle unrolled non-BIP peers) moves only {d['phyto_sibling_rail_26']:,.2f} c-days in 2026 and leaves rail_handoff at "
        f"{rt['rigorous']['members']['rail_handoff']:,.0f} (still wrongly REMEDIATE); testing booked-minus-loaded slot shortfalls against notice lead times "
        f"identifies the {d['empiric_lock_h']}-hour rail loading lock ({cs['locked_phyto_slots']} locked rail boxes)."
    )
    lines.append(
        f"6. Verified empty-wagon mass conservation on `rail_shuttle_departures_2026.csv`: regressing train_total_gross_tonnes on wagon count, booked slots, "
        f"post-24h locked slots, and non-BIP slot shortfall (booked minus loaded minus locked, measuring {d['non_bip_sf_vs_booked_t']:.2f} t vs booked and "
        f"{d['non_bip_sf_vs_loaded_t']:.2f} t vs loaded) measures {d['F2_tonnes_per_slot']:.2f} tonnes per locked slot (matching the {d['measured_reefer_tonnes']:.2f} tonne "
        f"mean loaded reefer gross mass in `customs_consignment_bol_2026.csv`, refuting 0.00 t rail resale), reallocating {d['ph_bump_26']:,.2f} standby rollover "
        f"c-days in 2026 ({d['measured_rollover_days']:.2f} c-days per box, measured as rolled {d['mean_rolled_cdays']:.4f} minus unrolled non-BIP "
        f"{d['mean_unrolled_cdays']:.4f} c-days); combining Step 5's {d['phyto_sibling_rail_26']:,.2f} direct CHED rail sibling c-days and Step 6's "
        f"{d['ph_bump_26']:,.2f} rollover c-days shifts {d['s2_total_26']:,.2f} c-days in 2026 to phyto_insp (2027: rail_handoff {rh['cdays_2027_int']:,}, phyto_insp {ph['cdays_2027_int']:,})."
    )
    lines.append(
        f"7. Reconciled `depot_turnin_log_2026.csv` ({cl['turnin_superseded_dropped']} superseded rows dropped, {cl['turnin_legacy_carrier_rows']:,} legacy "
        f"carrier codes mapped; {cl['turnin_physical_acceptance_pct']:.2f} percent physical gate acceptance across {cl['turnin_turnaway_events']} turn-aways) "
        f"against `depot_portal_requests_2026.csv` ({cs['portal_rejected_total']:,} unlinked daily rejections): contrasting {cs['closed_quota_boxes']:,} containers "
        f"unloaded on quota-closed line-days against same-DC same-day open-quota lines ({cs['s3_unpaired_boxes']} unpaired boxes fall back to the DC open-quota mean) "
        f"isolates +{d['F3_line_gap_h']:.2f} h excess empty return per box ({d['ed_blk_26']:,.2f} c-days in 2026; {cs['portal_rejected_total']:,} portal rejections "
        f"over {d['ed_blk_26']:,.2f} attributed c-days equals {d['F3_retry_mult']:.2f} rejections per attributed c-day, or {d['s3_rej_per_box']:.2f} rejections per affected "
        f"container), raising 2027 empty_depot to {ed['cdays_2027_int']:,} and reducing drayage_carrier to {dr['cdays_2027_int']:,}."
    )
    lines.append(
        f"8. Projected all eight conserved 2026 cause totals onto 2027 using the uniform Charter RC-2027 Annex C equations in `import_plan_2027.csv` "
        f"and valued exposure at Schedule B tariffs: network total reaches {fig['A_total_2027']:,} c-days (EUR {fig['A_cost_eur_m']:.3f}M), "
        f"Mandatory Remediation covers {fig['A_remed_days']:,} c-days (EUR {fig['A_avoidable_eur_m']:.3f}M across five REMEDIATE causes), "
        f"Bremerhaven totals {fig['A_bhv_2027']:,}, Hamburg totals {fig['A_ham_2027']:,}, and peak Q3 totals {fig['A_q3_2027']:,} c-days."
    )
    lines.append("")
    lines.append(
        f"No other designation survives the shipped files and Charter RC-2027. All 22 defensible estimator implementations across S1, S2, and S3 "
        f"and all eight +/-20 percent parameter perturbations preserve the identical five-cause REMEDIATE slate (minimum REMEDIATE {fig['forcing_min_remed']:,} c-days "
        f"under -20 percent baseline stress; maximum MONITOR {fig['forcing_max_monitor']:,} c-days under +20 percent BIP stress). Every shortcut and over-correction is "
        f"refuted directly in native physical units: dropping S1 alone leaves coldstore_dock at {lat['S1']['members']['coldstore_dock']:,.0f} (MONITOR, "
        f"refuted by the +{d['F1_twin_gap_h']:.2f} h same-vessel twin jump); dropping S2 alone leaves rail_handoff at {lat['S2']['members']['rail_handoff']:,.0f} "
        f"(REMEDIATE, refuted by the {d['F2_tonnes_per_slot']:.2f} t/slot weighbridge deficit); dropping S3 alone leaves empty_depot at "
        f"{lat['S3']['members']['empty_depot']:,.0f} (MONITOR, refuted by the +{d['F3_line_gap_h']:.2f} h same-DC line contrast); "
        f"while unnetted over-corrections wrongly drop reefer_plug to {rt['S1_over']['members']['reefer_plug']:,.0f} (S1-over), "
        f"push phyto_insp to {rt['S2_over']['members']['phyto_insp']:,.0f} (S2-over), or drop drayage_carrier to "
        f"{rt['S3_over']['members']['drayage_carrier']:,.0f} (S3-over, ignoring {d['F3_retry_mult']:.2f}x retry multiplicity), and "
        f"using unprojected 2026 actuals wrongly leaves empty_depot at {ed['cdays_2026_int']:,} (MONITOR). Dropping pairs keeps both missed members wrong "
        f"(S1+S2 dropped: coldstore_dock {lat['S1+S2']['members']['coldstore_dock']:,.0f}, rail_handoff {lat['S1+S2']['members']['rail_handoff']:,.0f}; "
        f"S1+S3 dropped: coldstore_dock {lat['S1+S3']['members']['coldstore_dock']:,.0f}, empty_depot {lat['S1+S3']['members']['empty_depot']:,.0f}; "
        f"S2+S3 dropped: rail_handoff {lat['S2+S3']['members']['rail_handoff']:,.0f}, empty_depot {lat['S2+S3']['members']['empty_depot']:,.0f}), "
        f"confirming all three decisive steps are strictly independent."
    )

    txt = "\n".join(lines) + "\n"
    assert "\u2014" not in txt and "\u2013" not in txt, "Em/en dash found in submission.md!"
    out_path = os.path.join(TASK_DIR, "submission.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(txt)
    return out_path


if __name__ == "__main__":
    p = render()
    print("Wrote", p)
