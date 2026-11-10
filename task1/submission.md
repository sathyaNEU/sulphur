## Tags

**Domain:** Product Analytics, Cohort and LTV modeling (retention curves, customer lifetime value).
**Task type:** forecast of a seat-licensed SaaS book's December 2027 ARR, built flow by flow, with an 80 per cent band and a bridge.
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Commit EUR 9.9 million of December 2027 ARR in the 2027 plan, not the draft's EUR 10.2 million**: December 2027 ARR has an 80 per cent chance of reaching EUR 9,890,000 (expected EUR 10,050,000, 80 per cent range EUR 9,770,000 to EUR 10,320,000), and the draft is met only about 24 times in 100. A forecast that applies the average price rise to every renewal, pools renewal rates, values the pipeline at the CRM's stage probabilities and draws accounts independently puts the 80 per cent figure at EUR 10.2 million and wrongly clears the draft.

## Supplementary Questions

### arr_2027_forecast.xlsx

1. Sheet Forecast: one row per month end from October 2026 (on the books, 8,900,000) to December 2027, columns month end, expected ARR, 80 per cent range low (10th percentile) and high (90th percentile), EUR to the nearest 10,000: Nov 2026 9,110,000 (9,070,000 to 9,150,000); Dec 2026 9,240,000 (9,180,000 to 9,300,000); Jan 2027 9,390,000 (9,310,000 to 9,460,000); Feb 2027 9,520,000 (9,420,000 to 9,620,000); Mar 2027 9,560,000 (9,420,000 to 9,690,000); Apr 2027 9,610,000 (9,460,000 to 9,760,000); May 2027 9,670,000 (9,500,000 to 9,830,000); Jun 2027 9,720,000 (9,540,000 to 9,900,000); Jul 2027 9,750,000 (9,550,000 to 9,940,000); Aug 2027 9,780,000 (9,550,000 to 9,990,000); Sep 2027 9,830,000 (9,590,000 to 10,060,000); Oct 2027 9,870,000 (9,620,000 to 10,120,000); Nov 2027 9,960,000 (9,690,000 to 10,210,000); Dec 2027 10,050,000 (9,770,000 to 10,320,000). Below it the December 2027 summary: expected 10,050,000, P10 9,770,000, P90 10,320,000, the 80 per cent figure 9,890,000, commitment EUR 9.9 million, draft EUR 10.2 million, draft clears: No.
2. Sheet Bridge: ARR 31 October 2026 EUR 8,900,000; new Business EUR 1,350,000; Business seat additions EUR 550,000; price EUR 300,000; Business seat reductions -EUR 200,000; Business accounts lost -EUR 860,000; change in Team EUR 10,000; expected ARR 31 December 2027 EUR 10,050,000, the lines adding up exactly at the nearest EUR 10,000. Under it the new Business split (open deals EUR 630,000, deals created from November 2026 EUR 490,000, Team accounts moving to Business EUR 230,000) and the Team split (accounts on Team at 31 October 2026 EUR 1,370,000, Team accounts signing from November 2026 EUR 570,000). Further sheets list the inputs and what each shortcut gives.

### arr_2027_note.docx

3. The call: commit EUR 9.9 million (the 80 per cent figure is EUR 9,890,000); the draft's EUR 10.2 million does not clear the 80 per cent bar (met about 24 times in 100).
4. ARR on the books at 31 October 2026: Business EUR 6,970,000, Team EUR 1,930,000 (total EUR 8,900,000).
5. Team ARR in December 2027 from accounts already on the Team plan at 31 October 2026: EUR 1,370,000 (the defensible methods give EUR 1,370,000 to EUR 1,390,000).
6. New Business ARR signed November 2026 to December 2027 from deals open at 31 October 2026: EUR 630,000 (the defensible methods give EUR 630,000 to EUR 660,000) (of EUR 1,350,000 new Business in all).

## Critical Components

