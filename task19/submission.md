## Tags

**Domain:** Other, Survey Research & Official Statistics (nonresponse, calibration and measurement-error adjustment).  
**Analytical objective:** Descriptive & Distribution Analysis.

## Final Recommendation

**Certify Port Ardain, Ballinrea, Drumcastle, Tullaghvane as qualifying for the 2027/28 urban-services supplement, report Newbrook as too close to call (chance of 25,000 or more 0.57, so half rate under circular 2026/14 paragraph 3.2), and Fort Larrick, Carnmoyle, Rossmullan, Glenarra, Loughmeen, Ardvale, Fennabeg as not qualifying**, on estimated usual residents of 319,260 for Kilvarra (90 per cent interval 315,700 to 322,800). Reject the register's counts, which put Carnmoyle and Newbrook over the line; the 328,400 that reading the matcher's links as the register's coverage and assuming independence gives, with Newbrook qualifying on a national interval of plus or minus 0.6 per cent; and the rolled-forward 325,624 as a check on either, because it misses the same emigrants the register still lists.

## Supplementary Questions

### kilvarra_district_population_mid2026.xlsx

1. An "Estimates" sheet with one row per district and a Kilvarra row: usual residents on 30 June 2026, each district within 1.0 per cent and Kilvarra within 0.6 per cent: Port Ardain 55,480; Ballinrea 40,000; Drumcastle 32,830; Fort Larrick 22,540; Tullaghvane 26,000; Carnmoyle 24,200; Newbrook 25,050; Rossmullan 18,800; Glenarra 16,860; Loughmeen 21,910; Ardvale 14,670; Fennabeg 20,910; Kilvarra 319,260.
2. Beside each estimate its 90 per cent interval; for Kilvarra 315,700 to 322,800, a half-width of 1.1 per cent (between 0.75 and 1.45 per cent). Tullaghvane 25,280 to 26,720; Carnmoyle 23,760 to 24,640; Newbrook 24,560 to 25,550.
3. The supplement column: Port Ardain, Ballinrea, Drumcastle, Tullaghvane qualify; Newbrook too close to call, with a chance of 25,000 or more of 0.57 (within 0.16); Fort Larrick, Carnmoyle, Rossmullan, Glenarra, Loughmeen, Ardvale, Fennabeg do not qualify.
4. A "Register to estimate" sheet: for each district its register count, the entries that are not correct for the district (people who left Kilvarra or died, duplicate registrations and people living elsewhere in Kilvarra), the residents listed in another district and the residents on no list, adding to the estimate. Entries not correct for the district, each within 8 per cent: Port Ardain 9,150; Ballinrea 5,640; Drumcastle 4,330; Fort Larrick 2,380; Tullaghvane 3,660; Carnmoyle 3,440; Newbrook 3,070; Rossmullan 2,340; Glenarra 1,560; Loughmeen 2,420; Ardvale 1,620; Fennabeg 2,350.
5. Residents listed in another district, each within 25 per cent (or 40 people): Port Ardain 1,470; Ballinrea 1,150; Drumcastle 1,950; Fort Larrick 670; Tullaghvane 1,810; Carnmoyle 690; Newbrook 1,230; Rossmullan 540; Glenarra 550; Loughmeen 980; Ardvale 460; Fennabeg 850. Residents on no list, each within 25 per cent (or 40 people): Port Ardain 2,770; Ballinrea 1,810; Drumcastle 1,500; Fort Larrick 840; Tullaghvane 1,080; Carnmoyle 1,000; Newbrook 1,090; Rossmullan 630; Glenarra 480; Loughmeen 740; Ardvale 480; Fennabeg 830.
6. A "National bridge" sheet from the rolled-forward 325,624 to the estimate: a gap of 6,360 (within 0.6 per cent of the national figure), of which emigrants since mid-2021 never recorded in the accounts 6,920 (within 15 per cent), arrivals on the border record missing from the accounts 608 (exact), and a remainder of 50.
7. The share of the coverage survey's residents (serving personnel aside) on their own district's list, missed and false links counted: Kilvarran citizens 95.0 per cent (within 0.6 point), others 84.7 per cent (within 2.5 points).

### memo_district_estimates_mid2026.docx

8. One to two pages for the Commission: the call with each close district's chance, how the estimates were made, how sure they are, and why they differ from the register and from the rolled-forward estimate, with the same figures as the workbook.

## Critical Components

1. The matcher links 92.2 per cent of the survey's Kilvarran citizens and 71.8 per cent of others to their own district's list, but the clerical review shows it misses true links (recall 97.0 and 83.0 per cent): on the list are **95.0** and **84.7 per cent**.
2. The register and the survey miss the same young men: births and survival put men per woman above the estimate's, so men aged 18 to 29 are raised by **1.086** and 30 to 44 by **1.116** (each within 0.04).
3. Kilvarra's 90 per cent interval is **315,700 to 322,800** (plus or minus 1.1 per cent); resampling the survey blocks with the linkage correction and the raising factors held fixed gives plus or minus 0.6.
4. The rolled-forward estimate of 325,624 is **6,360** above the estimate; **6,920** emigrants since mid-2021 are still listed and missing from the accounts, against 608 arrivals the accounts left out.

## Step-by-Step

1. Placed every register entry in the district its postcode belongs to through the postcode directory (codes retired in 2024 included, keying differences removed), and the survey's people and the follow-up's entries by their block.
2. Linked the survey's people to the register on names, dates of birth, sex and postcodes, allowing other romanisations, nicknames and Irish forms, swapped day and month, defaulted dates of birth and name order swapped; one person per record. On the clerical review the matcher links 97.0 per cent of Kilvarran citizens who are on their own district's list and 83.0 per cent of others; the table of verified status against linked status, by citizenship and sex, gives each survey person their chance of being on their own district's list (95.0 and 84.7 per cent overall).
3. Measured each district's correct entries from the follow-up: resident at the address, or moved within the district; movers with no district recorded at the share the district's known movers give; people the household could not place and vacant addresses at the district's placed outcomes; no-contact entries at the chance a logistic model fitted on the resolved ones gives (last attendance, registration date, dwelling type, age, sex, district). Entries not correct: Tullaghvane 3,660, Carnmoyle 3,440, Newbrook 3,070.
4. Divided each district's correct entries, by age group and sex, by the share of the survey's people in that cell on the district's list; serving personnel came from the Defence Forces' return instead.
5. Built men per woman for Kilvarrans aged 18 to 29 and 30 to 44 from births by sex and the life table's survival, and compared it with the estimate's (serving personnel added back on that side): raising factors 1.086 and 1.116 applied to every district's men of those ages. Independence leaves Kilvarra 5,900 lower.
6. Resampled the survey's blocks within districts and repeated every step, the clerical review's table and the raising factors included: Kilvarra 319,260 (315,700 to 322,800); each district's chance of 25,000 or more from its estimate and spread, and the call under paragraph 3.2.
7. Bridged each register count to its estimate, the parts adding up, and the rolled-forward figure to the estimate: emigrants since mid-2021 still listed (the follow-up's people who left Kilvarra, dated by the year they left, those not known at the address shared out as the district's known outcomes are) less those whose departure the border system recorded: 6,920.

No other call survives. Reading the matcher's links as coverage lifts the districts by 2.3 to 4.9 per cent, and independence lowers them by 1.5 to 2.1 per cent; with both, and with the survey alone resampled (plus or minus 0.6 per cent for Kilvarra against 1.1), Newbrook reads as qualifying. Calibrating to the rolled-forward total, or reading the register's own counts, carries the emigrants both still hold, and puts Carnmoyle and Newbrook over the line.
