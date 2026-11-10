"""task5 architecture 4: the fixed facts of the State of Franklin's unemployment insurance report census.

Fourteen counties, the industries and their NAICS codes, the quarter calendar with due dates and flash cut-offs,
the shipped file names and the people. Everything here is a fact of the fiction; sim.py draws the employers."""
import datetime as dt

SEED = 50431

STATE = "Franklin"
EXTRACT = dt.datetime(2027, 2, 15, 23, 59, 59)       # the Division's extract: everything received by then
CUTOFF_DAY = 15                                       # a quarter's flash takes the reports received by the 15th of
                                                      # the second month after the quarter ends
THRESHOLD = -2.0                                      # section 4: a change of minus 2.0 per cent or lower designates

# county: FIPS-style code (alphabetical, Sayre formed in 1931 from Talcott and given the next number), name,
# accounts at the start of 2023, healthy trend a year, share of small employers filing through a payroll agent,
# share of agent clients served by a statewide bureau, lake county, LMI region
COUNTIES = [
    # code   name        n0     target  agent  bureau  lake   region
    ("001", "Bray",       1130, -0.0100, 0.60, 0.34, False, "Southern Tier"),
    ("003", "Calder",     5380,  0.0160, 0.62, 0.58, False, "Capital"),
    ("005", "Corliss",     840,  0.0070, 0.58, 0.30, False, "Southern Tier"),
    ("007", "Fenwick",     990,  0.0020, 0.57, 0.33, False, "North Woods"),
    ("009", "Garrow",     1880, -0.0300, 0.66, 0.22, False, "Capital"),
    ("011", "Hadley",     1490,  0.0130, 0.60, 0.40, False, "Southern Tier"),
    ("013", "Kittredge",   590, -0.0315, 0.61, 0.52, True,  "Lakes"),
    ("015", "Linden",     2470,  0.0090, 0.63, 0.56, False, "Capital"),
    ("017", "Merritt",    2880, -0.0080, 0.59, 0.36, False, "River"),
    ("019", "Ostrom",     1290, -0.0305, 0.50, 0.30, False, "North Woods"),
    ("021", "Pell",       1690,  0.0050, 0.60, 0.38, False, "River"),
    ("023", "Talcott",     690,  0.0040, 0.62, 0.55, True,  "Lakes"),
    ("025", "Whitcomb",   2080,  0.0060, 0.61, 0.44, False, "River"),
    ("027", "Sayre",       500,  0.0150, 0.58, 0.31, False, "Lakes"),
]
CODES = [c[0] for c in COUNTIES]
# each county's employer sizes, as drawn, times this factor
SCALE = {c: 1.0 for c in CODES}
# each county's 2026 drift beyond the calibrated target (set after the golden is measured)
NUDGE = {c: 0.0 for c in CODES}
NAMES = {c[0]: c[1] for c in COUNTIES}
LAKES = ("013", "023", "027")                          # the Lakes region: summer trade at the lake worksites
# how much likelier a chain in trade or leisure is to keep a worksite in a lake county than its size alone would make it
LAKE_SITES = {"013": 8.5, "023": 5.5, "027": 7.0}
NORTH = ("007", "019")                                 # the North Woods: outdoor work slows in winter

# BLS supersectors: code, title, month factors Jan..Dec (pay period including the 12th)
SUPERSECTORS = {
    "1011": ("Natural resources and mining", [0.88, 0.88, 0.92, 0.99, 1.06, 1.10, 1.10, 1.09, 1.06, 1.03, 0.97, 0.92]),
    "1012": ("Construction", [0.88, 0.88, 0.93, 1.00, 1.05, 1.08, 1.09, 1.09, 1.07, 1.05, 1.00, 0.93]),
    "1013": ("Manufacturing", [0.99, 0.99, 0.99, 1.00, 1.00, 1.01, 1.00, 1.01, 1.01, 1.00, 1.00, 0.99]),
    "1021": ("Trade, transportation, and utilities", [0.97, 0.96, 0.97, 0.98, 0.99, 1.00, 1.00, 1.00, 0.99, 1.00, 1.04, 1.07]),
    "1022": ("Information", [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00]),
    "1023": ("Financial activities", [0.99, 0.99, 1.00, 1.00, 1.00, 1.01, 1.01, 1.01, 1.00, 1.00, 1.00, 1.00]),
    "1024": ("Professional and business services", [0.97, 0.98, 0.99, 1.00, 1.00, 1.01, 1.01, 1.01, 1.01, 1.01, 1.01, 1.00]),
    "1025": ("Education and health services", [1.01, 1.01, 1.01, 1.01, 1.00, 0.97, 0.95, 0.97, 1.01, 1.02, 1.02, 1.01]),
    "1026": ("Leisure and hospitality", [0.92, 0.92, 0.95, 0.98, 1.04, 1.10, 1.12, 1.11, 1.03, 0.98, 0.94, 0.94]),
    "1027": ("Other services", [0.99, 0.99, 1.00, 1.00, 1.00, 1.01, 1.01, 1.01, 1.00, 1.00, 1.00, 0.99]),
    "1028": ("Public administration", [1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.01, 1.00, 1.00, 1.00, 1.00, 1.00]),
}

