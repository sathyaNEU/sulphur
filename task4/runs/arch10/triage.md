# task4 architecture 10: platform round triage (2026-11-11)

Source: the author's paste of both runs on the target.zip of commit 0c3b7fc (runs/arch10/run1.md, run2.md). Scores not
reported; the author's verdict: not stumped.

Verdict: REDESIGN. Both runs landed the call (order 17, the same 17 blocks in priority order, M145 the first refused,
23 qualifying) and every graded figure inside its band: the diesel figures (within 0.2 l/100 km of the golden), the
design-day energies, the verdicts, the loss (4.37 and 4.39 per cent against 4.3, band 2.7 to 5.0), the night's draw
(8.92 and 9.07 MWh against 9.1, band 0.3) and the conditioning (both modelled a cold overhead on the charger's mains
energy; run 2 files 22.63 kWh a bus on the design night, 2.4 kW over 9.4 hours against 3.5 kW and its band 2.8 to 4.2).

Loss map: none. Every result the design priced lost was earned, each by a move the runs make unprompted:
- R2 and R4, the pilot's selection on the diesel figures: both runs used each block's diesel figure as the predictor of
  its energy ("reconstructed diesel demand ... to predict non-HVAC battery energy"; "diesel-service intensity and
  scheduled kilometres"), validated by leave-one-block-out (8.09 and 8.52 kWh). The prompt asked for each block's diesel
  figure and its energy forecast side by side, so the bridge was the obvious join.
- R3, the heaters' share: both read the workshop's two heater-fault episodes as the record of all-electric heating
  (11.84 and 12.37 kW at -15 C against the golden's 12.4), a natural experiment in the record (the move R15 records).
- R7 and R8, the charging split: both fitted the charger's mains energy on the battery's gain with a cold term and the
  hours on charge ("fitted mains energy against battery replenishment and cold-weather overhead"), one regression on one
  join.
- R5, R6 and R9: reflexes (a front-loaded age form chosen on a holdout, the verdicts, the exact feasibility check).

What this round teaches (the run record and precedents.json): a quantity the prompt asks for beside the forecast becomes
the forecast's predictor; a logged outage of the component that differs is read as the natural experiment; a metered
total with a cold overhead is split by one regression. Each judgment the design priced was a single recognition
followed by a routine fit, so the architecture is spent, and with it the slot's scaffold (a count of vehicles for
duties under an energy limit and a night supply, architectures 5 to 10): the next architecture changes the world, the
deciding lessons and the decision form.

The runs' own waved-through assumptions, true in this world and recorded for the next draw: comparable tank stocks at
refills; the 2027 heating hardware comparable to the pilot's heater-out operation; the pilots' first-year loss carried
to the new model; controllable charging with no taper curve; five assigned blocks outside the observed diesel range.
