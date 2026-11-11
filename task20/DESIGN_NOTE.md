# task20: whether Brindle & Moss's fourth-quarter fiscal 2025 revenue clears the street's figure, from the Kestrel card panel three weeks before the release

Architecture 2, drawn 2026-11-11 as a re-root of architecture 1 (spent: see the last lines of `## Tried and rejected`),
from the author's concept note (Concept 3, "Card panel to reported revenue"). Stage 1: the card is filed; the design
sections are written at stage 2.

## Draw

Subdomain: Quantitative Finance (Quantitative Finance and Trading), task type Alpha research (finding and validating
  return-predictive signals), carded under `strategy-backtesting-evaluation`, the Quantitative Finance key that serves
  Forecasting
Analysis type: Forecasting & Predictive Modeling
Answer shape: a forecast with its band and drivers: the quarter's revenue, an 80 per cent range earned on past
  quarters, each adjustment's worth, and whether the whole range clears the street's figure
Weight: validation: the range and the growth index have to be earned on rolling origins that include the kind of
  panel change the target quarter carries; the last three live builds sat on etl conformance (task8), root-cause
  investigation (task9) and pricing (task21)
People: Audrey Hanson (consumer analyst, Larkhill Partners' research desk), Robert Campbell (portfolio manager, chairs
  the investment committee) (`guard.py names --geo us --seed 2611`). Neither appears in the prompt.

## Tried and rejected

- A fully generated credit relative-value book (the concept note's Concept 1 as written): set aside at the draw because its volatility regime would be a generator setting (a 1.45 multiplier for 50 days), and the client's Quantitative Finance strategies ask for the market records to be real.
- A desk on real NASDAQ single-stock closes (the skfolio research dataset, 1,455 names, 2018 to May 2023): prototyped on 2026-11-11 (official counts 6 to 23 by book, a proxy class of 5 to 9, a volatility class of 0 to 5 that moved with the decay chosen); set aside because the dataset carries no licence (Yahoo-derived, marked not for commercial use), and its 2022 bear market sat inside a two-year window that already held 2020 to 2021, so the volatility class came out thin.
- A credit desk priced off FRED Treasury and Moody's yields: set aside because every counterfactual engine would need a bond pricing convention (spread duration, convexity, carry), each one a fork on every result.
- Filed first as task19 on 2026-11-11; another session filed task19 (Kilvarra) minutes earlier, so this draw moved to task20 with the skeleton and Frontier rules of the same day applied (forcing event redrawn to the supervisor's review, the prompt opening on why).
- 2026-11-11, prototype: closing blocks booked late on 22 random days caused no breach in four worlds (a block meets a large move too rarely); rebuilt as the middle office's daily allocation step, which swells after big moves, and the fees as a share of flow.
- 2026-11-11, prototype: the engine's hedge recomputed from the snapshot's cash book (inconsistent with futures booked before the run); the engine now reads the futures position its snapshot holds, and the world was re-searched (400 seeds, seed 970 the only one passing every band with margin on every volatility variant).
- 2026-11-11, the ten names to move first (ranked by the VaR each name's move adds to the desk's book): dropped; on the 30 June book 68 of 89 proxied names have negative single-name marginals, the marginal and greedy top tens share one name, and a fifth-largest-loss VaR's name-level marginals follow which scenario sits fifth, not the names.
- 2026-11-11, the engine's shortfall split into the book's move into proxied names and the names getting riskier: dropped; the two orders of the two-step decomposition give composition 97 and 29 per cent of the rise.
- 2026-11-11, the breaches a year the planned book would show on the engine as it stands: dropped; the planned book's 17.5 sits next to the year's own 16 by coincidence, so the history shortcut would land inside any honest band.
- 2026-11-11, the seed search on the exact-accounting world (1,200 seeds): 985 set aside for a hypothetical knife-edge on 1 November 2024, 30, 621 and 785 for a zone variant at or over the line, 262 and 1190 for a variant sound count of 5 to 6; 1114 kept.
- 2026-11-11, an end-of-day position file holding the book at the close: dropped at the pack design, because a literal 4(b) re-run of the engine on that file hands over the inputs heading with no investigation (R3, R4 and R6 earned by the careful pass).
- 2026-11-11, the engine's extracts as the only daily positions with the hypothetical P&L computed from them: dropped, because the missing allocations (a median USD 39 million gross a night) then scramble the hypothetical P&L itself and the cutoff decides most results (one thing); product control's hypothetical P&L ships instead, as MRS-4 3.2 says product control produces it.
- 2026-11-11, the plan's book scaled from the true 30 June close book: dropped, because the cutoff then decides the add-on path as well (0.34 in July, 0.42 in August and 0.14 in December against 0.32, 0.27 and nil); the plan's basis is the engine's 30 June run.
- 2026-11-11, FUTS snapshots carrying the CME trade date (a day ahead in the evening): dropped, because a run dating the futures by it moves seven headings, a mess item that would decide results; the snapshot carries its New York position date.
- 2026-11-11, a flat second-half target from July: replaced by the plan's own ramp, because with nothing in a flat plan changing month to month the store's graduations are the only story the month-by-month ask can find; the ramp is the story a hurried run stops at.
- 2026-11-11, allocation amendments that changed quantities after the extract: changed to moves between client accounts, because taking first versions then moved a heading (mess not neutral).
- 2026-11-11, architecture 1 as built (the extracts' cutoff as the careful pass's loss at R3, R4 and R6, the store's graduations as its loss at R8): the determinism judge's isolated thread, at medium effort and before it opened the answer blocks, replicated ERE to the dollar, reconciled product control's hypothetical P&L against the extracts and found the closing allocations booked after the cut, classified every exception as the golden does ((a) 1, (b) 4 on the golden's dates, (c) 11) and computed the month-by-month add-on from MRS-4 6 read literally (0.324, 0.273, 0.114, 0.076, 0.035, 0); priced on that pass the careful column lands near 95, so the chain returns to stage 2. In this world the cutoff cannot be both hidden and not one thing: the allocations (a median USD 39 million gross a night) show in any reconciliation of a P&L that carries them, and kept out of every P&L they decide most results; and the add-on's month-by-month mapping is a filed rule once MRS-4 6 pins it. The judge's determinism findings carried to the redesign: the 4(d) EWMA timing (the then-current volatility through the scenario date gives a sound count of 3 at every decay, 28 March 2025 under (e)); the runs on which the reported VaR sat above ERE's on the book held (133 of 250, not 129 of 249); the add-on's base book pinned to the positions ERE read on 30 June; the plan approved after the 30 June run it cites; the crosswalk dated from the 17 January replay.
- 2026-11-11, re-root: architecture 1 (the SMCF desk's VaR exception classification on the S&P 500 and Nasdaq-100 tape) is spent on the judge's first pass above; architecture 2 moves to another world, dataset and shell, the author's Concept 3 (a card panel's nowcast of a retailer's quarterly revenue before the release), whose answer is an estimate no record holds.

