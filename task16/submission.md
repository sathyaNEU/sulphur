# task16 answer blocks

## Tags

**Domain:** Machine Learning Research, General Statistics & Data Science (data integration, record linkage and entity resolution).
**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).

## Final Recommendation

**Offer the assistant first through the peak season for Delivery day and time, Redirect and address, Pickup point and collection, Returns and labels and Charges and refunds, and an adviser first for Track and trace, Missed delivery and redelivery, Customs and import charges, Damaged parcel and Missing parcel.** On the season plan those last five come to 70.7, 70.4, 68.6, 70.6 and 54.9 per cent, all under the 75 per cent rule, and the assistant resolves 75.5 per cent across all ten families (90 per cent range 74.3 to 76.7). This rejects keeping Track and trace with the assistant, which is what the weeks observed carried into the season unchanged would do: it reads 76.5 per cent on October's conversations and 70.7 on the season's, because late and exception parcels generate 56.4 per cent of the conversations the plan implies against 39.7 per cent of October's.

## Supplementary Questions

### peak_assistant_scope.xlsx

1. The workbook's first sheet has one row per reason family, sorted by expected rate, highest first, and a last row for all ten families together; columns: reason family, conversations in the record, resolution rate so far (per cent), expected rate over the season (per cent), the 90 per cent range's low and high, the distance to 75, and which is offered first (assistant or adviser). Further sheets show how the figures are built up from the contact records: the linked record and the follow-ups it cannot see, the season's conversations by delivery outcome, the rates by family and outcome, and what each shorter reading gives. Rates are stated to 0.1 of a point.
2. Each reason family's expected resolution rate over the season, per cent, with the band a sound rebuild lands in:
   - Returns and labels: **93.7** (92.7 to 94.7), assistant first.
   - Pickup point and collection: **89.1** (87.9 to 90.3), assistant first.
   - Redirect and address: **83.4** (81.8 to 85.0), assistant first.
   - Charges and refunds: **82.0** (80.4 to 83.6), assistant first.
   - Delivery day and time: **78.0** (76.8 to 79.2), assistant first.
   - Track and trace: **70.7** (69.3 to 72.1), adviser first.
   - Damaged parcel: **70.6** (68.8 to 72.4), adviser first.
   - Missed delivery and redelivery: **70.4** (68.0 to 72.8), adviser first.
   - Customs and import charges: **68.6** (67.2 to 70.0), adviser first.
   - Missing parcel: **54.9** (52.3 to 57.5), adviser first.
   - All ten families together: **75.5** (74.6 to 76.4).
3. Each rate's 90 per cent range, per cent. The range is graded on its width: half the distance from low to high, with the band a day-by-day resampling lands in:
   - Returns and labels: 92.4 to 94.9 (half-width **1.27**, band 0.83 to 2.03).
   - Pickup point and collection: 87.3 to 90.8 (half-width **1.77**, band 1.15 to 2.83).
   - Redirect and address: 81.8 to 84.9 (half-width **1.55**, band 1.01 to 2.48).
   - Charges and refunds: 79.5 to 84.3 (half-width **2.41**, band 1.57 to 3.86).
   - Delivery day and time: 76.1 to 79.7 (half-width **1.77**, band 1.15 to 2.83).
   - Track and trace: 69.0 to 72.4 (half-width **1.73**, band 1.12 to 2.77).
   - Damaged parcel: 67.3 to 74.0 (half-width **3.34**, band 2.17 to 5.34).
   - Missed delivery and redelivery: 67.5 to 73.3 (half-width **2.85**, band 1.85 to 4.56).
   - Customs and import charges: 65.5 to 71.6 (half-width **3.07**, band 2.0 to 4.91).
   - Missing parcel: 51.1 to 59.0 (half-width **3.95**, band 2.57 to 6.32).
   - All ten families together: 74.3 to 76.7 (half-width **1.2**, band 0.78 to 1.92).
4. The build-up from the contact records starts from the linked record: **30,745** version 3 conversations about a consignment that ended from 28 September to 1 November 2026 (30,591 to 30,899), of which 4,941 are followed within 168 hours by a linked contact (1,293 by another assistant conversation, 1,340 by live chat, 1,747 by a telephone call that carries the tracking number, 1,196 by a written case in the resolution extract), a resolution rate of **83.9** per cent on the linked record alone (83.5 to 84.3).

### peak_assistant_scope_memo.docx

5. A memo of about a page that opens with the recommendation (the five families kept with the assistant and the five offered an adviser first), gives the all-families expected rate with its range, says why the linked record and the weeks observed both overstate the season, and carries one chart of the ten expected rates with their ranges against the 75 per cent line and a short table of the same figures.

## Critical Components

