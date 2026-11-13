"""Shared constants for the task13 generator (architecture 5): paths, the cooperative, its people, the pack's files and
each file's save times, the seeds and the clock helpers. The world runs on UTC. Each record is written on the clock
its system keeps: the EventRecall relays and the SCADA master in UTC, the GridVue relays and the control room in
Central prevailing time, the solar farm's plant controller in Central Standard Time all year, the outage system in
Central prevailing time."""
import datetime as dt
import os
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, 'target')
GOLDEN = os.path.join(TASK, 'golden')
ZONE = 'America/Chicago'
TZ = ZoneInfo(ZONE)
CST = dt.timezone(dt.timedelta(hours=-6))
UTC = dt.timezone.utc

SEED = 51301          # the network, its structures, sources, taps and members
WX_SEED = 51302       # weather, fog, rain and lightning
EV_SEED = 51303       # faults, relays, operations and the field records

ORG = 'Laguna Prieta Electric Cooperative'
ORG_SHORT = 'Laguna Prieta EC'
TOWN = 'Port Alcorn'
IPP = 'Coyote Draw Solar LLC'
IPP_SHORT = 'Coyote Draw Solar'

PEOPLE = {
    'reliability': 'Brittany Melton',      # reliability engineer (the golden's author)
    'engineering': 'Thomas Evans',         # manager of engineering (the memo's reader)
    'operations': 'Derek Hart',            # system operations supervisor (the control room log)
    'environment': 'Joanna Choi',          # environmental compliance specialist (the roost survey)
    'vegetation': 'Allison Ward',          # vegetation management coordinator
    'planning': 'Andrew Russell',          # transmission planning engineer (the protection studies)
    'lines': 'Julie Peterson',             # line superintendent (patrols, washing, maintenance)
}

FILES = {
    'er': 'relay_events_eventrecall_export_2022-2026.csv',
    'gv': 'relay_records_gridvue_2022-2026.json',
    'legacy': 'ponder_creek_relay_targets_2022-2026.xlsx',
    'soe': 'scada_soe_2022-2026.csv',
    'crlog': 'control_room_69kv_log_2022-2026.xlsx',
    'oms': 'oms_extract_2022-2026.sqlite',
    'members': 'members_by_feeder_monthly_2022-2026.csv',
    'lines': 'line_register_69kv_2026.xlsx',
    'structures': 'structure_inventory_69kv_2026.csv',
    'subs': 'substation_register_2026.xlsx',
    'study22': 'protection_study_2022.pdf',
    'study25': 'protection_study_2025.pdf',
    'settings': 'relay_settings_69kv_2026.xlsx',
    'loading': 'scada_line_loading_hourly_2022-2026.csv',
    'apt': 'port_alcorn_airport_hourly_2022-2026.csv',
    'inl_apt': 'inland_regional_airport_hourly_2022-2026.csv',
    'stations': 'substation_weather_stations_2023-2026.csv',
    'strokes': 'lightning_strokes_2022-2026.csv',
    'patrols': 'line_patrol_reports_2022-2026.xlsx',
    'avian': 'waterbird_and_raptor_roost_survey_2021-2026.xlsx',
    'esdd': 'esdd_monitoring_2022-2026.xlsx',
    'washing': 'insulator_washing_log_2022-2026.xlsx',
    'veg': 'vegetation_work_orders_2022-2026.csv',
    'maint': 'line_maintenance_work_orders_2022-2026.csv',
    'ipp': 'coyote_draw_solar_protection_events_2023-2026.csv',
    'procedure': 'reliability_reporting_procedure_rev4.docx',
    'corrosion': 'tower_and_pole_condition_survey_2025.xlsx',
    'easements': 'row_easement_register.csv',
}
DISTRACTORS = ['corrosion', 'easements']
DELIVERABLES = ['lpec_69kv_faults_2022-2026.csv', 'lpec_69kv_fault_review_2026.xlsx', '69kv_work_list_winter_2026-27.docx']

