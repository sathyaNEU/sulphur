# Run triage, task10 (architecture 5), 2026-11-08
**Verdict:** FIX_ASKS
**Scores:** run 1 about 92, run 2 about 31, average about 61; counterfactual about 99, 34, average about 67

Scores are estimates because no rubric was pasted: no `runs/rubric.md`, no per-criterion grades. Each figure and claim
in the four answer blocks is treated as a likely criterion and weighted by the house split (Final Recommendation plus
Critical Components 38, the asks 55, instruction-following 7). The author's estimate is about 68. Mine is about 61
(range 58 to 66, depending on how the grader weights upstream figures). The two agree on the shape: one run on the
call, one off, average at or a little above 60. The author's figure is consistent with mine if the generated rubric
grades the upstream figures too. Those are the before-flexibility demand (30, 25, 36, 23 MW) and the contracted MW
(9.5, 8.0, 14.0, 7.5), which both runs reproduce (see "Run 2 still collects").

Assumed weights: Final Recommendation 18; Critical Components 1 to 4, 5 each (20); SQ1 layout 5; SQ2 to SQ5, 11 each
(delivery, credit, after, over-firm, 2.75 each); SQ6 chart 3; SQ7 slides 3; instruction-following 7 (the prompt's
rounding 4, the two named files 3).

## Run 1
- Committed: "Commit reinforcement of Ashcombe Road and Hartwell Common for winter 2027/28." LANDED.
- First wrong step: none on the main call. The run nets the neighbours' rise in step 7: "Event-time reductions at
  Ashcombe, Fenwick and Hartwell coincide with increases at connected Tollbrook, Wexley and Kestwick respectively. I
  used paired demand totals to remove these offsetting changes, leaving Charlecote unpaired". This is the golden's
  steps 5 and 6, done as the design note's "pair taken together". It then reads the delivery at the design condition:
  "0.3952 MW/MW ... for Corvane and 0.4967 MW/MW ... for Quillon" (golden 0.4 and 0.5). The before-flexibility
  demand of 30.05, 25.06, 35.96 and 22.91 MW rounds to the golden's 30, 25, 36 and 23. Credits of 3.75, 3.97, 6.95
  and 2.96 round to 4, 4, 7 and 3. After-flexibility demand of 26.30, 21.08, 29.01 and 19.94 rounds to 26, 21, 29
  and 20. All of these match golden steps 3, 6 and 7.
- Class: `none_landed`, because the run took the golden's path (net the linked rise, read at minus 3.0 C) and every
  graded row figure rounds into the golden's bin. One-fact test: not applicable.
- Points lost by cause: deep step 0, surface 0, formatting about 8, wrong criterion 0.
  - CC1 (about 2.5 of 5): the run names the three neighbours and Charlecote's lack of one, but never states the rises
    (1.4, 1.4, 0.8 MW). It did the netting, so this is a reporting omission, not a reasoning one. Filed as
    formatting/reporting.
  - CC2 (about 1.5 of 5): 0.4 and 0.5 are right. The contrast with the 0.9 the event records show is not stated. Its
    nearest statement is "Crediting all own-primary event relief would put Hartwell 0.43 MW below firm". Also filed as
    reporting.
  - Instruction-following rounding (about 4 of 7): the response reports demand and credit to two decimals and delivery
    to four ("0.3952 MW/MW", "26.30 MW"), not whole MW and one decimal. The workbook was not pasted, so this may be
    only the chat text.

