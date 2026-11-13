# task1 architecture 5, reshipped cut (9ecc8c8): a platform run (pasted by the author with the holistic audit, 2026-11-13)

Score not pasted. Its recommendation: go ahead with Onbeperkt and Gezin, withdraw Flex and Standaard (golden then:
Gezin alone). Excerpts kept verbatim for the precedents.

## Its figures against the shipped golden

| Figure | Run | Golden (band) |
|---|---|---|
| Change in 2027 contribution, EUR per October subscription | Flex -1.58, Standaard -14.00, Onbeperkt +4.35, Gezin +0.91 | -4.4 (-4.7 to -3.2), -15.5 (-16.4 to -12.4), -5.9 (-6.3 to -5.0), 6.1 (2.5 to 7.8) |
| Paying at 31 October 2026 | 697, 1,222, 1,461, 1,010 (4,390) | exact |
| Still paying at 31 December 2027 | 160.4, 296.7, 693.9, 613.5 | 149 (143 to 158), 279 (273 to 299), 700 (685 to 720), 660 (628 to 679) |
| First-bill extra cancellations / downgrades per 100, Standaard | 11.36 and 10.88 / 44.09 | 21.2 / 16.1 |

## What it did unprompted (reflexes)

- "Selected small models using price-change size, crossing a rival's price, and compatibility with the next-lower
  plan. Leaving entire historical events out, cancellation prediction error was 4.64 per 100 versus 10.64 for a
  price-change-only model; downgrade error was 1.40 versus 13.65."
- "Included ordinary November attrition, December anticipation and a one-time first-bill response."
- "December anticipation is included. Historical notification dates are unavailable, so preceding-December
  associations are treated as an explicit planning assumption. Without anticipation, Flex changes from -EUR 1.58 to
  +EUR 1.16."
- "Used billing-month profile lists rather than assigning earlier listening to owners in profiles_export_2026-11-03.csv."
- "Counted progress is the positive increment above the previous cumulative maximum ... This prevents replay and
  multiple-device reports from being paid twice."
- "Ordinary cancellation in the 2026 holdout was 5.0338 per 100 observed versus 5.0620 predicted ... Usage holdout bias
  ranged from -0.34% to +2.07%."
- "Count downgrades as lost customers" and "Continue using the old 52% publisher tariff" listed as alternatives
  rejected.

## What it named and waved through

- "No reactivation, new acquisition or post-cancellation reporting costs are forecast."
- "Standaard's crossing response is an extrapolation."
- "Forecast account usage used recent history, plan/profile differences and seasonality." (no change in the stayers'
  listening after a rise)

## Where it went wrong

Onbeperkt only: the stayers' second profiles after a rise were never modelled, so Onbeperkt went ahead (+4.35 against
-5.9). Its Standaard response was nearer the world's truth than the golden's (see arch5_audit_2026-11-13.md).
