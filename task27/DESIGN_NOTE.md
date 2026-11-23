# task27: Allocating Weserfrucht Import GmbH's EUR 1.75M 2027 Carrier-Remediation Capital Budget Across Six North Sea Port-to-DC Import Corridors

## Draw

Subdomain: Trade Flows
Analysis type: Root-Cause
Answer shape: A ranked list under a cap (ranked-list-cap: corridor remediation slate under a EUR 1,750,000 fixed capital cap, backed by per-corridor Benefit-Cost Ratios and separated 2026 non-carrier bottleneck attributions)
Weight: allocation (estimating six coupled corridor Benefit-Cost Ratios under a EUR 1,750,000 fixed 2027 capital cap via three open-book econometric separation models; differs from recent builds task9 in interpretability/decomposition, task28 in anomaly-detection/model-selection, and task26 in distribution-losses/etl)
Data-native sentence: Every corridor's 2027 Benefit-Cost Ratio combines three carrier-controllable delay channels whose primary TMS stage logs mingle carrier bottlenecks with three disclosed non-carrier processes (asymmetric filling-vs-draining inland chamber pull-backs, terminal-varying stochastic BIP rail booking locks overlapping Nordbahn short-consist cuts, and multi-day ocean-line empty-depot return backlogs scaled by inland haul distance) that must each be modeled jointly at separate operational grains before ranking corridors under the capital cap.
People: Friedhilde Naser, Hilma Hofmann, Vanessa Hörle, Hans-Peter Briemer, Carmelo Hermighausen, Mariechen Reuter, Meinhard Herrmann, Pero Kusch

## Stump screen

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| Asymmetric convex cold-store chamber pull-back hidden inside TERM_YARD_HOLD while opposing produce seasons hold aggregate DC occupancy flat at 69-78% | Aggregate warehouse occupancy checks (~74% flat) or symmetric linear / binary >=92% chamber thresholds capture DC yard throttling equally on filling and draining days (L26, L28, L38, N36) | warehouse_pallet_movements_2026.csv + dc_chamber_catalog.csv reconstructed to daily (DC, zone) stock and net flow (pallet_in - pallet_out) paired with same-vessel container_milestones_2026.csv | none | kept (S1) |
| Terminal-varying smooth logistic BIP rail booking locks (BHV ~16h, HAM ~28h, WHV ~12h, stochastic pass-through ~0.66) overlapping correlated peak-day Nordbahn short-consist and locomotive-derate cuts on every-3-day block trains | Pooled TMS RAIL_HANDOFF logs, direct CHED sibling tags, fixed-24h bivariate BIP regressions omitting consist_wagons_short and loco_derate, or attributing entire BIP-present shuttles to phyto_insp accurately isolate carrier rail shortfalls (L03, L07, L48, N07) | bip_phyto_notices_2026.csv (continuous Gamma lead hours) joined to rail_shuttle_departures_2026.csv (consist_wagons_short, loco_derate_events, wf_standby_rolled, train_gross_tonnes) | none | kept (S2) |
| Conserved (port, shipping_line) empty-depot queue stock that accumulates during 3-4 day episodic portal closures and persists across 5-7 subsequent OPEN drain days scaled linearly by corridor haul distance | Unload-day binary portal_rejected > 0 flags, raw TMS DRAYAGE_TURNAROUND logs, or port-level aggregated depot queues (ignoring shipping-line isolation) correctly separate ocean-line depot blocking from carrier drayage turnaround (N14, N27, L56, L57) | empty_depot_portal_log_2026.csv (daily port x shipping_line gate-ins and rejections) combined with container_milestones_2026.csv daily inland unloads by exact stock-flow conservation cumsum(unloads - gate_ins) / mean_daily_unloads | none | kept (S3) |
| Vessel berth arrival slippage vs terminal crane turnaround inside VESSEL_BERTH | Berth delay is already outside the three carrier-controllable corridor remediation channels under Charter Clause 2.2 | port_berth_calls_2026.csv | fails test 9 (worth 0; excluded from remediation scope) | dropped |
| EDI customs clearance dwell inside EDI_DOCS | Routine EDI clearance dwell is small and stable across corridors | customs_edi_clearance_2026.csv | fails test 9 (worth 0; excluded from remediation scope) | dropped |

## Deep reasoning

