## Tags

**Domain:** Energy Systems & Utilities, energy efficiency and demand response evaluation (tariff and demand-response evaluation).
**Analytical objective:** Experiment & Causal Analysis.

## Final Recommendation

**Make Quillpoint Sequence the EV Overnight rate's charging default for 2027 and carry 13 transformer replacements ($196,700) in the 2027 work plan**: at $249,200 for the year it costs less than Quillpoint Stagger ($397,100) or the members' own schedules ($812,200). This rejects Stagger, which the pilot's average managed night shows clearing all but 2 transformers ($52,600 for the year), because a random start still lets the few chargers on a small transformer land together on some night of the summer: replayed night by night, Stagger leaves 29.7 over.

## Supplementary Questions

### ev_overnight_default_2027_memo.docx

1. The call, in the memo's title and first paragraph: Quillpoint Sequence as the 2027 default, with 13 transformer replacements in the 2027 work plan (between 12 and 14) costing $196,700 (between $178,500 and $214,900).
2. Transformers serving the rate's chargers that each option leaves over their limit in a summer like 2026: members' own schedules 53 (between 52 and 55), Quillpoint Stagger 29.7 with each transformer at its chance of being over (between 28.5 and 31.0), Quillpoint Sequence 13 (between 12 and 14).
3. The platform's fee for the 1,313 enrolled chargers for 2027: own schedules $0, Stagger $23,600 ($18 a charger), Sequence $52,500 ($40 a charger).
4. What the replacements would cost at DPS-7's installed costs: own schedules $812,200 (between $801,400 and $832,900), Stagger $373,500 (between $360,300 and $386,300), Sequence $196,700 (between $178,500 and $214,900).
5. The total for 2027: own schedules $812,200 (between $801,400 and $832,900), Stagger $397,100 (between $383,900 and $410,000), Sequence $249,200 (between $231,000 and $267,400).
6. The pilot's managed charging took 4.95 kW per enrolled charger off the 23:00 to 23:15 interval in July and August 2026 (within 0.1 kW): 0.34 kW in the managed quarter against 5.29 kW on the owners' own schedules.
7. Chargers enrolled on the rate on 1 November 2026: 1,313.
8. The call changes if Sequence's fee rises above about $153 per charger for the year (between $128 and $177), where Stagger would cost the same.
9. A chart of the transformers over their limit under each option, stacked by transformer size.

### ev_overnight_transformers_2027.csv

10. 382 rows, one for each transformer serving an enrolled charger, with its location, substation, kVA, 15-minute limit in kW, homes, enrolled chargers, and its summer peak in kW under each option: own schedules (53 marked over), Stagger (its mean peak and its chance of being over, the chances summing to 29.7) and Sequence (13 marked over), with the replacement cost.

## Critical Components

1. Quillpoint Stagger leaves **29.7** transformers over their limit (between 28.5 and 31.0), not the **2** the pilot's average managed night suggests.
2. Quillpoint Sequence leaves **13** transformers over (between 12 and 14): its rule has to start a late charger alongside others on heavy nights, and every later charger in the queue then waits for it too, where one charger at a time would leave **3**.
3. The members' own schedules leave **53** transformers over (between 52 and 55), not the **44** the 2026 meters show with a quarter of the chargers under Stagger.
4. The pilot's managed charging took **4.95 kW** per enrolled charger off 23:00 to 23:15.

## Step-by-Step

1. From `ev_overnight_roster_2026-11-02.csv`, with the re-imported rows dropped, each swapped charger followed to its replacement and the closed ones left out: 1,313 chargers enrolled on 1 November 2026.
2. Through `gis_service_points_2026-10-30.csv`, the transfers in `distribution_work_orders_2025_2026.xlsx` and `ami_meter_exchanges_2026.csv`, they sit on 382 transformers; each one's nameplate is the register's as corrected by the change-outs (DPS-7 section 4).
3. Each transformer's base is its homes' hourly reads (the three `mdm_hourly_` files, re-sent rows dropped) less the enrolled chargers' own charging from `quillpoint_sessions_2024-06_2026-09.csv`, put from UTC onto local daylight time (six hours behind UTC, where the sessions line up with the charging in the hourly reads), each hour then brought to the quarter-hour by DPS-7 Table 2's peaking factor for the transformer's nameplate (from 1.15 on the smallest units down to 1.10 on the largest), monitored or not (DPS-7's Table 2, EV-4 4.1).
4. The pilot's randomised comparison (`pilot_assignment_2025.csv`): the managed quarter charged 0.34 kW per enrolled charger at 23:00 to 23:15 against 5.29 on own schedules. Carried to the transformers as the managed quarter's average night times their chargers, it puts Stagger at 2 transformers over, the shallow read.
5. The limit is each transformer's single highest quarter-hour of the summer (DPS-7 2.1), so Stagger is replayed night by night on every charger's 2026 sessions with its random start drawn 400 times: the few chargers on a small transformer still coincide on some nights, and Stagger leaves 29.7 over at their chance (EV-4 4.3).
6. Sequence, never piloted, is run by its rule in `quillpoint_proposal_2027.xlsx` on each night's plug-ins, energy, charge times and unplug times (each session drawing its energy over its recorded charge time, ready-by at the unplug time rounded down to the quarter-hour, the earlier plug-in first, each charger waiting for every one before it, a charger started late at its latest start included): on heavy nights a late charger starts alongside, and 13 transformers stay over, where one charger at a time would leave 3.
7. Own schedules are rebuilt for every charger (its own-schedule sessions, the managed quarter's from summer 2024, or the usual charging the member gave at enrolment): 53 over, where the 2026 loads as metered give 44.
8. Each option's charging goes in at the quarter-hour it would be drawn, on top of that base, and each transformer's highest quarter-hour of July and August is set against its limit (DPS-7 2.1); the 48 monitored transformers are read like every other, from their homes' hourly reads.
9. At DPS-7's installed costs and Quillpoint's fees, Sequence costs $249,200, Stagger $397,100 and own schedules $812,200; Sequence stays cheapest until its fee passes about $153 a charger.

No other conclusion survives. The pilot's average night prices a coincidence it cannot see, so it files Stagger with 2 to replace; taking Sequence as the pilot's managed quarter files Stagger again, and taking it as one charger at a time files Sequence with 3 replacements, where its own rule leaves 13. The 2026 meters are not the members' own schedules. With the replay's frame filed (the queue waiting for a late charger, ready-by at the unplug time, DPS-7's peaking factors), the readings the files still leave open (each charger on its declared setting, the own three-quarters at their recorded starts, the sessions the window cannot fit started early, other draws) land Sequence between 12 and 14 and the call nowhere else.
