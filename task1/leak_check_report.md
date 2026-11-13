# leak check, task1

**Verdict: REVIEW.** 18 files read, 62 golden figures and 10 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: onbeperkt, golden, million, standaard, months, carries, trailing, account, pooled, family, december, accounts, listening, creation, carried, chosen, hurried, nearest, inside, priced, platform, graded, missed, uploaded, stayers

## 3 answer figures in the pack (REVIEW 6)
- **REVIEW** `SUL_licence_agreement_2027-2029_schedule_B.pdf`: golden figure 0.40 appears: ...For each month Kraanvogel pays each publisher EUR 0.40 for every counted hour of the publisher's titles...
- **REVIEW** `SUL_licence_agreement_2027-2029_schedule_B.pdf`: golden figure 3.1 appears: ...ed under schedule C. B3. Statements and payment B3.1 Kraanvogel sends each publisher a statement of it...
- **REVIEW** `SUL_licence_agreement_2027-2029_schedule_B.pdf`: golden figure 2.2 appears: ...ed hour of the publisher's titles in the month. B2.2 A profile's counted hours of a title in a month a...
- **REVIEW** `growth_planning_guideline_2026-10.pdf`: golden figure 3.1 appears: ...nce and the agencies' briefs. 3. Planning figures 3.1 A paying subscription is a consumer account whose...
- **REVIEW** `growth_planning_guideline_2026-10.pdf`: golden figure 3.3 appears: ...nthly charge was collected, on the plan charged. 3.3 An account's counted hours in a month are the cou...
- **REVIEW** `growth_planning_guideline_2026-10.pdf`: golden figure 3.8 appears: ...r cent after; Google 15 per cent), less refunds. 3.8 Forecasts use the licence agreement in force in t...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `growth_planning_guideline_2026-10.pdf`: 3 of 25 stump-paragraph terms appear (months, account, accounts); read whether the document names the move
- **REVIEW** `price_list_2027.pdf`: 5 of 25 stump-paragraph terms appear (onbeperkt, standaard, december, listening, nearest); read whether the document names the move
- **REVIEW** `spring_campaign_2027_quote_Bureau_Grauwe_Gans.pdf`: 3 of 25 stump-paragraph terms appear (onbeperkt, standaard, account); read whether the document names the move

## 8 column names (REVIEW 1)
- **REVIEW** `licence_server_renewals_2024-01_2026-10.csv`: columns a generator names and an organisation does not: device_id

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'pptx+xlsx' at 27% of 22 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 18 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)


## Solver's-eye read

### 1. Sentence/file that tells you how a step should be done
`growth_planning_guideline_2026-10.pdf` 3.10: "A January price rise goes ahead on a plan when it raises the 2027
contribution of the subscriptions paying on that plan at 31 October 2026, followed through 2027, against holding the
plan's 2026 price. A rise's extra cancellations and extra downgrades are those at a subscription's first bill at the
new price beyond what the same months would have brought without the rise, counted among the subscriptions that
reach that bill." This fixes the comparison, the population and the window for the go/no-go call, not the method of
computing either side.

### 2. File that already ranks/scores the four plans' rises
None. No file states a per-plan verdict, a ranked list, or a go/no-go. `price_list_2027.pdf` only says a rise "may
still be withdrawn ... until 30 November 2026" without naming which plan.

### 3. File that exists only to help the analyst
`growth_planning_guideline_2026-10.pdf`: pure definitions text, no transaction rows of its own; it exists only to
pin terms (paying subscription, net revenue, contribution, the rise test) that the raw tables don't define.
`publisher_code_crosswalk_2025.csv` (9 rows) is a small lookup aid for the same purpose on one file
(`remuneration_statements`), but that pairing (old-scheme, per-publisher statements) looks unused for this prompt:
the 2027 remuneration is a flat EUR 0.40 per counted hour (schedule B2.1), publisher-agnostic, so neither file is
needed to get a per-subscription remuneration figure. `catalogue.csv` confirms this: its publisher_code values are
all new-style (`PUB-####`, `KRV-EIGEN`, `PD`), never the old `U###` codes the crosswalk maps.

### 4. Figure or name that reads as the answer rather than context
None found. The plan names and both price lists are formula inputs (list price, VAT, app-store cut, the 0.40 rate),
not outputs; nothing states a euro delta, a subscriber count, or a loss/downgrade rate.

### 5. Filed sentences that fix a graded figure or its population (literal, not computed)
- 3.1: "The paying subscriptions on a plan at a month end are the accounts paying on the month's last day, on the
  plan charged" and "Staff and test accounts are not consumer accounts" — fixes the population for every subscriber
  count (excludes the real `staff`/`test` account_type rows the data carries).
