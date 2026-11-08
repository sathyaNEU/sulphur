"""task8 architecture 18: submission.md (the platform's four answer blocks) and metadata.json, drafted from
figures.json so that every number in the blocks is a number the generator emitted."""
import json

import pack as PK
import params as P


def submission(f, path):
    reg = f["regions"]
    reg_txt = ", ".join("%s %d" % (k, v) for k, v in reg.items())
    below = f["items_below_band"]
    above = ", ".join(f["items_above_band"]) if f["items_above_band"] else "none"
    pr = {k: v for k, v in f["chances"].items() if int(k[1:]) > 28}
    pr_in = [v for k, v in pr.items() if k not in below]
    pr_out = [v for k, v in pr.items() if k in below]
    lines = [
        "## Tags", "",
        "**Domain:** Education & Learning Sciences (item response theory and test equating: an adult numeracy awarding "
        "body pre-equating its 2027 Level 1 paper from its Rasch item bank).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
        "## 1. Final Recommendation", "",
        "**Set the 2027 Level 1 Numeracy pass mark at %d of 40: a candidate who just meets the standard can be expected "
        "to score %.2f on the paper once its twelve Level 2 patterns and relationships items carry the reading cost "
        "Level 1 candidates pay on long stems; the bank's own values give %.2f and a pass mark of %d, which this "
        "rejects.**" % (f["pass_mark"], f["expected_golden"], f["expected_bank"], f["pass_mark_bank"]), "",
        "## 2. Supplementary Questions", "",
        "1. pass_mark_2027.docx: a memo to the Awards Committee recommending a pass mark of %d of 40, stating the "
        "expected mark of %.2f at the standard (26 of 40 on the 2022 paper) against the bank's %.2f, and why the "
        "twelve patterns and relationships items are harder for Level 1 candidates than their bank values." %
        (f["pass_mark"], f["expected_golden"], f["expected_bank"]),
        "2. l1_2027_items.xlsx, item table: one row for each of the 40 items on the 2027 paper with its chance at the "
        "standard (two decimals) and whether it sits inside the 0.20 to 0.90 band. %s of the twelve patterns and "
        "relationships items (%s) sit below the band, at %.2f to %.2f; the other %s sit inside it at %.2f to %.2f; "
        "no item sits above the band." % (NUM[len(below)].capitalize(), ", ".join(below), min(pr_out), max(pr_out),
                                           NUM[len(pr_in)], min(pr_in), max(pr_in)),
        "3. l1_2027_items.xlsx, regions: the mean mark the candidates who sat the 2026 Level 1 paper in each region "
        "could be expected to score on the 2027 paper (whole marks): %s." % reg_txt, "",
        "## 3. Critical Components", "",
        "- The bank's final 2026 values put the 2027 paper's expected mark at the standard at %.2f (pass mark %d); "
        "they carry the twelve patterns and relationships items at difficulties set by Level 2 candidates." %
        (f["expected_bank"], f["pass_mark_bank"]),
        "- On the %d Level 2 items the 2023 to 2026 Level 1 papers carried, each item's Level 1 difficulty less its "
        "Level 2 difficulty needs two causes together: an everyday-context advantage of about %.1f logits and a "
        "reading cost of about %.1f logits per 100 words of stem. On the long everyday items the two cancel (their "
        "shift sits %.2f logits from the short mathematical items', the short everyday items' %.2f)." %
        (f["n_bridging"], f["everyday_advantage"], f["reading_cost_per_100_words"], f["lp_mean_shift_rel"],
         f["sp_mean_shift_rel"]),
        "- The twelve patterns and relationships items are long and mathematical, so only the reading cost applies: "
        "at the standard they are worth %.2f marks against %.2f on the bank's values, and %s of them fall below the "
        "band." % (f["pr_expected_golden"], f["pr_expected_bank"], NUM[len(below)]),
        "- Expected mark at the standard on the 2027 paper: %.2f, so the pass mark is %d." % (f["expected_golden"],
                                                                                              f["pass_mark"]), "",
        "## 4. Step-by-Step Solution", "",
        "1. Conform the response export: map the 2022 and 2023 sittings' positions (Q01 to Q40) to bank codes through "
        "the paper layouts, keep the later answer of every item answered twice after a reconnect, and attach each "
        "sitting to its paper; count each register sitting once.",
        "2. The bank's final 2026 run gives %.2f at the standard on the 2027 paper; screening the shared items the "
        "usual way (link through them, set aside the outliers) flags the short everyday items and leaves the rest "
        "looking unchanged, which still files %d. That reading is rejected." % (f["expected_bank"],
                                                                               round(f["rival_screen"])),
        "3. Calibrate the Level 1 sittings and the Level 2 sittings each on their own (Rasch) and take, for each of the "
        "%d Level 2 items set on Level 1 papers, its Level 1 difficulty less its Level 2 difficulty." % f["n_bridging"],
        "4. The short everyday items are easier for Level 1 candidates and the long everyday items are not, so a second "
        "cause offsets the everyday advantage on the long ones: fit the shift on an intercept (the link), the stem's "
        "length and the context together. Context alone (%.2f at the standard) or length alone (%.2f) leaves one kind "
        "of item misfitting." % (f["rival_context"], f["rival_reading"]),
        "5. Give each 2027 patterns and relationships item its Level 2 difficulty plus the link and the reading cost "
        "for its stem; the Level 1 items keep their Level 1 values.",
        "6. Find the ability at which the 2022 paper's expected mark is 26 and sum the 2027 paper's chances there: "
        "%.2f, so the pass mark is %d; the item chances and the band follow from the same ability." %
        (f["expected_golden"], f["pass_mark"]),
        "7. Regions: join each 2026 Level 1 sitting to the register's sitting centre (one row per candidate) and the "
        "centres list. The 2026 paper is heavy in everyday items and the 2027 paper light, and the regions differ in "
        "how much easier everyday items are for their candidates, so estimate each region's own everyday deviation "
        "on the Level 1 sittings, each candidate's ability on the 2026 paper with it, and average the expected 2027 "
        "marks by region; one ability scale for every region files other whole marks in some regions.",
        "No other reading survives: every route that leaves the 2027 items on their Level 2 values, credits only the "
        "everyday advantage or prices only stem length files %d or more, and every form of the two-cause model "
        "(linear, logarithmic or a long-against-short step in stem length, weighted or not) files %d." %
        (min(round(f["rival_context"]), round(f["rival_reading"]), round(f["rival_screen"])), f["pass_mark"]),
    ]
    open(path, "w").write("\n".join(lines) + "\n")


