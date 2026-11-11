# task20: which of the equity facilitation desk's VaR breaches in the year to 30 June 2025 the model answers for

## Draw

Subdomain: Quantitative Finance, task type Risk modeling (VaR/ES, stress testing, credit and counterparty risk), carded under the taxonomy key `factor-return-attribution`, the one Quantitative Finance task type that serves Root-Cause
Analysis type: Root-Cause
Answer shape: A timeline of what went wrong and when (every breach date in the year under one heading, the engine's input failures dated, the counts adding back to the total, the count a sound model shows, the names to fix first and the add-on for the planned book)
Weight: investigation: most of the work is forming a cause for each breach, testing it by re-running the engine without that fault, and ruling it in or out; the last three builds sat on validation (task9), metric or rule design (task13) and synthesis (task15)
Data-native sentence: the desk's booked P&L, its position systems and its risk engine each record a different book on a different clock, so a breach only gets a cause once the forecast's own book is rebuilt and the engine is re-run with each of its faults removed in turn, on a real market tape whose volatility rose in bursts the engine's two-year window could not follow.
People: Nancy Ayala (head of market risk control, files the classification), Christopher Reilly (desk head, Small and Mid Cap Facilitation)

## Results chain (sketched at the draw; the full table is written at stage 2)

R1 the official count and zone (framing); R2 the breaches of the P&L the VaR forecast, the prior-close book revalued at the day's closes, with the masked days and the booked days that drop out (assembly and reconciliation); R3 the engine runs that read a book other than the prior close, outage reruns and late-booked blocks the 18:30 cutoff left out, and the breaches each caused (investigation loops); R4 the reported VaR as a share of a full own-name VaR across the year (modeling); R5 the breaches the proxies answer for (decomposition and attribution); R6 the breaches a volatility-responsive VaR answers for (modeling); R7 every breach date under one heading adding to the total, the count a sound model shows and its zone (synthesis); R8 the ten names to move onto their own history first, by what each adds to the VaR the desk's book misses (exploration and triage); R9 the VaR to add to the desk's planned second-half 2025 book until they are moved (forecasting).

Careful-column losses, each with its precedent (stumping Part 1b, references/precedents.json): R3 (L26, the outage-day breaches charged to inputs without a re-run; L01, the late-block mismatches set aside as timing), R8 (L16, names ranked on their own rather than by what they add to the desk's VaR net of hedges and offsets), R9 (N01, the add-on scaled to the planned book in proportion although its growth sits in proxied names), and the recommendation and the classification through them.

One-fact test at the draw: "the engine only sees trades booked before its 18:30 cutoff" rescues the late-booking half of R3 and nothing else, 1 of 9.

## Tried and rejected

- A fully generated credit relative-value book (the concept note's Concept 1 as written): set aside at the draw because its volatility regime would be a generator setting (a 1.45 multiplier for 50 days), and the client's Quantitative Finance strategies ask for the market records to be real.
- A desk on real NASDAQ single-stock closes (the skfolio research dataset, 1,455 names, 2018 to May 2023): prototyped on 2026-11-11 (official counts 6 to 23 by book, a proxy class of 5 to 9, a volatility class of 0 to 5 that moved with the decay chosen); set aside because the dataset carries no licence (Yahoo-derived, marked not for commercial use), and its 2022 bear market sat inside a two-year window that already held 2020 to 2021, so the volatility class came out thin.
- A credit desk priced off FRED Treasury and Moody's yields: set aside because every counterfactual engine would need a bond pricing convention (spread duration, convexity, carry), each one a fork on every result.
- Filed first as task19 on 2026-11-11; another session filed task19 (Kilvarra) minutes earlier, so this draw moved to task20 with the skeleton and Frontier rules of the same day applied (forcing event redrawn to the supervisor's review, the prompt opening on why).
