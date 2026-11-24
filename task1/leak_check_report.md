# leak check, task1

**Verdict: REVIEW.** 14 files read, 53 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: android, google, budget, install, applovin, stores, network, tiktok, continuation, snapchat, pinterest, record, billed, charges, delivery, channels, fitted, declined, beside, carried, reports, accounts, charge, checkout, inside

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `growth_policy_paid_channels_v3_2026-09.pdf`: 9 of 25 stump-paragraph terms appear (google, budget, install, stores, record, charges); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "Our records run to 8 November 2026 and none of the installs that spend buys will be twelve months old before 2028, so each channel's return has to be an estimate."

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `media_plan_2027.xlsx`: 156 ISO dates after 2026-11-09, e.g. 2027-01-04, 2027-01-11, 2027-01-18, 2027-01-25, 2027-02-01

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 14 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

First read, 2026-11-21, of the cut with pack digest 17c5286326eccd58 (one isolated reader on Sonnet at medium, shown only fresh copies of the prompt and the pack; it reads for leaks and does not solve). Its answers, as returned:

1. How-to sentences
- growth_policy PDF 2.2: "Each install is bought by at most one channel, the one whose ad drove it, whether or not the attribution partner can name it; an install no ad drove is organic." Tells the reader that unnamed (untracked) installs still belong to channels, so attribution rows alone undercount.
- PDF 2.2: "An install is the first install of a new consumer account. A second device, a reinstall, a staff account and a test account are not installs." Population filter (accounts.account_type, attribution is_reinstall).
- PDF 2.3: "...every charge the App Store, Google Play or the web checkout made on its account in the 365 days from the install, each at the time of the transaction, less the net revenue of any of those charges refunded." Window and revenue sources.
- PDF 2.4: VAT 21/22/23 per cent by storefront, store commission "15 per cent of the price net of VAT", web "3 per cent of the price net of VAT". Formula.
- PDF 2.6: "the 12-month net revenue that one more euro of spend returns at that spend, every week of the period raised in the same proportion." Defines the marginal as a proportional scale-up of every week.
- PDF 2.1: spend "as the platform bills it"; 3.1 band cut-offs 1.20 / 0.90; 4.1 "each return is an estimate, and it is given as a committed figure".
- paid_budgets_weekly xlsx, Changes sheet, column "Reason": e.g. "Finance asked for a hold while the January agency invoice is disputed", "CEO asked for a higher run-rate ahead of the January board pack", "Card limit reached on the ad account..." Not instructions, but they say spend moves were decided by finance/management, i.e. not by performance.
- skadnetwork_conversion_values.json: "measurement_window_hours": 48; bits for sessions_bucket, trial_started, purchased. Says how the SKAN value is encoded.

2. Ranking or scoring of channels
none. (PDF 3.1 gives band thresholds only; no file scores a channel. ad_spend_daily and creative_tests carry network-reported installs, which are raw counts, not a ranking.)

3. Files that exist only to help the analyst
- skadnetwork_conversion_values.json (a codebook for accounts.conversion_value_48h and skan_postbacks.conversion_value). Closest case; a real company would hold it as the SKAN config.
- growth_policy PDF is a governing document, not a helper; no data dictionary, README or file map exists.

4. Figure or name that reads as the answer
none. Band thresholds (1.20, 0.90) are definitions. The media_plan "Stretch case" sheet gives stretch spends (about 1.3x to 2x plan), which are inputs the request asks to be evaluated at, not results.

5. Filed sentences that fix computation, read word for word
- PDF 2.1: return = 12-month net revenue of the installs the plan's 52 weeks of spend buys, divided by that spend; the plan's weekly spend "as the platform bills it" (media_plan "Growth channels" sheet, weeks 1 to 52 of 2027, EUR).
- PDF 2.2: count only first installs of accounts with account_type consumer; exclude reinstalls; attribute to the channel whose ad drove it, including installs the partner cannot name.
- PDF 2.3: sum every charge on the account (store and web, from billing_events) with transaction_at within 365 days of install_time, each at its transaction time, minus refunds of those charges.
- PDF 2.4: net = price / (1 + VAT) (21/22/23 per cent by storefront), then for store charges multiplied by 0.85, for web charges by 0.97.
- PDF 2.6: marginal = change in 12-month net revenue from one more euro with every week scaled by the same factor, at the plan spend and at the stretch spend.
- PDF 3.1: band by return at the plan's weekly spend: >= 1.20 scale, >= 0.90 and < 1.20 hold, < 0.90 cut.
- PDF 3.2 (with the prompt): "latest year of installs that are twelve months old" is read by the prompt as the year to 2 November 2025.
- PDF 4.1: records to the start of November; the figure is "committed" (one number, not a range).
- PDF 2.5: prices 9.99 monthly, 59.99 annual, seven-day free trial, unchanged in 2027.
- PDF 1.2: the Apple Search Ads brand sheet is outside the placement.