NUM = {0: "none", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve"}


def metadata(path, n_rows):
    files = []
    desc = {
        "responses": ("evidence", "synthetic: the response platform's export of every scored item response at the "
                      "Board's Level 1 and Level 2 online sittings, 2022 to 2026", "2026-11-06"),
        "register": ("evidence", "synthetic: the Board's candidate register, centre uploads and regional office "
                     "entries, 2022 to 2026", "2026-11-06"),
        "bank": ("evidence", "synthetic: the Board's item bank file with the preliminary and final 2026 calibration "
                 "runs", "2026-11-04"),
        "layouts": ("evidence", "synthetic: the Board's paper layouts, 2022 to 2027", "2026-11-04"),
        "centres": ("evidence", "synthetic: the Board's registered learning centres", "2026-11-02"),
        "spec": ("governing", "synthetic: the Level 1 Numeracy specification, version 2026.1", "2026-03-12"),
        "standard": ("governing", "synthetic: the 2022 standard-setting record for Level 1 Numeracy", "2022-05-20"),
        "minute": ("context", "synthetic: the Awards Committee's minute of 17 September 2026", "2026-09-21"),
        "email": ("context", "synthetic: the committee chair's email to the assessment manager", "2026-11-09"),
        "survey": ("distractor", "synthetic: the Board's 2026 learner confidence survey", "2026-07-02"),
        "audit": ("distractor", "synthetic: the operations group's 2026 audit of centres' computer suites", "2026-08-28"),
    }
    for k, name in PK.FILES.items():
        role, src, date = desc[k]
        files.append(dict(name=name, role=role, source=src, date=date, license="CC0 1.0 (synthetic, authored for this task)"))
    meta = dict(task="task8", architecture=18, setting="2026-11-09",
                organisation=P.ORG + " (fictional), Manitoba and Saskatchewan, Canada",
                decision="the pass mark of the 2027 Level 1 Numeracy paper",
                deliverables=["pass_mark_2027.docx", "l1_2027_items.xlsx"],
                distractor_files=[PK.FILES[k] for k in PK.DISTRACTORS],
                rows={k: v for k, v in n_rows.items()},
                files=sorted(files, key=lambda x: x["name"]))
    open(path, "w").write(json.dumps(meta, indent=1) + "\n")