Task type: interpretability and root-cause driver attribution for capital remediation allocation across port-to-hinterland refrigerated trade corridors
Domain test: The quantities are physical cold-chain container-days, daily sealed thermal-chamber pallet stocks (+2C berries/leafy, +7C citrus/stone fruit, +13C tropicals), every-3-day block-train wagon shortfalls and phytosanitary border-inspection lock windows, daily ocean-line empty-container queue stocks in days of flow, and projected 2027 Schedule B detention and demurrage EUR per EUR of corridor remediation capital. A cold-chain logistics analyst reconciles all operational logs onto one 24,000-container lifecycle spine, fits the three physical attribution models, validates residual orthogonality and genuine carrier-slope preservation across clean vs overlap regimes, projects 2027 corridor avoidable carrier-controllable EUR, and ranks the six corridors under the EUR 1,750,000 cap.
Swap: Replacing North Sea port-to-DC refrigerated import corridors with hospital outpatient clinics or retail ad campaigns breaks sealed multi-temperature pallet stock conservation, intermodal block-train booking-lock cutoffs versus locomotive derates and consist shortfalls, and ocean shipping-line empty-box return depot queues outliving booking-portal closures.
Where the weight sits: The weight sits in jointly building and validating the three econometric separation models across six interdependent corridors (R2, R3, R4, R6) so that every corridor's projected 2027 Benefit-Cost Ratio reflects true carrier-controllable exposure across reefer plugs, rail handoff, and road drayage without under-subtracting or over-subtracting any non-carrier channel.
Layer 1: (1) mixed German DD.MM.YYYY and ISO YYYY-MM-DD dates from port EDI vs warehouse WMS; (2) duplicate nightly warehouse pallet EDI transmissions with revision numbers requiring latest-revision deduplication; (3) UTC terminal/rail timestamps versus CET inland DC gate timestamps; (4) legacy facility and carrier code mappings in entity_crosswalk.csv; (5) case-to-pallet conversion factors in sku_thermal_catalog.csv; (6) two unlabelled distractor files (north_sea_bunker_index_2026.csv and german_maut_toll_schedule_2026.csv). Every Layer 1 mess is neutral across corridors and changes no ranking on its own.
Not one thing: The strongest single mechanism is S1 (asymmetric convex chamber pull-back, C1 = 7,436.9 c-days, worth 0.944 BCR on BHV-KAS); a run that nails S1 completely from the reflex baseline still misses S2 (HAM-MAG stays inflated at 1.929) and S3 (BHV-HAN stays inflated at 1.773), filing the wrong slate and scoring only 18 on the v4-ECF rubric (16 on the house rubric).
One-fact test: All three mechanisms are already disclosed openly in Charter RC-2027 Rev 3 without hiding rules or catches; giving a run any single-sentence rule-of-thumb shortcut (e.g. subtract yard hold above 92% chamber load, regress rail rolls on 24h BIP counts, or flag unload days with portal rejections) fails both the funding slate and that mechanism's own critical component, and even fixing one entire mechanism from reflex lifts v4-ECF score from 7 to 18 (+11, rescuing 1 of 9 graded figures).
Not semantics: Reading every column header, tariff, Charter clause, and unit correctly still leaves raw TMS stage totals, aggregate DC occupancy checks, symmetric linear fits, bivariate BIP regressions, and binary portal flags completely wrong on both sides of the top-3 budget cap.
Not rule application: Charter RC-2027 Rev 3 pins the estimands, EUR 1,750,000 budget cap, corridor ranking by BCR, Schedule B tariffs, Annex C 2027 growth/capacity factors, and cause scope (reefer_plug, rail_handoff, drayage_carrier are carrier-controllable; coldstore_dock, phyto_insp, empty_depot are non-carrier), and openly describes all three physical overlap mechanisms, while intentionally leaving the statistical estimation functional forms, fixed-effect structures, port lock cutoffs, and queue-state models to the analyst's empirical judgment on the 2026 logs.
Estimand: Charter RC-2027 Rev 3 Section 2 defines carrier-controllable 2026 excess container-days per corridor as attributed reefer_plug + rail_handoff + drayage_carrier across all 24,000 final-revision settled 2026 import containers, excluding inland cold-store pull-back (coldstore_dock), border-inspection holds and BIP-induced rail rollovers (phyto_insp), and ocean-line empty-depot return backlogs (empty_depot). Section 3 defines projected 2027 corridor avoidable carrier-controllable EUR using corridor volume growth, port-level 2027 capacity factors, Schedule B tariffs (EUR 210/d plug, EUR 175/d rail, EUR 160/d drayage), and each corridor's published capture rate. Section 4 defines corridor BCR = projected 2027 avoidable carrier-controllable EUR / corridor remediation budget EUR and funds corridors in descending BCR order within the EUR 1,750,000 cap (matching exact integer knapsack).
No decoy: Zero documents state a wrong figure or argue a wrong ranking; carrier_dispute_closeout_2026.csv and dc_aggregate_occupancy_2026.csv reconcile accurately to their own narrower scopes (billed dispute settlements and whole-building daily pallet totals) and never fabricate errors.
No replay: No shipped document contains any pre-computed corridor BCR, 2027 avoidable EUR, or separated C1/C2/C3 attribution figure.
Pinned: Across 21 honest modeling variants spanning functional forms, fixed effects, Huber robust regression, Poisson IRLS, non-parametric lead bins, harmonic seasonality, and booked-slot controls, all 21 variants file the identical funding slate (WHV-OSN, BHV-OSN, HAM-HAN) and bound every graded figure within tight data-driven bands, while all shortcuts and over-corrections are refuted by two-sided observable residual orthogonality and genuine carrier-slope preservation checks (golden error 36.2 vs rivals 301 to 1,730).
Run forecast: R2 (method shortcut / self-confirming check on aggregate DC util or symmetric linear cut); R3 (method shortcut / narrow look on fixed-24h bivariate BIP count omitting short-consist confounders); R4 (unfinished chain / first story on unload-day binary portal_rejected > 0 ignoring multi-day conserved queue drain tails); R6 and R7 (downstream cascade from missing any one of R2, R3, or R4 across coupled corridor BCRs).
Strategy label: own (open-book three-mechanism corridor capital allocation off all 45 closed strategies)
Depth level: 5 (three independent modeling judgments on distinct axes what/unit/when, each opening a different false-alarm corridor across the top-3 budget cap, producing 7 distinct wrong slates across all 7 non-empty lattice drops, and all 3 passing coded two-sided and one-fact catch checks).
Lesson: Jointly modeling non-linear asymmetric state hysteresis, confounded multi-driver shared-group count events with terminal-varying cutoffs, and stock-flow queue persistence outliving source outages inside a coupled multi-corridor capital allocation problem; no build on file or in the client library teaches this skeleton (skeleton.py check severity none; 0 of 4 lessons closed).

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | Reconciled 2026 lifecycle spine (24,000 containers across 6 corridors, 480 vessels, 732 rail block trains, 4 DCs, 4 ocean lines) and exact daily chamber/depot stock-flow series | Assembly & Reconciliation | Exact ledger deduplication, unit conversion, and stock-flow conservation | exact | Unfinished chain: stops at aggregate DC occupancy (69-78%) or raw portal rejection tallies without building chamber net flow and queue stock | - | supporting (checked via R2-R4) |
| R2 | 2026 inland cold-store pull-back attribution C1 = 7,436.9 c-days (separating asymmetric convex filling-vs-draining chamber hysteresis from carrier reefer_plug) | Modeling | 21-variant honest family (vessel/port-day/corr-week FE; quadratic/spline/binned/Huber; hinge 0.76-0.80) | 7,173 to 7,644 c-days | Method shortcut / self-confirming check: verifies flat aggregate DC util (0 c-days), applies binary >=92% cut (4,460 c-days), or fits symmetric linear slope | R1 | Component 1 (`C1_coldstore_pullback_2026`) |
| R3 | 2026 BIP-induced rail rollover attribution C2 = 4,304.4 c-days (jointly separating terminal-varying smooth BIP lock cutoffs BHV ~16h / HAM ~28h / WHV ~12h from overlapping Nordbahn short-consist & loco-derate cuts) | Causal Reasoning | 21-variant honest family (smooth logistic / hard step / binned lead / Poisson IRLS / Huber / month+corr FE / pooled slope / booked-slot ctrl) | 4,086 to 4,436 c-days | Dismissed own evidence: treats raw rail rolls as carrier (0 c-days), runs bivariate fixed-24h BIP OLS omitting consist cuts (6,861 c-days), or attributes all BIP-present shuttles to phyto | R1 | Component 2 (`C2_phyto_rail_roll_2026`) |
| R4 | 2026 ocean-line empty-depot backlog attribution C3 = 7,171.5 c-days (conserved port x shipping_line queue stock across open-portal drain tails scaled by corridor distance) | Investigation Loops | 21-variant honest family (dc-week / dc-day / port-day / corr-week FE; harmonic OLS; Huber; linear / distance-parametric) | 6,742 to 7,280 c-days | Method shortcut / dismissed own evidence: ignores unlinked portal log (0 c-days), flags only binary unload-day rejections (3,723 c-days), or aggregates queue across shipping lines at port level | R1 | Component 3 (`C3_depot_backlog_2026`) |
| R5 | Observable two-sided physical validation diagnostic (residual orthogonality + genuine carrier-slope preservation across all 3 mechanisms: golden 36.2 vs rivals 301 to 1,730) | Validation | Parameter-free observable residual tests on shipped logs | golden <= 100 (exact 36.2) | Self-confirming check: tests only aggregate DC occupancy or bivariate shuttle correlation | R2, R3, R4 | supporting (evidence in deck & Step-by-Step) |
| R6 | Coupled 2027 projected corridor carrier-controllable avoidable EUR and Benefit-Cost Ratios for all 6 corridors (WHV-OSN 1.139, BHV-OSN 1.100, HAM-HAN 1.086, HAM-MAG 0.988, BHV-HAN 0.949, BHV-KAS 0.901) | Forecasting | Charter RC-2027 Rev 3 Section 3 factors, Schedule B tariffs, corridor capture rates, and 21-variant family bands | WHV-OSN 1.109-1.159; BHV-OSN 1.084-1.124; HAM-HAN 1.073-1.114; HAM-MAG 0.974-1.020; BHV-HAN 0.920-1.061; BHV-KAS 0.886-0.920 | Unfinished chain: projects unseparated TMS logs (BHV-KAS 2.176, HAM-MAG 2.136, BHV-HAN 2.012) or partially corrected channels | R2, R3, R4 | Ask 1-6 (`BCR_BHV_HAN`..`BCR_WHV_OSN`) |
| R7 | 2027 EUR 1,750,000 capital remediation slate: FUND WHV-OSN (EUR 560k), BHV-OSN (EUR 560k), HAM-HAN (EUR 585k) [EUR 1,705,000 deployed, EUR 1,889,237 avoidable, BCR 1.108]; DEFER HAM-MAG, BHV-HAN, BHV-KAS | Synthesis | Exact descending BCR ranking under EUR 1,750,000 cap (equals integer knapsack optimum); 21/21 variants and 8/8 +/-15% stresses hold | exact set (WHV-OSN, BHV-OSN, HAM-HAN) | Method shortcut: funds naive top-3 (BHV-HAN, BHV-KAS, HAM-MAG) or single-stump-dropped wrong slates | R5, R6 | Final Recommendation |

