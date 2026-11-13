# task20 determinism check, pass 2 (run t20v3b)

Verdict: DETERMINISTIC (provisional on one point, see Limits). Disposition: APPROVE.

## Evidence (recomputed from a fresh unzip)
| Item | Blocks | Recomputed |
|---|---|---|
| 2022 records: cumulative outflow (NEX statements with the restated 8 Mar row and the superseded one dropped, day-ahead by settlement date, customer cash incl. the PAY split payments), from 3 Jan 2022 | 548.5 on 26 Aug 2022 | 548.46 on 26 Aug 2022 (Fri, flat over the weekend, first business day) |
| Book 30 Dec 2026 (cancels dropped, amends kept, MWh converted) | 2027 1.848 TWh, 2028 0.685 TWh | trade capture 211 MW and 78 MW = NEX position statement, 1.848 / 0.685 TWh |
| Hedge ratio 31 Dec 2026 with Fjordal (100 MW, 38.00, to 2029) / exchange only | 68.6 / 39.6 / 22.2; 46.5 / 17.4 / 0.0 | 68.6 for 2027 and the others by arithmetic from the register and the October 2026 budget generation; exchange only 46.5 |
| Month ends 2020-2026 where exchange-only ratio is more than 5 points under the policy minimum | 64 of 84 | 64 of 84; with Fjordal counted: 0 of 84 under min-5 (the files close this fork by the desk's own behaviour) |
| NEX rate rule (front contract, per-contract 2-day log moves, 250-day 99th percentile, times price) | 212 of 222 notices | 199 of 220 match to the cent with my quick replay (87/102, 69/74, 43/44), same rule family, so it is recoverable; I did not tune the rest |
| Payment lags | 39/30/51/21 days | means 38.5/30.3/51.2/21.2 days (Fjordal/Nesbyen/Straum/Bygdenett) |
| Year-end 2026 storage | 875 GWh vs floor 700 GWh | 875.0 (week 53), licence floor 700 filed |
| Peak date 27 Aug 2027, facility rule | Friday; 328.8 rounds to 350 | Friday; whole band 320-345 maps to 350, the hurried 297.1 to 300, so the band cannot flip the call |

Forks run: (1) hedge ratio on exchange positions only versus with Fjordal: closed by the policy wording ("sold forward at a fixed price"), the supply register, and the 64/0 test above; (2) cancelled / amended / MWh trades: closed by file (cancel and re-entry R id). (3) quantile and look-back variants of the NEX rule: with one-day differently-defined moves or a cross-roll front series I got 23/102 matches against 87/102 for per-contract moves, so the per-contract reading is forced by the notices (not a free choice). The blocks claim all other variants land 320 to 345; I did not re-run these.

## Limits
I did not replay the whole stress year end to end (stress curve, cascade, desk pace, plant release, customers), so 328.8, 59.7, 1,743, 82.3, 173.7 and the four book volumes are consistent with the filed facts I checked but not independently reproduced. The desk's 1.25 / 3.0-point rule was only crudely tested (my weekly bucketing was too coarse to confirm it); the 2028-2030 volumes and the 2.2/1.1/1.0 TWh depend on it.

## Notes (no fix needed)
- Gate B: all decisive facts are filed (policy table in the docx, standard annex, licence floor, register, margin notices). Distinctive recommendation terms (committed margin facility, stress requirement, hedge ratio) appear in the standard and policy.
- Gate E: asks have units; "after it" in the hedge-book ask could include or exclude the peak day's delivery (about 5 GWh at 211 MW), inside the 0.03 TWh band.
- Dec 2026 and 31 Dec cash items falling in early January 2027 (December invoices, delivery settlement of 30-31 Dec) could be read in or out; their size is inside the stated bands for the graded cash figures.

## Fix
None. If the author wants the end-to-end figure confirmed, that needs the generator's own replay (outside this judge's inputs).