6. The one thing
- Candidate: the Changes sheet of paid_budgets_weekly_2024-2026.xlsx, a log of every deliberate spend move with an administrative reason (finance holds, top-ups, board-pack requests, phasing). Once noticed it tells the analyst the spend variation is management-driven and so usable to read how installs respond to spend. It would settle how to measure the response of installs to spend (the planned and stretch return, and the marginal return), not the revenue side or the per-install figures. The PDF's 2.2 ("whether or not the attribution partner can name it") is a second pointer, settling that installs lost to tracking must be assigned to channels (affects installs a week and per-install revenue, not the response).
- Neither alone makes most of the ask routine; no sentence names a response model, a lag or a saturation form.
- Per ask:
  - Return at plan and stretch spend: analysis (response to spend, revenue per install, forward estimate for installs not yet 12 months old), plus rule application for the revenue formula (2.3, 2.4).
  - Installs a week and 12-month net revenue per install at plan spend: analysis, with a definition read (2.2 population, which accounts count, partner-unnamed installs).
  - Marginal return at plan and stretch spend: analysis, with a stated procedure (2.6, scale every week proportionally).
  - Net revenue per install of the year to 2 November 2025: mostly a stated rule (2.3, 2.4, 2.2) over the files; reading and following definitions, with refunds, VAT by storefront and the web/store commission to get right. No planted item seen.
  - Band per channel: rule application of 3.1 on the return.

7. Generated or exercise-like
- paid_budgets Changes sheet: the "Change against the seasonal base" column holds only nine values ("-25%", "-30%", "-35%", "-40%", "+35%", "+40%", "+50%", "+60%", "back to base") and the "Reason" text is drawn from a short list repeated with month names swapped ("Planning trimmed March to stay inside the half-year envelope", "...October...", "...September...", "...December..."). Regular for a real log. Also three reasons recur in near-identical form ("Unspent brand budget moved across for March / May / June / August / February").
- media_plan_2027.xlsx: weekly plan values are step functions repeated exactly for 4 to 9 weeks and the stretch case is a fixed multiple on each channel (e.g. Meta iOS 5070 to 6591 is x1.3, Pinterest iOS 2510 to 4392.5 is x1.75), too regular for a real stretch plan. Zip entry dates 01-01-1980 inside media_plan_2027.xlsx (library signature). Title row "Draft for the insertion orders, 30 October 2026" reads naturally.
- Workbook authors: media_plan creator "Ester Rey", last modified by "Rafa Naranjo"; budgets "Rafa Naranjo". Plausible.
- PDF is one page and self-describing as policy ("What this policy is for"); the "Version 3 adds ... (2.3, 2.4), ... (2.6), ... (3.1) and ... (3.2)" sentence (4.2) maps the new clauses to this task's exact asks, which reads as written for the exercise. Producer is LibreOffice (fine).
- File names with date ranges and the ad_spend campaign names ("ES_Today_Tab_Test", "NewYear_Push_PT") read like real exports. skan JSON "config_version": 3 / "in_use_since" fine.

Ruling on `media_plan_2027.xlsx`: 156 ISO dates after 2026-11-09
Harmless: they are the plan's own week-starting dates for 2027 (52 weeks x 3 sheets = 156), the forward plan the request is about, not information leaking from after the data cutoff.