Carry-forward: Every non-ECF ask figure (all 6 of 6 corridor BCRs, 100% coupled) shifts outside its band under 2 or 3 independent stumps (`BCR_BHV_HAN` under S1 & S3; `BCR_BHV_KAS`, `BCR_BHV_OSN`, `BCR_HAM_HAN`, `BCR_HAM_MAG`, `BCR_WHV_OSN` under all three S1, S2, and S3). Each stump exclusively owns one independent critical component (`C1_coldstore_pullback_2026` by S1, `C2_phyto_rail_roll_2026` by S2, `C3_depot_backlog_2026` by S3).

## Hidden factor record

No hidden factor: Charter RC-2027 Rev 3 openly discloses all three operational attribution mechanisms (asymmetric chamber filling-vs-draining pull-back, terminal-varying BIP rail booking locks overlapping Nordbahn consist cuts, and multi-day ocean-line empty-depot return backlogs) in plain business terms; there are no planted defects, hidden clauses, dead zones, or synthetic catches. Difficulty comes entirely from empirically modeling all three mechanisms accurately across multi-grain operational logs.

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 Reconciled 2026 spine & stock-flow series | Missed | Right | Right |
| R2 C1_coldstore_pullback_2026 | Missed | Missed | Right |
| R3 C2_phyto_rail_roll_2026 | Missed | Missed | Right |
| R4 C3_depot_backlog_2026 | Missed | Missed | Right |
| R5 Observable residual validation | Missed | Missed | Right |
| R6 Six coupled 2027 corridor BCRs | Missed | Missed | Right |
| R7 EUR 1.75M capital remediation slate | Missed | Missed | Right |
| Roughly | 0 of 7 | 1 of 7 | 7 of 7 |

Measured by: .agents/skills/stumping/effort.py on generator/effort.json
Largest single hint: Fixing one complete mechanism (e.g. asymmetric chamber hysteresis C1) from the reflex baseline; rescues 1 of 9 graded figures (lifts v4-ECF score from 7 to 18, house score from 9 to 16)
Pair estimate: 25.3 (measured by effort.py; 7 on v4-ECF rubric / 9 on corelib house rubric for reflex baseline; 30/37/30 v4-ECF if any single stump is missed)

## Stump core

Unobserved part: The true per-container and per-shuttle split between carrier-controllable excess days (reefer_plug, rail_handoff, drayage_carrier) and non-carrier operational bottlenecks (coldstore_dock pull-back, phyto_insp rail rollovers, empty_depot queue backlogs) is never recorded in any single file; TMS records only combined stage timers (`term_yard_hold_cdays`, `rail_excess_cdays`, `dray_empty_hold_cdays`).
Instruments: (1) `container_milestones_2026.csv` observes combined stage delays at container grain but never flags chamber pull-back, BIP-caused vs consist-caused rail rollovers, or open-day depot queue drag (read raw, it funds BHV-HAN, BHV-KAS, HAM-MAG at BCRs 2.012-2.176); (2) `warehouse_pallet_movements_2026.csv` observes daily SKU-level pallet in/out movements per DC and thermal zone while `dc_aggregate_occupancy_2026.csv` shows flat 69-78% whole-DC utilization; (3) `bip_phyto_notices_2026.csv` observes continuous Gamma inspection notice lead times while `rail_shuttle_departures_2026.csv` observes combined shuttle standby rollovers alongside `consist_wagons_short`, `loco_derate_events`, and noisy `train_gross_tonnes`; (4) `empty_depot_portal_log_2026.csv` observes daily `(port, shipping_line)` confirmed gate-ins and closure rejections without container IDs.
Referee: Observable two-sided physical residual orthogonality and genuine carrier-slope preservation diagnostic (`fal_err`, `observes_target: False`): golden error = 36.2, whereas every rival fails by 8x to 48x (`S1_one_fact` 301, `S2_one_fact` 554, `S3_one_fact` 803, `generous` 919, `hedge` 1,420, `rigorous` 1,560, `direct` 1,680, `cutoff` 1,730). No calibration slice directly reveals the unobserved target split.
Strongest standard route: Per open member, the rigorous standard route runs aggregate DC utilization > 78% with vessel fixed effects (finds ~0 because opposing produce seasons keep total DC utilization flat in 69-78%), removes only direct CHED sibling rail holds (leaves all 4,304 c-days of BIP-induced standby rollovers in rail_handoff), and sets aside unlinked portal rejections (leaves all 7,171 c-days of depot queue backlog in drayage_carrier); it files BHV-KAS 2.158, HAM-MAG 2.039, BHV-HAN 1.990 (exact wrong top-3) and fails `fal_err` at 1,560 vs golden 36.2.
Said out loud: (S1) "inland DC thermal chambers pull back containers at the port yard more steeply when filling than when draining" -> 4 dependent steps remain (reconstruct sealed chamber daily stocks and net flows from SKU pallet movements, fit asymmetric convex filling-vs-draining within-vessel FE response, apply proportional Gamma posterior sharing per container, propagate across 2027 corridor BCRs); (S2) "late EU BIP inspection notices lock booked rail slots with terminal-specific cutoffs and overlap Nordbahn short-consist cuts" -> 4 dependent steps remain (estimate port-specific smooth booking-lock cutoffs from continuous lead times, run joint multivariate shuttle count model controlling for consist_wagons_short and loco_derate, compute Poisson-thinning posterior rollover share, propagate across 2027 corridor BCRs); (S3) "ocean-line empty-depot portal closures build multi-day return queues that outlive portal reopening across inland corridors" -> 4 dependent steps remain (reconstruct exact physical queue stock per port x shipping_line from daily unloads minus gate-ins, normalize in days of flow, estimate corridor-varying fixed-effects delay slope across open drain days, propagate with proportional posterior sharing into 2027 corridor BCRs).
Worth: S1 worth 0.944 BCR on BHV-KAS = 72.2x honest family spread (0.0131), band 0.886 to 0.920; S2 worth 0.732 BCR on HAM-MAG = 30.5x family spread (0.0240), band 0.974 to 1.020; S3 worth 0.746 BCR on BHV-HAN = 8.4x family spread (0.0891), band 0.920 to 1.061.
Regimes: Three independent stumps each open a distinct false-alarm corridor and protect a distinct channel-dominant winner: S1 opens BHV-KAS (filling-heavy DC) while over-correction crashes BHV-OSN (draining-heavy plug-dominant winner); S2 opens HAM-MAG (late-notice BIP-heavy) while over-correction or bivariate 24h shortcuts crash HAM-HAN (early-notice BIP, rail-dominant winner); S3 opens BHV-HAN (96% LINE_A/B) while port-aggregated over-correction crashes WHV-OSN (drayage-dominant winner).
Sharp: (S1) wrong route passes whole-DC occupancy check and binary 92% cut; right route commits to chamber-level net-flow sign hysteresis + convexity; evidence in `warehouse_pallet_movements_2026.csv`; differs across KAS (82% filling) vs OSN (90% draining); owns `C1_coldstore_pullback_2026`. (S2) wrong route passes direct CHED sibling removal and bivariate 24h BIP regression; right route commits to port-specific lock cutoffs + multivariate control for correlated Nordbahn short-consist & loco cuts; evidence in `bip_phyto_notices_2026.csv` + `rail_shuttle_departures_2026.csv`; differs across HAM (~28h lock, high BIP on HAM-MAG vs early BIP + high short-consist on HAM-HAN) vs BHV (~16h) vs WHV (~12h); owns `C2_phyto_rail_roll_2026`. (S3) wrong route passes unload-day binary portal_rejected flag or port-level queue cut; right route commits to conserved `(port, shipping_line)` queue stock outliving portal reopening scaled by corridor haul distance; evidence in `empty_depot_portal_log_2026.csv`; differs across BHV-HAN (96% quota-constrained lines) vs WHV-OSN (73% unconstrained LINE_C/D); owns `C3_depot_backlog_2026`.
Earns: From `core.py` (21 variants): S1 lost alone = 30 v4-ECF (22 house), S2 lost alone = 37 v4-ECF (31 house), S3 lost alone = 30 v4-ECF (22 house); S1/S2/S3 fixed alone = 18/18/18 v4-ECF (16/16/16 house); reflex = 7 v4-ECF (9 house); rigorous = 7 (9); cutoff = 14 (18); generous = 7 (9); hedge = 7 (9). Zero graded figures land on the reflex route.

