# Determinism check, task23, pass 2 (Gates A to E)

**Verdict:** DETERMINISTIC (call: package D).
**Disposition:** FIX_NOW (one wording/convention edit in the solution; no change to what solvers see).

## Evidence (fresh unzip, blocks' own method)

| Item | Block (band) | Mine | Status |
|---|---|---|---|
| 2025 report: 8,354 / 0.7844, 10% ox, 0.99 destr. | 2,149 | 2,149 | reproduced |
| Cell 5 MSW through Oct 2026 (VOID dropped, REISSUE kept, MSW* codes, arealess ticket to day's active cell) | 574,197 (1%) | 574,196.6 | reproduced; dropping both void and reissue 570,799 (-0.6%), inside band; no area fill 555,233 (outside, but the block says to fill) |
| Pressure response, 16 h EMA gap, log flux, chamber-month levels, dT, 6 h rain, AC-1+AC-3 QC OK, UTC-8 | 0.100 | 0.0997 (SS lowest at 16 h of 4..48) | reproduced |
| Mean campaign factor 2025 | 0.711 | 0.711 (DST clock in summer) | reproduced |
| 2025 actual emissions | 4,924 (10%) | 4,922 | reproduced |
| Same, campaign clock read as standard time all year | | 4,820 (-2%) | inside band |
| Same, lag 8 / 12 / 20 / 24 h (beta refit for 12, 8, 24) | | 4,762 / 4,925 / 4,868 / 4,749 (LST clock 4,588 to 4,820) | inside band (4,431 to 5,415) |
| 2026 campaign factor mean (cell 5 level input), lags 8 to 24 h, both clocks | | 0.78 to 0.84 vs 0.79 at 16 h | about +-5%, inside the 12% band on cell 5 generation |
| Oxidation: saturating V/(V+J), J = flux/(1-share), per-cover V15, one Q10 | daily 27.0 g/m2/d, Q10 1.89 | 27.03, 1.891 ("active" plots mean 39.3%) | reproduced |
| Call margin | C 5,549, D 4,495 vs 5,100 | with the 7% bands: C floor 5,160 (over), D ceiling 4,810 (under) | call holds inside every band |

Not recomputed (budget): cell 4 well split and +85.1, decay rates, cell 5 generation 3,752, the 2027 package table, the report bridge items +3,280/-467. Input files for each are present (well register, wellfield, recirculation log, fill plan, options paper).

Pass 1 findings re-tested:
1. Ticket wording: now "voided tickets dropped and their reissues kept"; matches. Closed.
2. Pressure fit and 2025 figure: reproduced exactly under the block's stated specification; pass 1's 0.06 / 4,250 came from a different clock or specification and is not a fork under the stated text. Rival lags and clock readings stay inside the band. Closed.
3. Q10: reproduced (1.891). Closed.

## Findings

A. **Cell 5 cover area (Gate C, low to moderate).** Step 6 uses 24.2 acres (Cells sheet footprint). The 2025 report lists cell 5 as 14.6 "filled area" acres, a 2025-only figure. A solver using 14.6 for the 2027 flux gets a flux about 1.66x higher; at roughly 105 g/m2/d (24.2 acres) versus about 174 g/m2/d, the share falls from 17.1 to about 11 per cent (my hand estimate, not a run), outside the 4-point band. The 2027 package totals move little (package D about +1 to 2 per cent, call unchanged). Fix (solution): in Step 6 say that the cover area is the cell's 24.2-acre footprint from the Cells sheet because the waste and the leachate lines cover the whole footprint in 2027 and the report's 14.6 acres is the 2025 filled area only, and add the 14.6-acre rival to `checks.py` (graded 17.1 share would then need either that ruling-out fact or a lower band edge).

B. Gate B: every decisive fact checked is filed (limit and selection rule, design capture and dates, costs, report equation, campaign table, 2019 plots, fill plan, leachate start July 13, 2026, footprint). No missing fact.

C. Gates D and E: asks pin one figure each with a unit; the report bridge order is pinned by the prompt. No finding.

## Fix
- prompt: none; input_files: none; solution: Finding A sentence in Step 6.
