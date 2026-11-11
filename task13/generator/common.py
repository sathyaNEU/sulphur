"""Shared constants for the task13 generator: paths, names, files and save times."""
import datetime as dt
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, 'target')
GOLDEN = os.path.join(TASK, 'golden')
ZONE = 'Asia/Manila'

SEED = 3421          # the network, the zones, their equipment, defects and inspections, faults and device logs
STORM_SEED = 3422    # thunderstorm cells, flashes and strokes; the lightning network's records use STORM_SEED + 1

ORG = 'Kalumpang Valley Electric Cooperative, Inc.'
ORG_SHORT = 'KALVECO'
LLS = 'Kidlat Data Services Inc.'
SUPPLIER = 'Silangan Electrical Trading Corp.'

PEOPLE = {
    'tsd_manager': 'Lucas Ramirez',          # technical services department manager
    'reliability': 'Donna Rodriguez',        # reliability and protection engineer (the golden's author)
    'inspection': 'Laurie Diaz',             # line inspection supervisor
    'gm': 'Elizabeth Hernandez',             # general manager
    'scada': 'John Fuentes',                 # SCADA and metering supervisor
    'materials': 'Michelle Garcia',          # materials and warehouse
}

SUBSTATIONS = [('BTG', 'Bantug'), ('MLN', 'Malinao'), ('SRQ', 'San Roque'), ('DLP', 'Dalayap'), ('CLB', 'Calabasa'),
               ('TGP', 'Tagumpay'), ('PGP', 'Pinagpala'), ('SNJ', 'Sinasajan'), ('MPD', 'Mapalad'), ('LRD', 'Lourdes'),
               ('CBR', 'Cabaruan'), ('BGS', 'Bagong Sikat')]

FILES = {
    'strokes': 'kidlat_strokes_2016-11_2026-10.csv',
    'scada': 'scada_event_history_2016-12_2026-10.csv',
    'downloads': 'recloser_event_downloads_2016-2026.csv',
    'oms': 'oms_outages_2016-12_2026-10.csv',
    'transformers': 'distribution_transformer_replacements_2016-2026.xlsx',
    'zones': 'protection_zones_register_2026.xlsx',
    'routes': 'overhead_line_routes_2026.geojson',
    'inspections': 'cyclic_line_inspections_2016-2026.xlsx',
    'terms': 'lightning_protection_refit_2027_programme_terms.docx',
    'procedure': 'line_inspection_procedure_rev4.pdf',
    'raingauge': 'substation_raingauge_daily_2022-2026.csv',
    'quotation': 'refit_materials_quotation_2027.xlsx',
}
DISTRACTORS = ['raingauge', 'quotation']
DELIVERABLES = ['lightning_referrals_2027.csv', 'lightning_refit_2027_note.docx']

# each file's own created and last saved times (Philippine local), from the system or person that keeps it
STAMP = {
    'strokes': (dt.datetime(2026, 11, 4, 9, 12, 41), dt.datetime(2026, 11, 4, 9, 12, 41)),
    'scada': (dt.datetime(2026, 11, 3, 14, 6, 18), dt.datetime(2026, 11, 3, 14, 6, 18)),
    'downloads': (dt.datetime(2026, 11, 3, 16, 41, 5), dt.datetime(2026, 11, 3, 16, 41, 5)),
    'oms': (dt.datetime(2026, 11, 2, 8, 27, 52), dt.datetime(2026, 11, 2, 8, 27, 52)),
    'transformers': (dt.datetime(2019, 2, 18, 10, 14, 0), dt.datetime(2026, 10, 29, 15, 38, 0)),
    'zones': (dt.datetime(2018, 6, 4, 13, 2, 0), dt.datetime(2026, 9, 17, 11, 21, 0)),
    'routes': (dt.datetime(2026, 9, 17, 11, 44, 23), dt.datetime(2026, 9, 17, 11, 44, 23)),
    'inspections': (dt.datetime(2016, 11, 21, 8, 30, 0), dt.datetime(2026, 4, 7, 16, 5, 0)),
    'terms': (dt.datetime(2026, 10, 12, 9, 40, 0), dt.datetime(2026, 10, 26, 17, 18, 0)),
    'procedure': (dt.datetime(2022, 8, 9, 10, 0, 0), dt.datetime(2022, 8, 11, 15, 22, 0)),
    'raingauge': (dt.datetime(2026, 11, 2, 7, 55, 9), dt.datetime(2026, 11, 2, 7, 55, 9)),
    'quotation': (dt.datetime(2026, 10, 19, 13, 47, 0), dt.datetime(2026, 10, 21, 10, 9, 0)),
}
GOLD_STAMP = {
    'csv': (dt.datetime(2026, 11, 9, 16, 3, 0), dt.datetime(2026, 11, 9, 16, 3, 0)),
    'note': (dt.datetime(2026, 11, 9, 9, 41, 0), dt.datetime(2026, 11, 10, 11, 26, 0)),
}

LAT0, LON0 = 15.25, 120.60
KX, KY = 107.25, 110.6          # km per degree of longitude (at 15.5 N) and of latitude


def to_latlon(x, y):
    return LAT0 + y / KY, LON0 + x / KX


def to_xy(lat, lon):
    return (lon - LON0) * KX, (lat - LAT0) * KY


def local(t):
    """a Philippine wall-clock time as an aware datetime, so a file's saved time is the same instant anywhere"""
    from zoneinfo import ZoneInfo
    return t.replace(tzinfo=ZoneInfo(ZONE))


def utc_z(t):
    from zoneinfo import ZoneInfo
    return t.replace(tzinfo=ZoneInfo(ZONE)).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