| Member | Line | Golden | Family spread | Reflex route | Direct | Rigorous | Opened by |
|---|---|---|---|---|---|---|---|
| BHV-HAN | top-k | 0.9487 | 0.0891 | 2.012 | 2.012 | 1.99 | S3 |
| BHV-KAS | top-k | 0.9011 | 0.0131 | 2.176 | 2.176 | 2.158 | S1 |
| BHV-OSN | top-k | 1.1 | 0.0169 | 1.761 | 1.761 | 1.745 | forced |
| HAM-HAN | top-k | 1.086 | 0.0215 | 1.839 | 1.839 | 1.766 | forced |
| HAM-MAG | top-k | 0.9882 | 0.024 | 2.136 | 2.136 | 2.039 | S2 |
| WHV-OSN | top-k | 1.139 | 0.0221 | 1.766 | 1.766 | 1.753 | forced |

| Figure | Block | ECF | Golden | Band | S1 lost | S2 lost | S3 lost | Reflex route |
|---|---|---|---|---|---|---|---|---|
| C1_coldstore_pullback_2026 | components | no | 7437 | 7173 to 7644 | moves | - | - | lost |
| C2_phyto_rail_roll_2026 | components | no | 4304 | 4086 to 4436 | - | moves | - | lost |
| C3_depot_backlog_2026 | components | no | 7171 | 6742 to 7280 | - | - | moves | lost |
| BCR_BHV_HAN | asks | no | 0.9487 | 0.9197 to 1.061 | moves | - | flips | lost |
| BCR_BHV_KAS | asks | no | 0.9011 | 0.8855 to 0.9199 | flips | moves | moves | lost |
| BCR_BHV_OSN | asks | no | 1.1 | 1.084 to 1.124 | moves | flips | moves | lost |
| BCR_HAM_HAN | asks | no | 1.086 | 1.073 to 1.114 | flips | moves | flips | lost |
| BCR_HAM_MAG | asks | no | 0.9882 | 0.9744 to 1.02 | moves | flips | moves | lost |
| BCR_WHV_OSN | asks | no | 1.139 | 1.109 to 1.159 | moves | moves | moves | lost |

| Route | Call | House rubric | v4-ECF rubric |
|---|---|---|---|
| golden | right | 100 | 100 |
| S1 lost alone | wrong | 22 | 30 |
| S2 lost alone | wrong | 31 | 37 |
| S3 lost alone | wrong | 22 | 30 |
| S1 fixed alone | wrong | 16 | 18 |
| S2 fixed alone | wrong | 16 | 18 |
| S3 fixed alone | wrong | 16 | 18 |
| reflex route (every stump lost) | wrong | 9 | 7 |
| rigorous standard route | wrong | 9 | 7 |
| cutoff run route | wrong | 18 | 14 |
| generous run route | wrong | 9 | 7 |
| hedge run route | wrong | 9 | 7 |

CORE PASS level 5  task27

## Stump factorial

Reflex route: Deduplicates all logs, converts cases to pallets, harmonizes dates/timezones, joins entity crosswalk, applies Charter Section 3 tariffs/growth/capacity factors, and computes corridor BCRs directly from TMS stage codes without S1, S2, or S3 modeling; files BHV-KAS (2.176), HAM-MAG (2.136), BHV-HAN (2.012), missing all three golden winners (WHV-OSN, BHV-OSN, HAM-HAN) and scoring 7 on v4-ECF (9 house).

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| S1 Asymmetric convex chamber-load hysteresis | stump | Whole-DC occupancy check (~74% flat) or binary >=92% / symmetric linear cut | L26, L28, L38, N36 | Funds BHV-KAS, BHV-OSN, WHV-OSN (BHV-KAS 1.845, drops HAM-HAN) | Funds BHV-HAN, HAM-HAN, HAM-MAG (still wrong; rescues 1 of 9 figures) | no |
| S2 Joint terminal-varying BIP lock vs Nordbahn short-consist rail model | stump | Raw TMS rail logs, direct CHED siblings only, or bivariate fixed-24h BIP regression | L03, L07, L48, N07 | Funds HAM-HAN, HAM-MAG, WHV-OSN (HAM-MAG 1.720, drops BHV-OSN) | Funds BHV-HAN, BHV-KAS, WHV-OSN (still wrong; rescues 1 of 9 figures) | no |
| S3 Conserved shipping-line empty-depot queue stock across open drain days | stump | Raw TMS drayage logs, binary unload-day portal rejection flag, or port-aggregated queue | N14, N27, L56, L57 | Funds BHV-HAN, BHV-OSN, WHV-OSN (BHV-HAN 1.695, drops HAM-HAN) | Funds BHV-KAS, HAM-HAN, HAM-MAG (still wrong; rescues 1 of 9 figures) | no |
| R1 Layer 1 EDI deduplication, date/timezone harmonization, and SKU case-to-pallet crosswalk | reflex | Raw uncleaned extracts | R01, R04 | Same call (WHV-OSN, BHV-OSN, HAM-HAN) | - | - |

Level: 5 (three necessary independent stumps on distinct axes what/unit/when, none sufficient alone, producing 7 distinct wrong slates across all 7 non-empty lattice drops).

## Open members

| Member | Golden margin | Family spread | Reflex route | Direct route | Opened by |
|---|---|---|---|---|---|
| BHV-HAN | -0.137 below #3 cutoff (0.949 vs 1.086) | 0.0891 | 2.012 (wrong: #3 funded) | 2.012 (wrong: #3 funded) | S3 |
| BHV-KAS | -0.185 below #3 cutoff (0.901 vs 1.086) | 0.0131 | 2.176 (wrong: #1 funded) | 2.176 (wrong: #1 funded) | S1 |
| BHV-OSN | +0.112 above #4 cutoff (1.100 vs 0.988) | 0.0169 | 1.761 (wrong: #6 deferred) | 1.761 (wrong: #6 deferred) | forced |
| HAM-HAN | +0.098 above #4 cutoff (1.086 vs 0.988) | 0.0215 | 1.839 (wrong: #4 deferred) | 1.839 (wrong: #4 deferred) | forced |
| HAM-MAG | -0.098 below #3 cutoff (0.988 vs 1.086) | 0.0240 | 2.136 (wrong: #2 funded) | 2.136 (wrong: #2 funded) | S2 |
| WHV-OSN | +0.151 above #4 cutoff (1.139 vs 0.988) | 0.0221 | 1.766 (wrong: #5 deferred) | 1.766 (wrong: #5 deferred) | forced |

