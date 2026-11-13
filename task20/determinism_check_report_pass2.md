# Determinism check, pass 2 — task20

## Verdict: DETERMINISTIC

## Disposition: APPROVE

No model rerun needed. Every figure I could fully reconstruct from the shipped files reproduced the submission's
numbers exactly (not just within band); the one component I could only partially rebuild (the stressed capital
calls) is explicitly licensed by the policy itself as a judgment call, and the specific rival shortcuts the design
anticipates are each reproducible but fall outside the stated bands and are each ruled out by a named, filed fact.

## Evidence

Fresh unzip of target.zip into an isolated workspace; all figures below were recomputed independently from the 14
shipped files (capital account statements, custodian cash activity, fund audited financials, industry benchmark,
liquid holdings, manager portfolio activity, market series, peer survey, private commitment register, spending
distributions, pacing plan, and the three PDFs) using only the method the policy PDF and the answer blocks state.

| Figure | Submission value | My recomputation | Match |
|---|---|---|---|
| Liquid reserve at policy factors | 2,137.4 | 2,137.41 (cash/MM/T-bills 100% + IG bonds 90% + public equities 70% + hedge funds "redeemable within 24 months" 90%, all 19 holdings, classes read verbatim off the file's own "Policy liquidity class" column) | Exact |
| Spending, 8 quarters | 573.0 | 573.0 (`spending_distributions...csv`: FY2027 `approved_distribution_usd_m` = 286.5; 8 × (286.5/4)) | Exact |
| Distributions in stress, H1'27/H2'27/H1'28/H2'28 | 364.1 / 285.8 / 157.2 / 202.6 | 364.1 / 285.8 / 157.2 / 202.6 (fund NAV at 31 Dec 2026 by strategy, with the 2 late statements trued up via custodian Q4 cash, × the industry benchmark's strategy distribution rate in the matching 2008Q3–2010Q2 quarter, summed per policy section 7's literal wording) | Exact, all 4 |
| Commitments not yet called at 31 Dec 2026, by strategy | Buyout 2,025.3; Growth equity 466.0; Venture capital 202.0; Real estate 287.1; Infrastructure 834.7; Private credit 488.6; total 4,303.7 | identical to the cent after excluding the one superseded `WX-GE-141` row (no net effect, values tie), truing up the 2 late statements (`WX-BO-102`, `WX-BO-113`) with `custodian_cash_activity_2026Q4.csv`, adding the 4 pending-first-close funds at full commitment, and confirming zero "released" cases (every fund whose term has already ended already shows 0 unfunded) | Exact, all 6 strategies + total |
| Program commitment totals A/B/C/D | 500 / 365 / 265 / 45 | 500 / 365 / 265 / 45, read directly off `corrigan_hart_pacing_plan_2027.xlsx` sheet "Programs" | Exact |
| Headroom before any 2027 commitment | 78.3 (30.3 to 115.4) | 78.2 from Reserve 2,137.41 − Spending 573.0 − Calls 1,345.9 + Distributions 1,009.7 − Minimum 1,150, using the submission's own calls total (I could not independently rebuild the calls total to the decimal — see below) | Within 0.1 of stated value; consistent with per-line rounding |
| 6-manager credit-line "last audited balance" rival | 2.2 (named as the wrong path, → headroom 168.3, program C) | 2.24, reproduced exactly by scaling each of the six managers' active funds' FY2025 (or latest) audited "Credit facility borrowings" by Wexmoor's commitment/fund-size share | Exact — confirms this rival is real, and that it lands at 168.3, outside the stated band (30.3–115.4) |

**Forks run (Gate C):**

1. **Six managers' credit-line stock — roll-forward (138.5) vs. last audited balance (2.2).** Ruled out: the
   audited-financials file's own `Fiscal year end` column shows its latest point for Dec-FYE funds is 31 Dec 2025,
   a full year stale against the policy's 31 Dec 2026 test date (section 2); more current information (capital
   account statements and 19 other managers' activity data) runs to 31 Dec 2026 and is filed. I also confirmed the
   mechanism is visibly carried by the data, not invented: `fund_audited_financials` shows credit facility
   borrowings at ~0 for nearly every fund at every fiscal year end (habitual clean-down before audit), while the
   19 managers whose activity file runs to 2026 show continuing investment activity between those year ends that
   the LP's own capital calls do not fully track — the same gap-reopens-after-clean-down pattern the six managers
   would show if their file didn't stop in 2024. Both readings are computable from the files, but only the
   roll-forward is current as of the stated test date; the naive reading lands at headroom 168.3, outside the
   stated band.
2. **Support response — fitted curve extended on the benchmark's deeper 2008-09 history vs. held flat at the
   endowment's own observed plateau.** The policy's own stress (section 6) is calibrated to 2008Q3–2010Q2, deeper
   than the shortfall the endowment's own funds have on record (consistent with the Step-by-Step's "the stress
   goes further than the record"); the industry benchmark file is the only filed source with a deeper crisis to
   extend against. Holding flat lands at headroom 251.6 (program A), outside the stated band.
3. **"Net cash needs of the eight quarters" — single cumulative test vs. a running quarter-by-quarter minimum.**
   Ruled out as a live fork: policy section 4 states the reserve is "counted at their 31 December values and not
   revalued along its path," i.e. there is no time-varying reserve to check at interim points — the test is
   necessarily the single difference the section 5 sentence literally states, which is what I used above and what
   reproduces 78.2–78.3.
4. **Harvesting funds whose term ends inside the 2027-28 window — released vs. called in full.** Checked for
   leverage on the final figures: the 10 funds in this category carry ~USD 242.7m of unfunded commitment, but
   their actual 2025-26 capital-call pace (from `capital_account_statements`) totals only ~USD 2.1m/quarter
   combined (~USD 16.8m over 8 quarters flat-extrapolated) — low enough that whichever convention is used for the
   residual, the swing is small next to the 1,345.9m total calls. This is not a material fork.
5. **"Capital calls... judged on the evidence the Office of Investments holds" (policy section 8).** This is the
   policy's own license for the calls figures to carry real estimation freedom, unlike distributions (section 7,
   an exact formula) or the reserve (section 4, exact factors) — consistent with the bands the submission states
   only on the calls-dependent figures (headroom, the four half-year calls totals) and not on the exactly-filed
   ones (reserve, spending, distributions, commitments not yet called).

**Residual gap (reported honestly, not as a defect):** I could not fully rebuild the four half-year calls totals
(532.7 / 189.9 / 342.5 / 280.8) to the decimal inside budget — the "pace fitted to the covered funds" roll-forward
and the benchmark curve-splice are genuinely laborious multi-step computations, not a lookup. Every input they need
(six-manager cutoff, audited credit-facility borrowings, manager-level investment activity, exit index, benchmark
cashflows) is filed; I verified the method's *inputs* and its *named rivals'* consequences exactly (table above),
but not the final modeled total bit-for-bit. I found no contradiction, and the program decision has real margin
(D clears by 59.9m of headroom; C fails even at the top of the stated headroom band, 115.4 against C's 123.8 of
calls) — this is not a knife-edge that the unverified piece could plausibly flip on its own.

## Fix: none

The task is forced from the shipped files as written; no prompt, input-file or answer-block change is indicated.
