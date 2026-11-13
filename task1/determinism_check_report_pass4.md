# Determinism check, pass 4 (re-judge after pass-3 SEND_BACK)

## Verdict: DETERMINISTIC
## Disposition: APPROVE

## What this pass targeted

Pass 3 sent the build back because "passes the rival" had two readings (crossing from
at-or-below to above the rival's comparable plan, vs. simply sitting above the rival's 2027
price) that disagreed on the Flanders 2027 first-bill cells for Onbeperkt and Gezin, because
those two plans had briefly sat above the rival's *old* Flanders price before the rival's July
2026 repricing. The author says the pack now makes both readings agree once the rival's most
recent (October 2026) scan is used region by region. I rebuilt this from the shipped files
directly rather than taking the claim on faith.

## Evidence

**Rival price scan, full series by (country, rival plan)** (`rival_price_scan_2024-01_2026-10.csv`,
promotion months excluded): confirms the rival's July 2026 change exactly as the Step-by-Step
states: BE Basis 10 uur rose from EUR 9.79 to EUR 10.29 (then NL matched at 10.29 from
2026-08); BE Onbeperkt rose from EUR 18.49 to EUR 20.49 (now equal to NL's 20.49); BE Familie
rose from EUR 22.49 to EUR 24.49 (now equal to NL's 24.49). BE Plus 30 uur never moved,
constant at EUR 16.99 in both regions throughout.

**price_list_2027.pdf, full table extracted** (pdfplumber, not a flattened text read -- the one
table on the page was read intact): gives all 8 past rises and the 2027 rise explicitly:
- 2025-01: Flanders Standaard 13.49->14.99, Onbeperkt 17.99->18.99; NL Flex 9.49->9.99, Gezin
  21.99->22.99.
- 2026-01: NL Standaard 13.49->14.99, Onbeperkt 17.99->18.99; Flanders Flex 9.49->9.99, Gezin
  21.99->22.99.
- Pre-2025 prices (unchanged since 2022) are stated as common to both regions, so each plan's
  pre-rise price is the same in NL and Flanders until its own region's rise.
- 2027: Flex 9.99->10.49, Standaard 14.99->16.49, Onbeperkt 18.99->19.99, Gezin 22.99->23.99,
  one price, both regions (prices had already converged region-wide by end of 2026).

**Region-by-region pass/fail of all 8 past rises against the plan's own pre-rise-month rival
price** (Dec scan before the rise, promotions out, matching the Step-by-Step's stated method):

| Rise | Region | Pre-price | Rival pre-rise | Post-price | Rival (same) | Crosses? | New price > rival? |
|---|---|---|---|---|---|---|---|
| Flex | NL, Jan25 | 9.49 | 9.79 | 9.99 | 9.79 | below->above | yes |
| Gezin | NL, Jan25 | 21.99 | 24.49 | 22.99 | 24.49 | below->below | no |
| Standaard | BE, Jan25 | 13.49 | 16.99 | 14.99 | 16.99 | below->below | no |
| Onbeperkt | BE, Jan25 | 17.99 | 18.49 | 18.99 | 18.49 | below->above | yes |
| Flex | BE, Jan26 | 9.49 | 9.79 | 9.99 | 9.79 | below->above | yes |
| Gezin | BE, Jan26 | 21.99 | 22.49 | 22.99 | 22.49 | below->above | yes |
| Standaard | NL, Jan26 | 13.49 | 16.99 | 14.99 | 16.99 | below->below | no |
| Onbeperkt | NL, Jan26 | 17.99 | 20.49 | 18.99 | 20.49 | below->below | no |

Both readings agree on every one of the 8 cells: the same 4 rises pass (Flex NL, Onbeperkt BE,
Flex BE, Gezin BE) and the same 4 do not (Gezin NL, Standaard BE, Standaard NL, Onbeperkt NL).
The pre-rise price is at or below the rival's comparable plan in all 8 cases, so "crosses from
at-or-below to above" and "new price sits above the rival" are the same test here; this matches
the Step-by-Step's "4 ... lost 10.8, 11.7, 9.9, 29.7 ... the others 7.8, -1.5, 4.0, 0.3" (a count
of 4 and 4).

**The 2027 cells, both regions, against the last (October 2026) scan**, per plan's end-2026
price (common to both regions by then: Flex 9.99, Standaard 14.99, Onbeperkt 18.99, Gezin
22.99) and the rival's October 2026 price in each region:

| Plan | Pre-2027 price | Rival Oct26, NL | Rival Oct26, BE | Below rival pre-rise (both regions)? | 2027 price | Passes (both regions)? |
|---|---|---|---|---|---|---|
| Flex | 9.99 | 10.29 | 10.29 | yes | 10.49 | yes, both |
| Standaard | 14.99 | 16.99 | 16.99 | yes | 16.49 | no, both |
| Onbeperkt | 18.99 | 20.49 | 20.49 | yes | 19.99 | no, both |
| Gezin | 22.99 | 24.49 | 24.49 | yes | 23.99 | no, both |

Every plan sits at or below the rival in both regions before the 2027 rise (the author's claim
holds, checked directly, not assumed), and the two readings of "passes" give the same answer in
both regions for all four plans: only Flex's 2027 price clears the rival, in NL and in Flanders
alike. This matches Step 4 ("in both regions only Flex's 2027 price passes the rival ... Flex
loses 10.5 per 100 ...") and Supplementary Q7's near-equal Netherlands/Flanders bands for every
plan (Flex 10.5/10.5, Standaard 3.8/3.7, Onbeperkt 0.8/0.9, Gezin 0.5/0.6), which is what you
expect once the rival price itself no longer differs by region at the comparison point. The
fork pass 3 found is closed: it is closed by a fact already in the shipped scan (the rival's
own July 2026 repricing, read region by region and at the right point in time), not by a new
assumption.

**Gate A spot check on the headline subscriber count.** Reproduced the 31 October 2026 paying
subscriber count independently from `payments_2024-01_2026-10.csv` and
`accounts_export_2026-11-03.csv`: counting only `status == collected` consumer accounts gives
6,780, 97 short of the stated 6,877. Counting a subscription as paying in October when its last
relevant row that month is `collected` **or** `re-presented` (a retried charge that succeeded)
reproduces the stated figures exactly and per plan: Flex 1,371, Standaard 2,146, Onbeperkt
2,136, Gezin 1,224, total 6,877. No other combination of statuses lands on 6,877; this is forced
by the data, not a free choice (a `collected`-only read undercounts every plan by about the same
share and is not a competing convention anyone would stop at, since it silently drops
successfully-collected-on-retry subscribers).

**Rival-plan mapping (Gate C).** Flex (10 hours, 1 profile) <-> Luistr Basis 10 uur; Standaard
(30 hours, 1 profile) <-> Luistr Plus 30 uur; Onbeperkt (unlimited, up to 2 profiles) <->
Luistr Onbeperkt; Gezin (unlimited, up to 4 profiles) <-> Luistr Familie. The hours and the
family/individual framing pin this one-to-one; no plan has two plausible rival analogues.

## What I did not re-derive this pass

The stops-that-come-back and stayers'-listening figures (Critical Components 2 and 3) and the
exact loss percentages in Step 3 were not rebuilt from the large payments/listening files this
pass; pass 3's SEND_BACK was specifically about the rival-read fork, and that fork is now closed
on the shipped scan and price list as shown above. The subscriber-count reproduction above is an
independent Gate A check on this pass's own initiative, not a re-check of a prior finding.

## Fix

None. No change needed to prompt, input_files or solution on this pass.