Direct route: Reading primary TMS stage durations in `container_milestones_2026.csv` at face value (`estimate_s1/s2/s3 mode="direct"`) computes corridor BCRs directly from raw `term_yard_hold_cdays`, `rail_excess_cdays`, and `dray_empty_hold_cdays`, ranking BHV-KAS (2.176), HAM-MAG (2.136), and BHV-HAN (2.012) ahead of HAM-HAN (1.839), WHV-OSN (1.766), and BHV-OSN (1.761), funding the exact wrong three corridors because all three non-carrier bottlenecks sit inside those three TMS stage timers.

## Data provenance

Source: Generated by `task27/generator/core.py` and `task27/generator/pack.py` (seeded physical cold-chain simulation, `SEED = 2701`) modeling Weserfrucht Import GmbH's 2026 North Sea refrigerated import network.
Behaves like the real thing: Simulates 24,000 40-foot reefer container lifecycles across 480 vessel calls, 6 port-to-DC corridors, 732 every-3-day intermodal block trains, 4 multi-temperature cold-storage DCs (+2C/+7C/+13C), and 4 ocean shipping lines with Gamma dwell distributions, smooth AR(1) chamber/yard occupancy waves, continuous Gamma BIP notice lead times, stochastic Binomial/Poisson train rollovers with CV ~0.30 wait durations, noisy weighbridge gross tonnage (R^2 ~0.95-0.96), and exact physical daily empty-depot stock-flow conservation.
Genuine patterns: (1) opposing winter (+7C citrus) and summer (+2C berry/stone-fruit) produce peaks offset by +13C tropical buffer chambers holding whole-DC utilization flat at 69-78%; (2) shared summer and winter freight peaks driving correlated BIP inspection surges and Nordbahn short-consist/loco cuts; (3) episodic 3-4 day ocean-line depot portal closures building return queues that drain over 5-7 subsequent open days across varying corridor haul distances (128 to 268 km).
Problems by process: (1) mixed German/ISO date formats from port terminal TOS vs warehouse WMS exports; (2) nightly WMS EDI resend batches with revision sequence numbers; (3) UTC maritime/rail clocks vs CET inland gate clocks; (4) legacy facility/carrier code aliases from Weserfrucht's 2024 ERP migration; (5) case-to-pallet conversion across 18 produce SKUs; (6) routine procurement reference tables for bunker fuel and German road Maut tolls that do not enter D&D billing.
Breadth: 18 files across CSV, XLSX, PDF, DOCX, TXT, and JSON (including a 24,000-row container spine, a 60,000+-row warehouse pallet movement ledger, a 10+-page Charter PDF, and 2 unlabelled distractors), requiring purposeful selection and cross-grain linkage.

## Template check

Chain signature: assembly-reconciliation -> modeling -> causal-reasoning -> investigation-loops -> validation -> forecasting -> synthesis
Question form: what ("What North Sea import corridors should Weserfrucht fund under Charter RC-2027's EUR 1.75 million 2027 carrier-remediation budget")
Nearest build: task21 v1 (severity none by skeleton.py check; task21 sets motor-insurance rate changes on pricing tiers, whereas task27 allocates a fixed cold-chain capital budget across six port-to-DC corridors via asymmetric chamber hysteresis, joint BIP/short-consist separation, and conserved empty-depot queue persistence).

## Frontier check

