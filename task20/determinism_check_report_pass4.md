# task20 determinism check (pass 4)

## Verdict: DETERMINISTIC

## Disposition: APPROVE

The pass-3 finding (property/infrastructure loan balance at Wexmoor's share did not reproduce) is
closed: with the six stop-after-2024 managers now drawn from equity/credit only, every real-asset
activity record runs to end-2026, and my independent recompute, by the same method as pass 3, lands
exactly on the blocks' new figures. Everything else that doesn't depend on the loan file or the minimum
reserve still reproduces exactly on the rebuilt files.

## Evidence

| Figure | Blocks | Recomputed | Status |
|---|---|---|---|
| Minimum reserve (policy) | 1,535 | 1,535 (confirmed in liquidity policy PDF text) | exact |
| Liquid reserve at policy factors | 2,778.7 | 2,778.7 | exact |
| Spending, 8 quarters | 791.0 | 791.0 | exact |
| Distributions H1/H2 2027, H1/H2 2028 | 685.6/466.2/273.9/291.3 | identical | exact |
| Commitments not yet called by strategy + total | 1,601.8/421.4/223.7/581.2/1,172.7/474.0/4,474.8 | identical | exact |
| **Property/infra loans due 2027-2028, Wexmoor's share** | **16 loans, USD 661.9m** | **16 loans, USD 661.9m** (same filter: latest asset-loan record per RE/Infra portfolio company, realized companies dropped, maturity in window, Commitment/Fund size) | **exact -- pass-3 finding closed** |
| Program re-up calls -> totals (A/B/C/D) | 288.9/180.1/139.8/17.4 | ties exactly from the blocks' own per-fund figures | exact |
| Headroom before 2027 commitments | 214.3 (180.9-238.4) | 214.2 from reserve - (791.0+1,955.5-1,717.0) - 1,535 | within rounding |

**Call vs. band vs. program lines (asked explicitly):** program A's calls (288.9) exceed the band's upper
edge (238.4) by 50.5 -- fails throughout the band. Program B's calls (180.1) clear the band's lower edge
(180.9) by only 0.8 -- thinner than pass 3's 1.7, but the band is the author's own stated alternative-fit
range and B clears it at every point inside it, so this is thin-but-clean (Gate C), not a competing
estimate straddling the line. Worth a sentence of caution to the author given how little room is left,
not a disqualifying fork.

**Open choices:** fiscal-year convention (FY2027 spending) and the liquid-holdings liquidity-class
assignment are closed the same way as pass 3, by the same filed facts (investment policy statement
section 2; the holdings workbook's own class column); both reproduced exactly above, so neither reopened
on the rebuilt files. No new fork found.

## Fix

None.