# each file's own created and last saved times (Central prevailing wall clock), from the system or person keeping it
STAMP = {
    'er': (dt.datetime(2026, 11, 3, 8, 47, 12), dt.datetime(2026, 11, 3, 8, 47, 12)),
    'gv': (dt.datetime(2026, 11, 3, 9, 6, 41), dt.datetime(2026, 11, 3, 9, 6, 41)),
    'legacy': (dt.datetime(2019, 6, 4, 13, 22, 9), dt.datetime(2026, 10, 28, 15, 3, 44)),
    'soe': (dt.datetime(2026, 11, 3, 10, 14, 26), dt.datetime(2026, 11, 3, 10, 14, 26)),
    'crlog': (dt.datetime(2021, 12, 30, 22, 41, 7), dt.datetime(2026, 11, 1, 6, 12, 55)),
    'oms': (dt.datetime(2026, 11, 2, 14, 30, 18), dt.datetime(2026, 11, 2, 14, 30, 18)),
    'members': (dt.datetime(2026, 11, 2, 11, 5, 33), dt.datetime(2026, 11, 2, 11, 5, 33)),
    'lines': (dt.datetime(2017, 2, 14, 9, 31, 50), dt.datetime(2026, 8, 19, 16, 24, 2)),
    'structures': (dt.datetime(2026, 10, 30, 13, 48, 26), dt.datetime(2026, 10, 30, 13, 48, 26)),
    'subs': (dt.datetime(2018, 5, 7, 10, 12, 31), dt.datetime(2026, 9, 9, 14, 57, 18)),
    'study22': (dt.datetime(2022, 3, 17, 9, 4, 22), dt.datetime(2022, 3, 22, 15, 38, 46)),
    'study25': (dt.datetime(2025, 2, 10, 8, 51, 39), dt.datetime(2025, 2, 13, 16, 20, 5)),
    'settings': (dt.datetime(2016, 9, 26, 14, 2, 11), dt.datetime(2026, 7, 8, 10, 33, 57)),
    'loading': (dt.datetime(2026, 11, 3, 10, 41, 3), dt.datetime(2026, 11, 3, 10, 41, 3)),
    'apt': (dt.datetime(2026, 11, 2, 7, 26, 15), dt.datetime(2026, 11, 2, 7, 26, 15)),
    'inl_apt': (dt.datetime(2026, 11, 2, 7, 28, 49), dt.datetime(2026, 11, 2, 7, 28, 49)),
    'stations': (dt.datetime(2026, 11, 2, 8, 2, 37), dt.datetime(2026, 11, 2, 8, 2, 37)),
    'strokes': (dt.datetime(2026, 11, 2, 9, 40, 11), dt.datetime(2026, 11, 2, 9, 40, 11)),
    'patrols': (dt.datetime(2020, 3, 2, 7, 55, 18), dt.datetime(2026, 10, 30, 16, 41, 29)),
    'avian': (dt.datetime(2021, 11, 8, 10, 27, 40), dt.datetime(2026, 3, 12, 14, 9, 52)),
    'esdd': (dt.datetime(2021, 12, 6, 15, 33, 4), dt.datetime(2026, 10, 27, 11, 18, 37)),
    'washing': (dt.datetime(2021, 10, 19, 8, 12, 56), dt.datetime(2026, 10, 23, 15, 47, 10)),
    'veg': (dt.datetime(2026, 11, 2, 12, 16, 8), dt.datetime(2026, 11, 2, 12, 16, 8)),
    'maint': (dt.datetime(2026, 11, 2, 12, 31, 45), dt.datetime(2026, 11, 2, 12, 31, 45)),
    'ipp': (dt.datetime(2026, 10, 30, 9, 2, 17), dt.datetime(2026, 10, 30, 9, 2, 17)),
    'procedure': (dt.datetime(2023, 1, 9, 9, 40, 13), dt.datetime(2024, 2, 27, 16, 5, 41)),
    'corrosion': (dt.datetime(2025, 4, 14, 8, 28, 30), dt.datetime(2025, 9, 3, 13, 12, 6)),
    'easements': (dt.datetime(2026, 6, 23, 10, 54, 19), dt.datetime(2026, 6, 23, 10, 54, 19)),
}
GOLD_STAMP = {
    'csv': (dt.datetime(2026, 11, 10, 16, 52, 8), dt.datetime(2026, 11, 10, 16, 52, 8)),
    'xlsx': (dt.datetime(2026, 11, 5, 8, 37, 44), dt.datetime(2026, 11, 11, 17, 9, 26)),
    'memo': (dt.datetime(2026, 11, 11, 9, 26, 3), dt.datetime(2026, 11, 12, 10, 41, 52)),
}

T0 = dt.datetime(2021, 9, 1, 5, 0, tzinfo=UTC)       # the simulation starts 00:00 CDT 1 Sep 2021 (deposits, roosts)
REC0 = dt.datetime(2022, 1, 1, 6, 0, tzinfo=UTC)     # the record starts 00:00 CST 1 Jan 2022
T_END = dt.datetime(2026, 11, 1, 5, 0, tzinfo=UTC)   # 00:00 CDT 1 Nov 2026
AS_OF = dt.date(2026, 11, 3)
YEAR26_0 = dt.datetime(2026, 1, 1, 6, 0, tzinfo=UTC)
INLAND_NEW_AUTO = dt.datetime(2024, 3, 14, 19, 30, tzinfo=UTC)   # Inland T2 (150 MVA) energized; T1 (75 MVA) retired
SOLAR_ENERGIZED = dt.datetime(2023, 2, 20, 17, 0, tzinfo=UTC)    # Coyote Draw Solar's GSU first energized
STATIONS_FROM = dt.datetime(2023, 3, 14, 6, 0, tzinfo=UTC)       # the substation weather stations' first readings
FOG_SEASON = (dt.date(2026, 12, 1), dt.date(2027, 3, 31))
LETTER_MM = (215.9, 279.4)
NH = int((T_END - T0).total_seconds() // 3600)


def local(t):
    """a Central wall-clock datetime (naive) as an aware datetime"""
    return t.replace(tzinfo=TZ)


def utc_z(t):
    return local(t).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


def to_local(ts):
    """aware UTC -> naive Central prevailing"""
    return ts.astimezone(TZ).replace(tzinfo=None)


def to_cst(ts):
    """aware UTC -> naive Central Standard Time (no daylight saving)"""
    return ts.astimezone(CST).replace(tzinfo=None)


def hour_index(ts):
    """hours since T0 for an aware datetime"""
    return int((ts - T0).total_seconds() // 3600)


def ts_of(h, sec=0.0):
    return T0 + dt.timedelta(hours=float(h), seconds=float(sec))


def local_hour(h):
    """the Central prevailing clock hour (0-23) and date of simulation hour h"""
    t = to_local(ts_of(h))
    return t.hour, t.date()
