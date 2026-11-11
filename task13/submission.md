# task13 answer blocks

## Tags

**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities (grid reliability & outage analysis).
**Analytical objective:** Anomaly Detection & Diagnostics.

## Final Recommendation

**Refit these 11 zones before the 2027 lightning season: BGS-F3-R1, CLB-F1, CLB-F2, CLB-F2-R1, LRD-F1-R2, MLN-F2, MLN-F4, MLN-F4-R2, PGP-F2, PGP-F4-R3 and TGP-F3-R1; and after every season refer each zone whose lightning faults since its last cyclic inspection (each fault matched to a stroke within 400 m on its recloser's own clock, with the events a memory lost or nobody has read restored) exceed what its lines would have had with sound protection, at the zone's own level learned from the seasons a later inspection confirmed it sound, by more than chance explains with that level as uncertain as those seasons leave it, at a chance below 1 in 715 a zone a season.** A rule that takes the scatter season by season refers 13 instead (it adds BGS-F3 and MPD-F2-R2, which run high whenever their protection is sound, and SNJ-F3, and drops CLB-F2, a failed zone that runs low), and one that takes each zone's level as known refers 17 and would refer a sound zone about 1.2 times a season, six times what the terms allow.

## Supplementary Questions

### lightning_referrals_2027.csv

1. One row for each of the 143 zones in the protection zones register, in the register's order: zone, feeder, substation, whether its recloser has a radio link, the date its last cyclic inspection finished, then the zone's lightning faults in each season from 2022 to 2026 (1 April to 31 October, one decimal), each fault counted once on the zone whose lines it was on, with the events a radio-less recloser's memory overwrote or that are still unread restored at the zone's own rate. The season columns total **561, 413, 593, 620 and 655** (each within 4 per cent), and the 32 zones whose reclosers are read on site total **130** in 2026 (120 to 138), of which their memories kept 87.
2. The record since each zone's last cyclic inspection: the number of its confirmed-sound seasons and its own sound level, the seasons since inspection, the zone's lightning faults in them, what its lines would have had with sound protection (the register-feature rate times the strokes within 400 m, times its own level), the ratio of the two, and the chance of that many faults or more with sound protection, judged on the faults the records hold against the expectation for the same recorded months. For the referred zones (faults within 10 per cent, expectation within 20 per cent):
   - BGS-F3-R1: 31.6 faults against 9.4 (ratio 3.38).
   - CLB-F1: 17 against 3.0 (5.68).
   - CLB-F2: 15 against 3.3 (4.59).
   - CLB-F2-R1: 28 against 8.8 (3.19).
   - LRD-F1-R2: 38 against 12.1 (3.15).
   - MLN-F2: 17 against 3.5 (4.84).
   - MLN-F4: 33 against 8.7 (3.81).
   - MLN-F4-R2: 45.8 against 9.5 (4.82).
   - PGP-F2: 27 against 4.9 (5.55).
   - PGP-F4-R3: 35.9 against 9.2 (3.92).
   - TGP-F3-R1: 39 against 8.9 (4.37).
3. Referred: yes for the 11 zones of the recommendation, no for the other 132.

### lightning_refit_2027_note.docx

4. The rule as the recommendation states it, and the 11 zones it refers for the 2027 refit.
5. Its alert load: zones referred after each season, **2** after 2022 (1 to 3), **2** after 2023 (1 to 3), **4** after 2024 (3 to 5), **8** after 2025 (7 to 10) and **11** after 2026 (10 to 12), each zone's level learned from its confirmed seasons outside the record being judged; and the sound zones a season's referrals should hold, the rule's own expected rate, about **0.14** a season (0.12 to 0.16), one in about seven seasons, where the terms' one in five (0.2) is the ceiling it stays under, not its rate.
6. Against the next cyclic inspections: the rounds of 2022-23 to 2025-26 inspected **5** zones the rule had referred after the season before (3 to 6) and confirmed all **5** (3 to 6); they found failed protection on **21** zones it had not referred (20 to 23).
7. The network's lightning faults: **561** in 2022, **413** in 2023, **593** in 2024, **620** in 2025 and **655** in 2026 (each within 4 per cent).
8. 2026's lightning faults caused by failed protection: **186** (170 to 200), the season's 655 against **469** with every zone's protection sound at its own level.
9. Lightning faults the refit should avoid in a season of average lightning: **116** (104 to 128), each referred zone valued at the state its protection had reached by the end of 2026, its 2026 season above its own sound level taken at its 2022 to 2026 mean lightning (the seasons since each failure began give 115), where the record since each inspection averaged gives 72, because most of these zones failed partway through it.
10. The chart plots each zone's lightning faults since its last inspection against what sound protection would have given it, with the line where the two are equal and the 11 referred zones marked and named; under it, a table of the referred zones and one of what simpler versions of the rule would refer and report.

## Critical Components

1. The network's lightning faults in 2022 to 2026 are **561, 413, 593, 620 and 655**, with each radio-less recloser's clock fitted read by read and the 32 radio-less zones' lost and unread months restored (**130** of 2026's, 87 kept).
2. The refit avoids **116** lightning faults in a season of average lightning because it is valued at the state each zone's protection had reached by the end of 2026: in the first season after inspection **9** of the 11 referred zones ran at less than half the multiple of their own sound level they reached in 2026, and in 2026 all **11** ran above twice it, so the record since inspection averaged (**72**) undervalues it.
3. Failed protection caused **186** of 2026's **655** lightning faults, against **469** with every zone sound at its own level.