1. **40.7 per cent** of the telephone calls that follow a version 3 conversation carry no tracking number (36.0 to 46.0): 1,657 keyed follow-up calls stand for about 2,793 once each is weighted by the share of consignment calls keyed in its queue with the IVR bypass running or not.
2. About **235** written cases that follow a version 3 conversation were still open at the cut and so are not in the resolution extract (188 to 282), beside 1,187 that are.
3. With both restored, version 3 has resolved **80.4 per cent** of its conversations (79.6 to 81.2), not the 83.9 per cent the linked record shows.
4. The delay alerts cut assistant conversations per late parcel by **41 per cent** at the pilot depots (35 to 48), measured after against before 12 October and against the other seven depots.
5. Late and exception parcels generate **56.4 per cent** of the conversations the season plan implies (53.4 to 59.4), against 39.7 per cent in the weeks observed, at about **10,700** conversations a week (10,000 to 11,400).

## Step-by-Step

1. Cleaned the four contact exports: kept conversations in `assistant_conversations_2026w32_w45.csv` that carry a tracking number, kept the first leg of each inbound call in `acd_call_legs_2026-08-03_2026-11-08.csv` (a transferred call is one contact, callbacks are not contacts, KS-07 2.1) and put its UTC times on the local clock, brought every tracking number to one form, and mapped intents, wrap-up codes and case categories to the ten reason families with the three code lists; the cleaned inbound calls equal telephony's weekly summary (72,868) in every week and queue.
2. Linked each of the 30,745 version 3 conversations that ended from 28 September to 1 November to later contacts on the same tracking number within 168 hours (KS-07 3.1): 4,941 are followed, a rate of 83.9 per cent. This is the hurried reading: it keeps every family but Missing parcel.
3. The telephone export keys a tracking number on only part of its calls, and far fewer when the IVR bypass is running. Weighted each keyed follow-up call by the inverse of the share of consignment calls keyed in its queue and bypass state: 1,657 keyed calls stand for about 2,793, so 40.7 per cent of telephone follow-ups carry no number. The advisers' previous-contact tick agrees: it marks 1,480 unkeyed calls since 28 September as following the assistant where the capture weights give 1,473.
4. `case_resolutions_to_2026-11-08.csv` holds resolved cases only: its 28,101 customer cases plus the 2,743 the backlog report counts open equal the 30,844 opened. Each closed follow-up case stands for the cases raised in its queue on its day and the days either side that are still open: about 235 open follow-up cases. Completing on the summer's closing times instead finds 77, because the queues have slowed since October.
5. With a conversation whose only follow-up is a keyed call or a closed case standing for those the record cannot see, version 3 has resolved 80.4 per cent, by family from 55.3 (Missing parcel) to 93.9 (Returns and labels).
6. Carrying those rates into the season unchanged keeps Track and trace at 76.5 per cent (the careful but hurried reading). But the rate depends on how the parcel runs (Track and trace: 86.8 per cent when on time, 49.1 when two or more days late), and the season's conversations come from its parcels: joined conversations to `consignments_referenced.csv` and `network_performance_daily.csv` for conversations per parcel by delivery outcome, 11.7 per 1,000 on-time parcels against 168.7 per 1,000 two or more days late.
7. Weighting each family's rates by the plan's parcel service levels as if parcels were conversations gives 85.3 per cent for all families, above the rate achieved; that reading is wrong because a late parcel is many times as likely to generate a conversation.
8. The plan turns delay alerts on at every depot from 16 November. At Linz, Graz and Innsbruck, where they have run since 12 October, conversations per late parcel fell 41 per cent against the other depots over the same weeks. Without that cut the season would read 72.6 per cent for all families and 74.2 for Delivery day and time, under the line.
9. Season conversations by outcome are plan parcels times contact rate, late classes cut by the alerts: about 10,700 a week, 56.4 per cent from late and exception parcels (39.7 in the weeks observed). Each family's expected rate is its rates by outcome weighted by its own season conversations: 75.5 per cent for all families; five families at 75 or more.
10. Ranges from 1,000 resamples of whole days, every step redone: plus or minus 1.2 points for all families. Resampling conversations one by one gives plus or minus 0.34, too narrow because good and bad days move every family together.

No other conclusion survives. The linked record (83.9 per cent) leaves out follow-ups the files themselves show exist: the call counts reconcile only with unkeyed calls in, and the case counts only with the backlog in. Leaving out the calls keeps Missed delivery and redelivery; leaving out the open cases keeps Damaged parcel. The weeks observed cannot stand for the season, because the plan's parcels run later and the record shows what lateness does to both the number of conversations and their outcome; and the alerts cannot be left out, because the plan turns them on and the pilot depots measure them. Every sound variant of each step (capture by week, day, hour or wait; open cases by day or week raised; the alerts read class by class or against version 3 weeks only) keeps the same five families.
