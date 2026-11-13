# task20 determinism check (run t20v3a)

**Verdict:** NOT_DETERMINISTIC (one Gate E wording fork in the prompt; the peak, facility and most supplementary figures could not be fully re-run, see Limits).
**Disposition:** SEND_BACK (prompt wording, one clause), plus a FIX_NOW band check on the customer-payments figure.

## Evidence (recomputed from a fresh unzip, by the blocks' own method)

| Item | Blocks | Recomputed | Result |
|---|---|---|---|
| 2022 records: peak of statements + day-ahead settlements - customer payments received (restated 8 Mar statement kept) | 548.5 on 26 Aug 2022 | 548.46 on 26 Aug 2022 (flat Sat/Sun after) | reproduced |
| Hedge ratios 31 Dec 2026, Fjordal counted (positions file 211/78 MW, Oct 2026 budget 3,974/3,947/3,940 GWh) | 68.6 / 39.6 / 22.2 | 68.55 / 39.61 / 22.23 | reproduced |
| Exchange-only ratio 2027 | 46.5 | 46.5 | reproduced |
| NEX rule (front contract's own 2-day log moves, 99th pct, last 250 bd, Thursday review, 10% tolerance, state from notices) | reproduces notices | 199 of 218 notices exact to the cent, 3 false alarms (Base Month 88/100, Quarter 68/74, Year 43/44); the front-series variant that mixes contracts matches only 47 | rule recoverable; small residual convention |
| Desk rule: year-contract price / latest October budget price vs a Tuesday sale | threshold 1.25 | trade share 11% below 1.25, 0% at 1.24-1.25, 67% just above | threshold recoverable |
| Straum price = mean system price of 12 months ending 2 months before delivery | every invoice to the cent | 88 of 90 invoices within a cent (end offset 3 months: 0 of 90) | reproduced |
| Payment habits | 39/30/51/21 days | ledger 2022 on: mean 38.2 / 30.5 / 51.0 / 21.0 (ranges 32-47, 25-36, 39-60, 16-26) | mean habits, not fixed days |
| Payments received 1 Jan to 27 Aug 2027 on my stress system prices (stress curve = 2026-12-30 curve moved by 2022's same-month, same-date-of-year moves, delivery year offset by 5 years; sys price = next-month forward x 2022 ratio) | 173.7 (band 160-182) | 160.4 (Fjordal 22.1, Nesbyen 40.9, Straum 76.4, Bygdenett 20.9) | inside the band but at its lower edge, 13 below the golden |

## Forks run
- Exchange-only vs Fjordal-inclusive hedge ratio: ruled out by the policy's own definition ("sold forward at a fixed price") and the register; the Gate B fact is filed. No fork.
- Quantile convention for NEX (linear/higher/lower/nearest) on the same-contract moves was only run on the front-series version; the same-contract linear version reproduces the notices, the others are not distinguished here (not run on the stress year).
- Peak plateau: in 2022 the cumulative is flat Fri-Sun, so a calendar-day listing can name 28 Aug; the stated date is the first day (26 Aug). Inside the 2027 band (23-31 Aug) this does no harm; for the 2022 records pair the grader should accept 26-28 Aug or the blocks should say "first day".

## Findings
1. **Gate E, Supplementary 2 (prompt).** The prompt asks for "the exchange hedge book in TWh for each delivery year from 2027 to 2030" at the peak date. The blocks grade 2027 at 0.775 TWh, the part still to be delivered (consistent with initial margin on energy not yet settled). A solver reading the book as the contracted annual volume gets about 2.2 TWh for 2027 (211 MW plus desk sales, full year), and nothing in the prompt picks between them. 2028 to 2030 are unaffected. This is a reading split, not an analysis split.
2. **Customer payments (Gate C/A).** My independent run gives 160.4, at the band edge and 13 below the golden. I cannot tell from the files alone whether the gap is my calendar/mapping choices (2027 holidays, corresponding-date mapping of 2022 moves, invoice on the third business day, scatter in payment days) or the golden. Since payments feed the call directly (each 10 of payments moves the requirement about 10), the golden and the band for both payments and the requirement should be checked against the variants above.

## Limits
I did not rebuild the plant release model, day-ahead purchases or the desk's trades through the stress year, so 328.8, 27 August 2027, EUR 350 million, output 1,743 GWh, DA net 82.3 and initial margin 59.7 are not independently reproduced. The facts they rest on (stress standard, NEX rule, desk threshold, Straum window, hedge book, licence floor 700 GWh) are all filed and the sub-rules I tested reproduce. The 2022 pair figure (548.2 by method) was not re-run.

## Fix
- **prompt:** in the hedge-book ask add "still to be delivered after that date" (e.g. "give the exchange hedge book still to be delivered, in TWh, for each delivery year from 2027 to 2030").
- **solution:** re-run the payments figure against the variants listed (invoice date convention, 2027 holiday calendar, corresponding-date mapping); if any lands outside 160-182 or the requirement leaves 320-345, widen the band or pin the convention in the blocks. State "first day of the plateau" for both peak dates.
