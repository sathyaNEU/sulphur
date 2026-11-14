## Tags

**Domain:** General Statistics & Data Science (data integration, record linkage and entity resolution: a merged health system's enterprise master patient index).
**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).

## Final Recommendation

**Run Rule B at the One Chart conversion:** it joins 35,566 pairs of records and about 3 of them are two different patients (0.17 per 2,000 automatic links, inside HIM-14's one) once its 5 blood-group mismatches are explained (3 on Calder Bay records that already hold two patients, split before the conversion; 2 left as false merges). Reject Rule A (about 60 false merges, 1.85 per 2,000: names cluster by community and birth year and the men who came to work the boats carry 1 January document dates, which the engine's national rates (0.14) and the blood bank's mostly older patients do not see), Rule C (about 41 pairs of twins, 1.63 per 2,000, of which the delivery log and the registration visits show only 16) and Rule D (104, 4.86).

## Supplementary Questions

### one_chart_autolink_rule_evaluation.xlsx

1. Rules sheet, one row per candidate rule ordered by automatic links, with columns rule, definition, automatic links, estimated false merges, false merges per 2,000 links and within the policy: Rule A 64,484 links, 59.5 false merges (42 to 71), 1.85 per 2,000 (1.31 to 2.20), over it; Rule C 50,411 links, 41 false merges (34 to 48), 1.63 per 2,000 (1.35 to 1.90), over it; Rule D 42,835 links, 104 false merges (85 to 191), 4.86 per 2,000 (3.97 to 8.92), over it; Rule B 35,566 links, 3 false merges (0 to 8), 0.17 per 2,000 (0.00 to 0.45), inside the policy; each rule's links are exact under the specification's standardization and within 0.1 per cent of these under another careful reading of it.
2. Index sheet and Overlays to split sheet: 556 Calder Bay records hold two or more patients (471 to 601), each listed with its surviving MRN, name and birth date.
3. Index sheet: 212,402 distinct patients in the converted index (209,215 to 215,588) and 69,318 patients held by both Calder Bay and Rosario (67,585 to 71,051).
4. Index sheet: 44,567 patients still under more than one active record once Rule B's links are made (43,229 to 45,904).
5. Index sheet: 124 of Rule B's links touch a record that holds two or more patients (105 to 144), 119 such records in all (101 to 138), each split before those links are made.

### one_chart_autolink_recommendation.pdf

6. One page: run Rule B, with its links and false merges per 2,000 and how its blood mismatches are explained; why not Rules A, C and D, each with its false merges per 2,000; the Calder Bay records that hold two or more patients and the links that touch them; the distinct patients, the patients both indexes hold and the patients left under more than one record.

## Critical Components

1. Rule A's false merges: **59.5** (42 to 71) of its 64,484 links, **1.85 per 2,000** (1.31 to 2.20, against one), from pairs of different patients who share first name, last name, sex and birth date; 34 per cent of them among men born since 1975 and 12 per cent among patients born before 1960.
2. Rule C's false merges: **41** pairs of twins (34 to 48) among its 50,411 links, **1.63 per 2,000** (1.35 to 1.90), of which the delivery log and one registration visit show only **16**.
3. Rule B's false merges once its blood mismatches are explained: **3** (0 to 8), **0.17 per 2,000**: of its **5** links whose records differ in ABO group or Rh type, **3** touch a Calder Bay record that holds two patients (2 of them under one SSN), **0** a record whose own typings disagree, and **2** are left as false merges, beside the twins one registration visit shows.

## Step-by-Step

1. Read calder_bay_patient_index_2026-11-02.csv and rosario_patient_index_20261102.csv into one table of 294,713 active records, compared as halvard_match_6_specification.pdf standardizes them (names upper-cased with hyphens as spaces, unit designators off the street address, ten-digit phones, all-zero and all-nine SSNs missing).
2. Applied each rule of one_chart_empi_conversion_plan.pdf section 7.2 to every pair of active records across and within the two indexes: Rule A 64,484 links, Rule C 50,411, Rule D 42,835, Rule B 35,566; their lines under HIM-14 are 32.2, 25.2, 21.4 and 17.8 false merges.
3. Rule A: the specification's national rates put chance agreement on all four fields at 4.4 merges here and the records' own field rates at 8.5, both inside its line; counting the pairs of patients who share first name, last name, sex and birth year, each pair's chance of one birth date taken from its surname community's 1 January and 1 July shares by decade (shrunk toward the decade's), gives 59.5, 1.85 per 2,000, 34 per cent of it among men born since 1975, who came to work the boats and the yards with document dates.
4. The blood bank cannot settle Rule A: of its links whose records both carry results (3,730), 5 differ in ABO group or Rh type, 3 on a record that holds two patients and about 2.0 what mislabelled specimens give; among the links Rule B does not make, 0 discordant pairs carry different SSNs, which looks like the national rate; but typed patients were born 27 years earlier on average than Rule A's linked patients, so the groups see almost none of the men and children where its chance merges sit (net of both errors, 1, 95 per cent interval 0 to 138).
5. Rule C: halvard_pilot_review_2026.xlsx reviewed none of Rule C's links, and the delivery log's two newborns of one delivery and the records made on one registration visit document only 16 twin pairs among them, under its line of 25.2; but most twins here were registered on separate visits or born before their families came to Port Calder. Linking the index on every field the rules do not compare (each twin's own SSN, phone and visit history, with the documented pairs kept apart) keeps 41 pairs of twins apart that Rule C joins, 1.63 per 2,000, at a match probability of 0.3 or 0.7 alike.
6. Rule D: a family's SSN on several children's records joins 104 pairs of two patients, 4.86 per 2,000; the delivery log and one visit alone already show 59.
7. Overlays: calder_bay_merge_history_2006-2026.csv shows Calder Bay's automatic merges from March 2019 joined new registrations on last name, birth date and sex alone; reading each retired record's first name against its survivor's (forms of one name in halvard_name_equivalence_table.csv and typing slips as one patient), 556 surviving records hold two or more patients, where every merge whose names differ as typed would give 1,028.
8. Rule B: 5 of its typed links differ in ABO group or Rh type, which read as false merges and scaled from the typed links would put it at 122, over its line of 17.8; 3 of them touch one of those overlaid records (the record also holds a second patient's typing; HIM-14 section 4 splits it before the conversion), 0 are a record whose own typings disagree, and 2 are left as false merges, which with the twins one visit shows gives 3, 0.17 per 2,000. 124 of its links touch 119 overlaid records.
9. The linked index: Fellegi-Sunter weights fitted by EM on the candidate pairs, the evidence above keeping two patients apart and the merge history's retired records included, gives 212,402 distinct patients, 69,318 held by both indexes, and 44,567 still under more than one active record once Rule B's links are made.
10. Under patient_identity_policy_him-14.pdf section 3 only Rule B is inside one false merge per 2,000 automatic links (0.17), so the conversion runs it.

No other rule survives. Rule A stays over its line however its communities' 1 January shares are estimated (49.5 to 61.6 against 32.2), Rule C on the linkage at either threshold (41), Rule D on names alone or with blood groups (100 to 166), and Rule B under its line on every reading of its mismatches (3 on each against 17.8). Each shortcut lands on another answer: the documented failures counted with Rule B's mismatches held, as a careful but hurried pass reads the files, runs Rule A; correcting Rule A alone runs Rule C; holding Rule B's mismatches with A and C right runs no rule; the blood groups read as they stand condemn every rule.
