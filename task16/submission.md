## Tags

**Domain:** Machine Learning Research, General Statistics & Data Science (data integration, record linkage and entity resolution: a merged health system's enterprise master patient index).
**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).

## Final Recommendation

**Run Rule B at the One Chart conversion:** it joins 39,810 pairs of records and about 5 of them are two different patients (0.25 per 2,000 automatic links, inside the policy's one). Reject Rule A, which the matching engine's chance rates put at 0.14 per 2,000 but which merges about 107 pairs of different patients (2.97 per 2,000) because Port Calder's first names run in birth cohorts within surname communities and many foreign-born patients' birth dates were recorded as 1 January; Rule C would merge about 153 pairs of twins (5.44 per 2,000) and Rule D about 164 (7.12), mostly twins registered at Rosario under a parent's SSN.

## Supplementary Questions

### one_chart_autolink_rule_evaluation.xlsx

1. Rules sheet, one row per candidate rule ordered by automatic links, with columns rule, definition, automatic links, estimated false merges, false merges per 2,000 links and within the policy: Rule A 71,728 links, 106.7 false merges (65 to 170), 2.97 per 2,000 (1.81 to 4.74), over it; Rule C 56,207 links, 153 false merges (70 to 220), 5.44 per 2,000 (2.49 to 7.83), over it; Rule D 46,046 links, 164 false merges (140 to 250), 7.12 per 2,000 (6.08 to 10.86), over it; Rule B 39,810 links, 5 false merges (0 to 15), 0.25 per 2,000 (0.00 to 0.75), inside the policy.
2. Index sheet and Overlays to split sheet: 568 Calder Bay records hold two or more patients (480 to 660), each listed with its surviving MRN, name and birth date.
3. Index sheet: 220,669 distinct patients in the converted index (217,358 to 223,979) and 76,062 patients held by both Calder Bay and Rosario (74,160 to 77,964).
4. Index sheet: 48,754 patients still under more than one active record once Rule B's links are made (47,291 to 50,217).

### one_chart_autolink_recommendation.docx

5. One page: run Rule B, with its links and false merges per 2,000; why not Rules A, C and D, each with its false merges per 2,000; the Calder Bay records that hold two or more patients; the distinct patients, the patients both indexes hold and the patients left under more than one record.

## Critical Components

1. Rule A's false merges: **106.7** (65 to 170) of its 71,728 links, **2.97 per 2,000** (1.81 to 4.74), from pairs of different patients who share first name, last name, sex and birth date.
2. Rule C's false merges: **153** pairs of twins (70 to 220) among its 56,207 links, **5.44 per 2,000** (2.49 to 7.83), none of them a pair the 2026 pilot reviewed.

## Step-by-Step

1. Read calder_bay_patient_index_2026-11-02.csv and rosario_patient_index_20261102.csv into one table of 311,965 active records, compared as halvard_match_6_specification.pdf standardizes them (names upper-cased with hyphens as spaces, unit designators off the street address, ten-digit phones, all-zero and all-nine SSNs missing).
2. Applied each rule of one_chart_empi_conversion_plan.pdf section 7.2 to every pair of active records across and within the two indexes: Rule A 71,728 links, Rule C 56,207, Rule D 46,046, Rule B 39,810.
3. Rule A: the specification's national rates put chance agreement on all four fields at about one in 10 billion pairs (5.0 merges here) and the records' own field rates at 12.1, but first names run in birth cohorts within surname communities and many foreign-born patients' birth dates sit on 1 January; counting the pairs of patients who share first name, last name, sex and birth year, each pair's chance of one birth date taken from its surname community's 1 January and 1 July shares by decade (shrunk toward the decade's), gives 106.7 false merges, 2.97 per 2,000, 32 per cent of them among Nguyen patients and 64 per cent among patients born before 1980.
4. Checked it on blood_bank_type_screen_2016-2026.csv: of Rule A's links whose records both carry results, 30 of 8,043 differ in group, 9 of them on a Calder Bay record that holds two patients and about 6 what mislabelled specimens give (25 of 23,085 records typed twice or more disagree with themselves); the 21 left against 6.1 expected give about 205 (95 per cent interval 95 to 357), but typed patients were born 8 years earlier on average than Rule A's linked patients, in the cohorts where chance agreement sits, so the groups test the estimate rather than count it; read as they stand (410) they would condemn Rule B too (97).
5. Rule C: halvard_pilot_review_2026.xlsx reviewed none of Rule C's links, because twins and nickname pairs at one address score above its review band, and the blood groups see only the twins whose groups differ (59); linking the index with what the rules never compare (two newborns of one delivery in labor_delivery_log_2006-2026.csv, two records made on one registration visit, groups that differ) keeps 153 pairs of twins apart that Rule C joins, 5.44 per 2,000.
6. Rule D: a family's SSN on several children's records makes the links whose first names are not one person's (143) look like the whole problem, but 21 of the links whose names are one person's are twins a delivery or one visit shows, so Rule D merges 164 pairs of two patients, 7.12 per 2,000.
7. Overlays: calder_bay_merge_history_2006-2026.csv shows Calder Bay's automatic merges from March 2019 joined new registrations on last name, birth date and sex alone; reading each retired record's first name against its survivor's (forms of one name in halvard_name_equivalence_table.csv and typing slips as one patient), 568 surviving records hold two or more patients, where every merge whose names differ as typed would give 1,119.
8. The linked index: Fellegi-Sunter weights fitted by EM on the candidate pairs, the evidence above keeping two patients apart and the merge history's retired records included, gives 220,669 distinct patients, 76,062 held by both indexes, and 48,754 still under more than one active record once Rule B's links are made (the specification's own fixed weights, at its automatic or its review cut-off, give figures inside the same bands).
9. Under patient_identity_policy_him-14.pdf section 3 only Rule B is inside one false merge per 2,000 automatic links (0.25), so the conversion runs it.

No other rule survives. Rule A stays over the cap however each community's 1 January share is estimated (70.8 to 113.3 false merges against a line of 35.9), Rule C from the evidence on each linked pair alone still gives 76 and Rule D from first names alone 143, and every rule read from the blood groups net of their errors leaves Rule B the only one inside; each shortcut lands on another rule: the engine's checks keep Rule A, correcting Rule A alone moves the call to Rule C, correcting Rules A and C but not D moves it to Rule D, and the blood groups read as they stand condemn every rule.
