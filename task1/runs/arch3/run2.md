# Platform run, task1 architecture 3 (the 2026-11-11 reshipped cut)

Pasted by the author on 2026-11-12 beside the review; no rubric score given. Verbatim.

Recommendation. Fund 15 lines for EUR 139,168; do not fund TEL-GAZ, APP-GAZ or TEL-ELN. The funding threshold is expected 36-month household net revenue of at least 3.5 times planned cost per start; the three rejected lines achieve 1.80x, 2.40x and 1.46x, respectively.

Final answers. The spreadsheet and one-page funding note are packaged in 2027_acquisition_package.zip.

Funding and economics

The funded budget covers 2,561 starts and leaves EUR 24,756 of the full EUR 163,924 plan unfunded.

Below, each line shows expected 36-month net revenue per start / planned cost per start, followed by annual planned spend. All amounts are EUR. These are recorded in 2027_acquisition_decision.xlsx, sheet Plan_Lines; the funded lines and budget also appear in 2027_funding_note.pdf.

SOC-BHR: 161.36 / 38.00; spend 10,982; fund.
SEA-BHR: 375.82 / 60.00; spend 16,680; fund.
PART-BHR: 259.45 / 67.50; spend 13,636; fund.
TEL-BHR: 334.21 / 71.00; spend 16,259; fund.
APP-BHR: 313.48 / 58.50; spend 10,588; fund.
SOC-GAZ: 275.40 / 66.00; spend 11,946; fund.
SEA-GAZ: 208.67 / 44.51; spend 7,477; fund.
PART-GAZ: 290.41 / 52.00; spend 7,540; fund.
TEL-GAZ: 113.45 / 63.00; spend 11,403; do not fund.
APP-GAZ: 127.22 / 53.00; spend 5,777; do not fund.
SOC-KBO: 148.18 / 31.50; spend 4,914; fund.
SEA-KBO: 337.33 / 49.00; spend 7,056; fund.
PART-KBO: 232.84 / 63.49; spend 7,555; fund.
TEL-KBO: 299.31 / 63.00; spend 10,458; fund.
APP-KBO: 142.22 / 39.00; spend 3,783; fund.
SOC-ELN: 242.20 / 57.50; spend 6,268; fund.
SEA-ELN: 187.87 / 41.51; spend 4,026; fund.
TEL-ELN: 101.76 / 69.50; spend 7,576; do not fund.
The funded budget by title is BHR EUR 68,145; GAZ EUR 26,963; KBO EUR 33,766; ELN EUR 10,294. The note's "Lines to fund" table carries these allocations. Decisions use unrounded annual spend divided by starts, not the displayed rounded cost per start.

October paying subscribers

At 31 October 2026, paying subscriptions total 12,230: BHR 5,076; GAZ 3,065; KBO 2,608; ELN 1,481. These appear in Price_Impact, supported by the subscription-level Stock_Audit sheet.

2027 starts still paying at year-end

If every plan line ran, expected original subscriptions paying at 31 December 2027 would be: paid social, SOC 423.61 from 735 planned starts; paid search, SEA 489.85 from 687; cashback partners, PART 370.98 from 466; telemarketing, TEL 419.11 from 685; app-store campaigns, APP 254.51 from 387; direct, DIR 0.00 from 0 plan starts (direct is not a funded plan line). The total is 1,958.06, versus 1,885.90 for the funded lines alone. These are expected counts, not rounded observed people. See Paying_2027, Title_Channel and Plan_Months.

Offer-expiry losses

These figures use all planned starts using each offer as the denominator. The April increment respects the monthly acquisition schedule and introductory prices locked at entry.

G3, three free months: 71.69% leave at expiry at 2026 prices; April prices add 2.02 percentage points, producing 73.71%.
H6, six months at half price: 29.78%; add 1.42 points, producing 31.20%.
J12, twelve months at 60% of list: 27.60%; add 1.20 points, producing 28.80%.
M3E1, three months at EUR 1 per month: 59.99%; add 2.46 points, producing 62.45%.
PM1, one month at EUR 0.99: 68.40%; add 1.80 points, producing 70.21%.
See Offer_Expiry. Expiry_Lines supplies title/channel detail and conditional losses among subscriptions reaching expiry. J12 expiry occurs in 2028 for these 2027 starts.

April-rise cancellations from the October base

