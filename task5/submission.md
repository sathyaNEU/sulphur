## Tags

**Domain:** Other, Survey Research & Official Statistics (census, register and administrative-data quality).  
**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).

## Final Recommendation

Certify Garrow and Ostrom for the 2027 Community Transition Fund: their December 2026 covered jobs are an estimated 3.0 and 3.1 per cent below December 2025 once each outstanding report is read by whether its usual transmission arrived, and no other county reaches the line (the lowest, Kittredge, is at -1.2). The field's imputation, carrying every outstanding employer's September jobs by its county's reporting employers, designates no county (Garrow 0.3, Ostrom -0.5), because it keeps the jobs of employers missing from transmissions that arrived, most of which had shed jobs or closed.

## Supplementary Questions

### ctf_certification_december_2026.xlsx

1. The Certification sheet names the designated counties at the top, Garrow and Ostrom, under section 4 of the Act, above a table with one row per county in county-code order: county code, county, December 2025 jobs, December 2026 jobs from the reports received, December 2026 jobs estimated for employers whose report had not arrived, December 2026 jobs, change on December 2025 (per cent) and designated, with a state row; jobs are rounded to the nearest hundred.
2. December 2026 jobs: Bray 20,800; Calder 104,800; Corliss 17,900; Fenwick 23,100; Garrow 31,600; Hadley 32,000; Kittredge 11,900; Linden 46,600; Merritt 54,300; Ostrom 27,100; Pell 32,500; Talcott 16,300; Whitcomb 45,400; Sayre 15,100; state 479,600.
3. Of those, estimated for employers whose report had not arrived: Bray 700; Calder 6,100; Corliss 800; Fenwick 700; Garrow 1,200; Hadley 3,000; Kittredge 500; Linden 3,700; Merritt 2,100; Ostrom 900; Pell 1,500; Talcott 700; Whitcomb 2,300; Sayre 700; state 24,900.
4. Change on December 2025, per cent: Bray -0.9; Calder 1.6; Corliss 0.0; Fenwick 0.3; Garrow -3.0; Hadley 1.3; Kittredge -1.2; Linden 1.1; Merritt -0.9; Ostrom -3.1; Pell 0.5; Talcott 0.3; Whitcomb 0.6; Sayre 1.5; state 0.1.
5. The chart is a column chart of the fourteen counties' changes with the minus 2.0 per cent line drawn across it; Garrow (-3.0) and Ostrom (-3.1) are the only columns below the line.

### ctf_employer_jobs_december_2026.csv

6. One row for each employer liable for the fourth quarter of 2026 and each county in which it has a worksite, 28,558 rows, with columns account_no, legal_name, county_code, county, report_received (Y or N), december_2026_jobs (as reported or estimated, to one decimal) and basis. The 27,657 liable accounts are 23,383 with a report received and 4,274 without, of which 2,538 are in a transmission that had not arrived, 496 report after the cutoff every quarter, 636 are missing from a transmission that arrived or late for the first time and 604 have no third-quarter report either.

## Critical Components

1. Of the **4,274** reports outstanding at the cutoff, **2,538** belong to employers whose usual transmission (the reports received in the same second as theirs for the third quarter) had not arrived either, and **636** to employers missing from a transmission that arrived or late for the first time.
2. On the quarters 2024Q1 to 2025Q3, whose outstanding employers have all since filed or been inactivated, employers missing that way kept **0.29** of their September jobs in December, against **0.97** for employers whose transmission was late.
3. Garrow's December 2026 covered jobs are an estimated **31,600**, **-3.0 per cent** on December 2025; Ostrom's **27,100**, **-3.1 per cent**.

## Step-by-Step

1. Conformed ui_quarterly_reports_2023q1_2026q4.csv (the latest version of each report received by 15 February 2027, a resubmission once), the liable accounts from ui_employer_accounts_2027-02-15.csv and ui_account_status_history_2023-2027.csv (an account out from an inactivation, closure or transfer effective by the quarter's first day) and ui_multiple_worksite_reports_2023q1_2026q4.csv for worksite counties: 27,657 liable accounts, 23,383 reports received, 4,274 outstanding.
2. Took December 2025 from the closed fourth-quarter 2025 reports by worksite county: 478,900 jobs statewide, the same as covered_employment_by_county_2025q4.xlsx.
3. The shallow read: imputed every outstanding employer's December from its September 2026 jobs moved by the reporting employers' change in its county and supersector, an employer missing two quarters as ceased; no county falls 2.0 per cent (Garrow 0.3, Ostrom -0.5).
4. Rebuilt the payroll agents' transmissions from received_at (three or more electronic reports in the same second) and read each outstanding employer by whether its third-quarter transmission-mates had reported (either none of them had or at least 0.67 of them had), giving 2,538 in late transmissions, 636 missing alone or late for the first time, 496 late every quarter and 604 with no third-quarter report.
5. Measured what such employers turned out to have at the 2024Q1 to 2025Q3 cutoffs, each one resolved since by a late report or an inactivation counted at nought: missing alone kept 0.29 of September, a late transmission 0.97, two quarters missing 0.002; the six months before the flash read 0.72 because their closures are not yet recorded, and dropping the employers that never filed reads 0.70.
6. Carried each outstanding employer at those shares, a seasonal lake resort at its own December-to-September pattern.
7. Summed by worksite county: Garrow -3.0 and Ostrom -3.1 per cent, Kittredge next at -1.2; designated Garrow and Ostrom.

No other conclusion survives. Reading every outstanding report as if it had kept its September jobs designates no county and is refuted by the closed quarters, where employers missing alone kept 0.29 of their September jobs. Taking every payroll agent's client as late with its agent designates Ostrom, but Garrow's missing employers are agent clients whose transmissions arrived. Reading their outcome from the latest quarters (no county) or without the employers that never filed (no county) counts survivors only, because those employers are closed and inactivated later. Counting only the reports received designates 14 counties and breaks section 2 of the Act, which counts every liable employer whether or not its report has arrived.
