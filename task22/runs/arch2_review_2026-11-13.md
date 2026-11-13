# Platform review, architecture 2 (2026-11-13)

Task ID 18327116-b08b-4cd9-a922-49bee882e26a, version 13, reward 71.0. Stumped failed; determinism (main, supp)
passed; solution (main, supp) passed; task type match passed; stumped type match failed; duplicate not tested.
Prelim verdict: sent back for fixes. Final verdict: none yet. The platform's own runs scored 49 and 46 per cent on the
generated rubric (average 47.5); the runs are `arch2_run1.md` and `arch2_run2.md`. The reviewer's feedback, verbatim:

> What's good:
> This is a serious piece of Project Sulfur work. The question (which districts enter the 2027-2029 main replacement
> program under Rule 1 and which get the 2027 meter changeout under Rule 2) is a real lost and unaccounted-for gas
> problem, and the 22 shipped data files build it honestly: regulator station correctors with a Riverside
> communication gap, a Lakeview transducer failure and a stuck Westgate temperature transmitter; AMR cycle reads with
> repeated rows, estimated reads, rollovers and exchanges; a premise meter register with blank TempComp flags; the
> logger study and its memo; the Prairie soil network series; the commercial correctors' recorded gas temperatures;
> revenue protection case notes; and the 2024-2025 changeout work orders. Determinism holds: the committed lists
> reproduce from the shipped data files, and the alternative readings we tested (gas-in fills for the station gaps,
> billing shapes, changeout pace) do not move them.
>
> The committed answer is correct and well argued. The soil-based gas temperature model (soil at 20 inches plus 0.181
> of the air-soil difference, with a wall term below 45 F) fits the loggers far better than the memo's straight line
> on air and matches the outdoor commercial correctors through 2025-26, which is what keeps Airport (2.99 per cent)
> and College Hill (3.05 per cent) out of the Rule 2 set. The separation of bypasses and furnace taps from the
> absentees whose winter use kept a reduced heating response, checked against Lakeview's own station history (leak
> loss near 1.1 to 1.2 per cent in FY2024 and FY2025), is exactly the kind of reasoning a utility analyst should do.
>
> What's bad:
> The task is not difficult enough. It is not being returned for correctness or determinism. The test responses did
> most of this task correctly: both rebuilt gas in close to your 1,844,373 Mcf for the twelve months, both repaired
> the Lakeview pressure and Riverside gap, both used a soil-aware temperature model and reached your exact Rule 2 set
> (Elm Grove, Halvorsen, Lakeview, North End, Prairie Rose, Riverside, Sundquist), and one reached 662 of the 976
> scheduled changeouts against your 668. The layered work you built (temperature model, station repairs, calendarized
> billing, changeout pacing) did not separate them from the committed answer.
>
> Almost everything that separated them sits in one step: the unauthorized-use screen. Both test responses booked
> every FY2026 winter collapse as unauthorized use (about 76 to 78 accounts against your 15), which dropped Lakeview's
> leak loss to about 0.26 to 0.43 per cent and took Lakeview out of the Rule 1 program. They noticed the issue and set
> it aside; one wrote "Vacancy, fuel switching, meter faults, and changed occupants remain possible explanations", and
> the other said to "Prioritize 16 whole-load or heating-only signatures" yet still deducted all 72 premises. So the
> deliverable as a whole is largely reachable, and the hard part of the answer rests on a single classification call
> rather than on several independent judgments that each have to go right.
>
> What needs fixing:
> - Recheck the unauthorized-use list: premise 3135379 shows a furnace-tap pattern from February 2026 (winter use
>   down to base, heating response gone, summer whole) and is not in the committed 15. Either add it (16 accounts) or
>   state in the committed answer why it is excluded.
> - Make the collapse count in step 4 of your explanation agree with the data: it says 61 accounts collapsed, while
>   the screen on the shipped AMR reads finds the 15 thefts plus a cluster of about 55 absentee premises across 11
>   districts.
> - State the unit of the count (premises or accounts) in the prompt, since several premises changed account holders
>   during the year.
>
> How to fix it:
> Keep the data, the district set and the deciding logic; they are good. The goal is to make more of the answer
> depend on analysis the test responses could get wrong, so the outcome is not carried by the theft screen alone.
> - Ask for the gas temperature model's error against the commercial correctors' recorded AvgGasTempF in the 2025-26
>   winter as its own checkable figure (bias and RMSE by month), so the temperature judgment has to be shown, not only
>   applied.
> - Ask for Lakeview's and East Industrial's leak loss per cent of gas in for FY2024, FY2025 and FY2026 side by side,
>   with and without the unauthorized-use deduction. That makes the station-history cross-check an explicit result
>   and ties the theft classification to a figure the solver must defend.
> - Tighten the changeout pace ask: require the completion forecast by meter location (outside and inside) with a band
>   from the 2024-2025 work order delays, so the 668 figure rests on a modelled delay distribution rather than a
>   single pooled rate.
>
> Ways to make the task harder:
> 1. Make the Rule 2 margins tighter for more districts. Right now Airport and College Hill sit close to the 3.5 per
>    cent line only under the memo's air line; place one or two districts within about 0.2 points of the line under
>    the soil model so the wall term and the indoor/outdoor split in the premise meter register actually decide them.
> 2. Add a second competing explanation that must be separated with modelling, for example a district where a real
>    main leak began in FY2026 at the same time as an absentee cluster, so the solver must split station-level loss
>    growth from premise-level collapses using the leak's spatial or seasonal profile.
> 3. Let the billing shape matter in more than Halvorsen: give a second district a strong non-weather pattern (for
>    example a seasonal business closure) so that an HDD-based shape and the station-sendout shape give different leak
>    shares on either side of the 1.0 per cent line.
> 4. Make the changeout forecast censored: ship work orders where some 2025 inside-meter jobs are still open at the
>    extract date, so the completion curve has to be estimated with the open jobs handled properly rather than read
>    off closed ones.
> 5. Ask for an uncertainty band on each district's leak loss share that reflects the gas-in fill and the temperature
>    model error, and make the Rule 1 call depend on whether the district is clearly above the 1.0 per cent line.
>
> These are general suggestions for strengthening the task, not a guaranteed stump. Please test your own model
> rollouts and only resubmit if at least two strong models still miss the answer.

