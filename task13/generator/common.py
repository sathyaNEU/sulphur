"""Shared constants for the task13 generator (architecture 4): paths, the organisation, its people, the pack's files
and each file's save times, and the clock helpers. The world runs on UTC; each file is written on the clock its
system keeps (the ADMS archive and the airport weather in UTC, the SCADA historian in Central Standard Time all
year, the outage record and the maintenance books in Central prevailing time)."""
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

SEED = 41327          # the network, its customers, devices, batteries, radio links and settings
WX_SEED = 41328       # the airport weather
EV_SEED = 41337       # faults, operations, archive losses, maintenance, outage handling

ORG = 'Blue Earth Valley Power Company'
ORG_SHORT = 'Blue Earth Valley Power'
COMMISSION = 'Minnesota Public Utilities Commission'
VENDOR = 'Gridwise Systems'

PEOPLE = {
    'gm_perf': 'Shawn Hudson',          # manager, grid modernization performance (files the report)
    'da_engineer': 'Nathan Reeves',     # distribution automation engineer (the golden's author)
    'protection': 'Elaine Stewart',     # system protection engineer
    'ops': 'Jacob Barton',              # distribution operations superintendent
    'regulatory': 'Debra Reed',         # director, regulatory affairs
    'capital': 'Ruben Nicholson',       # capital projects manager
}

SUBSTATIONS = [('RPD', 'Rapidan'), ('EGL', 'Eagle Lake'), ('KST', 'Kasota'), ('MNP', 'Minneopa'),
               ('LMV', 'Lime Valley'), ('SKY', 'Skyline'), ('MDL', 'Madison Lake'), ('JUD', 'Judson'),
               ('GTH', 'Good Thunder')]

RADIO_SITES = ['Skyline Tower', 'Eagle Lake Water Tower', 'Kasota Bluff', 'Madison Lake', 'Judson Elevator']

FILES = {
    'adms': 'adms_flisr_event_archive_2022-2026.csv',
    'oms': 'oms_outage_events_2022-2026.csv',
    'scada': 'scada_hourly_amps_2025-2026.csv',
    'devents': 'scada_device_events_2022-2026.csv',
    'register': 'da_device_register_2026.xlsx',
    'loops': 'flisr_loop_configuration_2026.xlsx',
    'maint': 'da_maintenance_records_2019-2026.xlsx',
    'weather': 'kmkt_hourly_weather_2022-2026.csv',
    'incidents': 'comms_and_control_system_incidents_2022-2026.csv',
    'capital': 'distribution_capital_works_2019-2027.xlsx',
    'loads': 'large_load_requests_2026-2027.xlsx',
    'order': 'mpuc_grid_modernization_metrics_order.pdf',
    'design': 'da_design_basis_rev3.pdf',
    'dashboard': 'adms_flisr_kpi_dashboard_2022-2026.xlsx',
    'ami': 'ami_outage_notifications_daily_2025-2026.csv',
    'veg': 'vegetation_cycle_status_2026.xlsx',
}
DISTRACTORS = ['ami', 'veg']
DELIVERABLES = ['flisr_review_2026.xlsx', 'flisr_2026_memo.pdf']

# each file's own created and last saved times (Central prevailing wall clock), from the system or person keeping it
STAMP = {
    'adms': (dt.datetime(2026, 11, 3, 9, 14, 37), dt.datetime(2026, 11, 3, 9, 14, 37)),
    'oms': (dt.datetime(2026, 11, 2, 15, 41, 8), dt.datetime(2026, 11, 2, 15, 41, 8)),
    'scada': (dt.datetime(2026, 11, 3, 10, 2, 55), dt.datetime(2026, 11, 3, 10, 2, 55)),
    'devents': (dt.datetime(2026, 11, 3, 10, 27, 19), dt.datetime(2026, 11, 3, 10, 27, 19)),
    'register': (dt.datetime(2019, 3, 12, 14, 5, 23), dt.datetime(2026, 10, 22, 16, 48, 51)),
    'loops': (dt.datetime(2020, 1, 28, 10, 31, 7), dt.datetime(2026, 9, 30, 11, 12, 39)),
    'maint': (dt.datetime(2019, 4, 2, 8, 16, 44), dt.datetime(2026, 10, 30, 14, 26, 12)),
    'weather': (dt.datetime(2026, 11, 2, 7, 18, 44), dt.datetime(2026, 11, 2, 7, 18, 44)),
    'incidents': (dt.datetime(2026, 11, 2, 13, 3, 21), dt.datetime(2026, 11, 2, 13, 3, 21)),
    'capital': (dt.datetime(2019, 1, 15, 9, 2, 31), dt.datetime(2026, 10, 15, 17, 34, 58)),
    'loads': (dt.datetime(2026, 2, 9, 11, 20, 46), dt.datetime(2026, 10, 27, 9, 52, 17)),
    'order': (dt.datetime(2024, 6, 20, 10, 7, 41), dt.datetime(2024, 6, 21, 14, 37, 26)),
    'design': (dt.datetime(2023, 3, 6, 9, 23, 18), dt.datetime(2023, 3, 8, 16, 10, 52)),
    'dashboard': (dt.datetime(2026, 11, 1, 6, 0, 3), dt.datetime(2026, 11, 1, 6, 0, 3)),
    'ami': (dt.datetime(2026, 11, 2, 16, 22, 40), dt.datetime(2026, 11, 2, 16, 22, 40)),
    'veg': (dt.datetime(2026, 1, 19, 13, 41, 9), dt.datetime(2026, 9, 24, 10, 5, 33)),
}
GOLD_STAMP = {
    'xlsx': (dt.datetime(2026, 11, 6, 8, 42, 37), dt.datetime(2026, 11, 10, 17, 26, 14)),
    'memo': (dt.datetime(2026, 11, 10, 9, 15, 48), dt.datetime(2026, 11, 11, 10, 48, 21)),
}

T0 = dt.datetime(2021, 12, 1, 6, 0, tzinfo=dt.timezone.utc)      # simulation start (00:00 CST 1 Dec 2021)
T_END = dt.datetime(2026, 11, 1, 5, 0, tzinfo=dt.timezone.utc)   # 00:00 CDT 1 Nov 2026
REC0 = dt.datetime(2022, 1, 1, 6, 0, tzinfo=dt.timezone.utc)     # the record starts 00:00 CST 1 Jan 2022
AS_OF = dt.date(2026, 11, 4)
DESIGN_MIN_C = -27.0
LETTER_MM = (215.9, 279.4)   # US Letter: the commission's and the utility's documents


def local(t):
    """a Central wall-clock datetime (naive) as an aware datetime"""
    return t.replace(tzinfo=TZ)


def utc_z(t):
    return local(t).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


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
    return T0 + dt.timedelta(hours=h, seconds=sec)
