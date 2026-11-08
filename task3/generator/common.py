"""Constants for task3 architecture 5: Tamsett County's Kinnard Road culvert on Ollery Creek, the creek's gauge and
rain records 1956 to 2025, the watershed's suburban build-out, the county's drainage standard and the three culverts."""
import datetime as dt

SEED = 96
ORG = "Tamsett County"
ROADS = "Tamsett County Roads Division"
YEAR0, YEAR1 = 1956, 2025                  # calendar years of the daily records; peaks by water year 1956 to 2025
AREA_SQMI = 11.5                           # drainage area at the Kinnard Road gauge
AREA_ACRES = AREA_SQMI * 640
DESIGN_AEP = 0.01                          # the standard's annual exceedance probability
SERVICE = (2027, 2036)                     # the culvert's first ten years of service
# the three culverts the division costed, the flow each passes before the road overtops (cfs), cost (USD)
CULVERTS = [("A", "twin 10 ft x 7 ft box", 7460, 1_640_000),
            ("B", "triple 10 ft x 9 ft box", 13380, 2_480_000),
            ("C", "quadruple 12 ft x 9 ft box", 18720, 3_390_000)]
PEOPLE = {"engineer": "Lisa Horne", "director": "James Reynolds"}

# watershed: paved (impervious) fraction rising through the suburban build-out, pervious curve number, time to peak
IMP0, IMP1, IMP_MID, IMP_WID = 0.06, 0.30, 1990, 6.0
CN_PERV = 88.0
DCIA_SHARE = 0.30                          # share of the paved area connected straight to the drains
RUNOFF_K, RUNOFF_EXP = 0.252, 1.45           # storm runoff depth (in) against storm rain (in)
VOL_RISE = 0.6                              # runoff volume's rise per unit of paved fraction
TP_RURAL_H = 6.0
LAG_DROP = 0.45                            # share of the rural time to peak the storm drains take off at full build-out
# storm climate: depth scale before and after the 1990s shift (the Piedmont's wet 1960s to 80s, drier since)
WET_PRE, WET_POST, SHIFT_YEAR = 1.06, 0.88, 1991
TROP_PRE, TROP_POST = 0.045, 0.024           # chance a late-summer storm start is tropical, before and after
CULVERT_RATINGS = (7460, 13380, 18720)

FILES = {
    "flow": "ollery_creek_daily_discharge_1956-2025.csv",
    "peaks": "ollery_creek_annual_peak_flows.csv",
    "pot": "ollery_creek_peaks_above_base_1956-2025.csv",
    "rain": "tamsett_rain_gauge_daily_1956-2025.csv",
    "parcels": "tamsett_stormwater_impervious_parcels.xlsx",
    "standard": "tamsett_drainage_standard_section_4.docx",
    "options": "kinnard_road_culvert_alternatives.docx",
    "inspection": "kinnard_road_culvert_inspection_2024.docx",
    "survey": "ollery_creek_kinnard_reach_cross_sections_2023.csv",
    "quality": "ollery_creek_grab_samples_2019-2025.csv",
}
DOCX_OUT = "kinnard_road_culvert_design_flow.docx"
CSV_OUT = "ollery_creek_design_peak_table.csv"