The platform's automated checks on the same page: input files clean; domain fit good; LLM prompt test NATURAL (1 of
9 signals: the enumerated balance columns read as a recipe); stumped (both runs excluded Lakeview from Rule 1); the
holistic audit reproduced the golden from the raw files; reward checker 47.5 per cent.

## Checked against the generator (2026-11-13)

- Premise 3135379 (Old Town, account 5101632) is a furnace tap in the simulation from 2025-12-20. The golden screen
  called it an absence: heating kept 0.13 and summer 0.84 (a tap's pattern), but base kept 0.28 against the 0.5 cut,
  an intercept from a four-month winter fit where days and degree days are nearly collinear. The note's pre-ship check
  had recorded "15 accounts found, 16 in the simulation". Adding it moves Old Town from 1.61 to 1.57 per cent.
- The step-by-step's 61 is the careful route's count (reads spread evenly and the air line); on the golden's own path
  the screen finds 69 collapses, 15 thefts and 54 absences, as the reviewer says.
- The golden sheet lists premises under an "Accounts" title: East Industrial premise 3148874 changed holders on
  2026-05-25 and 2026-05-28 during its bypass, so the 15 premises are 16 accounts (17 with 3135379).
- Run on both runs' route (soil-aware gas temperature, degree-day shapes, every collapse booked), the generator files
  Downtown, Old Town, Riverside and Sundquist with the golden Rule 2 set, the runs' answer; fixing only the
  diversion judgment on that route files both golden sets. One judgment was sufficient: a one-trick build by the
  stump factorial (Part 3.3), a rule filed after this cut.