Precedents: R2 (`C1_coldstore_pullback_2026`): L26, L28, L38, N36; R3 (`C2_phyto_rail_roll_2026`): L03, L07, L48, N07; R4 (`C3_depot_backlog_2026`): N14, N27, L56, L57; R6 & R7 (coupled corridor BCRs & slate): downstream of S1, S2, S3.
Shallow path checks: (S1) hurried route checks whole-DC utilization (`dc_aggregate_occupancy_2026.csv`, flat 69-78%) or fits symmetric linear/binary >=92% cut, refuted by `warehouse_pallet_movements_2026.csv` showing a 12+ hour filling-vs-draining residual plug gap in [84%, 94%] chamber utilization and port-rack slope distortion; (S2) hurried route removes direct CHED siblings or runs bivariate fixed-24h BIP OLS, refuted by `bip_phyto_notices_2026.csv` + `rail_shuttle_departures_2026.csv` showing cross-24h port contrast (HAM 24-28h vs BHV 16-24h) and collapsed `consist_wagons_short` slope on overlap shuttles; (S3) hurried route flags binary unload-day `portal_rejected > 0` or aggregates queues at port level, refuted by `empty_depot_portal_log_2026.csv` showing an 18+ hour residual open-portal drain-tail gap on `portal_rejected == 0` days and wiped carrier baseline on unconstrained lines.
Assumption made false: (1) uniform symmetric chamber delay above a threshold is false because cold-store dock queuing is sharply convex and ~7.5x steeper during filling (`net_flow > 0`) than draining (`net_flow <= 0`); (2) a single network-wide 24h BIP rail cutoff independent of consist shortages is false because terminals operate different booking locks (BHV ~16h, HAM ~28h, WHV ~12h) overlapping peak-day Nordbahn short-consist & loco cuts; (3) depot portal blocking ends on the day the portal reopens is false because accumulated unreturned empties conserve physically and drain over 5-7 subsequent open days proportional to corridor haul distance.
Forcing: Top-3 funding line sits between #3 `HAM-HAN` (1.086, band 1.073-1.114) and #4 `HAM-MAG` (0.988, band 0.974-1.020), a 0.098 BCR separation (>4x wider than either corridor's honest family spread 0.022-0.024). All 21 honest modeling variants hold the exact slate (WHV-OSN, BHV-OSN, HAM-HAN), greedy Top-3 equals exact integer knapsack (EUR 1,705,000 <= EUR 1,750,000 cap; any 4 corridors >= EUR 2,255,000), and all 8 independent +/-15% parameter stress tests (`S1 +/-15%`, `S2 +/-15%`, `S3 +/-15%`, `base +/-15%`) hold the exact same slate (`FORCING: PASS`).
Noun swap: Nearest build on file is `task21 v1` (skeleton.py check `severity none`); swapping cold-chain corridors into private-motor pricing tiers breaks decision_form (`allocation_under_budget` vs `dial_or_cap_setting`), answer_pattern (`naive_leader_drops_winner_climbs` vs `shortcuts_land_on_distinct_wrong_answers`), 3 of 4 lessons (`shared_group_event_covariance`, `turnover_not_stock_driver`, `served_state_outlives_source_failure`), and all 4 physical mechanisms.
Closed strategies: The call turns on `asymmetric_response`, `shared_group_event_covariance`, `turnover_not_stock_driver`, and `served_state_outlives_source_failure`; `skeleton.py closed task27` confirms 0 of 4 lessons are on the client's 45 closed strategies list (0 closed supporting steps). No closed strategy moves any corridor across the funding cutoff.
Decisive steps: (1) S1 owns `C1_coldstore_pullback_2026` = 7,436.9 c-days (band 7,173-7,644), asked for as 2026 non-carrier cold-store pull-back container-days in workbook/deck/CSV, evidenced in `warehouse_pallet_movements_2026.csv` + `container_milestones_2026.csv`, leaving S2, S3, and 2027 BCR projection; (2) S2 owns `C2_phyto_rail_roll_2026` = 4,304.4 c-days (band 4,086-4,436), asked for as 2026 non-carrier border-inspection rail rollover container-days, evidenced in `bip_inspection_notices_2026.jsonl` + `rail_shuttle_departures_2026.csv`, leaving S1, S3, and 2027 BCR projection; (3) S3 owns `C3_depot_backlog_2026` = 7,171.5 c-days (band 6,742-7,280), asked for as 2026 non-carrier empty-depot return backlog container-days, evidenced in `depot_portal_requests_2026.csv` + `container_milestones_2026.csv`, leaving S1, S2, and 2027 BCR projection. Independence lattice: dropping S1 alone gives BHV-KAS/BHV-OSN/WHV-OSN (C1=0); dropping S2 alone gives HAM-HAN/HAM-MAG/WHV-OSN (C2=0); dropping S3 alone gives BHV-HAN/BHV-OSN/WHV-OSN (C3=0); all 7 non-empty drops give 7 distinct wrong slates.
Run routes: `generous` (broad over-correction on all 3 channels) -> wrong slate BHV-HAN/BHV-OSN/HAM-MAG (crashes HAM-HAN to 0.342 and WHV-OSN to 0.448), earns 7 v4-ECF (9 house); `calibrated` -> none (no shipped file observes true carrier-controllable split or any stump quantity directly); `hedge` (14% sensitivity haircut) -> wrong slate BHV-HAN/BHV-KAS/HAM-MAG, earns 7 (9); `cutoff` (binary >=95% chamber, <=32h any-BIP shuttle, binary unload-day portal rejection) -> wrong slate BHV-HAN/BHV-KAS/WHV-OSN (crashes HAM-HAN to 0.768), earns 14 v4-ECF (18 house); all 5 extra partial cutoffs (`cutoff:s1_sym_lin`, `cutoff:s1_one_fact`, `cutoff:s2_one_fact`, `cutoff:s3_one_fact`, `cutoff:s3_raw`) also file wrong slates.
Validation handles:
| Shipped file | S1 (asymmetric chamber pull-back) | S2 (terminal BIP locks vs short-consists) | S3 (conserved shipping-line depot queue) |
|---|---|---|---|
| container_milestones_2026.csv | no (combined excess_port_yard_cdays only) | no (combined excess_rail_cdays only) | no (combined excess_dray_empty_cdays only) |
| warehouse_pallet_movements_2026.csv | no (pallet flows only; no yard dwell) | no | no |
| coldstore_inventory_daily_2026.csv | no (whole-DC totals flat 70.7-77.6%) | no | no |
| bip_inspection_notices_2026.jsonl | no | no (lead timestamps only; no shuttle rolls) | no |
| rail_shuttle_departures_2026.csv | no | no (combined rolls + noisy gross tonnes R^2~0.96) | no |
| depot_portal_requests_2026.csv | no | no | no (unlinked daily bookings/rejections only) |
| carrier_dispute_closeout_2026.xlsx | no (commercial invoice settlements only) | no | no |
| remediation_program_budgets_2027.csv | no (2027 budgets, capture rates, schedule factors) | no | no |
| weserfrucht_remediation_charter_rc2027.pdf | no (discloses mechanisms, no parameter values) | no | no |
No shipped file or pair of files gives a direct calibration handle or validation label for any stump's unobserved split.
Forward window: 2027 corridor avoidable exposure is not 2026 actuals restated: Annex C applies distinct 2027 corridor volume growth factors (+12% to +22%: HAM-HAN +22%, BHV-OSN +18%, WHV-OSN +16%, BHV-KAS +15%, HAM-MAG +14%, BHV-HAN +12%) and port-specific 2027 infrastructure capacity factors (BHV plug 0.92 / rail 0.94 / dray 0.95; HAM plug 1.05 / rail 0.96 / dray 0.98; WHV plug 1.00 / rail 0.92 / dray 0.96), plus corridor-specific engineering capture rates (0.72 to 0.78) and corridor capital budgets (EUR 560k to EUR 585k). Without 2027 forward factors, raw 2026 EUR/budget ratios understate HAM-HAN and BHV-OSN by 14-18% relative to 2027 projections.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | Capital allocation objective | Greedy descending BCR vs exact integer knapsack under EUR 1,750,000 cap | Same slate (WHV-OSN, BHV-OSN, HAM-HAN; EUR 1,705,000) | `same call` (every 3-corridor set <= EUR 1.73M, every 4-corridor set >= EUR 2.255M) |
| SF2 | Carrier-controllable cause scope | 3 carrier channels (`reefer_plug`, `rail_handoff`, `drayage_carrier`) vs adding `vessel_berth` or `edi_docs` | 3 carrier channels only | `weserfrucht_remediation_charter_rc2027.pdf` Section 2.2 explicitly lists the 3 carrier-controllable channels and excludes `vessel_berth` and `edi_docs` |
| SF3 | S1 chamber estimation form & FE | Quadratic/spline/binned/Huber asymmetric FE, vessel vs port-day vs corr-week FE, hinge 0.76-0.80 | Vessel FE asymmetric quadratic, hinge 0.78 | `same call` (all 7 S1 honest variants inside band, 0 flips); symmetric/binary refuted by `fal_err` |
| SF4 | S2 rail shuttle lock & count model | Smooth logistic vs hard step vs binned lead, OLS vs Poisson IRLS vs Huber, port-specific vs pooled slope, with/without month+corr FE or booked-slot control | Smooth logistic empirical port cuts, OLS joint control for consist_wagons_short & loco_derate | `same call` (all 7 S2 honest variants inside band, 0 flips); bivariate 24h & whole-shuttle refuted by `fal_err` |
| SF5 | S3 depot queue FE & functional form | DC-week vs DC-day vs port-day vs corr-week FE vs harmonic OLS vs Huber vs distance-parametric | DC-week FE corridor-varying linear queue with proportional Gamma posterior share | `same call` (all 6 S3 honest variants inside band, 0 flips); binary rejection & port-aggregated queue refuted by `fal_err` |
| SF6 | Direct CHED rail sibling holds | Included inside `C2_phyto_rail_roll_2026` vs excluded (tracked as direct BIP holds) | Excluded from `C2_phyto_rail_roll_2026` (which measures BIP-induced standby rail rollovers) | `weserfrucht_remediation_charter_rc2027.pdf` Section 2.3 distinguishes direct CHED sibling holds from standby rail rollovers; excluded from `rail_handoff` under both readings (`same call`) |
| SF7 | Duplicate warehouse EDI batches & date/TZ formats | Latest `extract_version` deduplication and CET alignment vs raw rows | Latest `extract_version` deduplicated and CET-aligned | `weserfrucht_remediation_charter_rc2027.pdf` Section 1.3 & Annex A specify final-revision ledger and CET inland day |

## Pinning list

| Constant | Golden value | Home |
|---|---|---|
| 2027 capital remediation budget cap | EUR 1,750,000 | `weserfrucht_remediation_charter_rc2027.pdf` Section 4.1 & `remediation_program_budgets_2027.csv` |
| Corridor budgets & capture rates | BHV-HAN 575k (0.74), BHV-KAS 570k (0.72), BHV-OSN 560k (0.76), HAM-HAN 585k (0.78), HAM-MAG 565k (0.75), WHV-OSN 560k (0.76) | `remediation_program_budgets_2027.csv` & `weserfrucht_remediation_charter_rc2027.pdf` Annex B |
| Schedule B D&D tariffs | reefer_plug EUR 210/d, rail_handoff EUR 175/d, drayage_carrier EUR 160/d | `weserfrucht_remediation_charter_rc2027.pdf` Schedule B & `remediation_program_budgets_2027.csv` |
| Annex C 2027 volume growth & port capacity factors | Corridor vol growth 1.12-1.22; port plug/rail/dray factors (BHV 0.92/0.94/0.95, HAM 1.05/0.96/0.98, WHV 1.00/0.92/0.96) | `remediation_program_budgets_2027.csv` & `weserfrucht_remediation_charter_rc2027.pdf` Annex B & C |
| Chamber hinge utilization | 0.78 (empirically estimated; 0.76-0.80 spanned) | 21-variant estimator family (spread 314 c-days on C1, 0 flips) |
| Port BIP rail lock cutoffs | BHV ~14-16h, HAM ~26-28h, WHV ~10-12h (empirically profiled via RSS grid, never hardcoded in files) | 21-variant estimator family (spread 233 c-days on C2, 0 flips) |
| Depot queue normalization & corridor haul slope | Exact cumsum(unloads - confirmed_bookings) / mean_daily_unloads; corridor slopes estimated empirically | 21-variant estimator family (spread 359 c-days on C3, 0 flips) |

