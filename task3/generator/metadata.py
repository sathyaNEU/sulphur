"""task3 architecture 3: metadata.json (file roles, provenance, distractors)."""
import json
import os

LIC = "CC0 1.0 (synthetic, authored for this task)"
FILES = [
    ("PW-1_constant_rate_2026-09_transducers.csv", "evidence",
     "synthetic: Tillbrook Hydrogeologic's logger export for the 72-hour test of PW-1, six wells, one-minute absolute "
     "pressure from two logger brands", "2026-09-21"),
    ("barologger_BL-2231_2026-09.csv", "evidence", "synthetic: the on-site barologger, five-minute values in UTC",
     "2026-09-21"),
    ("PW-1_constant_rate_2026-09_field_readings.xlsx", "evidence",
     "synthetic: the test's field notes (loggers, tape readings, discharge, events)", "2026-09-21"),
    ("harlow_springs_MOR_well_production_2009-2026.csv", "evidence",
     "synthetic: Harlow Springs Utilities' monthly operating report extract, production by well", "2026-10-07"),
    ("mill_street_MW_water_levels_2008-2026.csv", "evidence",
     "synthetic: the Mill Street monitoring well's tape readings from the operating reports", "2026-10-07"),
    ("cvwcd_network_water_levels_2005-2026.csv", "evidence",
     "synthetic: the conservancy district's network water-level export", "2026-10-02"),
    ("cvwcd_well_register.xlsx", "evidence", "synthetic: the district's well register with measuring-point history",
     "2026-10-02"),
    ("CVWCD_Rule_WR-4_groundwater_withdrawal_permits.pdf", "evidence",
     "synthetic: the district's withdrawal permit rule as amended June 2023", "2023-06-20"),
    ("reidel_road_WR-4_application_requested_schedules.pdf", "evidence",
     "synthetic: the utility's application summary, requested schedules and the Mill Street projection", "2026-10-30"),
    ("drillers_logs_corrin_valley_wells.pdf", "evidence", "synthetic: drillers' logs compiled from the district's well records",
     "2026-10-02"),
    ("CVWCD_bedrock_surface_plate3_harlow_reach.png", "evidence",
     "synthetic: Plate 3 of the district's 2019 bedrock surface study, the Harlow reach, wells added 2026", "2026-10-02"),
    ("PW-1_step_drawdown_2026-08-27.csv", "distractor", "synthetic: the August step-drawdown test of PW-1", "2026-08-28"),
    ("PW-1_raw_water_quality_2026-09.xlsx", "distractor", "synthetic: the raw-water quality results from the test",
     "2026-10-05"),
]
DISTRACTOR_REASONS = {
    "PW-1_step_drawdown_2026-08-27.csv": "the step test sizes PW-1's well losses, which change the drawdown inside the "
    "pumping well and nowhere in the aquifer; the sentinel's drawdown never reads it",
    "PW-1_raw_water_quality_2026-09.xlsx": "the raw-water chemistry bears on treatment, not on the drawdown limit",
}


def write(task_dir):
    md = {"task": "task3", "architecture": 3, "setting": "2026-11-06",
          "files": [dict(name=n, role=r, source=s, date=d, license=LIC) for n, r, s, d in FILES],
          "distractor_files": [n for n, r, _, _ in FILES if r == "distractor"],
          "distractor_reasons": DISTRACTOR_REASONS,
          "stated_inputs": ["450", "700", "1,000", "1,250", "9.0", "2.1", "2.2", "4.1", "4.2", "4.3", "4.4", "1.2",
                            "2027", "2046", "0.56", "0.44", "548"],
          "deliverables": ["reidel_road_sentinel_forecast.xlsx", "reidel_road_WR-4_demonstration.pdf"]}
    json.dump(md, open(os.path.join(task_dir, "metadata.json"), "w"), indent=1)
