## Tags

**Domain:** Supply Chain & Logistics, Trade Flows (mapped to Machine Learning Research, General Statistics & Data Science: interpretability).
**Analytical objective:** Root-Cause Analysis.

## Final Recommendation

**Release 2027 Mandatory Remediation funding under Charter RC-2027 (>= 2,500 container-days) for five causes: vessel_berth (4,530 c-days), coldstore_dock (3,367), drayage_carrier (3,213), reefer_plug (3,150), and empty_depot (3,053), totaling 17,313 remediation container-days (EUR 3.721M of EUR 4.693M total 2027 detention and demurrage exposure), and keep phyto_insp (2,058), rail_handoff (1,734), and edi_docs (957) on Routine Monitoring.** This rejects the direct TMS and rigorous single-system slates (vessel_berth, reefer_plug, drayage_carrier, and rail_handoff at 2,620 to 2,797 c-days), which omit coldstore_dock (1,357 to 1,986) and empty_depot (947) by missing sealed thermal-chamber pull-backs, post-T-24h CHED-locked empty rail wagons, and ocean-line empty-depot portal closures.

## Supplementary Questions

### weserfrucht_delay_attribution_2027.csv
Eight rows, one per canonical operational cause sorted descending by projected 2027 excess container-days; columns cause_id, cdays_2026, cdays_2027, share_2027_pct, eur_2027, and designation (REMEDIATE or MONITOR).
1. Ranked 2027 projected excess container-days and 2026 attributed container-days for all eight operational causes (with 22-variant 2027 bands and Charter RC-2027 designations):
   a. vessel_berth: 4,530 c-days in 2027 (exact; 20.53 percent share; EUR 0.883M), 4,107 c-days in 2026, REMEDIATE.
   b. coldstore_dock: 3,367 c-days in 2027 (band 3,086 to 3,386; 15.26 percent share; EUR 0.959M), 2,732 c-days in 2026, REMEDIATE.
   c. drayage_carrier: 3,213 c-days in 2027 (band 3,167 to 3,240; 14.56 percent share; EUR 0.514M), 3,324 c-days in 2026, REMEDIATE.
   d. reefer_plug: 3,150 c-days in 2027 (band 3,135 to 3,385; 14.28 percent share; EUR 0.661M), 3,284 c-days in 2026, REMEDIATE.
   e. empty_depot: 3,053 c-days in 2027 (band 3,015 to 3,125; 13.84 percent share; EUR 0.702M), 2,006 c-days in 2026, REMEDIATE.
   f. phyto_insp: 2,058 c-days in 2027 (band 1,940 to 2,208; 9.33 percent share; EUR 0.535M), 1,514 c-days in 2026, MONITOR.
   g. rail_handoff: 1,734 c-days in 2027 (band 1,628 to 1,819; 7.86 percent share; EUR 0.303M), 1,875 c-days in 2026, MONITOR.
   h. edi_docs: 957 c-days in 2027 (exact; 4.34 percent share; EUR 0.134M), 870 c-days in 2026, MONITOR.

### weserfrucht_coldchain_remediation_2027.xlsx
Multi-sheet formula-driven workbook opening on Remediation_Summary with the headline recommendation, live 2026-to-2027 attribution table, embedded bar chart, Critical_Components, Corridor_Q3_Breakdown, Conservation_Diagnostics, Routes_Comparison, Variant_Battery, and Inputs_Plan_2027 tabs.
2. Total 2027 network excess container-days and designated Mandatory Remediation container-days:
   a. Total 2027 network excess container-days: 22,062 c-days (band 22,001 to 22,131; vs 19,713 settled c-days in 2026).
   b. Total 2027 designated Mandatory Remediation container-days (five REMEDIATE causes combined): 17,313 c-days (band 17,252 to 17,354).