Second read, 2026-11-21, of the cut with pack digest 877eafb222142fa6 (the first read's two fixes in: the budget sheet's change log rewritten and the policy's clause 4.2 cut to one line; the same isolated reader set-up, a fresh reader shown only fresh copies of the prompt and the pack, asked in addition to read every row of the change log and every clause of the policy). Its answers, as returned:

### 1. Which sentence or file tells you HOW to do any part
- growth_policy PDF 2.1: "A channel's return for a period is the 12-month net revenue of the installs the period's spend on the channel buys, per euro of that spend. For a plan year the period is the plan's 52 weeks and the spend is the plan's weekly spend on the channel, as the platform bills it." (formula: 12-month net revenue per euro of spend)
- PDF 2.2: "Each install is bought by at most one channel, the one whose ad drove it, whether or not the attribution partner can name it; an install no ad drove is organic." This tells the analyst attribution is incomplete (the attribution partner cannot name every install) and that unattributed ad-driven installs belong to channels. It names the issue but not the method.
- PDF 2.3: "net revenue of every charge ... in the 365 days from the install, each at the time of the transaction, less the net revenue of any of those charges refunded."
- PDF 2.4: VAT 21/22/23 per cent by storefront; "store's commission of 15 per cent of the price net of VAT"; "web checkout charge, the card processor's fee of 3 per cent of the price net of VAT."
- PDF 2.6: "A channel's marginal return at a stated spend is the 12-month net revenue that one more euro of spend returns at that spend, every week of the period raised in the same proportion." This fixes the marginal as a proportional raise of all weeks (a definition, hints at a spend-response curve).
- PDF 3.1: band thresholds 1.20 and 0.90. PDF 4.1: "so each return is an estimate, and it is given as a committed figure."
- paid_budgets_weekly_2024-2026.xlsx sheet "Changes" (column D "Change against the seasonal base", F "Reason"): discloses that weekly budgets were moved by logged ad hoc steps (e.g. "+60%", "-40%", "back to base") against a "seasonal base". Gives the budget-variation history in plain view, not a method.
- skadnetwork_conversion_values.json: describes what fine value bits mean ("sessions_bucket", "trial_started", "purchased", "first 48 hours"), so tells how to read conversion_value.
- Prompt: "each channel's return has to be estimated from our records to 8 November 2026" (the estimation horizon); "at the plan's weekly spend and at its stretch spend".

### 2. Which file ranks or scores the channels
None as a ranking of return. Closest: none of the files computes return or ROAS. (Campaign names such as "AppDiscovery_ROAS_D7-ES" are only names; creative_tests holds reported installs per arm; ad_spend holds installs_reported_by_network. None ranks channels on 12-month return.)

### 3. File that exists only to help the analyst
- skadnetwork_conversion_values.json (a bit-layout decoder for `conversion_value` / `conversion_value_48h`).
- growth_policy_paid_channels_v3_2026-09.pdf is partly a definitions document (sections 2.2 to 2.6 define install, 12-month net revenue, net revenue of a charge, marginal return), and the "Changes" sheet of paid_budgets_weekly explains why budgets moved. No file says how the files fit together (no README or data dictionary).

### 4. Figure or name that reads as the answer
- Nothing states a return, band or per-install revenue. Only the policy thresholds (1.20, 0.90) and the plan/stretch spends exist. The stretch sheet gives each channel a different stretch multiple of plan (e.g. Meta iOS 5070 to 6591, Pinterest iOS 2510 to 4392.5, AppLovin 5680 to 8236) which says where the plan expects spend to go but not a result. The sheet title "Growth channels" and the PDF 1.2 "Spend on the brand sheet ... is not placed under this policy" only scope the question.

### 5. Filed sentences that fix computation, read literally
- PDF 2.1: return = 12-month net revenue of the installs that the period's spend buys / that spend; period = plan's 52 weeks (ISO weeks 1 to 52 of 2027, week starting 2027-01-04 to 2027-12-27); spend = media plan "Growth channels" weekly figure per channel (as billed). Literal: per-channel total 2027 spend (e.g. Meta iOS 220,250) is the denominator; numerator is a forecast of the 12-month net revenue of installs that spend buys.
- PDF 2.2: counts only first install of a new consumer account; exclude second device, reinstall, staff, test accounts (accounts.account_type consumer/staff/test; attribution is_reinstall). Each install bought by at most one channel (the one whose ad drove it) including installs the partner cannot name (attribution media_source blank/NaN, 38,745 of first 100k rows, vs "organic" 23,000), so the literal reading is that blank-source installs may belong to channels and must be assigned.
- PDF 2.3: window = 365 days from the install timestamp; includes all store and web charges on the account, each at the transaction's time (transaction_at), minus refunds (refund rows, refund_of_event_id).
- PDF 2.4: net = price/(1+VAT) with VAT by storefront ES 21, IT 22, PT 23; then minus 15 per cent of that (stores) or 3 per cent of that (web). Literal formula: price/(1+v) x 0.85 or x 0.97.
- PDF 2.5: prices 9.99 month, 59.99 year, 7-day trial, unchanged in 2027.
- PDF 2.6: marginal return at spend S = 12-month net revenue from one extra euro, with every week raised in the same proportion (a uniform scale of the weekly plan, not a one-week bump).
- PDF 3.1: band thresholds on return at the plan's weekly spend (not stretch): >=1.20 scale; 0.90 to <1.20 hold; <0.90 cut.
- PDF 3.2: lists the per-channel figures; "the 12-month net revenue per install of the installs it bought in the latest year of installs that are twelve months old". Prompt pins this year as "the year to 2 November 2025".
- PDF 4.1: records "to the start of November"; return "given as a committed figure".
- PDF 1.2: channel = ad platform on one OS; brand sheet (Apple Search Ads) not placed.
- billing_events: `environment` column ("production" vs "sandbox", 201 sandbox rows) and `recorded_at` vs `transaction_at` (PDF 2.3 says "at the time of the transaction"), literal rule picks transaction time.

### 6. ONE thing that would make most of it routine, and nature of each ask
- Candidate: media_plan_2027 stretch sheet plus the "Changes" sheet of paid_budgets_weekly. The Changes log (columns Change against the seasonal base, Planned for, Reason) shows spend moved by finance and management for reasons unrelated to performance ("Cash plan, Dec: variable lines down", "Investor update in January", "CEO asked for a higher run-rate ahead of the June board pack"), which makes the weekly spend variation look like an exogenous, usable lever for estimating how installs and return respond to spend. Once noticed, it settles the marginal-return and stretch-spend asks (the response curve) but not the per-install revenue, the 2025 cohort figure or the attribution of unnamed installs.
- Second candidate: PDF 2.2 ("whether or not the attribution partner can name it") signals that the blank media_source installs include channel-driven installs (tracking_status denied/not_determined iOS, skan_postbacks). Noticing it settles the install counts per channel only.
- Neither settles most of the request on its own; the request has several different asks (return at plan and stretch, installs a week, revenue per install, marginal at plan and stretch, 2025 year revenue per install, bands).
- Per ask:
  - Band per channel: depends on analysis (estimation of return) followed by a stated rule (thresholds in PDF 3.1).
  - Return at plan and stretch: analysis (forecast of unobserved 12-month revenue for young cohorts, response to spend), with stated formula (PDF 2.1 to 2.4).
  - Installs a week at plan spend and revenue per install: analysis (attribution of installs to channels, spend response), with stated rules (PDF 2.2 to 2.4).
  - Marginal return at plan and stretch: analysis, with a stated definition (PDF 2.6).
  - 12-month net revenue per install for installs to 2 November 2025: mostly following a stated procedure (PDF 2.3, 2.4) on the billing file, plus the attribution of blank-source installs to channels (analysis) and the reading of store/product ids (three product-id spellings in billing_events: zancada.premium.monthly, premium_monthly, web_premium_monthly) and sandbox/reinstall/staff/test exclusions (field and code reading).
- Planted-looking items: 201 sandbox rows in billing_events, 23 staff and 8 test accounts, 420 reinstall flags, three product-id spellings, brand Apple Search Ads campaigns inside ad_spend (to exclude per PDF 1.2), storage "Apple Search Ads" in the budgets workbook but not in the plan's growth sheet.

### 7. Anything that reads as generated
- Plan sheets: stretch spend values like 8429.5, 4392.5, 41356.5 are plan x a constant per channel with half-euro results; plan spend is flat within blocks of 4 or 5 weeks and steps down by the same proportion across all seven channels at once (e.g. weeks 5 to 8 all 0.89 of weeks 1 to 4), which looks formula-driven rather than a human media plan (media_plan_2027.xlsx, "Growth channels" and "Stretch case").
- media_plan_2027.xlsx zip entries all dated 01-01-1980 (library-written container); docProps shows Application "Microsoft Excel" 16.0300 with Creator "Ester Rey" and lastModifiedBy "Rafa Naranjo" (Rafa Naranjo also appears in the Changes sheet; Ester Rey appears nowhere else).
- Free text in "Changes" column F: many repeated, templated reasons ("Sponsorship dropped, budget back with us", "Conference cancelled, travel budget moved across", "CEO asked for a higher run-rate ahead of the June board pack", "Room in the envelope after the reforecast", "Back to base as agreed", "End of the hold-back", "ok", "as planned") reused across channels and years; columns D and E draw from the same small set of values (+35/+40/+50/+60, -25/-30/-35/-40; 3, 4, 5 weeks) ; each change is followed by a "back to base" row; the column title "Change against the seasonal base" reads as a modelling term. Many "back to base" rows carry blank reasons.
- The "Changes" sheet header "Planned for (weeks)" and the identical-length step sizes are very regular.
- PDF: wording "committed figure", "latest year of installs that are twelve months old" and tables of bands, "Replaces version 2 of 22 September 2025" fits a policy, but it is a one-page document of pure definitions with no motivation or history (no rationale, no change log from v2), and section 2.6's marginal definition is unusually technical for a growth policy. PDF metadata: Producer LibreOffice 26.8.2.2, Creator Writer, CreationDate Sep 21 2026 (word-processor export, consistent with the house scrub).
- File names: "skadnetwork_conversion_values.json" file date "Oct 24 2024" is before the pack's "in_use_since 2024-11-04"; harmless. File names with date ranges (accounts_2024-11-04_2026-11-01.csv) look like exports. ad_spend campaign names are realistic platform-style. No file name hints at a trap.
- Round-number regularity: billing amounts take exactly four values (9.99, 59.99, -9.99, -59.99), prices constant for two years, and exactly 6 rows per month in web_checkout_settlements.
- Distractors visible: store_ratings_daily, creative_tests, skadnetwork json (not named as such).

### Ruling on the sweep line
`media_plan_2027.xlsx`: 156 ISO dates after 2026-11-09: harmless. The file is the 2027 media plan, drafted 30 October 2026, and the prompt itself asks about the 2027 plan, so the weeks starting 2027-01-04 to 2027-12-27 (52 weeks x 3 sheets = 156) are the plan's own calendar and reveal no result or method.

After the second read the final cut (pack digest 4811ca4627b3e1d3) changed seven cells of the change log's Reason column and nothing else in the pack: five reasons that stood twice in the same words, and two rows the re-deal moved with them, now carry another of the same writer's reasons, so that no reason for a budget move is written twice in the same words. One new wording entered the pack with them, the closer "Invoice settled" on the row that ends a hold over a disputed agency invoice, and no third read was run; the mechanical sweeps above are of the final cut. The rulings on both reads are in the design note's `## Leak rulings`.

Third read, 2026-11-24, of architecture 8's cut (target.zip md5 f4049ea8cb8e1f093e06abd50e203724; one isolated reader on Sonnet at medium, shown only fresh copies of the prompt and the pack; it reads for leaks and does not solve). Its answers, as returned:

1. Method, step, comparison, adjustment, grouping, population or window
Several filed sentences fix populations, windows and conventions. None names a method or estimator.
- growth_policy_paid_channels_v3_2026-09.pdf s2.2: "An install is the first install of a new consumer account. A second device, a reinstall, a staff account and a test account are not installs. Each install is bought by at most one channel, the one whose ad drove it, whether or not the attribution partner can name it; an install no ad drove is organic." This fixes the population. It also says the attribution partner may not name every ad-driven install.
- PDF s2.1: "For a plan year the period is the plan's 52 weeks and the spend is the plan's weekly spend on the channel, as the platform bills it."
- PDF s2.3: "...every charge the App Store, Google Play or the web checkout made on its account in the 365 days from the install, each at the time of the transaction, less the net revenue of any of those charges refunded."
- PDF s2.4: VAT of "Spain 21 per cent, Italy 22 per cent, Portugal 23 per cent, by the storefront". Store commission of "15 per cent of the price net of VAT". Web processor fee of "3 per cent of the price net of VAT".
- PDF s2.6: "A channel's marginal return at a stated spend is the 12-month net revenue that one more euro of spend returns at that spend, every week of the period raised in the same proportion."
- PDF s3.1: bands are scale at 1.20 or more, hold at 0.90 to under 1.20, cut under 0.90.
- PDF s4.1: "each return is an estimate, and it is given as a committed figure."
- prompt.txt: "how many payments on the monthly plan the installs it bought in the year to 2 November 2025 made in their first 12 months, per 100 installs". This fixes that population and window. "at the weekly spend the plan gives it" fixes the spend.
- PDF s1.2 excludes the brand sheet (Apple Search Ads) from placement.
- paid_budgets_weekly_2024-2026.xlsx 'Changes' sheet is a log of budget changes with reasons. It states no method.

2. A file that already ranks or scores the candidates
None. Nothing ships a per-channel return or a band. creative_tests_2025-2026.csv has per-arm network-reported installs only, not a ranking on the return question. The media plan has spend only.

3. A file that exists only to help the analyst
None as such. The nearest is skadnetwork_conversion_values.json, a conversion-value schema ("sessions_bucket", "trial_started", "purchased"). It documents the conversion_value fields in accounts and the SKAN postbacks, so it is a field dictionary. The PDF policy is a definitions document, but the question needs it.

4. A figure or name that reads as the answer
None. The nearest items are context:
- PDF s3.1 band thresholds (1.20 and 0.90). They are the task's bands, not results.
- media_plan_2027.xlsx "Total 2027" rows: 1135390 on Growth channels and 1497772.5 on Stretch case. They are plan spend, not results.
- The Stretch case sheet is a spend schedule only.

5. A filed sentence that fixes how a graded figure is computed or over which population
- PDF s2.3: "...the net revenue of every charge the App Store, Google Play or the web checkout made on its account in the 365 days from the install, each at the time of the transaction, less the net revenue of any of those charges refunded." Read literally, each install's revenue is the net of every charge in its first 365 days, including the trial-end first charge, renewals and web charges, minus refunded charges. Charges are taken at their transaction time.
- PDF s2.4 plus s2.5: net revenue per charge is price, less VAT by storefront, less 15% (store) or 3% (web) of the net-of-VAT price. Prices are EUR 9.99 a month and EUR 59.99 a year.
- PDF s2.1: return is the 12-month net revenue of the installs the plan year's spend buys, per euro of that spend. It is evaluated at the plan's weekly spend over 52 weeks.
- PDF s2.2: each install is credited to the one channel whose ad drove it, even where the attribution partner cannot name it. Read literally, installs with no media_source in the attribution file can still belong to a paid channel. Organic installs are those no ad drove.
- PDF s2.6: marginal return is the response to scaling every week's spend by the same proportion.
- prompt.txt: payments per 100 installs counts monthly-plan payments in each install's first 12 months, for installs in the year to 2 November 2025. It is not revenue, so it is a count of charges.

6. One thing that would make most of the ask routine
I found no single file, sentence or planted pattern that settles most of it. The nearest candidate is PDF s2.2, the sentence "whether or not the attribution partner can name it". It tells the analyst that installs the attribution partner leaves unnamed still belong to paid channels. It settles the credit population only. It does not give any channel's return, its response to spend, its 2027 estimate, the plan totals or the bands. The marginal return, the response curve and the extrapolation to a 2027 year not yet twelve months old are all left to the analyst.
By part of the ask:
- Band per channel: analysis, applying PDF s3.1 to estimated returns. The band cuts are a stated rule, but the figure being banded is an estimate.
- Committed 2027 return per channel, in euros of 12-month net revenue per euro of spend at the plan's weekly spend: analysis. The inputs are the attribution, accounts and billing joins. The 2027 return is a forward estimate under a spend response, since the installs are not yet twelve months old. The definition (PDF s2.1 to s2.4) is a stated convention that has to be followed correctly, but it does not produce the figure.
- Monthly-plan payments per 100 installs in the first 12 months, for installs in the year to 2 November 2025: partly "reading a definition correctly" (which installs count, and which payments on which plan). The filed population and window mean it is mostly counting, though assigning unnamed ad-driven installs to channels (PDF s2.2) and net-of-refund handling take real work.
- Plan-level installs bought by 2027 spend: analysis, a forward estimate of installs from spend.
- Plan-level 12-month net revenue of those installs: analysis, a forward estimate that chains installs and revenue per install.
Nothing here turns on catching a planted item as such. The sandbox, staff and test accounts and the reinstalls are named in the policy.

REVIEW item: `media_plan_2027.xlsx` dates after 2026-11-09: harmless. The file is the 2027 plan, so its 52 weekly rows (2027-01-04 onward, repeated on the three sheets) are the forward spend the prompt asks about.

Main thread, 2026-11-24: nothing to fix. Every quoted sentence is a definition of population, window or convention that executes to the golden's own (the policy's 2.1 to 2.5, the prompt's monthly plan and its year to 2 November 2025); no file ranks, helps or answers; question 6 finds no one thing. The two stump-vocabulary lines are ruled in the design note's `## Leak rulings`.