# NAICS 2022 code, title, supersector, weight in the private economy, the code it replaced in NAICS 2017 (or None)
NAICS = [
    ("111421", "Nursery and Tree Production", "1011", 0.6, None),
    ("111998", "All Other Miscellaneous Crop Farming", "1011", 0.5, None),
    ("112111", "Beef Cattle Ranching and Farming", "1011", 0.5, None),
    ("112120", "Dairy Cattle and Milk Production", "1011", 0.6, None),
    ("113310", "Logging", "1011", 0.7, None),
    ("115310", "Support Activities for Forestry", "1011", 0.3, None),
    ("212321", "Construction Sand and Gravel Mining", "1011", 0.2, None),
    ("236115", "New Single-Family Housing Construction (except For-Sale Builders)", "1012", 1.4, None),
    ("236118", "Residential Remodelers", "1012", 1.6, None),
    ("236220", "Commercial and Institutional Building Construction", "1012", 0.7, None),
    ("237310", "Highway, Street, and Bridge Construction", "1012", 0.4, None),
    ("238110", "Poured Concrete Foundation and Structure Contractors", "1012", 0.6, None),
    ("238160", "Roofing Contractors", "1012", 0.8, None),
    ("238210", "Electrical Contractors and Other Wiring Installation Contractors", "1012", 1.3, None),
    ("238220", "Plumbing, Heating, and Air-Conditioning Contractors", "1012", 1.5, None),
    ("238310", "Drywall and Insulation Contractors", "1012", 0.5, None),
    ("238320", "Painting and Wall Covering Contractors", "1012", 0.7, None),
    ("238910", "Site Preparation Contractors", "1012", 0.8, None),
    ("238990", "All Other Specialty Trade Contractors", "1012", 0.6, None),
    ("311812", "Commercial Bakeries", "1013", 0.3, None),
    ("321113", "Sawmills", "1013", 0.4, None),
    ("321918", "Other Millwork (including Flooring)", "1013", 0.3, None),
    ("322121", "Paper (except Newsprint) Mills", "1013", 0.1, None),
    ("326199", "All Other Plastics Product Manufacturing", "1013", 0.3, None),
    ("332323", "Ornamental and Architectural Metal Work Manufacturing", "1013", 0.3, None),
    ("332710", "Machine Shops", "1013", 0.8, None),
    ("336390", "Other Motor Vehicle Parts Manufacturing", "1013", 0.2, None),
    ("337110", "Wood Kitchen Cabinet and Countertop Manufacturing", "1013", 0.4, None),
    ("221122", "Electric Power Distribution", "1021", 0.1, None),
    ("423310", "Lumber, Plywood, Millwork, and Wood Panel Merchant Wholesalers", "1021", 0.3, None),
    ("423810", "Construction and Mining (except Oil Well) Machinery and Equipment Merchant Wholesalers", "1021", 0.3, None),
    ("424410", "General Line Grocery Merchant Wholesalers", "1021", 0.3, None),
    ("441110", "New Car Dealers", "1021", 0.6, None),
    ("444110", "Home Centers", "1021", 0.2, None),
    ("444180", "Other Building Material Dealers", "1021", 0.5, "444190"),
    ("445110", "Supermarkets and Other Grocery Retailers (except Convenience Retailers)", "1021", 0.7, None),
    ("445131", "Convenience Retailers", "1021", 0.6, "445120"),
    ("455211", "Warehouse Clubs and Supercenters", "1021", 0.1, "452311"),
    ("456110", "Pharmacies and Drug Retailers", "1021", 0.5, "446110"),
    ("457110", "Gasoline Stations with Convenience Stores", "1021", 0.7, "447110"),
    ("458110", "Clothing and Clothing Accessories Retailers", "1021", 0.5, "448140"),
    ("459110", "Sporting Goods Retailers", "1021", 0.3, "451110"),
    ("459420", "Gift, Novelty, and Souvenir Retailers", "1021", 0.4, "453220"),
    ("459999", "All Other Miscellaneous Retailers", "1021", 0.5, "453998"),
    ("484110", "General Freight Trucking, Local", "1021", 0.7, None),
    ("484220", "Specialized Freight (except Used Goods) Trucking, Local", "1021", 0.6, None),
    ("488410", "Motor Vehicle Towing", "1021", 0.3, None),
    ("492210", "Local Messengers and Local Delivery", "1021", 0.3, None),
    ("493110", "General Warehousing and Storage", "1021", 0.3, None),
    ("513110", "Newspaper Publishers", "1022", 0.2, "511110"),
    ("517112", "Wireless Telecommunications Carriers (except Satellite)", "1022", 0.2, "517312"),
    ("519290", "Web Search Portals and All Other Information Services", "1022", 0.2, "519130"),
    ("522110", "Commercial Banking", "1023", 0.4, None),
    ("522130", "Credit Unions", "1023", 0.3, None),
    ("524210", "Insurance Agencies and Brokerages", "1023", 0.9, None),
    ("531110", "Lessors of Residential Buildings and Dwellings", "1023", 0.6, None),
    ("531210", "Offices of Real Estate Agents and Brokers", "1023", 0.8, None),
    ("531311", "Residential Property Managers", "1023", 0.5, None),
    ("541110", "Offices of Lawyers", "1024", 1.4, None),
    ("541211", "Offices of Certified Public Accountants", "1024", 0.9, None),
    ("541213", "Tax Preparation Services", "1024", 0.4, None),
    ("541330", "Engineering Services", "1024", 0.7, None),
    ("541512", "Computer Systems Design Services", "1024", 0.6, None),
    ("541810", "Advertising Agencies", "1024", 0.3, None),
    ("561320", "Temporary Help Services", "1024", 0.3, None),
    ("561720", "Janitorial Services", "1024", 0.7, None),
    ("561730", "Landscaping Services", "1024", 1.2, None),
    ("562111", "Solid Waste Collection", "1024", 0.2, None),
    ("611110", "Elementary and Secondary Schools", "1025", 0.2, None),
    ("621111", "Offices of Physicians (except Mental Health Specialists)", "1025", 1.2, None),
    ("621210", "Offices of Dentists", "1025", 1.1, None),
    ("621340", "Offices of Physical, Occupational and Speech Therapists, and Audiologists", "1025", 0.6, None),
    ("621610", "Home Health Care Services", "1025", 0.5, None),
    ("622110", "General Medical and Surgical Hospitals", "1025", 0.05, None),
    ("623110", "Nursing Care Facilities (Skilled Nursing Facilities)", "1025", 0.3, None),
    ("623312", "Assisted Living Facilities for the Elderly", "1025", 0.3, None),
    ("624410", "Child Care Services", "1025", 0.8, None),
    ("713930", "Marinas", "1026", 0.15, None),
    ("713940", "Fitness and Recreational Sports Centers", "1026", 0.5, None),
    ("713990", "All Other Amusement and Recreation Industries", "1026", 0.4, None),
    ("721110", "Hotels (except Casino Hotels) and Motels", "1026", 0.5, None),
    ("721211", "RV (Recreational Vehicle) Parks and Campgrounds", "1026", 0.25, None),
    ("721214", "Recreational and Vacation Camps (except Campgrounds)", "1026", 0.15, None),
    ("722410", "Drinking Places (Alcoholic Beverages)", "1026", 0.6, None),
    ("722511", "Full-Service Restaurants", "1026", 2.2, None),
    ("722513", "Limited-Service Restaurants", "1026", 1.6, None),
    ("722515", "Snack and Nonalcoholic Beverage Bars", "1026", 0.5, None),
    ("811111", "General Automotive Repair", "1027", 1.0, None),
    ("811121", "Automotive Body, Paint, and Interior Repair and Maintenance", "1027", 0.5, None),
    ("812111", "Barber Shops", "1027", 0.3, None),
    ("812112", "Beauty Salons", "1027", 0.8, None),
    ("812910", "Pet Care (except Veterinary) Services", "1027", 0.3, None),
    ("813110", "Religious Organizations", "1027", 0.9, None),
]
GOV_NAICS = [("611110", "Elementary and Secondary Schools", "1025"), ("921140", "Executive and Legislative Offices, Combined", "1028"),
             ("922120", "Police Protection", "1028"), ("921190", "Other General Government Support", "1028"),
             ("622110", "General Medical and Surgical Hospitals", "1025")]