## Run 2
- Committed: "Commit reinforcement of Ashcombe Road only for winter 2027/28." OFF_CALL (Hartwell Common omitted;
  this is the design note's rung 1b answer).
- First wrong step: step 7, "Estimated design-day flexibility". The run estimates delivery as the zone primary's own
  fall: "Delivery is estimated at the primary ... The models estimate net primary relief associated with scheduling".
  Its figures at minus 3.0 C on the binding 18:00 slot are 0.6285 (Ashcombe Road), 0.4761 (Charlecote Way), 0.7396
  (Fenwick Street) and 0.7114 (Hartwell Common). Golden step 6 gives 0.4, 0.5, 0.5 and 0.4 net of the linked rise.
  The run departs from golden step 5 (read the open-point neighbours) and step 6 (net their rise event by event).
  Its own work had already found the signal: "Using every non-flex primary as a control: Tollbrook, Kestwick and Wexley
  show event-associated increases of 1.271, 0.997 and 1.680 MW at the design temperature. They were excluded as
  controls. These associations do not prove physical transfers." It drops them as controls, which avoids rung 2, but
  then credits the whole primary fall. Steps upstream of this are right: before-flexibility demand of 30.105, 25.025,
  36.014 and 22.915 MW matches golden step 3, and it reads the design condition, so it is past rung 3.
- Class: `dismissed_own_evidence`, because the run measured the mirror rise at exactly the three open-point neighbours
  and then explained it away ("do not prove physical transfers"). The data rule out its reading, and the run's own
  numbers show it. The same provider delivers 0.74 per MW at Fenwick Street but 0.48 at Charlecote Way, the one zone
  with no rising neighbour. Corvane delivers 0.71 at Hartwell Common against Quillon's 0.48 at Charlecote. The gap
  tracks the neighbour's rise, not the provider. Guideline section 6 credits "the reduction in the primary's demand
  that its provider will deliver", and the award notice measures delivery "on the provider's metered assets". So
  "net primary relief" is not a defensible alternative reading.
  - One-fact test, adversarial: "the rises at Tollbrook Lane, Wexley Hill and Kestwick Fields are load moved across
    the open points during the events" would rescue the call for this run. The run had already done every other step,
    including the design-day read. That sentence is the deciding inference itself, the separation of two explanations
    for one pattern. It is not a fact about a field, a planted row or a written procedure. So the class stays deep, but
    the run was one inference from landing, and a reviewer could note it.
- Points lost by cause: deep step and downstream about 62, surface 0, formatting about 4 (rounding: "24.134 MW",
  "0.6469 MW/MW"), wrong criterion 0.
  - Final Recommendation, 18.
  - CC1, 5: different quantity (1.271, 0.997, 1.680 at design temperature, not 1.4, 1.4, 0.8 in the half-hours), and
    not netted.
  - CC2, 5: 0.6 and 0.7, not 0.4 and 0.5.
  - CC3, 5: credits 6, 4, 10, 5 and after 24 and 18 for Ashcombe and Hartwell.
  - CC4, about 2.5: Fenwick Street 26, not 29.
  - Ashcombe Road row, 8.25: 0.6, 6 MW, 24 MW.
  - Fenwick Street row, 8.25: 0.7, 10 MW, 26 MW.
  - Hartwell Common row, 11: 0.7, 5 MW, 18 MW, "No".
  - SQ7 slides, 3: names Ashcombe Road only.
- Run 2 still collects (the criteria to re-site), about 31 points:
  - SQ3, the whole Charlecote Way row (0.4761 to 0.5, 3.809 to 4 MW, 21.216 to 21 MW, No): 11. Charlecote has no
    rising neighbour, so the deep step changes nothing there.
  - SQ2, Ashcombe Road "over firm: Yes": 2.75. It is over firm on both paths (24 and 26 against 23.0).
  - SQ4, Fenwick Street "over firm: No": 2.75. It is under firm on both paths (26 and 29 against 30.5).
  - CC4, the Charlecote half (21 against 22.5): about 2.5. Same reason as SQ3.
  - SQ1 layout (one row per zone, the right columns): 5. This is a format criterion.
  - SQ6 chart: 3. Format.
  - Instruction-following, the two named files: 3.
  - If the rubric grades them, both runs also collect the before-flexibility demand (30, 25, 36, 23 MW) and the
    contracted MW (9.5, 8.0, 14.0, 7.5). These come before the deep step. Such criteria would explain the gap between
    my 61 and the author's 68.

## Rubric criteria to edit
No rubric was pasted, so none can be named. Two answer-block items ride nothing analytical, and the re-siting should
remove them or replace them with something that does:
- the Charlecote Way row (SQ3) and the Charlecote half of CC4: the deep step does not touch that zone;
- the over-firm flags at Ashcombe Road and Fenwick Street (SQ2, SQ4): the default path gives the same flag.

No critical component lacks a likely criterion, and none contradicts the golden.

## Route
`/fix-rubric task10`. Run 1 landed (about 92) and run 2 was off the call (about 31, `dismissed_own_evidence`, a deep
class). The estimated average of 61, and the author's 68, are at or above 60. About 31 of run 2's points come from
criteria the deep step does not move (the Charlecote row, two over-firm flags, the before-demand if graded, format).
Re-site those asks onto quantities that move with the netting: per-zone net delivery, credit and after-flexibility
demand at the three linked zones, the neighbour rise per zone, and the margin to firm. Then re-run the evaluation.

Caveats for the author:
- With run 1 near 92, run 2 must fall to about 15 for the average to clear 55. That means nearly everything it
  collects has to stop paying.
- CLAUDE.md's law holds that hardening the asks after a landed call has never rescued a build. That law concerns both
  runs landing; here one did not. Still, if the regenerated pair again has one landed run in the 90s, the next route is
  REDESIGN at the deep step, not another rubric pass.
- Paste the generated rubric and grades with the next pair so these estimates can be replaced.
