# Holistic audit of task25 architecture 1, 2026-11-13 (pasted by the author, verbatim)

Step 0 passed: the golden is present, and the inputs (Saukko/Kaivola, the 11 configs, CAR-2027-1) match the task.

Part A, what reproduces. All 11 benchmark days reproduce from tpbench_results and the configs (38.54, 6.35, 7.76, 17.09, 69.83, 34.89, 51.78, 49.27, 27.93, 8.55, 6.01). The 2026 GPU-days held reproduce exactly: 1,332,946.4, of which hall A 234,166 and hall B 1,098,781. The run independently reached the same seven late runs.

Part A, the defect. The author's expected durations cannot all happen in hall B. Hall B has 1,024 nodes (node_states shows 1,024 in every row; Service Schedule S-3 says the same). From 22 Feb the reserved blocks already fill it: 512 + 256 + 64 + 192 = 1,024. The author puts kide-34b-v3 at 43.77 days, so it runs to about 16 Mar 18:30. CAR-2027-1 s.2 says that block "is extended until the run finishes, and nothing else is booked on those nodes". kide-13b-v4 (128 nodes) launches 15 Mar. My timeline from the author's own figures gives 1,152 nodes demanded from 15 Mar to 16.8 Mar, against 1,024 installed. The author's answer ignores this. It launches kide-13b-v4 on 15 Mar and finishes it 2027-04-17 at 33.6 days. The rules also conflict here: a run "launches when its window opens", yet extended nodes cannot be rebooked. The files give no precedence rule. So kide-13b-v4's expected days, range and finish date, all graded items, are neither feasible nor forced. The run caught this and deferred kide-13b-v4 by 3.0 days (38.3 days, finish 2027-04-22). A deferral also changes hall B's power-load composition in March, so the power-cap figure in the hall B bridge moves too.

Part B. Hall B's power-cap stretch rests on several unstated modelling choices. The author's choices: read the meter as censored at the contract, fit the stretch on the excess, and replay 2027 with a pool busy share of 0.368. The run's method gives 17.7 days on kide-120b-v1 against the author's 13.47, and 90.9 expected days against 86.2. That is outside the author's 3% tolerance, and nothing in the files pins one method. I could not settle that fork. The capacity conflict alone is enough to make determinism not_pinned on graded figures.

Part C. The task as built has real depth: rank-imbalance modelling, best-fit packing replay, a censored power meter, interruption pricing and a works overrun. This is roughly level 4. But the run reached the committed decision: the same seven late runs and the same fitting set, plus a justified rebooking. So it shows no valid failure on the decision. The losses it would take are on the per-run magnitudes, where the author's values are themselves not forced.

Fail conditions met: determinism is not_pinned, a graded figure is infeasible under the stated rules, and the run reached the correct decision.

The author's instruction: fix it while keeping the task stumped, and it must meet the client's expectation (depth scale 4 or 5).
