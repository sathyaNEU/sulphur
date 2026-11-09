"""Shared constants for the task13 generator: paths, names, files and save times."""
import datetime as dt
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, 'target')
GOLDEN = os.path.join(TASK, 'golden')
ZONE = 'Pacific/Auckland'

ORG = 'Kotuku Networks Limited'
ORG_SHORT = 'Kotuku Networks'
TRUST = 'Kotuku Electricity Consumer Trust'
WEATHER = 'Pou Weather Services'
CONTRACTOR = 'Ridgeline Arborists Limited'

PEOPLE = {
    'network_gm': 'Tania Foley',
    'veg_manager': 'Wayne Ward',
    'reliability_eng': 'Hoani Marshall',
    'regulatory_mgr': 'Kathryn Carter',
    'contractor': 'Sean Chapman',
    'customer_lead': 'Maria Hodson',
}

STATION_IDS = ['PBA', 'MTF', 'KWR', 'TSD']
FILES = {
    'oms': 'oms_interruptions_2022-04_2026-10.csv',
    'wx_PBA': 'pou_aws_hourly/pou_aws_PBA_hourly_2006-2026.csv',
    'wx_MTF': 'pou_aws_hourly/pou_aws_MTF_hourly_2006-2026.csv',
    'wx_KWR': 'pou_aws_hourly/pou_aws_KWR_hourly_2006-2026.csv',
    'wx_TSD': 'pou_aws_hourly/pou_aws_TSD_hourly_2006-2026.csv',
    'stations': 'pou_aws_station_register.csv',
    'feeders': 'feeder_register_2026.xlsx',
    'devices': 'protection_assets_2026-10.csv',
    'icps': 'icp_counts_by_feeder_2022-04_2026-10.csv',
    'vegcycle': 'vegetation_cycle_log_2014-2026.xlsx',
    'standard': 'reliability_reporting_standard.docx',
    'programme': 'vegetation_catchup_2027_programme_terms.docx',
    'notices': 'tree_notices_register_2024-2026.xlsx',
    'rates': 'ridgeline_2027_schedule_of_rates.docx',
}
DISTRACTORS = ['notices', 'rates']
DELIVERABLES = ['vegetation_catchup_2027_feeders.csv', 'vegetation_catchup_2027_board_note.docx']

# each file's own created and last saved times (New Zealand local), from the system or person that keeps it
STAMP = {
    'oms': (dt.datetime(2026, 11, 3, 7, 42, 11), dt.datetime(2026, 11, 3, 7, 42, 11)),
    'wx_PBA': (dt.datetime(2026, 11, 2, 2, 15, 4), dt.datetime(2026, 11, 2, 2, 15, 4)),
    'wx_MTF': (dt.datetime(2026, 11, 2, 2, 15, 39), dt.datetime(2026, 11, 2, 2, 15, 39)),
    'wx_KWR': (dt.datetime(2026, 11, 2, 2, 16, 12), dt.datetime(2026, 11, 2, 2, 16, 12)),
    'wx_TSD': (dt.datetime(2026, 11, 2, 2, 16, 47), dt.datetime(2026, 11, 2, 2, 16, 47)),
    'stations': (dt.datetime(2025, 8, 19, 10, 4, 0), dt.datetime(2025, 8, 19, 10, 4, 0)),
    'feeders': (dt.datetime(2019, 3, 11, 9, 20, 0), dt.datetime(2026, 7, 28, 15, 47, 0)),
    'devices': (dt.datetime(2026, 10, 6, 8, 31, 0), dt.datetime(2026, 10, 6, 8, 31, 0)),
    'icps': (dt.datetime(2026, 11, 2, 6, 5, 0), dt.datetime(2026, 11, 2, 6, 5, 0)),
    'vegcycle': (dt.datetime(2015, 2, 9, 11, 2, 0), dt.datetime(2026, 10, 30, 16, 12, 0)),
    'standard': (dt.datetime(2023, 3, 14, 13, 30, 0), dt.datetime(2026, 4, 8, 10, 51, 0)),
    'programme': (dt.datetime(2026, 9, 22, 9, 15, 0), dt.datetime(2026, 10, 14, 17, 2, 0)),
    'notices': (dt.datetime(2024, 1, 15, 8, 45, 0), dt.datetime(2026, 10, 21, 14, 38, 0)),
    'rates': (dt.datetime(2026, 9, 30, 11, 25, 0), dt.datetime(2026, 10, 2, 9, 40, 0)),
}
GOLD_STAMP = {
    'csv': (dt.datetime(2026, 11, 18, 15, 12, 0), dt.datetime(2026, 11, 18, 15, 12, 0)),
    'note': (dt.datetime(2026, 11, 17, 10, 3, 0), dt.datetime(2026, 11, 19, 16, 44, 0)),
}


def utc_z(t):
    """local New Zealand time to a UTC ISO stamp"""
    from zoneinfo import ZoneInfo
    return t.replace(tzinfo=ZoneInfo(ZONE)).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def local(t):
    """a New Zealand wall-clock time as an aware datetime, so a file's saved time is the same instant on any machine"""
    from zoneinfo import ZoneInfo
    return t.replace(tzinfo=ZoneInfo(ZONE))