Variant battery: 21 variants spanning S1 functional forms (quadratic, spline, non-parametric bins, Huber, hinges 0.76/0.78/0.80, vessel/port-day/corr-week FE), S2 models (smooth logistic, hard step, non-parametric lead bins, Poisson IRLS, Huber, month+corr FE, pooled slope, booked-slot control), S3 models (dc-week, dc-day, port-day, corr-week FE, harmonic OLS, Huber, distance-parametric), and a joint multi-channel alternative all file one answer (the same call: WHV-OSN, BHV-OSN, HAM-HAN) with 0 flips.

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: all 24,000 final-revision settled 2026 40-foot refrigerated import containers across Weserfrucht's six North Sea port-to-DC corridors (Charter Section 1.3) |
| 2 | Time window: full calendar year 2026 (2026-01-01 to 2026-12-31 vessel discharges, with empty-return completions tracked cleanly through 2027-01-18) projected onto 2027 schedule (Charter Section 1.3) |
| 3 | Geographic & corridor grain: six port-to-DC corridors (`BHV-HAN`, `BHV-KAS`, `BHV-OSN`, `HAM-HAN`, `HAM-MAG`, `WHV-OSN`) across 3 ports and 4 inland cold-storage DCs |
| 4 | Deduplication: retain highest `extract_version` per `movement_id`, `container_id`, and `gate_event_id`, and exclude `record_status = VOID` (Charter Section 1.3 & Annex A) |
| 5 | Date & timezone alignment: harmonize German DD.MM.YYYY and ISO dates; align inland cold-store and depot unload dates to `Europe/Berlin` CET/CEST operating day |
| 6 | Unit conversion: convert produce cases (`unit = CASE`) to Euro-pallets using exact `cases_per_pallet` in `sku_thermal_catalog.csv` |
| 7 | Entity resolution: map legacy ERP/WMS store and carrier codes through `entity_crosswalk_2026.csv` |
| 8 | Chamber stock-flow conservation: daily closing stock per `(dc_id, thermal_zone)` equals opening stock plus cumulative `(IN - OUT)` pallets, reconciling identically to `coldstore_inventory_daily_2026.csv` |
| 9 | Carrier-controllable scope: exactly three channels (`reefer_plug`, `rail_handoff`, `drayage_carrier`); `vessel_berth`, `edi_docs`, `coldstore_dock`, `phyto_insp`, and `empty_depot` excluded from corridor remediation BCR numerator (Charter Section 2.2) |
| 10 | Non-carrier separation S1: `C1_coldstore_pullback_2026` is the attributed inland thermal-chamber pull-back removed from `excess_port_yard_cdays`, leaving carrier `reefer_plug` |
| 11 | Non-carrier separation S2: `C2_phyto_rail_roll_2026` is the attributed BIP-induced standby rail rollover delay removed from `excess_rail_cdays` (separate from direct CHED sibling holds, which also belong to `phyto_insp`), leaving carrier `rail_handoff` |
| 12 | Non-carrier separation S3: `C3_depot_backlog_2026` is the attributed ocean-line empty-depot return backlog delay removed from `excess_dray_empty_cdays`, leaving carrier `drayage_carrier` |
| 13 | Posterior sharing: container/shuttle attribution uses proportional expected-share decomposition so every observation's carrier + non-carrier parts sum identically to its observed stage total |
| 14 | Schedule B valuation: EUR 210.00/day for `reefer_plug`, EUR 175.00/day for `rail_handoff`, EUR 160.00/day for `drayage_carrier` (Charter Schedule B) |
| 15 | Annex C 2027 projection: multiply each corridor's 2026 carrier-controllable channel days by corridor `vol_growth_2027` and port-level channel capacity factor (`plug_capacity_factor_2027`, `rail_fleet_factor_2027`, `dray_contract_factor_2027`) |
| 16 | Avoidable EUR: multiply projected 2027 gross carrier-controllable EUR by corridor `capture_rate_2027` from `remediation_program_budgets_2027.csv` |
| 17 | Corridor BCR: `projected_2027_avoidable_eur / remediation_budget_eur` |
| 18 | Funding rule: select corridors in descending BCR order within the fixed EUR 1,750,000 capital cap (no partial corridor funding; identical to exact integer knapsack) |
| 19 | Distractor exclusion: North Sea bunker fuel indices (`north_sea_bunker_fuel_index_2026.csv`) and German road Maut schedules (`german_toll_maut_rates_2026_2027.xlsx`) do not alter Schedule B D&D tariffs or corridor budgets |
| 20 | CSV deliverable schema: exact 13 column names and ordering specified in Charter RC-2027 Rev 3 Section 5.2 (`weserfrucht_corridor_allocation_2027.csv`) |
| 21 | Rounding & tie-breaking: compute at full IEEE-754 floating precision; display EUR to 2 decimals, container-days to 1 decimal, BCR to 3 decimals (no ties exist; min gap 0.014 BCR) |
| 22 | Cross-deliverable reconciliation: every figure in `submission.md`, CSV, XLSX, and PPTX derives from one controlling calculation (`figures.json`) and recomputes identically from `target.zip` |

## Literal reader

A reader following `weserfrucht_remediation_charter_rc2027.pdf` (Rev 3) word for word: (1) deduplicates the 2026 container and warehouse logs onto 24,000 settled containers and exact daily `(DC, zone)` chamber stocks; (2) reads Section 2.1-2.3 disclosing the three non-carrier overlap processes (asymmetric filling-vs-draining DC pull-back, terminal-varying BIP rail booking locks overlapping Nordbahn short-consist cuts, and multi-day ocean-line empty-depot return backlogs) and empirically models each across the multi-grain logs to obtain `C1 = 7,436.9`, `C2 = 4,304.4`, `C3 = 7,171.5` c-days; (3) validates residual orthogonality and genuine carrier-slope preservation (`fal_err = 36.3`); (4) projects 2027 carrier-controllable days and Schedule B avoidable EUR under Annex B & C and `remediation_program_budgets_2027.csv` to compute the six corridor BCRs (`WHV-OSN 1.139`, `BHV-OSN 1.100`, `HAM-HAN 1.086`, `HAM-MAG 0.988`, `BHV-HAN 0.949`, `BHV-KAS 0.901`); and (5) funds `WHV-OSN`, `BHV-OSN`, and `HAM-HAN` (EUR 1,705,000 of EUR 1,750,000 cap; EUR 1,889,111.37 avoidable; portfolio BCR 1.108) while deferring `HAM-MAG`, `BHV-HAN`, and `BHV-KAS`.

## Prompt contract

A voice rewrite must preserve: (1) the decision question asking what North Sea import corridors to fund under Charter RC-2027's EUR 1.75 million 2027 carrier-remediation budget; (2) the request for each corridor's projected 2027 benefit-cost ratio; (3) the request for 2026 non-carrier container-day volumes separated out across cold-store pull-back, border-inspection rail rollovers, and empty-depot return backlogs; and (4) the three deliverable types (slide deck, controlling spreadsheet, CSV corridor allocation register). It must never add estimation methods, formulas, file names, rounding rules, warnings, personas, or data-gap pre-diagnoses.

