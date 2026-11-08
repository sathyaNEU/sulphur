## Tags

**Domain:** Machine Learning Research, General Statistics & Data Science, robustness analysis (a recognizer's error rate carried to a deployment population the record never held).
**Analytical objective:** Descriptive & Distribution Analysis.

## Final Recommendation

Commit to **Ceiling C, 14 per cent**: under the frozen release 6.0 the expected share of audited dictations above 15 per cent word error rate stays under 10 per cent in the first quarter of 2027, sits between 10 and 12 in the second and third and reaches about 13 per cent in the fourth, so a 10 per cent ceiling is passed from the second quarter and a 12 per cent ceiling in the fourth. The steady record and its reweighting to 2027's hospitals (every quarter under 10 per cent) are rejected: the steadiness is each release cancelling a drift toward clinicians who began dictating once their hospital made it compulsory, and 2027 has no release and two teaching hospitals going compulsory.

## Supplementary Questions

### quality_schedule_2027_ceiling.pdf

1. The memo opens on the ceiling, 14 per cent (Ceiling C), and the first 2027 quarter that would pass each lower ceiling: 10 per cent in the second quarter, 12 per cent in the fourth.
2. A chart of each 2027 quarter's expected share of audited dictations above 15 per cent word error rate against the 10, 12, 14 and 16 per cent ceilings: the first quarter under 10, the second and third between 10 and 12, the fourth between 12 and 14, with the 2023 to 2026 audited shares before them.

### heavy_correction_2027.xlsx

3. Each 2027 quarter's lowest ceiling its share stays under: 10, 12, 12 and 14 per cent.
4. The word error rate nine in ten fourth-quarter dictations stay under: 16 per cent.

## Critical Components

1. The steady audited share (about 6 to 8 per cent since the middle of 2024) is two movements cancelling: each release lowered every clinician's error rate, while the dictation mix moved toward clinicians who began once their hospital was compulsory; with no release from February 2023 to June 2024 the share rose from about 6.6 per cent in the first half of 2023 to about 7.3 at the turn of the year.
2. Under release 6.0 about 19 per cent of the dictations of clinicians whose first dictation came on or after their hospital's compulsory date need heavy correction, against about 2 per cent for those who began before it, at every go-live on record alike.
3. 2027 brings no release (SN-2026-14) and compulsory dictation at Shannonside University (1 February 2027) and Ballykeel University (1 October 2027), whose 2,070 clinicians in post include only 503 dictating today, so the voluntary clinicians' share of dictation falls from about 68 per cent in December 2026 to under two fifths in the fourth quarter.
4. The expected share stays under 10 per cent in the first quarter, sits between 10 and 12 in the second and third and reaches about 13 per cent in the fourth: 10 per cent is passed from the second quarter and 12 per cent in the fourth, so Ceiling C (14 per cent) is the lowest no quarter passes.

## Step-by-Step

1. Cleaned dictation_audits_2023_2026.csv: the adjudicated score replaces the first pass (QA-07 4), unscorable audio is out, the word error rate is recomputed from substitutions, deletions and insertions over the reference words (the export changed from a fraction to a percentage in 2025), and the three release strings are read as one release; the quarterly shares tie to quality_reports_2023_2026.xlsx.
2. The insufficient route: the share held between about 6 and 8 per cent since the middle of 2024; carried forward it is 7.4 per cent each quarter, and reweighted to 2027's hospitals (each hospital's 2026 share at its 2027 dictations) it falls to 5.3 to 7.1 per cent, because the teaching hospitals dictate at about 1 per cent today; both commit to 10 per cent. Adding the 2024 release gap's climb gives 7.8 to 8.6 per cent and 10.
3. Measured each release's step within clinicians (each clinician's audits across releases): every release lowered error rates (4.0 by about 3 per cent, 5.0 by 6, 5.2 by 3, 6.0 by 3), so the steady share means something else rose.
4. Typed every clinician by the first month in dictation_volumes_2022_2026.csv (staff numbers reissued on a move linked through clinician_register_2026.xlsx) against the hospital's compulsory date in Schedule 2: carried to release 6.0, about 19 per cent of the dictations of those who began on or after it need heavy correction, against about 2 per cent for those who began before.
5. Built each 2027 month's dictations by hospital and kind: clinicians dictating in December 2026 at their own volume, leaving at the record's rate (about 9 per cent a year) and replaced by compulsory starters; at the two teaching hospitals every clinician in post not yet dictating (shannonside_dictation_rollout_2027.xlsx) starting on the compulsory date at the ramp the earlier go-lives show (about 23, 53 and 82 per cent of a full month in the first three months).
6. Weighted each kind's word error rates under 6.0 to each quarter's mix: the share under 10 per cent in the first quarter, between 10 and 12 in the second and third, about 13 per cent in the fourth; nine in ten fourth-quarter dictations under 16 per cent (each clinician's dictations scatter about their own level, so the percentile is of dictations, not of clinicians).
7. The ceiling: 10 per cent is passed from the second quarter and 12 per cent in the fourth; Ceiling C, 14 per cent.

No other conclusion survives. The steady share and its hospital reweighting read the teaching hospitals' clinicians as the few who chose to dictate there; giving 2027's new dictators the recent starters' level (10.3 per cent in the fourth quarter) mixes those who chose with those who had to, and stops at 12; every projection that types clinicians by their start against the compulsory date, with the release held, lands on 14.
