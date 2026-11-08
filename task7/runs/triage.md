# task7 round 1 triage (written in the /fix-rubric session from the author's paste; no run-triage agent ran)

Scores: run 1 98, run 2 58, average 78.0 (bar: under 60). Rubric: runs/rubric.csv (27 criteria, 100 points).

- Run 1, on the call (Kinloch Engineering and Matai Valley Foods, NZ$3,350,000). First wrong step: none on the
  analysis; lost ID 20 (2 points), the note does not state Matai's own expected write-off (NZ$817,000). Class: near
  miss or formatting. It priced the dependants with their own PDs as the baseline (converges with the golden, SF9).
- Run 2, off the call (Kinloch Engineering and Ridgeway Precast, NZ$3,000,000). First wrong step, step 8: "High-
  dependency recipients defaulted in 13 of 31 events ... Matai has eight borrowing counterparties ... This supports
  monitoring, but not automatic downstream defaults or a quantified intervention benefit under the supplied
  mandate." Class: dismissed own evidence (it also compared against the less dependent payees, 6 of 61, a
  contaminated control).
- Where the points went: both runs collected every security value (IDs 9 to 12), total commitment (13 to 15) and 2025
  sector share (16 to 19), the per-borrower values without dependants (7, 8) and every instruction item (21 to 27):
  49 points that no analysis decides. Run 2 also kept ID 3 (the count of Matai's dependants, 8).

Counterfactual average: 77.0 (run 1's note slip given back). Verdict: FIX_ASKS (one run off the call, the average
over 60 from asks the off-call run still collected). Route: /fix-rubric task7.
