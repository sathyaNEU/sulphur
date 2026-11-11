# task13 architecture 3, platform run (pasted by the author 2026-11-11)

Score: not given. The author's note: "model identified the ground truth (task13)".
Run length on the platform: 1h 18m, 173 resources reviewed. Only the run's final answer is kept below; the trace was
tool calls and thinking fragments (clock calibration with a whole-visit holdout, event-number gaps, a gamma-Poisson
fit with parameter uncertainty, an all-sound simulation, sensitivity checks).

## The run's final answer (verbatim)

Recommendation. Refer the 11 flagged zones for the 2027 lightning protection refit. The rule's modeled 2026 sound-zone referral expectation is 0.152, below the programme limit of 0.200 per network-season.

Final answers.

Annual rule: After each lightning season, compare each zone's recovered lightning faults since the day after its last cyclic repair completion with its predictive fault count under sound protection and the actual ground strokes within 400 m of its lines. Refer when the upper-tail probability is at most 0.2/143 = 0.0013986014. The comparison includes dry-season faults within that post-inspection record. The rule and calibration are in lightning_refit_2027_note.pdf, pages 1 and 3; each zone's probability and integer cutoff are in the CSV.
2027 referrals: BGS-F3-R1, CLB-F1, CLB-F2, CLB-F2-R1, LRD-F1-R2, MLN-F2, MLN-F4, MLN-F4-R2, PGP-F2, PGP-F4-R3 and TGP-F3-R1. These appear in the note's page 1 chart and have referred_2027 = YES in lightning_referrals_2027.csv.
Zone-level CSV: The file contains 143 unique zone rows, with seasonal recovered faults for 2022-2026, coverage-adjusted estimates, sound-protection expectations, cyclic inspection and repair dates, post-inspection comparisons, referral probabilities, cutoffs and flags. Uncertain zone assignments are flagged separately.
Referrals after each season: 2022: 2; 2023: 3; 2024: 6; 2025: 8; 2026: 11. These are retrospective snapshots using actual cyclic repairs, not hypothetical earlier refits. See the note's "Season-End Referral Workload" and the CSV's historical referral flags.
Expected sound-zone referrals: Under the fitted model, the all-zones-sound expectations are 0.148, 0.145, 0.156, 0.152 and 0.152 for 2022-2026. The actual sound subset contributes no more under that model. This is an expected-count limit, not a percentage of referrals. See page 1.
Comparison with subsequent inspections: Across 104 inspections, there were 4 confirmed referrals, 0 sound referrals, 22 missed failed zones and 78 sound non-referrals. Inspected-sample precision was 100.0%, sensitivity 15.4%, and false-positive rate 0.0%. Confirmations were LRD-F2 after 2022, CLB-F1 after 2023, TGP-F2 after 2024 and DLP-F5-R1 after 2025. No 2026-27 inspection findings were supplied. See page 2, "What The Next Cyclic Inspections Found."
Seasonal fault burden: Recovered device-initiated faults were 575, 419, 587, 626 and 628 in 2022-2026. Corresponding coverage-adjusted estimates were 578.1, 425.6, 616.7, 641.7 and 672.7; sound-protection counterfactuals were 488.6, 345.2, 542.0, 534.4 and 483.6. These appear on page 2 and reconcile to the CSV.
2026 faults attributable to failed protection: The modeled device-fault component is 189.1 faults, calculated as 672.7 minus 483.6, with a conditional 95% interval of 129.2-250.6. Without adjustment for missing logs, recovered-count excess is 144.4 faults. Complete all-network totals are not identifiable: transformer/cutout-only lightning faults remain unquantified. This qualification is prominent on page 2.
Expected refit benefit: 121.1 device-initiated faults avoided per average-lightning season, with a conditional 95% interval of 95.8-149.7. "Average lightning" uses each zone's own 2022-2026 mean exposure and spatial mix. This is a planning estimate assuming its observed 2026 rate represents year-end condition. See page 2, "Expected Avoidance," and CSV column refit_avoided_faults_average_lightning.

Step-by-step process (summary). Read the zip; programme terms for season, counting, inspection boundary, 400 m radius
and false-referral limit. Register and routes reconciled (143 zones, 45 feeders, 2,497.6 km). SCADA 63,558 rows and
downloads 133,973 rows, 95,092 repeated download rows removed, sequences reconstructed (15,465 episodes, 430 backup
pairs, 15,035 candidates). Offline clocks corrected on upstream lockout and downstream supply-loss pairs (1,201 pairs,
32 devices), whole-visit holdout 95th percentile 1.27 s. Strokes UTC to local, ground strokes within 400 m, matched
within 0.5 s (SCADA) and 3 s (corrected offline); 6,968 lightning faults, 2,835 in the five seasons. Sound reference
from 389 inspection-confirmed zone-seasons; gamma-Poisson with construction, surroundings, arresters and a persistent
zone level (pooled Poisson dispersion 4.02, adjusted 1.82), parameter uncertainty integrated into the predictive tail.
Overwritten-event gaps (63), missing event numbers (1,346), unread 2026 tails (2,032 device-days) excluded from
calibration exposure and adjusted for in the planning estimates. OMS and transformer book audited, no OMS-only faults
added; rain gauge and quotation reviewed and not used. Sensitivity: all 11 survive wider and narrower matching, partial
sequences out, coverage warnings out. All-sound simulation 0.157 referrals a run. Alternatives rejected: counting trips,
a constant clock offset (99.7 s error against 1.27 s), a point-mean Poisson test (19 zones), rain or codes as counts,
missing logs as fault-free, the whole post-inspection average for the benefit (75.8; two seasons 104.2; 2026 121.1).

## Against the golden (architecture 3), result by result

| Result | Golden and band | The run | Verdict |
|---|---|---|---|
| R1 season totals 2022 to 2026 | 561, 413, 593, 620, 655 (4 per cent each) | 578.1, 425.6, 616.7, 641.7, 672.7 | inside, 2024 at the edge |
| R2 2026 faults failed protection caused | 186 (170 to 200) | 189.1 | inside |
| R3 zones referred for 2027 | the 11 (exact set) | the same 11 | landed |
| R5 referrals after each season; sound referrals | 2, 2, 4, 8, 11 (1-3, 1-3, 3-5, 7-10, 10-12); 0.14 (0.12 to 0.16) | 2, 3, 6, 8, 11; 0.152 | 4 of 5 seasons and the sound rate inside |
| R6 against the next inspections | 5 inspected, 5 confirmed, 21 misses (3-6, 3-6, 20-23) | 4, 4, 22 | inside |
| R7 refit's avoided faults | 116 (104 to 128) | 121.1 | inside |

Every judgment the design priced as lost (each zone's own level from inspection-confirmed seasons, the level carried
uncertain into the tail, the state each failure had reached by the end of 2026, the radio-less reconstruction) was
made by the run unprompted. Architecture 3 is spent.
