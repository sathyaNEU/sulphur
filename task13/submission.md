# task13 answer blocks

## Tags

**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities (grid reliability & outage analysis).
**Analytical objective:** Anomaly Detection & Diagnostics.

## Final Recommendation

**Refit these 15 zones before the 2027 lightning season: BGS-F3-R2, BGS-F5-R2, BTG-F1-R3, CBR-F2-R2, CLB-F5-R1, DLP-F2-R2, DLP-F4, LRD-F1-R1, LRD-F2, LRD-F2-R1, LRD-F3-R3, MPD-F2-R1, PGP-F1-R2, PGP-F2-R3 and SNJ-F1; and after every season refer each zone whose lightning faults since its last cyclic inspection (each fault's first trip matched to a stroke within 400 m of its lines on the recloser's own clock, with the events a recloser's memory lost or nobody has read restored) exceed what sound protection gives under that lightning, learned only from seasons a later inspection confirmed sound, by more than those seasons' scatter allows, at a chance below 1 in 855 a zone a season.** Taking the reclosers' logs as recorded and fitting the sound rate on every season no inspection has yet found failed refers only BTG-F1-R3 and PGP-F1-R2: the radio-less zones' clocks and lost months are left as they are, and the failing zones sit inside the baseline that should judge them.

## Supplementary Questions

### lightning_referrals_2027.csv

1. One row for each of the 171 zones in the protection zones register, in the register's order: zone, feeder, substation, whether its recloser has a radio link, the date its last cyclic inspection finished, then the zone's lightning faults in each season from 2022 to 2026 (1 April to 31 October, one decimal), each fault counted once on the zone whose lines it was on, with the events a radio-less recloser's memory overwrote or that are still unread restored at the zone's own rate. The season columns total **892, 682, 924, 747 and 1,075** (each within 4 per cent), and the 46 zones whose reclosers are read on site total **259** in 2026 (243 to 275), of which their memories kept 163.
2. The record since each zone's last cyclic inspection: the seasons it covers, the zone's lightning faults in them, what sound protection would have given it under the strokes within 400 m of its lines, the ratio of the two, and the chance of that many faults or more with sound protection. The chance is judged on the faults the records hold against the expectation for the same recorded months; the restored counts are reported, not tested. For the referred zones (faults within 10 per cent, expectation within 20 per cent, since the sound model's specification moves it):
   - BGS-F3-R2: 20 faults against 5.2 (ratio 3.82).
   - BGS-F5-R2: 55.6 against 9.0 (6.18).
   - BTG-F1-R3: 76 against 13.8 (5.50).
   - CBR-F2-R2: 16.5 against 2.8 (5.97).
   - CLB-F5-R1: 27 against 6.8 (3.95).
   - DLP-F2-R2: 36 against 12.7 (2.84).
   - DLP-F4: 33 against 7.9 (4.18).
   - LRD-F1-R1: 23.8 against 5.0 (4.74).
   - LRD-F2: 62 against 7.0 (8.85).
   - LRD-F2-R1: 32 against 12.2 (2.63).
   - LRD-F3-R3: 52 against 13.6 (3.81).
   - MPD-F2-R1: 32 against 12.6 (2.55).
   - PGP-F1-R2: 22 against 2.6 (8.33).
   - PGP-F2-R3: 32.8 against 13.1 (2.51).
   - SNJ-F1: 46 against 11.7 (3.93).
3. Referred: yes for the 15 zones of the recommendation, no for the other 156.

### lightning_refit_2027_note.docx

4. The rule as the recommendation states it, and the 15 zones it refers for the 2027 refit (another sound scatter model the confirmed seasons allow refers 13 to 17; the list is the negative binomial's).
5. Zones the rule would have referred after each season: **11** after 2022, **10** after 2023, **12** after 2024, **10** after 2025 and **15** after 2026 (each within one).
6. Zones with sound protection among a season's referrals: the rule's own expected rate, about **0.13** a season (0.11 to 0.15), one in about eight seasons; the terms' one in five (0.2) is the ceiling it stays under, not its rate.
7. Against the next cyclic inspections: the rounds of 2022-23 to 2025-26 inspected **15** zones the rule had referred after the season before (14 to 17) and confirmed all **15** (14 to 16); they found failed protection on **26** zones it had not referred (25 to 27).
8. The network's lightning faults: **892** in 2022, **682** in 2023, **924** in 2024, **747** in 2025 and **1,075** in 2026 (each within 4 per cent).
9. 2026's lightning faults caused by failed protection: **279** (237 to 321), the season's 1,075 against **796** with every zone's protection sound.
10. Lightning faults the refit should avoid in a season of average lightning: **107** (91 to 123).
11. The chart plots each zone's lightning faults since its last inspection against what sound protection would have given it, with the line where the two are equal and the 15 referred zones marked and named; under it, a table of the referred zones (faults, expectation, ratio) and one of what simpler versions of the rule would refer and report.

## Critical Components

1. The network's lightning faults in 2022 to 2026 are **892, 682, 924, 747 and 1,075**, with each radio-less recloser's clock fitted read by read and the events its memory lost or nobody has read restored.
2. Failed protection caused **279** of 2026's **1,075** lightning faults: the season would have had **796** with every zone sound, on a sound rate fitted only on the **193** zone-seasons a later cyclic inspection confirmed sound.
3. Run after each season, the rule refers **11, 10, 12, 10 and 15** zones (2022 to 2026).
4. Against the cyclic inspections of 2022-23 to 2025-26: **15** referred zones inspected, **15** confirmed, **26** misses (bands 14 to 17, 14 to 16 and 25 to 27 across the sound scatter models the confirmed seasons allow).

## Step-by-Step

1. Collapsed each fault's trips and recloses in `scada_event_history_2021-12_2026-10.csv` and `recloser_event_downloads_2021-2026.csv` (each re-read event kept once, upstream breakers' sympathetic trips dropped) to its first trip, and matched that trip to a ground stroke in `kidlat_strokes_2021-11_2026-10.csv` within 400 m of the zone's lines in `overhead_line_routes_2026.geojson`, the strokes moved from UTC to Philippine time.
2. On the 125 zones with synchronised clocks the first trips sit within a second of a stroke; the 46 reclosers read on site keep their own clocks, whose lag to nearby strokes grows in a straight line between site visits and resets at each read, so each controller's drift and offset were fitted per read from its own trips. A ten-minute window around their own stamps instead counts storm trips as lightning (1,028 network faults in 2026 with nothing restored), and one fixed offset per controller finds 19 of their 259.
3. The downloads' event numbers jump where a memory overwrote events between reads (58 of 710 reads, 1,154 events, 22 zones), and every radio-less memory is unread since its last visit; those months' faults were restored at the zone's own faults per stroke in its observed months, giving 259 on the radio-less zones in 2026 against 163 kept, and 892, 682, 924, 747 and 1,075 across the network.
4. Fitted a Poisson regression of each zone-season's faults on the strokes within 400 m, with the zone's construction, area and arrester shares and transformers per km from `protection_zones_register_2026.xlsx`, only on the 193 zone-seasons a later inspection in `cyclic_line_inspections_2016-2026.xlsx` found sound: a season since a zone's last inspection is unverified (the book shows 32 zones inspected clean and found failed at the next round), and a rate fitted on every season not yet found failed absorbs the failing zones and leaves 126 of 2026's faults to failed protection, against 279 (1,075 against 796, terms 2(f)).
5. The confirmed seasons scatter more than Poisson allows (2 dlogL 4.95 for a negative binomial of size 22.8); a Poisson chance refers 17 zones.
6. Compared each zone's faults since its last inspection (terms 2(e)) with the expectation over the same recorded months and referred it when the negative binomial chance fell below 1 in 855 (terms 3(b): one sound zone in five seasons across 171 zones): 15 zones, the weakest referred at 0.00029 and the strongest left out at 0.004. The chance is judged on what the records hold, because a restored count is an estimate; judged on restored counts as if counted, SRQ-F4-R3 (7 faults recorded against 2.1 expected) would be added. The whole record instead of the record since inspection refers 25, and the logs as recorded with the unverified rate refer 2.
7. Ran the same rule after each season: 11, 10, 12, 10 and 15 referrals; summing each zone's chance at the smallest count it would be referred at gives 0.13 sound zones a season, the rule's own rate under the budget's ceiling of 0.2.
8. Checked each inspection of 2022-23 to 2025-26 against the rule after the season before it (terms 5): 15 referred zones inspected, all 15 confirmed, 26 misses, failures too recent to have run up enough faults; the 2-zone rule checks 8 and misses 33.
9. Summed each referred zone's ratio since inspection less one, times its 2022 to 2026 mean sound expectation (terms 4(c)): 107 faults avoided in a season of average lightning, where 2026's own lightning would give 133.

No other referral set survives the files. The logs as recorded leave the radio-less clocks drifting and their lost months empty, which moves every season's count and changes 6 of the referrals; a sound rate learned from unverified seasons carries the failing zones in its own baseline and scatter and refers 2 to 4 zones; a Poisson chance ignores a scatter the confirmed seasons show and refers 17; the whole record counts faults that inspections have since repaired and refers 25; and the budget's 0.2 is the ceiling the rule's tails stay under, not its rate.
