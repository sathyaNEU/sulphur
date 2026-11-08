"""task2 architecture 4: metadata.json (file roles, provenance, distractors)."""
import json
import os

LIC = "CC0 1.0 (synthetic, authored for this task)"
FILES = [
    ("MC_drillhole_collars.csv", "evidence", "synthetic: the Mount Carrow drillhole database's collar table", "2026-10-28"),
    ("MC_drillhole_assays.csv", "evidence", "synthetic: the database's assay table, 1 m samples and core intervals, two laboratories", "2026-10-28"),
    ("MC_qaqc_results_2019-2024.csv", "evidence", "synthetic: certified reference materials, blanks and field duplicates", "2026-10-28"),
    ("MC_bulk_density.csv", "evidence", "synthetic: dry bulk densities from diamond core", "2026-10-28"),
    ("MC_weathering_logs.csv", "evidence", "synthetic: the logged weathering intervals", "2026-10-28"),
    ("MC_stage5_design_flitches.csv", "evidence", "synthetic: the Stage 5 cutback design by flitch on the mine grid", "2026-10-20"),
    ("Yarrabin_OPA_2027-2028_term_sheet.pdf", "evidence", "synthetic: the ore purchase agreement's term sheet, revision 3", "2026-10-22"),
    ("MC_2027_mine_plan_summary.pdf", "evidence", "synthetic: the 2027 mine plan summary for the board", "2026-11-03"),
    ("MC_stage5_drilling_plan.png", "evidence", "synthetic: the geology office's plan of the Stage 5 drilling", "2026-10-28"),
    ("MC_metallurgical_testwork_2025.xlsx", "distractor", "synthetic: the toll mill's bottle-roll testwork", "2025-09-01"),
    ("MC_stage4_survey_pickup_2026-09.csv", "distractor", "synthetic: the surveyors' Stage 4 pickup", "2026-09-30"),
]
REASONS = {"MC_metallurgical_testwork_2025.xlsx": "recovery bears on payable gold at the mill; the agreement's tiers "
           "are contained gold in the blocks",
           "MC_stage4_survey_pickup_2026-09.csv": "the Stage 4 surface is west of the Stage 5 outlines and mined; no "
           "Stage 5 flitch reads it"}


def write(task_dir):
    md = {"task": "task2", "architecture": 4, "setting": "2026-11-06",
          "files": [dict(name=n, role=r, source=s, date=d, license=LIC) for n, r, s, d in FILES],
          "distractor_files": [n for n, r, _, _ in FILES if r == "distractor"], "distractor_reasons": REASONS,
          "stated_inputs": ["75,000", "125,000", "200,000", "2.5", "1.2", "2.1", "2.2", "2027", "2028", "5", "145",
                            "339,250.0", "6,601,480.0", "400", "305", "25", "12.5"],
          "deliverables": ["stage5_high_grade_resource.xlsx", "stage5_OPA_tier_board.pptx"]}
    json.dump(md, open(os.path.join(task_dir, "metadata.json"), "w"), indent=1)
