## Tags

**Domain:** Product Analytics, Product Analytics (retention, cohort and lifetime-value modeling).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Do not book the January and February re-run of AUT26 on the same terms.** Carried member by member through their tutors' odds of stopping, about 950 AUT26 members will pay a twelfth monthly charge, so the campaign cost about EUR 900 per twelfth-month member (80 per cent range EUR 850 to 975), above the EUR 800 bar; the usual retention curve by membership month puts it at about EUR 725 and would book the re-run, because it prices AUT26 members on the mix of tutors past members had, when 91.5 per cent of those still paying are with tutors in their first two months of teaching.

## Supplementary Questions

### aut26_rerun_memo.docx

1. Expected number of AUT26 members who will pay a twelfth monthly charge: about 950 of the 3,534 campaign members (27.1 per cent).
2. Cost per twelfth-month member: about EUR 900 against the EUR 800 bar (campaign cost EUR 868,150 over about 950 expected twelfth-month members); 80 per cent range EUR 850 to 975; 90 per cent range EUR 825 to 1,000. The ranges draw each tutor's stop once for all of that tutor's members, with the projection's inputs redrawn from their own sampling error; drawing members one at a time would narrow the 80 per cent range to EUR 875 to 950.
3. Cost per paid member at which members retaining like these would have met EUR 800 exactly: about EUR 225 (EUR 800 times the 27.1 per cent expected to pay a twelfth charge), against the EUR 250 AUT26 cost per paid member.
4. The chart: one line chart with the months November 2026 to September 2027 along the bottom and the expected share of AUT26 members paying on the vertical axis; one line for September joiners (81.1 per cent in November falling to 25.8 per cent in September 2027), one for October joiners (89.2 falling to 27.0), and the membership-month curve for all AUT26 members drawn dashed for comparison (85.3 falling to 32.8); the joiners' lines stay above the curve through the winter and fall below it from March 2027 for September joiners and April for October joiners, once their tutors reach the months in which tutors most often stop.

### aut26_member_forecast.xlsx

5. A monthly sheet with one row per month from November 2026 to September 2027 and columns for members who joined in September, members who joined in October and all AUT26 members, each cell rounded to the nearest 50 on its own (September joiners pay their twelfth charge in August 2027, October joiners in September 2027):
   - November 2026: 1,400; 1,600; 3,000.
   - December 2026: 1,250; 1,450; 2,700.
   - January 2027: 1,150; 1,300; 2,450.
   - February 2027: 950; 1,150; 2,100.
   - March 2027: 750; 950; 1,750.
   - April 2027: 650; 800; 1,450.
   - May 2027: 600; 700; 1,250.
   - June 2027: 550; 600; 1,150.
   - July 2027: 500; 550; 1,050.
   - August 2027: 450; 500; 1,000.
   - September 2027: 450; 500; 950.
6. Further sheets carry the twelfth-charge summary by joining month (about 450 of 1,718 September joiners and 500 of 1,816 October joiners), the cost build-up with both ranges, the inputs (cancellation by membership month on active-tutor months, cancellation in the first month without the tutor and the month after, stopping by months taught), each campaign member's projected chance of a twelfth charge, and a notes sheet with the data cut, the standard's definitions and the rounding.

## Critical Components

1. A member whose tutor stops teaching cancels **61.7 per cent** of the time in the first month without that tutor and **26.7 per cent** the month after, against **5.5 per cent** in an ordinary month (7,900 member months with a tutor stop since 2022).
2. Of tutors who have taught four, five and six months, **21.3, 26.0 and 24.8 per cent** do not teach the next month, against **0.8 per cent** a month for tutors past their first year (798 tutors).
3. **2,757 of the 3,013** AUT26 members still paying on 31 October (**91.5 per cent**) are with tutors in their first two months of teaching.
4. Carried through their tutors' stopping, about **950** AUT26 members pay a twelfth charge and the cost per twelfth-month member is about **EUR 900** against **EUR 800**; the membership-month curve gives about **1,200** members and **EUR 725**.

## Step-by-Step

1. Rebuilt collected charges from `billing_events_2022-01_2026-10.csv` (webhook replays dropped on the event id, retries counted once, charges refunded in full removed, amounts read across the 2025 column change) and joined `signup_attribution_2022-01_2026-10.csv` (the AUT26 code in any case or suffix) within the standard's Berlin-day window: 3,534 campaign members.
2. Summed the cost the standard defines from `fenwright_aut26_closeout_and_invoices.xlsx` (net of VAT and of the EUR 14,250 credit note, GBP at the ECB rate of each issue date) and the first-month discounts against `plans_and_promotions.json`: EUR 868,150, about EUR 250 per paid member.
3. The reasonable but insufficient read: the paid-retention curve by membership month from every membership projects about 1,200 twelfth-month members and EUR 725, and it checks out as conservative on the spring 2025 campaign (28.7 against 33.3 per cent kept) and last autumn's joiners (30.6 against 33.5), so it books the re-run.
4. Read each tutor's run of teaching months from `lesson_activity_monthly_2022-01_2026-10.csv` with `tutor_directory_2026-11-03.csv` and each member's tutor month by month: members cancel 61.7 per cent in the first month without their tutor and 26.7 the month after, against 5.5.
5. Built the tutors' stopping table by months taught from the same log: 2.1 and 2.5 per cent stop after one and two months, 21.3 to 26.0 after four to six, 0.8 a month past the first year.
6. Tested the curve where the two views disagree: over six-month windows it under-predicts the cancellations of members whose tutor is in their first three months of teaching by a factor of 1.22 and their fourth to ninth by 1.19, and over-predicts members of established tutors (0.74 in months ten to twelve, 0.85 past the first year), so it holds only for a member mix like the past.
7. Found from the same log that 172 tutors began teaching in September and October 2026 against 7 from March to August, and 2,757 of the 3,013 live AUT26 members (91.5 per cent) are with them.
8. Projected each live member month by month through their tutor's stopping odds and their own cancellation curve estimated on active-tutor months: about 950 twelfth-month members, EUR 900 each, and the break-even cost per paid member at about EUR 225.
9. Simulated the same projection with each tutor's stop drawn once for all of that tutor's members and the inputs redrawn from their sampling error: EUR 850 to 975 at 80 per cent and EUR 825 to 1,000 at 90 per cent.
10. Rolled the projection into each month from November 2026 to September 2027 by joining month for the workbook.

No other conclusion survives. Every construction without the tutors' stopping by months taught files EUR 625 to 739 per twelfth-month member and the re-run (the membership-month curve with or without calendar, engagement or recent-month terms, a shifted-beta-geometric fit, or members' tutors at one pooled stop rate), while every variant of the tutor-linked projection (calendar factors, a smoothed stopping table, a post-rematch term, inputs estimated from 2023, 2024 or 2025 on) files EUR 898 to 916 and the hold. The nearest half-step, shocking only the first month without the tutor, files EUR 812 and is ruled out by the next month's 26.7 per cent, and adding the shocks to the all-cause curve counts each stop twice (EUR 1,395). A classifier of the twelfth charge fitted on past members files the hold at EUR 839 to 1,077, but it learns only from members who joined by November 2025, leans on the 2022 launch months, when 57.4 per cent of members whose tutor stopped were moved to a tutor in that tutor's first nine months of teaching (0.6 per cent since 2023), and cannot give the months.