# county tilts toward an industry group (the weight of each listed industry times the factor)
TILT = {
    "009": (3.0, {"236115", "236118", "236220", "238110", "238160", "238210", "238220", "238310", "238320", "238910",
                  "238990", "423310", "444180", "321918", "337110", "332323"}),
    "019": (9.0, {"113310", "115310", "484220", "484110", "321113", "488410", "423810"}),
}
# the housing chain: residential and commercial building, the trades, and the wood that goes into them
HOUSING_CHAIN = {"236115", "236118", "236220", "237310", "238110", "238160", "238210", "238220", "238310", "238320",
                 "238910", "238990", "113310", "115310", "321113", "321918", "337110", "423310", "444180", "444190",
                 "484220", "423810", "444110"}
# the 2026 housing downturn: the chance, on top of the usual one, that a housing-chain employer got into trouble in
# each quarter of 2026 (by size class: the largest are spared), and how much of the usual number of new housing-chain
# employers started up
BUST_HAZARD = [0.004, 0.012, 0.035, 0.11]
BUST_SIZE = [1.0, 0.95, 0.95, 0.95, 0.45, 0.0, 0.0, 0.0]
BUST_BIRTHS = [0.86, 0.62, 0.42, 0.28]
OTHER_BIRTHS = [0.99, 0.95, 0.90, 0.84]
BIRTH_RATE = 0.045                                      # new employers a quarter, as a share of a county's 2023 accounts