- 3.5: net revenue = charge less VAT, less app-store fee (Apple 30% in a sub's first 12 paid months, 15% after;
  Google 15%), less refunds — fixes the revenue formula and the tenure-dependent Apple tier.
- 3.9: contribution = net revenue less remuneration on counted hours at the licence rate — fixes what "contribution"
  means.
- Schedule B2.1: EUR 0.40 per counted hour — fixes the rate.
- Schedule B2.2: counted hours are the increase in a profile's all-time furthest position in a title, and
  "Listening again to a part of a title the profile has already reached adds nothing" — fixes that counted hours
  are a cumulative, not a monthly, measure.
- Schedule B2.4: Kraanvogel's own productions and public-domain titles are not counted — fixes a population
  exclusion (confirmed present in `catalogue.csv` as `rights=own_production/public_domain`).
- `price_list_2027.pdf`: "Existing subscriptions move to the new price at their first billing date in 2027" — fixes
  when, per subscription, the new price and the "first bill" window start (not a flat 1 January cut).

### 6. Is there one thing that would make most of the prompt routine?
No. The closest candidate is B2.2's cumulative-position rule, and even noticing it only unlocks the remuneration
figures. I checked `listening_monthly...csv`: for a repeat-listened title, `furthest_position_s` is NOT monotonic
across months (e.g. profile P2672884/title T300546 reads 3207, 2918, 3207, 3207, 2622, ... across 30 months) — it is
a per-month figure, not the all-time maximum B2.2 requires, so naively differencing or summing it overcounts
re-listens. That settles only the counted-hours/remuneration pieces, not the go/no-go test, not the paying-subscriber
counts, not the per-country loss/downgrade rates, which come from unrelated parts of the pack.

Per ask: (a) go/no-go per plan: analysis (the comparison is a stated rule, 3.10, but both sides require assembling
revenue, tenure-tiered fees and counted hours across files). (b) euro change per subscription: analysis (same
build-up). (c) paying subscriptions per plan at Oct 2026: mostly reading a definition correctly (3.1, plus excluding
`staff`/`test`). (d) paying at end 2027 if the rise proceeds, and (e) remuneration on them: analysis (survivorship
through 2027 net of the rise's own extra attrition, plus the B2.2 trap). (f)/(g) per-100 lost/downgraded at first
bill, NL and Flanders: analysis — `price_list_2027.pdf`'s "Earlier price changes" section shows each of the 8
plan×country cells has exactly one historical precedent rise (2025 or 2026), so each cell's rate must be estimated
from its own cohort against a same-months baseline, not read off anywhere.

### Review-line verdicts
- `SUL_licence_agreement_2027-2029_schedule_B.pdf`: harmless. Its numbers (EUR 0.40, 52%, 2%) are rate/audit
  parameters the formula must use; their reappearance in a derived answer is expected, not a leak.
- `growth_planning_guideline_2026-10.pdf`: harmless. Carries no euro figures at all, only formula percentages
  (30%/15%/15%); same reasoning.
- `licence_server_renewals_...csv` (`device_id`): harmless. Checked cardinality on the full 598,230-row file:
  17,346 profiles to 17,336 devices, zero profiles with more than one device. The column carries no real
  multi-device aggregation requirement; it reads as a DRM/licence-checkout log (`licence_valid_until_utc` is
  consistently ~30 days after `renewed_at_utc`) covering a different, partial population from `listening_monthly`
  (e.g. profile P2672884 has zero rows here despite heavy monthly listening), so it looks like a realistic partial
  telemetry source, not a shortcut.
- `prompt.txt` deliverable set shared across a batch: harmless. "A workbook and a short deck" is a generic
  deliverable-format instruction, not a method, comparison, or figure; it names no file, no step, no population.

### Overall verdict
NO LEAK.

### Main thread's rulings (2026-11-13)

- Read on the cut before the rival scan's July 2026 alignment (a data-only change after the judge's pass 3): no document or the prompt changed after it, so the read stands (leak-check: the reader again only when a fix changes a document or the prompt).
- Q1, Q5: each quoted sentence fixes a WHAT (the comparison and population of 3.10, the definitions of 3.1, 3.5 and 3.9, the rate and the counting rule of schedule B, the price list's first billing date), and each executes to the golden's convention; none names a step. Harmless.
- Q3: the guideline is the governing standard, the crosswalk a Layer 1 lookup for the statements. Harmless.
- Q6: the counting rule's cumulative position (schedule B 2.2) is a Layer 1 assembly step graded nowhere. Harmless.
- Review lines (clause numbers and the rate, design-note vocabulary, device_id, shell quota): harmless.
