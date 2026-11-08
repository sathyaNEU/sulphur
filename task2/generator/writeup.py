"""task2 architecture 5: submission.md, the four answer blocks, drafted from figures.json so no figure is typed."""

QN = ["first", "second", "third", "fourth"]


def n(v):
    return format(int(v), ",")


def write(F, path):
    c, q, ev, rec, lad = F["call"], F["quarters_2027"], F["evidence"], F["record"], F["ladder"]
    sh = ev["heavy_share_frozen_pct"]
    flat = lad["R0 the 2026 share carried forward"]
    hosp = lad["R1 each hospital's 2026 share at 2027's hospital mix"]
    drift = lad["R2 the release gap's drift added"]
    recent = lad["R2 starters at the 2025 and 2026 starters' level"]
    md = ["## Tags", "",
          "**Domain:** Machine Learning Research, General Statistics & Data Science, robustness analysis (a recognizer's "
          "error rate carried to a deployment population the record never held).",
          "**Analytical objective:** Descriptive & Distribution Analysis.", ""]
    md += ["## Final Recommendation", "",
           "Commit to **Ceiling C, %d per cent**: under the frozen release 6.0 the expected share of audited dictations "
           "above 15 per cent word error rate stays under 10 per cent in the first quarter of 2027, sits between 10 and 12 "
           "in the second and third and reaches about %s per cent in the fourth, so a 10 per cent ceiling is passed from "
           "the %s quarter and a 12 per cent ceiling in the %s. The steady record and its reweighting to 2027's hospitals "
           "(every quarter under 10 per cent) are rejected: the steadiness is each release cancelling a drift toward "
           "clinicians who began dictating once their hospital made it compulsory, and 2027 has no release and two "
           "teaching hospitals going compulsory."
           % (c["ceiling_pct"], q["share_whole"][3], QN[c["first_quarter_past_10"] - 1],
              QN[c["first_quarter_past_12"] - 1]), ""]
    md += ["## Supplementary Questions", "", "### quality_schedule_2027_ceiling.pdf", "",
           "1. The memo opens on the ceiling, %d per cent (Ceiling C), and the first 2027 quarter that would pass each lower "
           "ceiling: 10 per cent in the %s quarter, 12 per cent in the %s." % (c["ceiling_pct"],
                                                                           QN[c["first_quarter_past_10"] - 1],
                                                                           QN[c["first_quarter_past_12"] - 1]),
           "2. A chart of each 2027 quarter's expected share of audited dictations above 15 per cent word error rate "
           "against the 10, 12, 14 and 16 per cent ceilings: the first quarter under 10, the second and third between 10 "
           "and 12, the fourth between 12 and 14, with the 2023 to 2026 audited shares before them.",
           "", "### heavy_correction_2027.xlsx", "",
           "3. Each 2027 quarter's lowest ceiling its share stays under: %s, %s, %s and %s per cent."
           % tuple(q["lowest_ceiling"]),
           "4. The word error rate nine in ten fourth-quarter dictations stay under: %s per cent." % q["p90_q4_pct"], ""]
    md += ["## Critical Components", "",
           "1. The steady audited share (about %s to %s per cent since the middle of 2024) is two movements cancelling: each "
           "release lowered every clinician's error rate, while the dictation mix moved toward clinicians who began "
           "once their hospital was compulsory; with no release from February 2023 to June 2024 the share rose from about "
           "%s per cent in the first half of 2023 to about %s at the turn of the year." % (rec["late_floor"], rec["late_ceil"], rec["gap_from_1dp"], rec["gap_to_1dp"]),
           "2. Under release 6.0 about %s per cent of the dictations of clinicians whose first dictation came on or after "
           "their hospital's compulsory date need heavy correction, against about %s per cent for those who began before "
           "it, at every go-live on record alike." % (ev["heavy_share_frozen_whole"]["compulsory"],
                                                    ev["heavy_share_frozen_whole"]["voluntary"]),
           "3. 2027 brings no release (SN-2026-14) and compulsory dictation at Shannonside University (%s) and "
           "Ballykeel University (%s), whose %s clinicians in post include only %s dictating today, so the "
           "voluntary clinicians' share of dictation falls from about %s per cent in December 2026 to under two fifths in "
           "the fourth quarter." % (F["constants"]["compulsory"]["SSU"], F["constants"]["compulsory"]["BKU"],
                                    n(sum(ev["staff_in_post"].values())), n(sum(ev["dictating_dec_2026"].values())),
                                    ev["voluntary_share_2026_pct"]),
           "4. The expected share stays under 10 per cent in the first quarter, sits between 10 and 12 in the second and "
           "third and reaches about %s per cent in the fourth: 10 per cent is passed from the %s quarter and 12 per cent "
           "in the %s, so Ceiling C (%d per cent) is the lowest no quarter passes."
           % (q["share_whole"][3], QN[c["first_quarter_past_10"] - 1], QN[c["first_quarter_past_12"] - 1],
              c["ceiling_pct"]), ""]
    md += ["## Step-by-Step", "",
           "1. Cleaned dictation_audits_2023_2026.csv: the adjudicated score replaces the first pass (QA-07 4), unscorable "
           "audio is out, the word error rate is recomputed from substitutions, deletions and insertions over the "
           "reference words (the export changed from a fraction to a percentage in 2025), and the three release strings "
           "are read as one release; the quarterly shares tie to quality_reports_2023_2026.xlsx.",
           "2. The insufficient route: the share held between about %s and %s per cent since the middle of 2024; carried "
           "forward it is %s per cent each quarter, and reweighted to 2027's hospitals (each hospital's 2026 share at its "
           "2027 dictations) it falls to %s to %s per cent, because the teaching hospitals dictate at about 1 per cent "
           "today; both commit to %d per cent. Adding the 2024 release gap's climb gives %s to %s per cent and %d."
           % (rec["late_floor"], rec["late_ceil"], flat["shares_1dp"][0], min(hosp["shares_1dp"], key=float),
              max(hosp["shares_1dp"], key=float), hosp["ceiling"], drift["shares_1dp"][0], drift["shares_1dp"][3],
              drift["ceiling"]),
           "3. Measured each release's step within clinicians (each clinician's audits across releases): every release "
           "lowered error rates (4.0 by about %s per cent, 5.0 by %s, 5.2 by %s, 6.0 by %s), so the steady share means "
           "something else rose." % (ev["release_cuts_pct"]["4.0"], ev["release_cuts_pct"]["5.0"],
                                     ev["release_cuts_pct"]["5.2"], ev["release_cuts_pct"]["6.0"]),
           "4. Typed every clinician by the first month in dictation_volumes_2022_2026.csv (staff numbers reissued on a "
           "move linked through clinician_register_2026.xlsx) against the hospital's compulsory date in Schedule 2: "
           "carried to release 6.0, about %s per cent of the dictations of those who began on or after it need heavy "
           "correction, against about %s per cent for those who began before."
           % (ev["heavy_share_frozen_whole"]["compulsory"], ev["heavy_share_frozen_whole"]["voluntary"]),
           "5. Built each 2027 month's dictations by hospital and kind: clinicians dictating in December 2026 at their "
           "own volume, leaving at the record's rate (about %s per cent a year) and replaced by compulsory starters; at "
           "the two teaching hospitals every clinician in post not yet dictating (shannonside_dictation_rollout_2027.xlsx) "
           "starting on the compulsory date at the ramp the earlier go-lives show (about %s, %s and %s per cent of a full "
           "month in the first three months)."
           % (ev["turnover_pct_year"], ev["ramp_pct"][0], ev["ramp_pct"][1], ev["ramp_pct"][2]),
           "6. Weighted each kind's word error rates under 6.0 to each quarter's mix: the share under 10 per cent in the "
           "first quarter, between 10 and 12 in the second and third, about %s per cent in the fourth; nine in ten "
           "fourth-quarter dictations under %s per cent (each clinician's dictations scatter about their own level, so the "
           "percentile is of dictations, not of clinicians)." % (q["share_whole"][3], q["p90_q4_pct"]),
           "7. The ceiling: 10 per cent is passed from the %s quarter and 12 per cent in the %s; Ceiling C, %d per cent."
           % (QN[c["first_quarter_past_10"] - 1], QN[c["first_quarter_past_12"] - 1], c["ceiling_pct"]),
           "",
           "No other conclusion survives. The steady share and its hospital reweighting read the teaching hospitals' "
           "clinicians as the few who chose to dictate there; giving 2027's new dictators the recent starters' level "
           "(%s per cent in the fourth quarter) mixes those who chose with those who had to, and stops at %d; every "
           "projection that types clinicians by their start against the compulsory date, with the release held, "
           "lands on %d." % (recent["shares_1dp"][3], recent["ceiling"], c["ceiling_pct"])]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
