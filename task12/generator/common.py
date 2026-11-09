"""Shared constants for the task12 generator: paths, the organisations and people of the fiction, the shipped file
names and each file's own save time."""
import datetime as dt
import hashlib
import os
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, 'target')
GOLDEN = os.path.join(TASK, 'golden')
ZONE = 'America/Toronto'
TZ = ZoneInfo(ZONE)
UTC = dt.timezone.utc

ORG = 'Northvale Oat Co.'
PANEL_ORG = 'Lakeshore Consumer Panel'          # the household panel provider
AUDIT_ORG = 'Meridian Retail Audit'             # the retail audit provider
AGENCY = 'Halyard & Finch'                       # Northvale's media agency
PEOPLE = {
    'brand_director': 'Gabriel Sloan',
    'vp_finance': 'Angela Reyes',
    'panel_lead': 'Brian Mueller',
    'trade_manager': 'Kimberly Stanley',
    'agency_lead': 'Eric Hernandez',
}
BAND_EDGES = (2.0, 2.9, 3.8)     # the standard's treatment bands, per cent of 2027 category litres
UNIVERSE_HH = {2024: 15_810_000, 2025: 16_020_000, 2026: 16_230_000}   # private households, the panel's universe

FILES = {
    'purchases': 'lcp_purchases_plant_beverages_2024w01_2026w44.csv',
    'households': 'lcp_household_register_2026w44.csv',
    'master': 'lcp_product_master_plant_beverages_2026-10.xlsx',
    'banners': 'lcp_banner_codes.csv',
    'weeks': 'lcp_week_calendar_2024_2027.csv',
    'distribution': 'mra_weighted_distribution_northvale_2026.csv',
    'trade': 'northvale_trade_calendar_2026.xlsx',
    'media': 'northvale_media_plan_2026.xlsx',
    'standard': 'portfolio_review_standard_2026.docx',
    'tracker': 'brand_health_tracker_wave9_2026-09.xlsx',
    'proposal': 'halyard_finch_northvale_2027_support_proposal.docx',
}
DELIVERABLES = {'paper': 'northvale_oat_2027_treatment.docx', 'book': 'northvale_oat_2027_forecast.xlsx'}
DISTRACTORS = ['tracker', 'proposal']

# each file's own last save (local time in Toronto), inside the fiction's calendar and all distinct
STAMP = {
    'purchases': dt.datetime(2026, 11, 5, 6, 12, 41),
    'households': dt.datetime(2026, 11, 5, 6, 14, 3),
    'master': dt.datetime(2026, 10, 28, 15, 47, 0),
    'banners': dt.datetime(2026, 7, 2, 10, 21, 55),
    'weeks': dt.datetime(2026, 1, 9, 11, 3, 17),
    'distribution': dt.datetime(2026, 11, 4, 9, 38, 26),
    'trade': dt.datetime(2026, 9, 18, 16, 52, 0),
    'media': dt.datetime(2026, 9, 29, 13, 25, 0),
    'standard': dt.datetime(2026, 2, 17, 14, 6, 0),
    'tracker': dt.datetime(2026, 10, 9, 17, 41, 0),
    'proposal': dt.datetime(2026, 11, 2, 18, 19, 0),
}
CREATED = {
    'master': dt.datetime(2025, 1, 14, 9, 2, 0),
    'trade': dt.datetime(2026, 2, 26, 10, 15, 0),
    'media': dt.datetime(2026, 1, 30, 14, 40, 0),
    'standard': dt.datetime(2026, 1, 21, 9, 30, 0),
    'tracker': dt.datetime(2026, 10, 6, 11, 5, 0),
    'proposal': dt.datetime(2026, 10, 26, 9, 48, 0),
}
GOLD_STAMP = {'paper': (dt.datetime(2026, 11, 10, 16, 5, 0), dt.datetime(2026, 11, 12, 18, 32, 0)),
              'book': (dt.datetime(2026, 11, 9, 9, 41, 0), dt.datetime(2026, 11, 12, 17, 58, 0))}


def utc_z(local):
    """A Toronto local time as the ISO stamp Office stores (UTC, ending Z)."""
    return local.replace(tzinfo=TZ).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


def local(when):
    return when.replace(tzinfo=TZ)


def stable_int(*parts):
    return int(hashlib.blake2b('|'.join(str(p) for p in parts).encode(), digest_size=6).hexdigest(), 16)
