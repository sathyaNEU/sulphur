# leak check, task9

**Verdict: REVIEW.** 21 files read, 63 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: settlements, architecture, ostvale, missed, strikes, review, sentence, method, carried, golden, careful, expectation, result, published, closed, recovery, outside, forecast, standing, schedule, estimator, results, priced, dependence, default

## 2 author vocabulary (REVIEW 2)
- **REVIEW** `IPS_Schedule_D_Volatility_Premium_Sleeve.pdf`: \bladder\b x7, a field term declared in metadata.json: ...carries its receipts in the Foundation's cash plan. D.2 Program (a) A ladder is one swap of a given maturity sold on every monthly sale date at a...
- **REVIEW** `Indicative_Terms_3M_6M_Variance_Swaps_2027.pdf`: \bladder\b x4, a field term declared in metadata.json: ...Capital Markets, Wexcombe Bank, N.A.). November 4, 2026. Term 3-month ladder 6-month ladder Product S&P 500 Index variance swap, Foundation sells...

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `IPS_Schedule_D_Volatility_Premium_Sleeve.pdf`: carries 5 of 5 distinctive words of the committed call: 'Set the new 3-month ladder at USD 114,400 a point per monthly sale'
- **REVIEW** `Indicative_Terms_3M_6M_Variance_Swaps_2027.pdf`: carries 4 of 5 distinctive words of the committed call: 'Set the new 3-month ladder at USD 114,400 a point per monthly sale'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `IPS_Schedule_D_Volatility_Premium_Sleeve.pdf`: 5 of 25 stump-paragraph terms appear (settlements, review, published, closed, schedule); read whether the document names the move

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `CFF_VolPremium_Blotter.xlsx`: 24 ISO dates after 2026-11-10, e.g. 2026-11-20, 2026-12-18, 2027-01-15, 2027-02-19, 2027-03-19
- **REVIEW** `NYSE_Holidays_2026_2028.csv`: 26 ISO dates after 2026-11-10, e.g. 2026-11-26, 2026-11-27, 2026-12-24, 2026-12-25, 2027-01-01

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 21 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Stage 4 reader, 2026-11-10, on cut 4a76ff2f (target.zip sha256), one isolated thread that saw only prompt.txt and the
unzipped pack and solved nothing. Its answers, as returned:

1. Sentences that say how the analysis is done: schedule D.5(b) ("A program is inside the limits if neither would have
   been exceeded in any calendar year or on any day of the record had every ladder of the Sleeve been sold at its size
   on every monthly sale date of the record. A monthly sale date of the record counts for a ladder whether or not the
   volatility index for that ladder's maturity was yet being published on that date."); D.5(a), (c), (d) and (e) (the
   record from January 2007, a settlement in the calendar year of expiry, collateral as the open swaps taken together
   valued against the Sleeve "on the basis the dealers use for their daily valuations", no discounting); D.7(a) to
   (e) (open swaps at their expected settlement, unsold swaps at the ladder's record average per sale "taken over the
   swaps that would have expired by the review date", "the experience is that of the whole record and not of the
   Sleeve's own years alone", and the two 80 percent ranges); D.2 and D.8 (sale date, expiry, sizes, the review
   date); D.3 (the strike index and the cap); the master confirmation's sections 2 to 4 ("contract definitions, not
   method choices"); the annex summary (exposure never above the capped settlement; one dealer in variance units);
   the term sheet ("The panel will paper one ladder").
2. Files that rank, score or size: none. The term sheet's "up to USD 200,000 per monthly sale" is a quote ceiling; the
   statements carry the open swaps' values and the ledger the posted collateral, "context for the open swaps, not a
   size or a plan figure".
3. Files that exist only to help the analyst: none clearly (the term sheet is the request's context, the holiday file
   a reference calendar, the statement of net assets the source of Reference Assets).
4. Figures or names that read as the answer: none.
5. Sentences that fix a graded figure: D.5(b)'s second sentence (sale dates before an index began count; "The quoted
   sentence does not say what strike applies when the index did not yet exist ... nothing in the files fixes how the
   missing strike is filled. This is a gap: the quantity cannot be read off the files as they stand"); D.7(b) (the
   average over swaps expired by the review date, 9 November 2026 being the last close in the files); D.7(c) (the
   whole record); D.7(d) (the range of the average, not of a single settlement); D.7(e) (the range of the year's
   settlements); D.4 (2.0 and 3.0 percent of USD 1,487.6 million); D.5(d) ("partly ambiguous": the dealers' basis has
   to be inferred from the annex and the valuation files); D.2(a); the confirmation's observation days; the annex's
   cap on a transaction's exposure.
6. One thing: "Nothing single. The parts need separate work." The size and the binding day turn on analysis (daily
   valuation through the record) with the dealers' basis as a reading step; the ladder's record before its index
   existed "needs a fill-in rule, which D.5(b) leaves open"; the ranges turn on uncertainty analysis and on reading
   D.7(d) and (e); the open swaps' expected settlement turns on analysis; the plan combines a stated rule with
   analysis for its range. The dealers' date formats, units and references are "conformation, not a planted trap".
7. Realism: the three statements' date cells wrap inside the date ("11/24/202" then "5"); settlement amounts agree to
   the cent across the two dealers on a sale date; the blotter is booked by one desk mailbox with order numbers in
   date order; the VVIX history starts sparse (as Cboe publishes it); the policy's "the experience is that of the
   whole record" and the term sheet read as written with a reader in mind.
8. Sweep lines: the policy and the term sheet state no size, plan figure, range or choice of maturity (harmless); the
   blotter's and the holiday file's later dates are open swaps' expiries and scheduled holidays (harmless).

Main thread's rulings (2026-11-10):
- Question 5, the strike where the index was not yet published: intended. D.5(b) files the population (those sale
  dates count) and no sentence files the method; the two-sided rebuilds agree inside every band, the one-index
  stand-ins sit 2.3 points high on the overlap's 102 stressed days (named data), and the index's own earlier history
  on FRED, which is not in the pack, puts the ladder's record inside the same bands. The judge's reading decides.
- Question 5, the dealers' basis: intended. The statements print accrued and implied variance to expiry swap by swap,
  and the annex files the cap on exposure; the four readings of the term structure stay inside the bands.
- Question 7: the statements' date columns are widened in the generator (a layout defect, no figure). Settlement
  amounts agreeing to the cent are what one formula on published closes gives two dealers, and the 104 settled
  confirmations reproduce to the cent. The desk mailbox and the ordered order numbers are how the blotter is kept.
  D.7(c) is a governance sentence that closes a fork (whose experience) and names no method.
