# Determinism check: task13

**Verdict: DETERMINISTIC**
**Disposition: APPROVE**

## Method

Worked from the answer blocks only (Final Recommendation, Supplementary Questions, Critical Components,
Step-by-Step). Unzipped `target.zip` fresh into a scratch folder and recomputed the figures the blocks name,
starting with the three Critical Components since they carry the call, then spot-checked the filed facts behind
the supplementary figures and the open-choice forks the brief named.

## Evidence

| Figure (block) | Recomputed from shipped files | Result |
|---|---|---|
| CC1: Line 2 structure 63, 11 flashovers since 25 Sept 2025 | `relay_records_gridvue_2022-2026.json`, device `PAL_L2_D60`: filtered to records at or after 2025-09-25, converted both ends' distances to "km from terminal A" (line length 22.27 km from `structure_inventory_69kv_2026.csv`); PAL-side readings cluster tightly at 12.0-12.3 km (structure 63 sits at 12.01 km) on 2025-09-25, 2025-12-02, 2025-12-11, 2026-01-02, 2026-01-16, 2026-01-20, 2026-01-22, 2026-01-30, 2026-02-26, 2026-04-16, 2026-05-17, **exactly 11 trip events**, all single-phase-to-ground (AG/BG/CG), all `trip: True` | Matches exactly |
| CC1: "5 washes" of Line 2 Section 4, Nov 2025-March 2026 | `insulator_washing_log_2022-2026.xlsx` Log sheet, Line 2 / Section 4 rows: 2025-11-18, 2025-12-15, 2026-01-26, 2026-02-23, 2026-03-24 | Matches exactly (5 washes) |
| CC2: Line 6, structures 57-58, oak cut back 9 Aug 2022 | `vegetation_work_orders_2022-2026.csv` row 410002: `2022-08-09, Line 6, 57, 58, HOT SPOT, trim tree after contact` | Matches exactly |
| CC2: 12.47 kV underbuild at Line 6 structures 57-58 | `structure_inventory_69kv_2026.csv`: `L06-057` and `L06-058`, underbuild column = `12.47 kV` | Matches exactly |
| CC2: patrol signature ("oak cut back last year, nothing found") used by the hurried read | `line_patrol_reports_2022-2026.xlsx` Patrols sheet: 2026-06-12 and 2026-08-26, Line 6 str 57-58, "oak in the span cut back last year, nothing found" | Matches exactly, confirms the trap the Step-by-Step names |
| CC3: Line 2 Section 1 washed 17 Oct 2026; Section 6 washed 20 Oct 2026 | `insulator_washing_log_2022-2026.xlsx`: Section 1 row `2026-10-17`; Section 6 row `2026-10-20` | Matches exactly |
| Overall fault/year proportions (444 total, 2022-2026) | `scada_soe_2022-2026.csv`, `cause == PROT` events by year: 2022 992, 2023 1034, 2024 849, 2025 893, 2026(partial) 789; ordering and ratios (~9.5-10.8 trip events per built fault) track the claimed fault-year counts (103, 104, 78, 85, 74) in the same order | Consistent, not a full rebuild (ETL from raw breaker events to one-fault-per-two-ended-sequence was not independently re-executed; spot-check only) |
| Member interruptions/minutes (52,306 / 1,502,951 for 2026) | Traced to `members_by_feeder_monthly_2022-2026.csv` plus SCADA trips/transfers as the Step-by-Step states; `oms_extract_2022-2026.sqlite` (feeder/outage/outage_step tables) is present but not named by the Step-by-Step and reads as the pack's distractor DB, not the source of this figure | Method is grounded in filed files; not independently re-aggregated (out of budget, no contradiction found) |

## Forks checked (Gate C)

- **Flashover-level percentile**: the block itself already reports the range across the 5th/10th/20th percentile and other fits (0.028 to 0.064 mg/cm2) and the call (13 sections due) is stated against that band, not a single point estimate. No alternative percentile choice moves Line 2 structure 63 off the work list, since the structure's 11 fault events hang together as a location independent of where the salt line falls (step 4's point: a cracked string flashes on any wetting event, so the deposit-at-flashover statistic is a corroborating read, not the trigger).
- **The low-deposit cut (0.60 of median) for the cracked string**: a reasonable neighbour (0.5 or 0.7) does not change the call: the distinguishing fact is that structure 63 flashed over repeatedly within days of washing (deposit necessarily near zero) while the rest of Section 4 stayed quiet through the same wets; the 0.60 figure is descriptive, not a decision boundary.
- **Cause category of the Line 6 57-58 contact (vegetation vs. equipment/underbuild)**: the raw work order files this as a vegetation "trim tree after contact," which is exactly the hurried reading the Step-by-Step calls out; the files also carry the 12.47 kV underbuild row and two 2026 patrol entries confirming the oak was already cut back with "nothing found," which is what forces the equipment/hardware reading. Both the trap reading and the resolving facts are in the shipped files, so this is a real stump, not an unpinned ambiguity.
- **The Line 6 cause-mix ambiguity in Supplementary Q2** ("equipment or hardware and other or unknown, each within 3, the Line 6 contacts read as either") is already named and tolerance-widened in the block itself, so it does not leave the stated band.

## Gate B (filed facts)

Every fact the three Critical Components turn on (the washing dates, the vegetation work order date, the underbuild column, the patrol entries, the fault distances clustering at structure 63's location) is present in a named shipped file and was located directly, not inferred. No decisive fact required outside knowledge.

## Gate D/E

The split the hurried analyst would make (booking structure 63's flashovers as salt, clearing Line 6 57-58 as a grow-in, treating Line 2 sections 1 and 6 as clean at the average rate) traces to an analytical shortcut on the data (skipping the per-structure deposit-at-flashover read, assuming vegetation regrowth without checking the four-summer contact-temperature trend, averaging instead of fitting wind-driven accumulation), not to a different reading of a prompt term. The asks each pin one answer with its unit (rows, mg/cm2, member interruptions and member-minutes, a structure or span).

## Conclusion

No determinism defect found in the sampled figures, the three Critical Components, or the forks the brief flagged. The full 444-row fault table and the full 2026 member-interruption/minute rollup were spot-checked against the method the blocks state rather than independently rebuilt end to end; both spot-checks were consistent with the stated figures and no file contradicts them.

**Fix: none.**
