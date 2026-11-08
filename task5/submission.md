## Tags

**Domain:** Survey Research & Official Statistics (Census, register & administrative-data quality: a municipality's vacancy share estimated from the cadastre, the meter data hub's metering points and hourly values and the population register, with the register's overcoverage, undercoverage and net bias).
**Analytical objective:** Data Extraction & Conformation (ETL).

## Final Recommendation

**Five of the ten municipalities qualify for the 2027 grant: Tverrvika (5802), Hesteby (5803), Solmoen (5805), Ørnevik (5807) and Fjordeid (5809).**
Their vacancy shares run from 5.4 to 8.2 per cent against the regulation's 5.0; the highest share below the line is Snøholt's 4.7 per cent. Not none, which a consumption floor anywhere from 1 to 10 kWh a day gives, because an empty dwelling in November is left heated and uses more electricity than many lived-in ones; not Tverrvika and Ørnevik alone, which a morning or evening rise over the night gives, because 70 empty dwellings were heated on a timer that rises at the same hours every day; and not all 10, which the population register's empty dwellings give, because the regulation counts who lived there, not who was registered.

## Supplementary Questions

### vacancy_grant_certification_2027.docx

1. Qualifying municipalities, named first in the letter: Tverrvika (7.3 per cent), Hesteby (6.4 per cent), Solmoen (6.5 per cent), Ørnevik (8.2 per cent) and Fjordeid (5.4 per cent).
2. A table of all ten municipalities with counted dwellings, vacant dwellings, vacancy share and its 90 per cent interval, and whether each qualifies; the intervals of Tverrvika, Hesteby and Ørnevik lie wholly above 5.0 per cent:
   - Brekkevoll (5801): 66 vacant of 1,640 counted dwellings, 4.0 per cent
   - Tverrvika (5802): 38 vacant of 520 counted dwellings, 7.3 per cent, qualifies
   - Hesteby (5803): 63 vacant of 980 counted dwellings, 6.4 per cent, qualifies
   - Kvernhaug (5804): 33 vacant of 860 counted dwellings, 3.8 per cent
   - Solmoen (5805): 28 vacant of 430 counted dwellings, 6.5 per cent, qualifies
   - Ravnsund (5806): 34 vacant of 740 counted dwellings, 4.6 per cent
   - Ørnevik (5807): 31 vacant of 380 counted dwellings, 8.2 per cent, qualifies
   - Langgrav (5808): 36 vacant of 1,120 counted dwellings, 3.2 per cent
   - Fjordeid (5809): 30 vacant of 560 counted dwellings, 5.4 per cent, qualifies
   - Snøholt (5810): 37 vacant of 790 counted dwellings, 4.7 per cent
3. A bar chart of the ten vacancy shares with their 90 per cent intervals against a line at 5.0 per cent, the qualifying municipalities highlighted.
4. The population register beside the vacancy figures, by municipality: overcoverage (dwellings, rate), undercoverage (dwellings, rate) and net bias, per cent:
   - Brekkevoll (5801): overcoverage 15 (1.1), undercoverage 197 (79.4), net bias 11.1
   - Tverrvika (5802): overcoverage 13 (2.7), undercoverage 7 (21.9), net bias -1.2
   - Hesteby (5803): overcoverage 8 (0.9), undercoverage 28 (33.7), net bias 2.0
   - Kvernhaug (5804): overcoverage 7 (1.0), undercoverage 146 (84.9), net bias 16.2
   - Solmoen (5805): overcoverage 12 (3.0), undercoverage 11 (40.7), net bias -0.2
   - Ravnsund (5806): overcoverage 10 (1.5), undercoverage 37 (60.7), net bias 3.6
   - Ørnevik (5807): overcoverage 19 (5.3), undercoverage 8 (40.0), net bias -2.9
   - Langgrav (5808): overcoverage 10 (1.0), undercoverage 55 (67.9), net bias 4.0
   - Fjordeid (5809): overcoverage 10 (1.9), undercoverage 23 (53.5), net bias 2.3
   - Snøholt (5810): overcoverage 14 (1.9), undercoverage 44 (65.7), net bias 3.8
   - County: overcoverage 118 (1.6), undercoverage 556 (66.7), net bias 5.5

### county_dwelling_occupancy_2026-11.xlsx

5. One row per counted dwelling, 8,020 rows, with municipality number and name, dwelling ID, address, unit, persons registered on 1 November 2026 (13,599 in all) and vacant yes or no (396 yes); a sheet by municipality carries the figures of answers 2 and 4.

## Critical Components

1. Counted dwellings in the county: **8,020**; vacant in the fortnight: **396**.
2. A dwelling was lived in when some hour of some day ran more than **0.9 kWh** above its own typical day (each day set at its night hours); vacant when its days repeated. **70** vacant dwellings heated on a timer rise every morning and evening, so a rise over the night alone reads them as lived in and leaves Tverrvika and Ørnevik.
3. Vacant dwellings still carrying a registered resident on 1 November: **118**; lived-in dwellings with nobody registered: **556**.

## Step-by-Step

1. Took the cadastre's units of type Bolig in use on or before 1 November 2026 (Section 3): 8,020 dwellings.
2. Joined each to its household metering points by bruksenhet_id, else by municipality and address for a single-unit house; Snøholt's points carry Fjordeid's old municipality number.
3. Put the hourly values on Norwegian time (UTC+1), kept the later delivery where an estimated day was replaced, and added a dwelling's two points where its meter changed.
4. Read occupancy as a consumption floor first: vacant dwellings used a median 22.8 kWh a day against 20.4 for lived-in ones, so any floor from 1 to 10 kWh designates no municipality; read it from the register's empty dwellings and all 10 qualify. Both are rejected.
5. Took the household's rise next: the mean of 06 to 09 or of 16 to 22 above the mean of 01 to 05 on any day. It separates cleanly and agrees with the register, but it leaves 326 vacant and only Tverrvika and Ørnevik qualifying, because 70 vacant dwellings heated on a timer rise at the same hours by the same amount every day. Rejected as the reading of occupancy.
6. Set each day against its own night hours and each dwelling against its typical day (the median of its days, hour by hour), and took the largest excess of any hour: no vacant dwelling exceeds 0.6 kWh and every lived-in one reaches 1.3, so any cut in that gap marks the same dwellings; a household on any day makes the dwelling lived in (Section 4): 396 vacant. A timer read as days alike gives the same dwellings when its cut sits in that statistic's own gap.
7. Divided each municipality's vacant dwellings by its counted dwellings, rounded to one decimal, and designated those at 5.0 per cent or more (Section 6); each share's 90 per cent exact binomial interval on its counted dwellings lies wholly above the line for Tverrvika, Hesteby and Ørnevik.
8. Rolled the population register of 5 January 2027 back to 1 November by undoing every later event, reading the November block renumberings as a change of unit number and every old number written before a block's day as the flat one floor up: the register held someone in 7,186 counted dwellings and nobody in 834.
9. Set the register beside the vacancy reading in the assignment's terms: overcoverage 118 dwellings (1.6 per cent), undercoverage 556 (66.7 per cent), net bias 5.5 per cent of counted dwellings.

No other designation survives. A level of use cannot separate an empty dwelling that is heated from a lived-in one, so every floor gives none; the register gives all ten because two in three of the dwellings where it holds nobody were lived in; a morning or evening rise gives Tverrvika and Ørnevik alone because a heating timer rises too; and the regulation decides on the share, which the departure from each dwelling's own typical day fixes at the same five for any cut the data allow.
