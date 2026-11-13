"""task22 architecture 2: Brandvold Public Utilities' gas system, the parameters every module reads."""
import datetime as dt

SEED = 22062

SIM0 = dt.date(2023, 8, 1)            # first simulated gas day
SIM1 = dt.date(2026, 11, 4)           # last simulated gas day (the extracts ran November 2 to 5, 2026)
W0, W1 = dt.date(2025, 10, 1), dt.date(2026, 9, 30)      # the program rules' twelve months
MON0, MON1 = dt.date(2023, 10, 1), dt.date(2026, 9, 30)  # the monthly balance the prompt asks for
FY = {"FY2024": (dt.date(2023, 10, 1), dt.date(2024, 9, 30)),
      "FY2025": (dt.date(2024, 10, 1), dt.date(2025, 9, 30)),
      "FY2026": (W0, W1)}

T_BASE_F = 60.0
R_BASE = T_BASE_F + 459.67
P_BASE = 14.73
P_ATM = 13.98            # Brandvold, 1,390 ft
DELIVERY_PSIG = 0.253    # 7 inches water column
PF = round((P_ATM + DELIVERY_PSIG) / P_BASE, 4)   # the billing pressure factor, 0.9663

LEAK_LINE = 1.0          # per cent of the gas delivered into the district
CHANGEOUT_LINE = 3.5      # per cent of the volume billed for the non-compensating meters
CHANGEOUT_MIN_METERS = 100

# district: code, name, residential premises, small commercial premises, non-compensating share, outdoor share of
# the non-compensating meters, student rentals, snowbirds every winter, snowbirds first away in 2025-26, leak loss
# target (per cent of gas in, FY2026), read cycles, bypasses (full, furnace tap), commercial bypasses, cast iron
# share of main (frost), regulator stations
DISTRICTS = [
    dict(code="OT", name="Old Town", res=900, com=92, ntc=0.80, out=0.34, stu=0.05, sbo=0.02, sbn=0.003, leak=1.60,
         cycles=[3, 4, 5, 6], byp=(1, 1), cbyp=0, ci=0.55, drs=["OT-1", "OT-2"]),
    dict(code="RS", name="Riverside", res=980, com=40, ntc=0.76, out=1.00, stu=0.0, sbo=0.02, sbn=0.005, leak=1.31,
         cycles=[13, 14, 15, 16], byp=(0, 1), cbyp=0, ci=0.25, drs=["RS-1"]),
    dict(code="CH", name="College Hill", res=820, com=46, ntc=0.62, out=0.58, stu=0.38, sbo=0.0, sbn=0.0, leak=0.76,
         cycles=[12, 13, 14], byp=(0, 0), cbyp=0, ci=0.10, drs=["CH-1"]),
    dict(code="NE", name="North End", res=960, com=30, ntc=0.81, out=1.00, stu=0.0, sbo=0.02, sbn=0.005, leak=0.61,
         cycles=[14, 15, 16, 17], byp=(0, 0), cbyp=0, ci=0.05, drs=["NE-1"]),
    dict(code="WG", name="Westgate", res=880, com=36, ntc=0.05, out=1.00, stu=0.0, sbo=0.02, sbn=0.004, leak=0.42,
         cycles=[18, 19, 20], byp=(0, 0), cbyp=0, ci=0.0, drs=["WG-1"]),
    dict(code="LV", name="Lakeview", res=700, com=15, ntc=0.74, out=1.00, stu=0.0, sbo=0.10, sbn=0.03, leak=1.21,
         cycles=[8, 9, 10], byp=(0, 0), cbyp=0, ci=0.0, drs=["LV-1"]),
    dict(code="PR", name="Prairie Rose", res=940, com=25, ntc=0.30, out=1.00, stu=0.0, sbo=0.02, sbn=0.005, leak=0.28,
         cycles=[17, 18, 19], byp=(0, 0), cbyp=0, ci=0.0, drs=["PR-1"]),
    dict(code="HP", name="Heritage Park", res=760, com=20, ntc=0.05, out=1.00, stu=0.0, sbo=0.01, sbn=0.003, leak=0.18,
         cycles=[19, 20], byp=(0, 0), cbyp=0, ci=0.0, drs=["HP-1"]),
    dict(code="EI", name="East Industrial", res=140, com=124, ntc=0.55, out=0.58, stu=0.0, sbo=0.0, sbn=0.0,
         leak=0.60, cycles=[6, 7, 8], byp=(0, 0), cbyp=2, ci=0.15, drs=["EI-1"]),
    dict(code="DT", name="Downtown", res=520, com=162, ntc=0.72, out=0.20, stu=0.06, sbo=0.0, sbn=0.0, leak=1.42,
         cycles=[1, 2, 3], byp=(0, 0), cbyp=1, ci=0.60, drs=["DT-1", "DT-2"]),
    dict(code="AP", name="Airport", res=260, com=72, ntc=0.62, out=0.70, stu=0.0, sbo=0.0, sbn=0.003, leak=0.66,
         cycles=[10, 11, 12], byp=(0, 0), cbyp=0, ci=0.0, drs=["AP-1"]),
    dict(code="EG", name="Elm Grove", res=780, com=25, ntc=0.84, out=1.00, stu=0.0, sbo=0.03, sbn=0.006, leak=0.68,
         cycles=[15, 16, 17], byp=(3, 3), cbyp=0, ci=0.10, drs=["EG-1"]),
    dict(code="HV", name="Halvorsen", res=430, com=25, ntc=0.88, out=1.00, stu=0.0, sbo=0.01, sbn=0.005, leak=0.80,
         cycles=[8, 9, 10], byp=(0, 0), cbyp=0, ci=0.0, drs=["HV-1"]),
    dict(code="SQ", name="Sundquist", res=470, com=30, ntc=0.85, out=1.00, stu=0.0, sbo=0.02, sbn=0.006, leak=1.36,
         cycles=[9, 10, 11], byp=(2, 2), cbyp=0, ci=0.35, drs=["SQ-1"]),
]
DCODES = [d["code"] for d in DISTRICTS]
DNAME = {d["code"]: d["name"] for d in DISTRICTS}