3. Projected 2027 detention and demurrage financial exposure under Charter RC-2027 Schedule B tariffs:
   a. Total 2027 network expenditure across all eight causes: EUR 4.693M (band EUR 4.654M to EUR 4.725M).
   b. Avoidable 2027 expenditure across the five designated REMEDIATE causes: EUR 3.721M (band EUR 3.681M to EUR 3.739M).
4. Projected 2027 excess container-days across key port corridors and the peak third quarter (all eight causes combined):
   a. Bremerhaven (BHV): 10,647 c-days (band 10,599 to 10,704).
   b. Hamburg (HAM): 8,216 c-days (band 8,187 to 8,252).
   c. Third quarter (Q3, 1 July to 30 September): 8,580 c-days (band 8,547 to 8,686).

### weserfrucht_remediation_review_2027.pptx
Seven-slide widescreen close-out review deck carrying the headline funding call, ranked 2027 cause chart against the 2,500 threshold, the three native-unit physical conservation proofs, port/Q3 exposure charts, and the 2027 partner remediation plan.

## Critical Components

1. Projected 2027 excess container-days attributable to coldstore_dock: **3,367 container-days** (band **3,086 to 3,386**, designation **REMEDIATE**).
2. Projected 2027 excess container-days attributable to rail_handoff: **1,734 container-days** (band **1,628 to 1,819**, designation **MONITOR**).
3. Projected 2027 excess container-days attributable to empty_depot: **3,053 container-days** (band **3,015 to 3,125**, designation **REMEDIATE**).

## Step-by-Step