1. The price line is **EUR 300,000**: the realised uplift at renewal falls with contract size (about 94 per cent of the list rise at 20 seats), so the average uplift applied flat (EUR 370,000) or the list rise (EUR 430,000) overstates it.
2. Business seat reductions are **EUR 200,000** (the defensible methods give EUR 190,000 to EUR 200,000) and Business accounts lost **EUR 860,000** (the defensible methods give EUR 850,000 to EUR 890,000), from a renewal model on utilisation (workspace activity through the dated links), first renewals and group exits; pooled rates give seat reductions of EUR 310,000.
3. New Business is **EUR 1,350,000** (the defensible methods give EUR 1,350,000 to EUR 1,370,000), of which **EUR 630,000** (the defensible methods give EUR 630,000 to EUR 660,000) from deals open at 31 October 2026, on win odds by stage and time in stage; the CRM's stage probabilities value the open deals at EUR 970,000.
4. December 2027 ARR has an 80 per cent range of **EUR 9,770,000 to EUR 10,320,000** and an 80 per cent figure of **EUR 9,890,000** (commitment EUR 9.9 million; the defensible methods give EUR 9.8 to 9.9 million) with a parent group's accounts drawn together; drawn independently the figure is EUR 10,120,000.

## Step-by-Step

1. Opening book (billing_contract_lines_2022-01_2026-10.csv, team_invoices_2022-01_2026-10.csv): re-exported lines counted once, credited lines replaced by their re-issues, onboarding fees and part-term true-up charges left out, failed card payments dropped, GBP at the plan rate (policy 2): Business EUR 6,970,000 and Team EUR 1,930,000 at 31 October 2026; September's figure reproduces the KPI export (EUR 8,790,000). Summing every exported line gives EUR 7,120,000 for Business.
2. Price: from the 396 repricings since 1 March 2026, the per-seat price change at renewal fitted on log seats (94 per cent of the list rise at 20 seats, less on larger contracts) and applied to each contract still to reprice: EUR 300,000. The mean uplift applied flat gives EUR 370,000, the list rise EUR 430,000.
3. Renewals: workspace activity joined to accounts through workspace_account_links.csv on the dated links, utilisation at each of the 2,224 renewals since 2022, CRM parent groups from crm_accounts_export_2026-11-02.xlsx; exits modelled on utilisation, first renewal and a sibling's recent exit, seat cuts on utilisation and renewal number: seat reductions EUR 200,000, accounts lost EUR 860,000. Pooled rates give EUR 310,000 and EUR 890,000.
4. Seat additions: each account's own drift in active users projected against its seats, true-ups when users pass seats: EUR 550,000 in the bridge.
5. Team: monthly exit rates by members and age before April 2026, plus the excess on the accounts padded to three seats, which fell month by month to a lasting 2.8 points a month; December 2027 Team ARR from the October accounts EUR 1,370,000. Reading the months since April as the new rate gives EUR 1,280,000, the trailing twelve months EUR 1,350,000.
6. Pipeline (pipeline_snapshots_2023-01_2026-10.csv, opportunities_closed_2022-01_2026-10.csv): re-run snapshot rows once, monthly amounts set aside for quoted seats priced at won deals' first contracts, win timing by stage and months in stage from snapshots with a full 14-month follow-up: open deals EUR 630,000, all new Business EUR 1,350,000. The CRM's probabilities give EUR 970,000 and EUR 1,690,000; stage alone EUR 680,000; the trailing run-rate of new ARR EUR 1,550,000.
7. Band: 2000 simulated paths with each parent group's exits feeding its siblings' next renewals and new deals drawn as whole deals: P10 EUR 9,770,000, P20 EUR 9,890,000, P90 EUR 10,320,000. Independent draws give a P20 of EUR 10,120,000.
8. Path and bridge: the monthly expected path and its range from the same paths, the six lines in the policy's order adding from EUR 8,900,000 to EUR 10,050,000; commitment EUR 9.9 million, below the draft.

No other figure survives the files. Carrying the last twelve months' growth forward (25.6 per cent a year) gives EUR 11,610,000; the shortcuts taken together (flat uplift, pooled renewals, the last three months' Team rates, CRM probabilities, independent draws) give a commitment of EUR 10.2 million; each is ruled out by the repricings' size gradient, the renewals' utilisation and group pattern, the decline in the April excess and the closed deals' history. The rivals a careful analyst can defend (uplift by size band, utilisation in bins or left out of the exit model, the April excess from two months or an exponential, win odds by stage and deal age, seat additions from 12 or 18 months of drift, each account's own trailing rate or the book's trailing rate at accounts near their seats) all keep the commitment at EUR 9.8 to 9.9 million, below the draft.