# regulator station outlet pressures (psig): the industrial loop east of the river and the airport park run higher
STATION_PSIG = {"EI-1": 58.0, "AP-1": 45.0}
# station correctors: the 2021 metering program fitted EVC-II units (pressure, temperature and supercompressibility);
# four stations kept the EVC-I units moved from customer sites, which correct for pressure and temperature only, as
# every customer corrector does
PT_ONLY_STATIONS = ["RS-1", "OT-2", "DT-2", "CH-1"]
GAS_SG = 0.592            # the interstate supply's specific gravity, about which the gate's analyser moves day to day

# large customers on electronic volume correctors (telemetered, billed on corrected volume)
EVC = {"OT": 3, "RS": 2, "CH": 7, "NE": 1, "WG": 2, "LV": 1, "PR": 2, "HP": 2, "EI": 16, "DT": 12, "AP": 7, "EG": 1,
       "HV": 1, "SQ": 1}

# process customers taking gas at line pressure on the industrial loop and in the airport park (district, name,
# base Mcf a day, heating slope Mcf per degree day, delivery psig)
EVC_LINE = [("EI", "creamery", 215.0, 0.9, 55.0),
            ("EI", "malt elevator and kiln", 175.0, 0.4, 54.0),
            ("EI", "foundry", 140.0, 0.6, 53.0),
            ("EI", "fiberboard plant", 110.0, 1.1, 53.0),
            ("EI", "rendering plant", 70.0, 0.5, 52.0),
            ("AP", "asphalt plant", 70.0, 0.3, 42.0),
            ("AP", "aircraft hangars", 30.0, 1.6, 40.0)]

# dual-fuel heat pumps added to gas-heated homes: the share of each district's occupied homes converted, most
# between April and October 2025; the furnace runs only below each system's switchover temperature
DUAL_FUEL = {"OT": 0.004, "RS": 0.005, "CH": 0.003, "NE": 0.004, "WG": 0.006, "LV": 0.004, "PR": 0.007,
             "HP": 0.006, "EI": 0.0, "DT": 0.003, "AP": 0.004, "EG": 0.005, "HV": 0.006, "SQ": 0.028}
DUAL_FUEL_REBATED = 0.25  # the share of conversions whose dual-fuel controls rebate is on file

# the 2024-25 gas temperature study: loggers at meter inlets, November 2024 to April 2025
STUDY0, STUDY1 = dt.date(2024, 11, 1), dt.date(2025, 4, 30)
STUDY_OUT = {"NE": 9, "RS": 9, "EG": 8, "HV": 8, "SQ": 9, "LV": 9}
STUDY_IN = {"OT": 5, "DT": 3}

# changeout programs: 2024 Westgate, 2025 Old Town east and an Elm Grove pilot (both complete before the window);
# the 2027 plan, set from the 2026 budget, schedules Old Town's and Downtown's remaining meters
PROGRAM_2024 = dict(district="WG", start=dt.date(2024, 4, 15), end=dt.date(2024, 9, 30))
PROGRAM_2025 = [dict(district="OT", start=dt.date(2025, 3, 31), end=dt.date(2025, 9, 26), n=380),
                dict(district="EG", start=dt.date(2025, 5, 5), end=dt.date(2025, 8, 29), n=150)]
PLAN_2027 = dict(districts=["OT", "DT"], start=dt.date(2027, 4, 5), end=dt.date(2027, 10, 29))
SEASON_2027 = dt.date(2027, 11, 1)

ORG = "Brandvold Public Utilities"
CITY = "City of Brandvold"
COMMISSION = "Brandvold Utilities Commission"
ENGINEER = "Marc Gilbert"
CONSULTANT = "Jocelyn Murray"
TZ = "America/Chicago"

FILES = {
    "reads": "amr_meter_reads_2023-08_2026-10.csv",
    "register": "premise_meter_register_2026-11-02.xlsx",
    "accounts": "customer_accounts_2023-08_2026-11.csv",
    "drs": "regulator_station_correctors_daily_2023-09_2026-10.csv",
    "gate": "city_gate_station_daily_2023-09_2026-10.csv",
    "evc": "commercial_correctors_daily_2023-09_2026-10.csv",
    "airport": "brandvold_regional_airport_daily_2023-08_2026-10.csv",
    "soil": "prairie_soil_network_brandvold_station_daily_2023-08_2026-10.csv",
    "loggers": "gas_temperature_study_loggers_2024-11_2025-04.csv",
    "study_memo": "gas_temperature_study_memo_2025-06.pdf",
    "lauf_study": "lauf_study_fy2019_consultant_report.pdf",
    "rules": "lauf_reduction_program_rules_2026.pdf",
    "damage": "third_party_damage_reports_2023-2026.xlsx",
    "own_use": "utility_own_use_2023-2026.xlsx",
    "workorders": "meter_changeout_work_orders_2024-2025.csv",
    "plan2027": "meter_changeout_plan_2027.xlsx",
    "rp_cases": "revenue_protection_cases_2021-2025.xlsx",
    "lauf_report": "annual_lauf_report_fy2019-fy2026.xlsx",
    "tariff": "gas_rate_schedules_2026.pdf",
    "rebates": "appliance_rebates_2024-2026.csv",
    "cng": "cng_station_sales_2024-2026.csv",
    "invoices": "interstate_supply_invoices_2023-2026.xlsx",
}