# size classes: upper bound of employees and share of private accounts
SIZE_CLASSES = [(4, 0.48), (9, 0.21), (19, 0.14), (49, 0.10), (99, 0.04), (249, 0.022), (499, 0.0055), (1500, 0.0025)]


def quarter_label(q):
    """q = 0 is 2023 Q1."""
    return "%dQ%d" % (2023 + q // 4, q % 4 + 1)


def quarter_end(q):
    y, k = 2023 + q // 4, q % 4 + 1
    return dt.date(y, 3 * k, [31, 30, 30, 31][k - 1])


def due_date(q):
    """the report is due the last day of the month after the quarter"""
    e = quarter_end(q)
    m, y = e.month + 1, e.year
    if m > 12:
        m, y = 1, y + 1
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


def cutoff(q):
    """the flash for quarter q counts reports received by the 15th of the second month after it, 23:59:59"""
    e = quarter_end(q)
    m, y = e.month + 2, e.year
    if m > 12:
        m, y = m - 12, y + 1
    return dt.datetime(y, m, CUTOFF_DAY, 23, 59, 59)


NQ = 16          # 2023Q1 .. 2026Q4
NM = 48          # January 2023 .. December 2026
FLASH_Q = 15     # 2026Q4
BASE_Q = 11      # 2025Q4

FILES = {
    "reports": "ui_quarterly_reports_2023q1_2026q4.csv",
    "accounts": "ui_employer_accounts_2027-02-15.csv",
    "status": "ui_account_status_history_2023-2027.csv",
    "worksites": "ui_multiple_worksite_reports_2023q1_2026q4.csv",
    "counties": "franklin_county_codes.csv",
    "naics": "naics_2017_2022_supersector_concordance.csv",
    "act": "community_transition_fund_act_2026.docx",
    "agreement": "ui_lmi_data_sharing_agreement_2025.docx",
    "request": "fund_board_certification_request_2027-01-12.eml",
    "published": "covered_employment_by_county_2025q4.xlsx",
    "rates": "ui_contribution_rate_notice_2027.docx",
    "population": "franklin_county_population_estimates_2025.csv",
}
DISTRACTORS = ["rates", "population"]
PUBLISHED_CUT = dt.datetime(2026, 5, 31, 23, 59, 59)    # the published 2025 Q4 table: reports posted through this day

DELIVERABLES = {"cert": "ctf_certification_december_2026.xlsx", "employers": "ctf_employer_jobs_december_2026.csv",
                "memo": "ctf_certification_memo_2027.docx"}

PEOPLE = {
    "lmi_director": ("Danielle Fuller", "Director, Labor Market Information", "dfuller@labor.franklin.gov"),
    "fund_admin": ("Matthew Cox", "Administrator, Community Transition Fund", "matthew.cox@commerce.franklin.gov"),
    "ui_chief": ("William Robertson", "Chief, Unemployment Insurance Tax Division", "wrobertson@labor.franklin.gov"),
}
