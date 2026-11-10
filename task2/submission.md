## Tags

**Domain:** Machine Learning Research, General Statistics & Data Science, robustness analysis (a recognizer's error rate carried to a deployment population the audit record never held).
**Analytical objective:** Descriptive & Distribution Analysis.

## Final Recommendation

Commit to **Ceiling C, 14 per cent**: under the frozen release 6.0 the expected share of audited dictations above 15 per cent word error rate is about 9.6 per cent in the first quarter of 2027, 11.2 and 11.6 in the second and third and 13.0 in the fourth, so a 10 per cent ceiling is passed from the second quarter and a 12 per cent ceiling in the fourth. Rejected: carrying 2026's 9.0 per cent forward (Ceiling A), giving the university hospitals' 2027 starters the smaller hospitals' compelled clinicians' rate (16.1 per cent in the fourth quarter, above every ceiling offered), and reading the university hospitals at the smaller hospitals' acoustic level (11.4 per cent, Ceiling B).

## Supplementary Questions

### quality_schedule_2027_ceiling.pdf

1. The memo opens on the ceiling, 14 per cent (Ceiling C), and the first 2027 quarter that would pass each lower ceiling: 10 per cent in the second quarter, 12 per cent in the fourth.
2. A chart of each 2027 quarter's expected share against the 10, 12, 14 and 16 per cent ceilings, the 2023 to 2026 audited shares before it: the first quarter about 9.6 per cent, the second about 11.2, the third about 11.6 and the fourth about 13.0 (12.9 to 13.0 under every reasonable variant of the method).

### heavy_correction_2027.xlsx

3. Each 2027 quarter's lowest ceiling its share stays under: 10, 12, 12, 14 per cent.
4. Each university hospital's expected fourth-quarter share: Shannonside University about 14.9 per cent (14.3 to 15.5), Ballykeel University about 12.9 per cent (12.3 to 13.5).
5. Ballykeel University Hospital's fourth-quarter dictations: about 88,000 (85,000 to 91,000), about 43,000 of them from the clinicians who start there in October.
6. The word error rate nine in ten fourth-quarter dictations stay under: about 16.1 per cent (15.8 to 16.3).
7. The group's audited share went from 10.1 per cent in the second quarter of 2023 to 7.8 per cent in the last quarter of 2026, a change of -2.2 points: the releases took off about 4.1 points (3.5 to 4.7, by which year's mix they are measured on) and the changing mix of dictations put back about 1.9 (1.2 to 2.5).

## Critical Components

1. Measured within the clinicians who dictated at two of the group's hospitals under a new staff number, dictating at Shannonside University raises a clinician's word error rate by about **5.0 per cent** and at Ballykeel by about **8.6 per cent** against the six smaller hospitals' average; the low heavy-correction shares of the clinicians dictating there now (**4.1** and **4.4 per cent**) are who chose to dictate, not the place.
2. The 2027 starters are most of each university hospital's staff (**631 of 818** at Shannonside University, **918 of 1,250** at Ballykeel): their heavy-correction share is the whole staff's, at the smaller hospitals' levels for their grades and specialties with the hospital's own effect, less what the volunteers already carry, about **18.2 per cent** and **21.7 per cent**, not the **27.7 per cent** of the smaller hospitals' compelled clinicians, the few who held out where most had chosen.
3. At the six earlier go-lives the compelled clinicians dictated about **15**, **36** and **64 per cent** of a settled month in the first three months as departments switched over, so Ballykeel's October go-live adds about **43,000** fourth-quarter dictations, not the **116,000** of a full-volume start.
4. Releases 5.0, 5.2 and 6.0 cut a clinician's error by about **10.6 per cent** together, taking about **4.1 points** off the audited share between the second quarter of 2023 and the end of 2026, while the mix of dictations put about **1.9** back.

## Step-by-Step

1. Cleaned dictation_audits_2023_2026.csv (the adjudicated score replaces the first pass under QA-07 4, unscorable audio out, the error rate recomputed from substitutions, deletions and insertions over the reference words, the three release strings read as one release): every quarter ties to quality_reports_2023_2026.xlsx, 10.1 per cent in the second quarter of 2023 and 7.8 per cent at the end of 2026.
2. Linked every staff number to its clinician through previous_staff_no in clinician_register_2026.xlsx (248 moves between the group's hospitals) and fitted each audited dictation's log error as the clinician's own level, the release in force and the hospital dictated at: the 4.0 to 6.0 releases cut error by about 10.6 per cent, so the releases took about 4.1 points off the share and the mix of dictations put about 1.9 back. Putting the whole change to the releases (-2.2 points), using the release notes' LCB-2 cuts (-5.9) or a shift-share by hospital (-1.7) misattributes it.
3. Read each hospital's own effect from the clinicians seen at two hospitals: Shannonside University about 5.0 per cent and Ballykeel about 8.6 per cent worse than the six smaller hospitals' average. A raw comparison of the clinicians dictating at each hospital now reads the university hospitals as the best places to dictate, because only the few who chose to dictate appear there.
4. Typed the smaller hospitals' clinicians by appointment and first dictation against Schedule 2's compulsory dates: those who chose carry 5.7 per cent heavy correction under 6.0, those hired after a go-live 10.0, those compelled at it 27.7, and uptake before the go-lives ran from 58 to 87 per cent, so the compelled are the most selected where most had chosen.
5. Built each university hospital's whole staff from the register (in post on 31 December 2026, as shannonside_dictation_rollout_2027.xlsx counts them) at the smaller hospitals' levels for each grade and specialty plus the hospital's own effect (14.9 and 16.9 per cent heavy correction), less the clinicians already dictating: the starters carry about 18.2 per cent at Shannonside University and 21.7 at Ballykeel. The smaller hospitals' compelled clinicians' rate (27.7) would put the fourth quarter at 16.1 per cent, and their pooled compulsory starters land on the ceiling only by coincidence, missing the third quarter (12.1 per cent) and both university hospitals.
6. Measured the switch-over at the six go-lives in dictation_volumes_2022_2026.csv (the compelled clinicians' dictations per clinician in post by month from the compulsory date against their own months six to eleven, the calendar taken out): about 15, 36 and 64 per cent in the first three months, so Ballykeel's fourth quarter holds about 88,000 dictations; starting everyone on the date at full volume gives 161,000, and at their own first months' volume 133,000.
7. Projected each 2027 month hospital by hospital with recognition held at 6.0 (SN-2026-14) and the staff in post held as on 31 December 2026: the quarters come to about 9.6, 11.2, 11.6 and 13.0 per cent, Shannonside University's fourth quarter 14.9 and Ballykeel's 12.9, and the lowest ceilings are 10, 12, 12, 14.
8. Mixed the groups' dictation-level error distributions to the fourth quarter's dictations: nine in ten stay under about 16.1 per cent (reading it off clinicians' typical levels gives 13.5, because each clinician's dictations scatter about their level).
9. The ceiling: 10 per cent is passed from the second quarter and 12 per cent in the fourth, so Ceiling C, 14 per cent.

No other conclusion survives. The 2026 record (9.0 per cent) and the record's highest quarter (11.3) read the university hospitals as the few who dictate there now. Without each hospital's own effect, measured only through the clinicians who moved, the fourth quarter falls to 11.4 and the ceiling to 12; with the smaller hospitals' compelled clinicians standing in for the starters it rises to 16.1, above every ceiling; and with the go-lives at full volume it reaches 14.6 and 16. Only the staff less its volunteers, with the place's own effect and the switch-over, holds every quarter at or under 14.