## Step-by-Step

1. Collapsed each fault's trips and recloses in `scada_event_history_2016-12_2026-10.csv` and `recloser_event_downloads_2016-2026.csv` (each re-read event kept once, upstream breakers' sympathetic trips dropped) to its first trip, and matched it to a ground stroke in `kidlat_strokes_2016-11_2026-10.csv` within 400 m of the zone's lines in `overhead_line_routes_2026.geojson`, the strokes moved from UTC to Philippine time.
2. On the 111 zones with synchronised clocks the first trips sit within a second of a stroke; the 32 reclosers read on site keep their own clocks, whose lag to nearby strokes grows in a straight line between site visits and resets at each read, so each controller's drift and offset were fitted per read from its own trips (their battery tests run at 03:00 on the controller's own clock and carry no offset). A ten-minute window around their stamps instead counts storm trips as lightning, and nothing restored leaves 630 for 2026.
3. The downloads' event numbers jump where a memory overwrote events between reads (63 of 947 reads, 1,346 events, 18 zones), and every radio-less memory is unread since its last visit; those months' faults were restored at the zone's own faults per stroke in the same season's observed months, giving 130 on the radio-less zones in 2026 against 87 kept, and 561, 413, 593, 620 and 655 across the network.
4. Fitted a Poisson regression of each zone-season's faults on the strokes within 400 m, with the zone's construction, area and arrester shares and transformers per km from `protection_zones_register_2026.xlsx`, only on the 779 zone-seasons a later inspection in `cyclic_line_inspections_2016-2026.xlsx` found sound (the book shows 16 zones inspected clean and found failed at the next round, so a season since an inspection is unverified).
5. The confirmed seasons' residuals stay with the zone: a gamma level per zone (shape 5.74, coefficient of variation 0.42) with the seasons near Poisson fits them far better than any scatter taken season by season (2 dlogL 165.6, and 79.2 for a pooled negative binomial over Poisson), so a zone's expectation is its own level times its lines' rate, learned from its own confirmed seasons outside the record being judged.
6. Compared each zone's faults since its last inspection (terms 2(e)) with that expectation over the same recorded months and referred it when the chance, with its level as uncertain as its confirmed seasons leave it, fell below 1 in 715 (terms 3(b): one sound zone in five seasons across 143 zones): 11 zones, the weakest referred at 0.000094 and the strongest left out at 0.0036. Taking each zone's level as known instead (its estimate plugged in) refers 17: the tails are too thin for zones with few confirmed seasons, and under the levels' own uncertainty that rule would refer about 1.2 sound zones a season. A scatter taken season by season refers 13; every zone at the network rate with no level of its own 8; Poisson 22; the whole record instead of the record since inspection 7. Judged on restored counts as if counted, LRD-F2-R2 (16 recorded against 5.4 expected) would be added.
7. Ran the same rule after each season: 2, 2, 4, 8 and 11 referrals, where the season-by-season scatter gives 2, 5, 4, 10 and 13 and the known-level rule 7, 4, 5, 11 and 17; summing each zone's chance at the smallest count it would be referred at gives 0.14 sound zones a season, the rule's own rate under the budget's ceiling of 0.2.
8. Checked each inspection of 2022-23 to 2025-26 against the rule after the season before it (terms 5): 5 referred zones inspected, all 5 confirmed, 21 misses, failures too recent to have run up enough faults; the season-by-season and known-level rules each check 8 referrals, one of them found sound, and miss 19.
9. Read each referred zone's seasons since its inspection against its own sound level: in the first season after inspection 9 of the 11 ran at less than half the multiple of their own sound level they reached in 2026, and in 2026 all 11 ran above twice it, so the state its protection had reached by the end of 2026 (terms 4(c)) is its 2026 season. Summing each one's 2026 faults above its own sound level, taken at its 2022 to 2026 mean lightning, gives 116 faults avoided in a season of average lightning (the seasons since each failure began give 115); the record since each inspection averaged gives 72, because it mixes in the seasons before the failure.

No other referral set survives the files. A scatter taken season by season treats a zone's seasons as independent when the confirmed seasons show a level that stays with the zone, so it passes zones that always run high as failures and hides failed zones that run low; a level taken as known judges a zone with three confirmed seasons as if it had thirty and refers sound zones six times as often as the terms allow; with no level of its own every low-level failed zone stays hidden; Poisson ignores a scatter the confirmed seasons show; the whole record counts faults that inspections have since repaired; the logs as recorded leave the radio-less clocks drifting and their lost months empty; and the record since inspection, averaged, values the refit at states most of these zones had already left.
