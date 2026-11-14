# leak check, task1

**Verdict: REVIEW.** 11 files read, 83 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: android, tiktok, google, applovin, networks, stores, charges, spread, result, reports, excess, consenting, missed, tracking, twelve-month, reflex, hurried, account, export, postbacks, eleven, shortcut, distinct, stumps, consent

## 1 file names (REVIEW 1)
- **REVIEW** `media_plan_2027.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `growth_policy_paid_channels_v2_2026-09.pdf`: golden figure 0.90 appears: ...when the return is 1.20 or more, hold when it is 0.90 or more and under 1.20, and cut when it is under...
- **REVIEW** `growth_policy_paid_channels_v2_2026-09.pdf`: golden figure 1.20 appears: ...eturn for the plan year: scale when the return is 1.20 or more, hold when it is 0.90 or more and under...

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `growth_policy_paid_channels_v2_2026-09.pdf`: 4 of 25 stump-paragraph terms appear (google, networks, charges, account); read whether the document names the move

## 6 ranking artifacts (REVIEW 3)
- **REVIEW** `ad_spend_daily_2024-11-04_2026-11-08.csv`: names 3 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `creative_tests_2025-2026.csv`: names 3 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `media_plan_2027.xlsx`: names 3 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `media_plan_2027.xlsx`: 52 ISO dates after 2026-11-10, e.g. 2027-01-04, 2027-01-11, 2027-01-18, 2027-01-25, 2027-02-01

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 30% of 23 prompts (cap 30%); deliverable set 'xlsx' at 22% of 23 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 11 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

**1. Sentence/file that tells you how to do a step.** `target/growth_policy_paid_channels_v2_2026-09.pdf`, section 2.1: "A channel's return for a plan year is the 12-month net revenue of the installs the plan's spend on the channel buys in that year, per euro of that spend." This is the literal formula for the prompt's "return per euro of spend." The same section also fixes the window (2.3: "the net revenue of the store charges on its account in the 365 days from the day of the install, less the net revenue of any of those charges refunded") and the unit (2.4, VAT and commission, quoted below).

**2. File that already ranks/scores the channels.** None. Checked `ad_spend_daily` (raw daily spend/impressions/clicks by channel+campaign), `creative_tests` (raw A/B arm metrics), `media_plan_2027.xlsx` (raw weekly EUR spend plus a "Total 2027" row and a text Notes sheet), and grepped every CSV and the workbook's cell values for band/return/rank/score/roas: no hits. No file carries a pre-computed return, band, or rank for any channel.

**3. File that exists only to help the analyst.** `creative_tests_2025-2026.csv` is the best fit: it shares channel names and an "installs_reported_by_network" column with the real inputs, so it reads as relevant, but it reports creative-arm CTR/impressions over short test windows and never feeds the install, revenue, spend, or band figures the prompt asks for. `store_ratings_daily_2024-11_2026-10.csv` (daily ratings count/average by store+country) is a second candidate with no path into any requested figure. The "Notes" sheet inside `media_plan_2027.xlsx` is pure orientation text ("spend as the networks bill it", "Weeks run Monday to Sunday") with no data of its own.

**4. Figure/name that reads as the answer rather than context.** None found. No channel is pre-labelled Scale/Hold/Cut anywhere; those words only appear in the PDF's generic band table (3.1), not attached to a channel. `media_plan_2027.xlsx` has a "Total 2027" row that could be mis-parsed as a 53rd week by a careless script, but it is clearly labelled in column A, not a leaked figure.

**5. Filed sentence that fixes a population/window/unit.** PDF 2.2: "An install is the first install of a new consumer account. A second device, a reinstall, a staff account and a test account are not installs. Each install is bought by at most one channel: the one whose ads drove it." In words: fixes the **population** for "installs it bought" to `accounts.account_type == consumer`, first install only (excludes `attribution_installs.is_reinstall == true`), single-channel credit, and excludes organic. PDF 2.4: "The net revenue of a charge is its price less VAT (Spain 21 per cent, Italy 22 per cent, Portugal 23 per cent, by the storefront) and less the store's commission of 15 per cent of the price net of VAT" fixes the **unit/definition** of net revenue per charge (country-specific VAT by storefront, then 15 percent off the VAT-exclusive price), not a number to compute.

**6. One thing that would make most of the ask routine?** Reading PDF sections 2 and 3 together fixes the entire WHAT: what counts as an install, what net revenue means, the 365-day window, the VAT/commission math, and the exact band cutoffs (3.1: scale >= 1.20, hold 0.90-1.20, cut < 0.90). Once read, the install-population rule and the band assignment become rule application, not judgment. What it does **not** settle: (a) reconciling channel identity across files, since `attribution_installs.media_source` ("Meta Ads", "AppLovin", "TikTok For Business", "Apple Search Ads", "organic") does not share a vocabulary with the 7 channel names in `ad_spend_daily`/`media_plan`/`creative_tests` ("Meta iOS", "Meta Android", "AppLovin Android", ...) and must be joined via platform (and/or `campaign_id`, which both `ad_spend_daily` and `attribution_installs` carry); (b) projecting "installs a week at its 2027 weekly spend" forward, a genuine forecast with no stated method or cited efficiency window; (c) assembling 365-day per-account revenue correctly from `billing_events` (first_charge/renewal/refund) against the 7-day trial, with `appstore_subscription_events_daily` and `googleplay_subscription_transactions_daily` as separate store-reported aggregates that could agree or disagree with it. So: the population and band cutoff turn on reading filed definitions/rules correctly; the install-window count and revenue assembly turn on cross-file joins and reconciliation; the installs-per-week-at-2027-spend figure turns on open analysis (forecasting), not on any filed sentence. One visible, not hidden, pattern worth flagging: for iOS, `att_status == denied` correlates with `media_source == organic` in about 90 percent of rows (vs. about 39 percent when authorized), a one-group-by-visible privacy effect that pushes real paid iOS installs into "organic" and motivates using `skan_postbacks` rather than a planted trap.

**Checks.**
(a) Coverage: `store_ratings_daily_2024-11_2026-10.csv` stops at 2026-10-31, short of "early November 2026"; every other file (accounts, ad_spend_daily, appstore_subscription_events, attribution_installs, billing_events, googleplay_subscription_transactions, skan_postbacks) runs to 2026-11-08 or 2026-11-09, consistent with the prompt. `creative_tests_2025-2026.csv` is a periodic test log (2025-04-12 to 2026-10-18), not a continuous series, so it is not held to that coverage claim.
(b) Yes: PDF section 3 ("3. Bands", 3.1 and its table) carries the exact band rule (scale >= 1.20, hold 0.90 to under 1.20, cut under 0.90) that the prompt's last ask ("its band") needs.
(c) No: `ad_spend_daily`, `creative_tests`, and `media_plan_2027.xlsx` are all raw inputs; none ranks or scores the channels on the prompt's question (checked headers, cell values, and grepped for band/return/rank/score terms).

### Rulings (main thread, 2026-11-13, on the read of cut 90e641dd3185f4cd)

- Q1, Q5 (policy 2.1 to 2.4): the WHAT, filed as it must be (the return, an install, the 365 days, net revenue); no step, adjustment or comparison is named. Harmless.
- Q3 (creative tests, store ratings): the two distractors, unused by every graded figure; neither is labelled as such. Harmless.
- Q6, the band rule: placing a figure against filed lines is the decision form; the work is the return itself. Harmless.
- Q6, the attribution export's denied users under organic: one group-by shows the export cannot attribute them, which points to the postbacks for the iOS networks' installs (R1, a reflex priced Right); the value of those installs still has to be built from the postbacks' conversion values. Harmless.
- Check (a), store_ratings_daily_2024-11_2026-10.csv ending on 31 October: the file's name states its own coverage and it is a distractor. Harmless.
- REVIEW lines (the plan's Notes sheet, plain policy words, channels beside spend, the 2027 plan's dates): read and harmless (reader's checks b and c; the first read's flags a to d).
