"""task23 architecture 1: Fernhallow Regional Landfill (Kelloway County Solid Waste Division), the parameters every
module reads. The world is simulated month by month for the waste and the gas, hour by hour for the weather, the
emissions and the instruments."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 23017
TZ = ZoneInfo("America/Los_Angeles")
UTC = dt.timezone.utc

# ---- the calendar ----
Y0 = 1986                                  # first month simulated: January 1986
YEND = 2028                                # months simulated to December 2027
WX0 = dt.datetime(2016, 1, 1, 0, 0)        # first hour of the station's record (local standard time)
DATA_END = dt.datetime(2026, 10, 31, 23, 0)  # last hour of every extract
FCST_END = dt.datetime(2027, 12, 31, 23, 0)
AS_OF = dt.date(2026, 11, 5)
PULLED = {"tickets": "2026-11-03", "scada": "2026-11-03", "wells": "2026-11-04", "weather": "2026-11-02",
          "chambers": "2026-11-02", "recirc": "2026-11-04", "workorders": "2026-11-04", "dailylog": "2026-11-03"}

# ---- the site ----
ORG = "Kelloway County Solid Waste Division"
COUNTY = "Kelloway County"
SITE = "Fernhallow Regional Landfill"
COUNCIL = "Kelloway County Council"
STATE_AGENCY = "Department of Environmental Stewardship"
CONTRACTOR = "Tessaline Environmental"
CONSULTANT = "Brightwater Geoscience"
ENGINEER = "Nathan Wheeler"
SURVEY_LEAD = "Diane Martinez"
TECHS = ["R. Okafor", "J. Lindqvist", "M. Tran"]

# cell: open month, close month (last month of placement), constructed area m2, cover in 2025-2027
CELLS = {
    1: dict(open=(1986, 4), close=(1995, 6), area=9.4e4, cover="final", capped=(1997, 9)),
    2: dict(open=(1995, 7), close=(2004, 9), area=10.6e4, cover="final", capped=(2006, 8)),
    3: dict(open=(2004, 10), close=(2013, 3), area=11.2e4, cover="final", capped=(2015, 7)),
    4: dict(open=(2013, 4), close=(2025, 1), area=15.6e4, cover="intermediate", capped=None),
    5: dict(open=(2025, 2), close=(2028, 6), area=9.8e4, cover="active", capped=None),
}
RECIRC = {4: dt.date(2023, 4, 17), 5: dt.date(2026, 7, 13)}

# ---- the waste ----
# methane potential, m3 CH4 per tonne as placed (the true world); the reporting rule's defaults sit beside them
L0_TRUE = {"MSW": 84.0, "CD": 12.3, "BIO": 49.9, "SOIL": 0.0, "SPEC": 0.0}
L0_RULE = {"MSW": 100.0, "CD": 15.0, "BIO": 60.0, "SOIL": 0.0, "SPEC": 0.0}
SHARE = {"MSW": 0.862, "CD": 0.071, "BIO": 0.024, "SOIL": 0.034, "SPEC": 0.009}
KD = 0.048          # first-order decay, per year, as placed
KW = 0.120          # decay of the waste recirculated leachate reaches
REACH = {4: 0.45, 5: 1.00}
RAMP_MONTHS = 3     # the reached waste's decay moves to KW over this many months
# a transfer contract: from April 2026 Silverbrook Transfer's trailers bring municipal waste on top of the site's own
# receipts, raising cell 5's municipal waste by this factor (the tickets carry the hauler, the fill plan the receipts)
CONTRACT = dict(start=dt.date(2026, 4, 1), factor=1.6, hauler="Silverbrook Transfer")
LAG_MONTHS = 6      # methanogenesis begins six months after placement
RHO_CH4 = 0.0006680  # t per m3 of methane at 20 C and 1 atm (the reporting rule's density)
KG_PER_SCF = 0.019200  # kg of methane per standard cubic foot (60 F, 14.696 psia)

# ---- collection ----
CE_FINAL = 0.90
CE_CLOSED_DESIGN = 0.92   # the 2015 closure plan's design collection for the capped cells (they collect CE_FINAL)
CE4_BASE = 0.700
CE5_HC = 0.15
CE5_WELLS = 0.78
CE4_CAP = 0.86
FLOOD_LOSS_MAX = 0.85   # a flooded well's yield loss when its screen is fully submerged
WELLFIELD_SD = 0.0      # the wellfield's month-to-month state beyond the blowers' outages (held steady)
PILOT_WELLS = 8
PILOT_DATE = dt.date(2025, 6, 9)
DESTRUCTION = 0.985     # methane destroyed at the flare and engines (the reporting rule books 0.99)

# ---- oxidation in cover soil (capacity at 15 C, g CH4 per m2 per day, and its temperature factor) ----
VOX15 = {"final": 22.0, "intermediate": 15.0, "active": 26.0}
Q10 = 1.9

# ---- gas held and released with the barometer ----
BARO_TAU_H = 16.0
BARO_C = {"final": 0.090, "intermediate": 0.100, "active": 0.100}   # per hPa of the lagged pressure gap

# ---- the 2027 packages (cumulative) ----
PACKAGES = {
    "A": dict(works=[], cost=0.0),
    "B": dict(works=["hc5"], cost=0.64),
    "C": dict(works=["hc5", "pumps4"], cost=1.21),
    "D": dict(works=["hc5", "pumps4", "wells5"], cost=2.38),
    "E": dict(works=["hc5", "pumps4", "wells5", "cap4"], cost=5.95),
}
WORKS = {"hc5": dt.date(2027, 5, 1), "pumps4": dt.date(2027, 5, 1), "wells5": dt.date(2027, 5, 1),
         "cap4": dt.date(2027, 10, 1)}
LIMIT_T = 5500.0   # the Council's limit, metric tons of methane leaving the site in calendar 2027
REPORTED_2025 = None   # set by docs.py from the report it writes

# ---- files under target/ ----
FILES = {
    "tickets": "scale_tickets_2021-01_2026-10.csv",
    "history": "tonnage_by_cell_1986-2020.xlsx",
    "dailylog": "operations_daily_log_2024-2026.csv",
    "scada": "lfg_plant_hourly_2023-2026.csv",
    "wells": "wellfield_monitoring_2019-2026.csv",
    "register": "gccs_well_register.xlsx",
    "workorders": "cmms_work_orders_2022-2026.csv",
    "recirc": "leachate_recirculation_log.csv",
    "weather": "fernhallow_met_station_hourly.csv",
    "chambers": "auto_chamber_flux_hourly.csv",
    "survey": "tessaline_whole_site_methane_2025_2026.pdf",
    "campaigns": "tessaline_campaign_results.csv",
    "drone": "drone_mass_balance_flights.xlsx",
    "oxstudy": "brightwater_cover_oxidation_2019.pdf",
    "oxplots": "brightwater_plot_measurements_2019.csv",
    "ghg2025": "ghg_annual_report_RY2025.pdf",
    "plan": "council_agenda_lfg_capital_2027.pdf",
    "fillplan": "fill_plan_2027.xlsx",
    "groundwater": "groundwater_monitoring_2019-2026.csv",
    "leachate": "leachate_quality_monthly.csv",
    "sem": "surface_emission_monitoring_quarterly.csv",
    "odor": "odor_complaints_2024-2026.csv",
}
DISTRACTORS = ["groundwater", "leachate", "sem", "odor"]

# ---- the state reporting rule's collection-based method (the division's annual report) ----
RULE = {"ce": {"final": 0.95, "intermediate": 0.75, "daily": 0.60, "none": 0.0}, "ox": 0.10, "de": 0.99,
        "k_default": 0.057, "lag_months": 6}
# 2025 areas by cover and collection status as the 2025 report files them (m2): cells 1-3 final cover with wells,
# cell 4 intermediate cover with wells, cell 5's filled area without collection
RULE_AREAS_2025 = {"final": 31.2e4, "intermediate": 15.6e4, "none": 5.9e4}
# 2021 to 2024, as those years' reports file them: cells 1-3 final cover with wells, cell 4's completed lifts under
# intermediate cover with wells, its working face under daily cover with wells
RULE_AREAS_HIST = {"final": 31.2e4, "intermediate": 11.8e4, "daily": 3.8e4}
