## Tags

**Domain:** Energy Systems & Utilities, Grid reliability & outage analysis (vegetation management on an 11 kV distribution network: tree-caused interruptions read against storm exposure and corridor regrowth).
**Analytical objective:** Anomaly Detection & Diagnostics.

## Final Recommendation

**Put PBY-10, HRK-03, HRK-05, WTK-02, PBY-11 and PBY-03, the six northern coastal feeders left longest since a cycle trim, into the 2027 vegetation catch-up: together they avoid about 12,984 sustained vegetation customer interruptions in 2027-28, 0.33 of network SAIFI.** This rejects the six feeders with the most vegetation customer interruptions in the three years to October 2026 (TOT-02, TIT-04, MKR-01, KWH-01, TIT-01 and TIT-03), whose counts carry the southern hills' stormiest three years in the record and, on the plantation feeders, a dense corridor a catch-up leaves in place: they would avoid 5,770.

## Supplementary Questions

### vegetation_catchup_2027_feeders.csv

1. One row for each of the 48 feeders, ranked by customer interruptions avoided, highest first, with columns rank, feeder, weather station, last cycle trim (the crew-finished date), tree-caused sustained interruptions expected in 2027-28 left as it is (one decimal), customers per tree-caused interruption, tree-caused customer interruptions expected left as it is and after the catch-up, the difference (customer interruptions avoided, whole numbers), and whether the feeder is in the catch-up.
2. The six at the top, each on Paua Bay's station record: PBY-10 59.3 interruptions left as is, 4,161 customer interruptions left as is, 1,419 after the catch-up, 2,741 avoided; HRK-03 48.0, 3,628, 1,291, 2,337; HRK-05 56.1, 3,553, 1,274, 2,279; WTK-02 48.5, 2,949, 1,032, 1,916; PBY-11 47.5, 2,891, 1,001, 1,890; PBY-03 55.0, 2,894, 1,073, 1,821.
3. Rank 7 is the plantation feeder TOT-02, the highest expected customer interruptions on the network left as it is (6,220) but 4,951 after a catch-up, so 1,268 avoided; the other plantation feeders sit lower (TIT-04 rank 11, 1,000 avoided; TIT-01 rank 17, 851; MKR-01 rank 18, 790; KWH-01 rank 19, 754).

### vegetation_catchup_2027_board_note.docx

4. Names the six and states that together they avoid 12,984 customer interruptions in 2027-28, 0.33 of network SAIFI on the 39,943 ICPs connected at 31 October 2026, against 1,268 for the next-best feeder, TOT-02.
5. The split across the regulatory year's quarters: 2,752 in April to June 2027, 5,466 in July to September, 3,102 in October to December and 1,664 in January to March 2028.
6. A 90 per cent range of 10,000 to 19,000 customer interruptions avoided, the spread of the six's saving across the weather of the station record's 19 regulatory years from 2006-07 to 2024-25.
7. One chart of the customer interruptions avoided on every feeder, the 48 bars ranked, the six highlighted and labelled, with the next feeder labelled beside them.

## Critical Components

1. In the three years to October 2026 Paua Bay recorded **38** hours a year of gusts of 60 km/h or more against its 2007-2023 normal of **106**, and Titi Saddle **312** against **133**, while mean wind moved only **-3.4** and **5.7** per cent: the recent vegetation record is the storm track, so each feeder is read per unit of its own station's gust load.
2. On that scale a corridor's vegetation interruptions rise **15.5** per cent for each year since its last cycle trim, fitted across the 48 feeders from April 2022; a catch-up removes only that growth.
3. The six avoid **12,984** customer interruptions (**0.33** SAIFI); the plantation feeder TOT-02, highest left as it is at **6,220**, keeps **4,951** after a catch-up and avoids **1,268**.
4. The six with the most recent vegetation customer interruptions would avoid **5,770**.

## Step-by-Step

1. Cleaned oms_interruptions_2022-04_2026-10.csv by reliability_reporting_standard.docx: dropped the 479 call-centre records of operations SCADA or the field crew logged, kept unplanned interruptions of 1 minute or longer, took vegetation as VEG to 30 September 2023 and TREE after, and mapped Rangiora Street's former RGS codes through feeder_register_2026.xlsx: 3,994 vegetation interruptions.
2. Marked major event days with the DPP3 and DPP4 SAIDI and SAIFI boundary values on daily indices over each regulatory year's mean month-end ICPs (icp_counts_by_feeder_2022-04_2026-10.csv): 5 days, all snow on the southern hills, none with a vegetation interruption.
3. The reasonable but insufficient analysis: ranked the feeders on vegetation customer interruptions in the three years to October 2026, the worst-performing-feeder list, giving TOT-02, TIT-04, MKR-01, KWH-01, TIT-01 and TIT-03 (31,591 to 9,009).
4. Linked each feeder to the station nearest its zone substation (feeder register coordinates against pou_aws_station_register.csv) and read the four hourly records (Titi Saddle's knots converted before July 2013, missing and suspect hours dropped): Paua Bay had 38 hours a year of gusts of 60 km/h or more against 106, Kowhai Ridge 260 against 122, Titi Saddle 312 against 133, with mean wind within 6 per cent, so the recent counts overstate the south and understate the north.
5. Took each station's monthly gust load (each hour's gust above 40 km/h, squared, summed), which fits the vegetation record best of the exposure measures tried; hour counts from 50 km/h leave months with vegetation interruptions and no exposure.
6. Fitted each feeder's monthly vegetation interruptions from April 2022 as Poisson counts on its station's gust load: a corridor rate for each feeder times a growth of 15.5 per cent a year since its last crew-finished cycle trim in vegetation_cycle_log_2014-2026.xlsx.
7. Projected 2027-28 month by month at each station's 2006 to 2025 mean gust load, with the growth running on and with it restarted on 31 March 2027, and turned each into customer interruptions at the feeder's own customers per vegetation interruption.
8. Ranked by the difference: PBY-10 2,741, HRK-03 2,337, HRK-05 2,279, WTK-02 1,916, PBY-11 1,890 and PBY-03 1,821, then TOT-02 1,268; the six total 12,984, 0.33 SAIFI on 39,943 ICPs, split 2,752, 5,466, 3,102 and 1,664 by quarter; across the station record's 19 regulatory years of weather the total runs 10,000 to 19,000 at the 5th and 95th percentiles, against 11,000 to 16,000 from the fit's own uncertainty alone.

No other conclusion survives. Ranking on the recent counts carries the southern storms and funds the plantation feeders; normalising for wind but counting every expected interruption as removable still funds them, because their corridor rate stays after a trim (TOT-02 keeps 4,951 of 6,220); fitting the growth on counts alone, or projecting at the three stormy years or the outage record's own weather, funds the southern late-cycle feeders; funding the most overdue feeders funds the open plains and small feeders with few trees. Every exposure measure tried (hours of 45 to 70 km/h, gust excess over 35 to 45 km/h, straight or squared), every base period, a lag or whole-year bins in the growth, a negative binomial fit, blended stations, job-closed trim dates, UTC months and every cleaning choice give the same six, with totals from 12,247 to 15,757.
