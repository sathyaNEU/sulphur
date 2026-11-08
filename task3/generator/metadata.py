"""task3 architecture 4: metadata.json (file roles, provenance, distractors)."""
import json
import os

LIC = "CC0 1.0 (synthetic, authored for this task)"
FILES = [
    ("corlinden_raw_water_nitrate_results_1988-2026.csv", "evidence",
     "synthetic: Corlinden Water Utility's nitrate results by sample point, raw water and entry point", "2026-11-04"),
    ("corlinden_well_pumping_daily_2009-2026.csv", "evidence", "synthetic: the utility's SCADA daily pumping by well",
     "2026-11-02"),
    ("ravell_county_groundwater_network_samples_1990-2026.csv", "evidence",
     "synthetic: Ravell County's groundwater network samples (water-table wells, spring and fall)", "2026-10-21"),
    ("ravell_county_groundwater_network_sites.xlsx", "evidence",
     "synthetic: the network's site register, land cover codes and field notes", "2026-10-21"),
    ("ravell_county_parcel_land_cover_1986-2026.csv", "evidence",
     "synthetic: the county's parcel land cover by year", "2026-10-21"),
    ("sallow_road_wellhead_protection_plan_2019.pdf", "evidence",
     "synthetic: Fenwright Hydrogeologic's 2019 wellhead protection plan for the well field", "2019-11-14"),
    ("sallow_road_WHPA_parcel_attributes_2019.xlsx", "evidence",
     "synthetic: the plan's Appendix B, parcel attributes and recharge by land cover", "2019-11-14"),
    ("sallow_road_WHPA_zones_figure3_2019.png", "evidence", "synthetic: the plan's Figure 3, zones of contribution",
     "2019-11-14"),
    ("ravell_county_groundwater_age_survey_2019.xlsx", "evidence",
     "synthetic: the county's 2019 tritium-helium survey", "2020-02-03"),
    ("corlinden_water_supply_plan_2025.pdf", "evidence", "synthetic: the utility's 2025 water supply plan", "2025-09-10"),
    ("sallow_road_well_construction_records.pdf", "distractor",
     "synthetic: the production wells' construction records", "2021-03-08"),
    ("corlinden_well_specific_capacity_2008-2026.xlsx", "distractor",
     "synthetic: the production wells' specific capacity tests", "2026-05-04"),
    ("ravell_county_fertilizer_sales_1990-2025.csv", "distractor",
     "synthetic: county nitrogen fertiliser sales by product", "2026-03-30"),
]
DISTRACTOR_REASONS = {
    "sallow_road_well_construction_records.pdf": "the screens and logs describe the wells, which all draw the full "
    "saturated thickness of one sand aquifer; the forecast turns on the land over the zones, not the wells' build",
    "corlinden_well_specific_capacity_2008-2026.xlsx": "specific capacity bears on pumping capacity and well "
    "rehabilitation, which the plan's fixed shares already settle",
    "ravell_county_fertilizer_sales_1990-2025.csv": "county-wide sales carry no parcel, land cover or timing; the "
    "leachate the wells receive is measured directly by the network",
}


def write(task_dir):
    md = {"task": "task3", "architecture": 4, "setting": "2026-11-06",
          "files": [dict(name=n, role=r, source=s, date=d, license=LIC) for n, r, s, d in FILES],
          "distractor_files": [n for n, r, _, _ in FILES if r == "distractor"],
          "distractor_reasons": DISTRACTOR_REASONS,
          "stated_inputs": ["2027", "2031", "2030", "2034", "10", "4.427", "8", "30", "32", "20", "27", "28", "25",
                            "9.0", "10.0", "10.5", "14.0", "11.0", "1.62", "15 December 2026"],
          "deliverables": ["corlinden_nitrate_plant_timing_memo.pdf", "corlinden_entry_point_nitrate_forecast.xlsx",
                           "corlinden_entry_point_nitrate_2027-2040.png"]}
    json.dump(md, open(os.path.join(task_dir, "metadata.json"), "w"), indent=1)