## Build brief

World: Weserfrucht Import GmbH operates 24,000 40-foot refrigerated produce import containers in 2026 across 480 North Sea vessel calls (Bremerhaven, Hamburg, Wilhelmshaven) into 4 German cold-storage DCs (Hannover, Osnabrueck, Kassel, Magdeburg) along 6 port-to-DC corridors, served by Nordbahn Intermodal AG every-3-day block trains (732 shuttles) and 4 ocean shipping lines (Nordic Reefer Line `LINE_A`, Hanseatic Ocean Alliance `LINE_B`, Atlantic Fruit Carriers `LINE_C`, Baltic Cold Express `LINE_D`). All simulation parameters and seed (`2701`) are frozen in `task27/generator/core.py`.
Frozen: `SEED = 2701`, all `core.py` simulation dials, all three estimators (`estimate_s1`, `estimate_s2`, `estimate_s3`), all 21 family variants, all 7 lattice drops, all 8 +/-15% forcing stresses, and the exact golden slate `(WHV-OSN, BHV-OSN, HAM-HAN)` with `C1 = 7,436.9`, `C2 = 4,304.4`, `C3 = 7,171.5` and corridor BCRs `1.139 / 1.100 / 1.086 / 0.988 / 0.949 / 0.901`.
Files: Build the 17-file realistic input pack under `task27/target/` packed into deterministic `task27/target.zip`:
- `container_milestones_2026.csv` (24,525 rows: 24,000 settled + 335 superseded + 190 VOID; TMS lifecycle spine with `corridor_id`, UTC/CET timestamps, and combined stage excess columns; never includes ground-truth split columns).
- `warehouse_pallet_movements_2026.csv` (179,359 rows: daily DC x SKU IN/OUT movements with mixed DD.MM.YYYY / ISO dates, CASE/PALLET units, legacy store codes, and 4,152 superseded EDI rows).
- `depot_turnin_log_2026.csv` (25,252 rows: physical empty-depot gate arrival and turn-away events with legacy carrier codes and 445 superseded rows).
- `customs_consignment_bol_2026.csv` (24,000 rows: container-to-CHED-lot bill-of-lading mapping and declared cargo weights).
- `dc_chamber_register_2026.csv` (12 rows: 4 DCs x 3 sealed thermal chambers Z02 +2C, Z07 +7C, Z13 +13C capacities and opening stocks).
- `coldstore_inventory_daily_2026.csv` (1,460 rows: 4 DCs x 365 days whole-DC stock reconciling identically to chamber totals, flat at 70.7-77.6%).
- `sku_thermal_catalog.csv` (180 produce SKUs with `thermal_zone` and `cases_per_pallet`).
- `terminal_yard_daily_2026.csv` (1,095 rows: 3 ports x 365 days daily reefer-rack utilization).
- `bip_inspection_notices_2026.jsonl` (1,250 BIP-selected CHED lots with continuous Gamma `exam_notice_ts_utc` across 1.5h-72h lead times, zero dead zones).
- `rail_shuttle_departures_2026.csv` (732 every-3-day corridor block trains with `planned_wf_slots`, `booked_wf_slots`, `loaded_wf_slots`, `wf_standby_rolled`, `consist_wagons_short`, `loco_derate_events`, `train_wagon_count`, `train_total_gross_tonnes`).
- `depot_portal_requests_2026.csv` (4,596 rows: 3 ports x 4 ocean lines x 383 days with daily `confirmed_bookings` and `quota_closed_rejections`, no container IDs).
- `remediation_program_budgets_2027.csv` (6 corridors with `remediation_budget_eur`, `capture_rate_2027`, `vol_growth_2027`, `haul_distance_km`, port 2027 capacity factors, and Schedule B tariffs).
- `entity_crosswalk_2026.csv` (legacy retail store and drayage carrier code mappings).
- `carrier_dispute_closeout_2026.xlsx` (normalized OOXML commercial invoice dispute settlement summary; strictly invoice scope, never corridor BCRs).
- `weserfrucht_remediation_charter_rc2027.pdf` (11 printed pages via `officepdf.py` / LibreOffice Writer; pins estimands, EUR 1.75M cap, Schedule B tariffs, Annex B & C factors, Section 5.2 CSV schema, and openly describes the 3 physical overlap mechanisms without formulas, exact cutoffs, or golden numbers).
- `north_sea_bunker_fuel_index_2026.csv` and `german_toll_maut_rates_2026_2027.xlsx` (2 unlabelled realistic distractors).
Never filed: Never write any golden figure (7,436.9, 4,304.4, 7,171.5, 1.139, 1.100, 1.086, 0.988, 0.949, 0.901, EUR 1,889,111, EUR 1,705,000), never name exact cutoffs (16h, 28h, 12h, 0.78 hinge, 0.66 pass-through), never prescribe a regression equation or estimator, never rank corridors or name winners in any input file, and never use stump vocabulary ("stump", "trap", "decoy", "reflex", "hurried", "lattice") anywhere in `target/`.
Goldens: Produce exact 3 files in `task27/golden/` zipped to `task27/golden.zip`: `weserfrucht_corridor_allocation_2027.csv` (exact Charter Section 5.2 schema), `weserfrucht_corridor_capital_model_2027.xlsx` (5-tab workbook with 154 live Excel formulas verified error-free in LibreOffice Calc), and `weserfrucht_remediation_allocation_2027.pptx` (10-slide executive committee deck with crisp matplotlib charts visually verified via LibreOffice PDF + PNG rendering).
Free: Narrative wording of Charter prose, visual layout and chart palette of deck/workbook, additional Layer 1 formatting texture that remains neutral across corridors.

## Tried and rejected

- Architecture 1 (8-cause 2027 Mandatory Remediation scorecard >=2,500 c-days, returned 2026-11-23): rejected because S2's 24h rail lock had an artificial 2.39h dead zone and zero-noise 2.25-day rollover constant (construction tell / catch), and disjoint 8-cause scorecard ECF rollups allowed Run 1 to score 65% despite missing S1 and S3. Rebuilt from scratch as Architecture 2 (open-book 6-corridor EUR 1.75M capital allocation, 100% coupled ask matrix, 0 ECF rollups, continuous Gamma lead times, noisy Gamma rollover durations CV=0.30, noisy weighbridge R^2=0.96, v4-ECF single-stump scores 30/37/30).
- Daily rail shuttles (`n_shuttles = 2,190`, ~8 boxes/shuttle) and every-2-day shuttles (`n_shuttles = 1,098`) with hard clipping `clip(bip_hat / rolled_sh, 0, 1)`: rejected because low per-shuttle eligible pools caused >30% Tobit censoring on HAM shuttles and Jensen clipping bias depressed `C2` by 31%. Replaced with every-3-day corridor block trains (`n_shuttles = 732`, ~30-45 boxes/shuttle, <1% censoring, 3.25d rollover matching 3-day timetable) and exact Poisson-thinning / Gamma posterior sharing (`TRUTH vs GOLDEN` within 0.3% on C1/C3 and 3.5% on C2).
- Container-level rounded return lag to reconstruct `daily_empty_gateins`: rejected because integer rounding created errors-in-variables attenuation on `WHV-OSN` and widened the `C3` band to 3,500 c-days. Replaced with exact physical daily depot gate-in conservation (`queue_stock = cumsum(unloads - gate_ins)`), tightening the `C3` band to 359 c-days (<5% width).
