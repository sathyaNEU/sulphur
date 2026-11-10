"""task2 architecture 6: submission.md, the four answer blocks, drafted from figures.json so no figure is typed."""

QN = ["first", "second", "third", "fourth"]


def n(v):
    return format(int(v), ",")


def write(F, path):
    r, b, ev, k = F["results"], F["bands"], F["evidence"], F["constants"]
    fr = F["full_routes"]
    fp = ev["first_past"]
    comp = "R2 the 2027 starters at the smaller hospitals' compelled clinicians' rate"
    nosite = "R3 no hospital effect (the university hospitals at the smaller hospitals' level)"
    full = "R4 the go-lives at full volume from the date"
    own = "R4 every clinician starting on the date at their own first months' volume"
    pooled = "R2 the 2027 starters at the smaller hospitals' compulsory starters' rate, pooled"
    br = ev["bridge_routes_1dp"]
    q = ev["quarters_1dp"]
    md = ["## Tags", "",
          "**Domain:** Machine Learning Research, General Statistics & Data Science, robustness analysis (a recognizer's "
          "error rate carried to a deployment population the audit record never held).",
          "**Analytical objective:** Descriptive & Distribution Analysis.", ""]
    md += ["## Final Recommendation", "",
           "Commit to **Ceiling C, %d per cent**: under the frozen release 6.0 the expected share of audited dictations "
           "above 15 per cent word error rate is about %s per cent in the first quarter of 2027, %s and %s in the second "
           "and third and %s in the fourth, so a 10 per cent ceiling is passed from the %s quarter and a 12 per cent "
           "ceiling in the %s. Rejected: carrying 2026's %s per cent forward (Ceiling A), giving the university "
           "hospitals' 2027 starters the smaller hospitals' compelled clinicians' rate (%s per cent in the fourth "
           "quarter, above every ceiling offered), and reading the university hospitals at the smaller hospitals' "
           "acoustic level (%s per cent, Ceiling B)."
           % (r["r9_ceiling"], q[0], q[1], q[2], q[3], QN[fp["10"] - 1], QN[fp["12"] - 1], ev["record_2026_1dp"],
              ev["compelled"]["q4_1dp"], ev["nosite"]["q4_1dp"]), ""]
    md += ["## Supplementary Questions", "", "### quality_schedule_2027_ceiling.pdf", "",
           "1. The memo opens on the ceiling, %d per cent (Ceiling C), and the first 2027 quarter that would pass each "
           "lower ceiling: 10 per cent in the %s quarter, 12 per cent in the %s."
           % (r["r9_ceiling"], QN[fp["10"] - 1], QN[fp["12"] - 1]),
           "2. A chart of each 2027 quarter's expected share against the 10, 12, 14 and 16 per cent ceilings, the 2023 to "
           "2026 audited shares before it: the first quarter about %s per cent, the second about %s, the third about %s "
           "and the fourth about %s (%s to %s under every reasonable variant of the method)."
           % (q[0], q[1], q[2], q[3], ev["family_q4_range"][0], ev["family_q4_range"][1]), "",
           "### heavy_correction_2027.xlsx", "",
           "3. Each 2027 quarter's lowest ceiling its share stays under: %s per cent."
           % ", ".join(str(x) for x in r["r7_lowest_ceilings"]),
           "4. Each university hospital's expected fourth-quarter share: Shannonside University about %s per cent "
           "(%s to %s), Ballykeel University about %s per cent (%s to %s)."
           % (r["r6_univ_q4_share"]["SSU"], b["r6_univ_q4_share"]["SSU"][0], b["r6_univ_q4_share"]["SSU"][1],
              r["r6_univ_q4_share"]["BKU"], b["r6_univ_q4_share"]["BKU"][0], b["r6_univ_q4_share"]["BKU"][1]),
           "5. Ballykeel University Hospital's fourth-quarter dictations: about %s (%s to %s), about %s of them from "
           "the clinicians who start there in October."
           % (n(r["r5_bku_q4_dictations"]), n(b["r5_bku_q4_dictations"]["band"][0]), n(b["r5_bku_q4_dictations"]["band"][1]),
              n(ev["bku_q4_starters"])),
           "6. The word error rate nine in ten fourth-quarter dictations stay under: about %s per cent (%s to %s)."
           % (r["r8_p90_q4"], b["r8_p90_q4"]["band"][0], b["r8_p90_q4"]["band"][1]),
           "7. The group's audited share went from %s per cent in the second quarter of 2023 to %s per cent in the last "
           "quarter of 2026, a change of %s points: the releases took off about %s points (%s to %s, by which year's mix "
           "they are measured on) and the changing mix of dictations put back about %s (%s to %s)."
           % (r["r1_bridge_ends"]["start"], r["r1_bridge_ends"]["end"], ev["bridge_change_1dp"],
              ev["releases_abs_1dp"], ev["releases_band_abs_1dp"][0], ev["releases_band_abs_1dp"][1],
              r["r2_bridge_split"]["mix"],
              b["r2_bridge_split"]["mix"][0], b["r2_bridge_split"]["mix"][1]), ""]
    md += ["## Critical Components", "",
           "1. Measured within the clinicians who dictated at two of the group's hospitals under a new staff number, "
           "dictating at Shannonside University raises a "
           "clinician's word error rate by about **%s per cent** and at Ballykeel by about **%s per cent** against the six "
           "smaller hospitals' average; the low heavy-correction shares of the clinicians dictating there now (**%s** and "
           "**%s per cent**) are who chose to dictate, not the place."
           % (r["r3_hospital_effects"]["SSU"], r["r3_hospital_effects"]["BKU"],
              ev["dictators_pct"]["SSU"], ev["dictators_pct"]["BKU"]),
           "2. The 2027 starters are most of each university hospital's staff (**%s of %s** at Shannonside University, "
           "**%s of %s** at Ballykeel): their heavy-correction share is the whole staff's, at the smaller hospitals' "
           "levels for their grades and specialties with the hospital's own effect, less what the volunteers already "
           "carry, about **%s per cent** and **%s per cent**, not the **%s per cent** of the smaller hospitals' compelled "
           "clinicians, the few who held out where most had chosen."
           % (n(ev["starters"]["SSU"]), n(ev["staff"]["SSU"]), n(ev["starters"]["BKU"]), n(ev["staff"]["BKU"]),
              r["r4_starters_share"]["SSU"], r["r4_starters_share"]["BKU"], ev["kinds_pct"]["compelled"]),
           "3. At the six earlier go-lives the compelled clinicians dictated about **%d**, **%d** and **%d per cent** of a "
           "settled month in the first three months as departments switched over, so Ballykeel's October go-live adds "
           "about **%s** fourth-quarter dictations, not the **%s** of a full-volume start."
           % (ev["ramp_pct"][0], ev["ramp_pct"][1], ev["ramp_pct"][2], n(ev["bku_q4_starters"]),
              n(ev["bku_q4_starters_full_volume"])),
           "4. Releases 5.0, 5.2 and 6.0 cut a clinician's error by about **%s per cent** together, taking about **%s "
           "points** off the audited share between the second quarter of 2023 and the end of 2026, while the mix of "
           "dictations put about **%s** back."
           % (ev["release_step_4_to_6_pct"], ev["releases_abs_1dp"], r["r2_bridge_split"]["mix"]), ""]
    md += ["## Step-by-Step", "",
           "1. Cleaned dictation_audits_2023_2026.csv (the adjudicated score replaces the first pass under QA-07 4, "
           "unscorable audio out, the error rate recomputed from substitutions, deletions and insertions over the "
           "reference words, the three release strings read as one release): every quarter ties to "
           "quality_reports_2023_2026.xlsx, %s per cent in the second quarter of 2023 and %s per cent at the end of 2026."
           % (r["r1_bridge_ends"]["start"], r["r1_bridge_ends"]["end"]),
           "2. Linked every staff number to its clinician through previous_staff_no in clinician_register_2026.xlsx (%d "
           "moves between the group's hospitals) and fitted each audited dictation's log error as the clinician's own "
           "level, the release in force and the hospital dictated at: the 4.0 to 6.0 releases cut error by about %s per "
           "cent, so the releases took about %s points off the share and the mix of dictations put about %s back. "
           "Putting the whole change to the releases (%s points), using the release notes' LCB-2 cuts (%s) or a "
           "shift-share by hospital (%s) misattributes it."
           % (ev["moved_staff_numbers"], ev["release_step_4_to_6_pct"], ev["releases_abs_1dp"],
              r["r2_bridge_split"]["mix"], ev["bridge_change_1dp"],
              br["the release notes' benchmark cuts"]["releases"], br["a shift-share by hospital"]["releases"]),
           "3. Read each hospital's own effect from the clinicians seen at two hospitals: Shannonside University about "
           "%s per cent and Ballykeel about %s per cent worse than the six smaller hospitals' average. A raw comparison "
           "of the clinicians dictating at each hospital now reads the university hospitals as the best places to dictate, because "
           "only the few who chose to dictate appear there."
           % (r["r3_hospital_effects"]["SSU"], r["r3_hospital_effects"]["BKU"]),
           "4. Typed the smaller hospitals' clinicians by appointment and first dictation against Schedule 2's "
           "compulsory dates: those who chose carry %s per cent heavy correction under 6.0, those hired after a go-live "
           "%s, those compelled at it %s, and uptake before the go-lives ran from %d to %d per cent, so the compelled are "
           "the most selected where most had chosen."
           % (ev["kinds_pct"]["chose"], ev["kinds_pct"]["hired"], ev["kinds_pct"]["compelled"],
              min(ev["uptake_pct"].values()), max(ev["uptake_pct"].values())),
           "5. Built each university hospital's whole staff from the register (in post on 31 December 2026, as "
           "shannonside_dictation_rollout_2027.xlsx counts them) at the smaller hospitals' levels for each grade and "
           "specialty plus the hospital's own effect (%s and %s per cent heavy correction), less the clinicians already "
           "dictating: the starters carry about %s per cent at Shannonside University and %s at Ballykeel. The smaller "
           "hospitals' compelled clinicians' rate (%s) would put the fourth quarter at %s per cent, and their pooled "
           "compulsory starters land on the ceiling only by coincidence, missing the third quarter (%s per cent) and "
           "both university hospitals."
           % (ev["whole_staff_pct"]["SSU"], ev["whole_staff_pct"]["BKU"], r["r4_starters_share"]["SSU"],
              r["r4_starters_share"]["BKU"], ev["kinds_pct"]["compelled"], ev["compelled"]["q4_1dp"],
              fr[pooled]["quarters_1dp"][2]),
           "6. Measured the switch-over at the six go-lives in dictation_volumes_2022_2026.csv (the compelled "
           "clinicians' dictations per clinician in post by month from the compulsory date against their own months six "
           "to eleven, the calendar taken out): about %d, %d and %d per cent in the first three months, so Ballykeel's "
           "fourth quarter holds about %s dictations; starting everyone on the date at full volume gives %s, and at "
           "their own first months' volume %s."
           % (ev["ramp_pct"][0], ev["ramp_pct"][1], ev["ramp_pct"][2], n(r["r5_bku_q4_dictations"]),
              n(ev["bku_q4_full_volume"]), n(ev["bku_q4_own_first"])),
           "7. Projected each 2027 month hospital by hospital with recognition held at 6.0 (SN-2026-14) and the staff in "
           "post held as on 31 December 2026: the quarters come to about %s, %s, %s and %s per cent, Shannonside "
           "University's fourth quarter %s and Ballykeel's %s, and the lowest ceilings are %s."
           % (q[0], q[1], q[2], q[3], r["r6_univ_q4_share"]["SSU"], r["r6_univ_q4_share"]["BKU"],
              ", ".join(str(x) for x in r["r7_lowest_ceilings"])),
           "8. Mixed the groups' dictation-level error distributions to the fourth quarter's dictations: nine in ten stay "
           "under about %s per cent (reading it off clinicians' typical levels gives %s, because each clinician's "
           "dictations scatter about their level)." % (r["r8_p90_q4"], ev["p90_levels_1dp"]),
           "9. The ceiling: 10 per cent is passed from the %s quarter and 12 per cent in the %s, so Ceiling C, %d per cent."
           % (QN[fp["10"] - 1], QN[fp["12"] - 1], r["r9_ceiling"]), "",
           "No other conclusion survives. The 2026 record (%s per cent) and the record's highest quarter (%s) read the "
           "university hospitals as the few who dictate there now. Without each hospital's own effect, measured only "
           "through the clinicians who moved, the fourth quarter falls to %s and the ceiling to 12; with the smaller "
           "hospitals' compelled clinicians standing in for the starters it rises to %s, above every ceiling; and with "
           "the go-lives at full volume it reaches %s and 16. Only the staff less its volunteers, with the place's own "
           "effect and the switch-over, holds every quarter at or under 14."
           % (ev["record_2026_1dp"], ev["record_max_1dp"], ev["nosite"]["q4_1dp"], ev["compelled"]["q4_1dp"],
              ev["noramp"]["q4_1dp"]), ""]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))
    return "\n".join(md)