1. Reconciled the 2026 container lifecycle in `container_milestones_2026.csv` per Charter RC-2027 Section 2: excluded 190 VOID test rows and 305 superseded version-1 rows to obtain 24,000 settled import containers and 19,712.53 conserved excess container-days (verified against UTC and Europe/Berlin timestamps across all eight stages to within 0.00001 c-days), setting aside unlabelled distractors `north_sea_bunker_fuel_index_2026.csv` and `german_toll_maut_rates_2026_2027.xlsx`.
2. Evaluated the direct TMS primary stage read (`container_milestones_2026.csv`) and settled commercial credits (`carrier_dispute_closeout_2026.xlsx`) projected via `import_plan_2027.csv`: the hurried read designates vessel_berth (4,530), reefer_plug (4,754), drayage_carrier (4,411), and rail_handoff (2,797), while leaving coldstore_dock at 1,357 and empty_depot at 947.
3. Cleaned `warehouse_pallet_movements_2026.csv` (179,544 raw rows; dropped 4,260 superseded EDI revisions, parsed 66,670 European DD.MM.YYYY dates, mapped 21,622 legacy store codes via `entity_crosswalk_2026.csv`, converted 61,598 CASE lines via `sku_thermal_catalog.csv`) and reconstructed daily stock-flow per (DC, thermal chamber) from `dc_chamber_register_2026.csv`, tying to `coldstore_inventory_daily_2026.csv` with 0 pallets error across all 1,460 DC-days.
4. Tested inland chamber saturation against port dwell: opposing seasonal chambers keep total DC utilization flat (69.0 to 79.0 percent), so a rigorous total-DC regression finds only +0.52 h inland effect and leaves coldstore_dock at 1,986; comparing 1,930 containers facing >= 95 percent end-of-day (EOD) destination chamber utilization on container discharge date against same-vessel unsaturated twins (< 92 percent utilization; < 95 percent yields 1,616.34 c-days and identical rounded 2027 outputs) reveals a +20.10 h port-dwell jump, reallocating 1,616.67 c-days in 2026 from reefer_plug to coldstore_dock (2027: coldstore_dock 3,367, reefer_plug 3,150).
5. Linked `customs_consignment_bol_2026.csv` to the 309 CHED-lot notices in `bip_inspection_notices_2026.jsonl` and the 1,095 daily corridor shuttle blocks in `rail_shuttle_departures_2026.csv`: direct unsampled CHED rail sibling attribution (netted against same-shuttle unrolled non-BIP peers) moves only 191.39 c-days in 2026 and leaves rail_handoff at 2,620 (still wrongly REMEDIATE); testing booked-minus-loaded slot shortfalls against notice lead times identifies the 24-hour rail loading lock (426 locked rail boxes).
6. Verified empty-wagon mass conservation on `rail_shuttle_departures_2026.csv`: regressing train_total_gross_tonnes on wagon count, booked slots, post-24h locked slots, and non-BIP slot shortfall (booked minus loaded minus locked, measuring -3.15 t vs booked and 0.65 t vs loaded) measures -28.01 tonnes per locked slot (matching the 28.52 tonne mean loaded reefer gross mass in `customs_consignment_bol_2026.csv`, refuting 0.00 t rail resale), reallocating 958.50 standby rollover c-days in 2026 (2.25 c-days per box, measured as rolled 2.2717 minus unrolled non-BIP 0.0214 c-days); combining Step 5's 191.39 direct CHED rail sibling c-days and Step 6's 958.50 rollover c-days shifts 1,149.89 c-days in 2026 to phyto_insp (2027: rail_handoff 1,734, phyto_insp 2,058).
7. Reconciled `depot_turnin_log_2026.csv` (433 superseded rows dropped, 5,590 legacy carrier codes mapped; 96.51 percent physical gate acceptance across 869 turn-aways) against `depot_portal_requests_2026.csv` (5,273 unlinked daily rejections): contrasting 2,809 containers unloaded on quota-closed line-days against same-DC same-day open-quota lines (25 unpaired boxes fall back to the DC open-quota mean) isolates +10.61 h excess empty return per box (1,242.01 c-days in 2026; 5,273 portal rejections over 1,242.01 attributed c-days equals 4.25 rejections per attributed c-day, or 1.88 rejections per affected container), raising 2027 empty_depot to 3,053 and reducing drayage_carrier to 3,213.
8. Projected all eight conserved 2026 cause totals onto 2027 using the uniform Charter RC-2027 Annex C equations in `import_plan_2027.csv` and valued exposure at Schedule B tariffs: network total reaches 22,062 c-days (EUR 4.693M), Mandatory Remediation covers 17,313 c-days (EUR 3.721M across five REMEDIATE causes), Bremerhaven totals 10,647, Hamburg totals 8,216, and peak Q3 totals 8,580 c-days.

No other designation survives the shipped files and Charter RC-2027. All 22 defensible estimator implementations across S1, S2, and S3 and all eight +/-20 percent parameter perturbations preserve the identical five-cause REMEDIATE slate (minimum REMEDIATE 2,520 c-days under -20 percent baseline stress; maximum MONITOR 2,318 c-days under +20 percent BIP stress). Every shortcut and over-correction is refuted directly in native physical units: dropping S1 alone leaves coldstore_dock at 1,357 (MONITOR, refuted by the +20.10 h same-vessel twin jump); dropping S2 alone leaves rail_handoff at 2,797 (REMEDIATE, refuted by the -28.01 t/slot weighbridge deficit); dropping S3 alone leaves empty_depot at 947 (MONITOR, refuted by the +10.61 h same-DC line contrast); while unnetted over-corrections wrongly drop reefer_plug to 1,895 (S1-over), push phyto_insp to 3,186 (S2-over), or drop drayage_carrier to 1,916 (S3-over, ignoring 4.25x retry multiplicity), and using unprojected 2026 actuals wrongly leaves empty_depot at 2,006 (MONITOR). Dropping pairs keeps both missed members wrong (S1+S2 dropped: coldstore_dock 1,357, rail_handoff 2,797; S1+S3 dropped: coldstore_dock 1,357, empty_depot 947; S2+S3 dropped: rail_handoff 2,797, empty_depot 947), confirming all three decisive steps are strictly independent.