Estimated additional subscriptions ended by 31 December 2027, among subscriptions paying at 31 October 2026, are: BHR 168.12; GAZ 101.52; KBO 86.50; ELN 49.55; total 405.69. These are differences between paired with-rise and no-rise forecasts, not all cancellations. See Price_Impact and Stock_Audit.

Three-year retention of recent starts

For November 2025-April 2026 starts, projected original-subscription survival to the third anniversary is: APP 10.09% from 228 starts; DIR 26.64% from 1,818; PART 12.82% from 228; SEA 23.16% from 363; SOC 10.37% from 345; TEL 6.36% from 353. These are forecasts, not observed three-year outcomes. The 3,335 starts produce 678.88 expected survivors. See Recent_Retention and Recent_Audit.

Observed historical revenue

For July-September 2023 starts, observed net household revenue over each start's first 36 months was: APP EUR 180.19 per start, 87 starts, bootstrap interval EUR 147.50-213.33; DIR EUR 256.37, 507 starts, 238.57-273.98; PART EUR 225.58, 87 starts, 183.33-271.85; SEA EUR 225.54, 130 starts, 191.04-259.12; SOC EUR 152.43, 157 starts, 121.82-184.39; TEL EUR 131.69, 116 starts, 100.71-161.62. The 1,084 starts generated EUR 233,811.78 of attributed household net revenue. See History_36m, History_Starts and History_Bills. The intervals are 95% household-bootstrap sampling intervals, not uncertainty about the recorded revenue total.

Step-by-step process.

Inspected all 18 archive members. The KPI-standard PDF established the funding rule, subscriber scope, household-value definition and fees. The price-list PDF established the announced price path. media_plan_2027.xlsx supplied offers, monthly starts and spend; kpi_digital_2026.xlsx supplied independent monthly checks. offer_catalogue.csv and marketing_channel_codes.csv supplied offer rules and channel mappings.

Built the subscription and household registers from subscriptions_2023-01_2026-10.csv, customers.csv, payment_methods.csv, price_periods_2023-01_2026-10.csv and payment_exceptions_2023-01_2026-10.csv.

Inspected but excluded unrelated or unsuitable measures. Advertising revenue, newsletter signups and print circulation are outside subscription net revenue. Historical marketing spend is not the planned acquisition cost. Reader-survey opinions do not identify realized cancellations. Logins and reading records do not provide an acquisition-time future engagement path, so using later reading would risk outcome leakage.

Cleaned the subscription population: removed 449 exact duplicates from 32,491 rows (32,042 unique); excluded 1,053 gifts, 160 staff, 38 group/business and 24 test subscriptions, then 340 withdrawals; 30,427 retained. Reclassified 11,489 subscriptions with the legacy channel mappings; kept 8,800 missing pre-2023 channels as a legacy category. Resolved households through matching email hashes, payment fingerprints and normalized addresses: 27,972 households across 30,280 customer accounts. Reconstructed 503,304 monthly billing records with 7% VAT, Apple's first-twelve-paid-month fee schedule, Google's fee and collection resolution. All 36 January to September paying counts and revenue figures matched the published results exactly.

Estimated survival and price response with a billing-cycle logistic end-hazard model (491,356 completed cycles, 18,055 ends) separating tenure, channel, title, payment route, offer phase, recent-cohort quality, scheduled price jumps, list-increase timing and prior household history. Household returns from a return model on 305,775 intervals and 3,922 return events. Calendar holdout: 4,520 observed ends against 4,614.40 predicted. A household-held-out mature-cohort check exposed underprediction for PART and SEA.

Assumptions and judgment calls: price effects observational, the April 2025 pattern transferred to April 2027; recent acquisition mix held representative; offer effects transferred across sparse cells; household matching treats a shared home or payment identity as the payer; the 198 late-October starts provisional; monthly plan starts on the 15th.

Alternatives rejected: fund the entire plan; ignore later household subscriptions (EUR 98,298, five lines fewer); one pooled churn rate; recent three-year retention as observed; mature channel averages for the new plan; subtracting write-offs again; treating the recommendation as risk-free (APP-KBO EUR 5.72 per start above its hurdle; a 25% cut in later-household value makes it fail, EUR 135,385; an upward price-response stress EUR 116,848); ignoring contrary validation evidence (mature PART survival 26.44% observed against 13.99% predicted, SEA 28.46% against 22.90%).
