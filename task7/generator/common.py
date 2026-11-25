"""Shared pieces of the pack writers: the feeder codes, the premises and their addresses, a CSV writer, and one seeded
random stream per file so that two builds write the same bytes."""
import csv
import datetime as dt
import os

import numpy as np

import params as P

FILES = {
    "scada": "scada_feeder_1min_2026.csv",
    "points": "scada_point_list.csv",
    "encoder": "paging_encoder_log_2026.csv",
    "register": "lm_switch_register.csv",
    "sites": "paging_transmitters.xlsx",
    "outages": "radio_shop_outage_log_2026.xlsx",
    "switching": "switching_log_2026.csv",
    "rebates": "hvac_rebates_2012_2026.csv",
    "permits": "county_mechanical_permits_2010_2026.csv",
    "study_homes": "study_homes.csv",
    "study_assign": "study_event_assignments_2026.csv",
    "study_meters": "study_meters_hourly_2026.csv",
    "index": "sunflower_basin_cooling_index_2026.csv",
    "invoices": "wholesale_invoices_2026.pdf",
    "plan": "work_plan_2027_load_management.docx",
    "report": "load_management_report_2025.pdf",
    "map": "tricounty_coverage_map_2026.png",
    "tests": "switch_bench_checks_2019_2026.csv",
    "orders": "service_work_orders_2019_2026.csv",
    "amr": "amr_monthly_reads_2024_2026.csv",
    "wh": "water_heater_winter_schedule_2025_26.csv",
}
DISTRACTORS = [FILES["amr"], FILES["wh"]]


def rng(name):
    """One stream per file, keyed by the file's role, so editing one writer never moves another file's bytes."""
    k = sorted(FILES).index(name) if name in FILES else 50 + sum(map(ord, name)) % 97
    return np.random.default_rng(P.SEED * 1000 + 17 * k + 3)


def write_csv(path, header, rows, crlf=False):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def feeder_codes(dist):
    """core's feeders, in core's order, as the cooperative codes them (substation code and breaker number)."""
    codes, subs = [], []
    for k in range(4):
        idx = [f for f in range(len(dist)) if dist[f] == k]
        j = 0
        for code, name, n in P.SUBSTATIONS[k]:
            for b in range(1, n + 1):
                codes.append("%s-%d" % (code, b))
                subs.append((code, name))
                j += 1
        assert j == len(idx)
    return codes, subs


def point_tag(code):
    sub, b = code.split("-")
    return "%s.F%02d.KW_3PH" % (sub, int(b))


# ---- premises and addresses ----------------------------------------------------------------------------------------
TOWN_STREETS = {
    "Larkin": ["Main", "Cottonwood", "Elm", "Walnut", "Kansas", "Santa Fe", "Locust", "Oak", "Maple", "Grant", "Lincoln",
               "Jefferson", "Pawnee", "Prairie View", "Cherry", "Hickory", "Spruce", "Sunset", "Ash", "Washington"],
    "Medora Flats": ["Main", "Railroad", "Elm", "Center", "Pine", "Church", "Sycamore", "Cedar"],
    "Halverson": ["Main", "Grand", "Second", "Third", "Mill", "Park", "Walnut", "School"],
    "Pruett": ["Main", "Broadway", "Depot", "Cedar", "Willow", "Maple", "Fourth", "Fifth"],
}
SUFFIX = ["Street", "Avenue", "Drive", "Lane", "Court", "Place"]
ABBR = {"Street": "ST", "Avenue": "AVE", "Drive": "DR", "Lane": "LN", "Court": "CT", "Place": "PL", "Road": "RD",
        "North": "N", "South": "S", "East": "E", "West": "W"}


def addresses(x, y, dist, r):
    """A service address for every premise: a town street address near a town, a county road address elsewhere (the
    county numbers rural roads on a mile grid). Unique by construction."""
    out, seen = [], set()
    for i in range(len(x)):
        town, (tx, ty) = P.TOWNS[int(dist[i])]
        d_town = np.hypot(x[i] - tx, y[i] - ty)
        while True:
            if d_town < (3.6 if dist[i] == 0 else 1.6):
                st = TOWN_STREETS[town][int(r.integers(len(TOWN_STREETS[town])))]
                suf = "Street" if st in ("Main", "Second", "Third", "Fourth", "Fifth", "Broadway") else SUFFIX[int(r.integers(len(SUFFIX)))]
                if st in ("Main", "Broadway", "Grand", "Center"):
                    pre = ["North", "South", "East", "West"][int(r.integers(4))] + " "
                else:
                    pre = ""
                num = int(r.integers(100, 2400))
                a = "%d %s%s %s" % (num, pre, st, suf)
                city = town
            else:
                # county roads: lettered roads run north and south, numbered roads east and west, one a mile
                if r.random() < 0.5:
                    road = "Road %d" % int(np.clip(np.rint((y[i] + 20) / 1.609) + 1, 1, 60))
                else:
                    road = "%s Road" % "ABCDEFGHJKLMNPQRSTUVWXYZ"[int(np.clip(np.rint((x[i] + 45) / 3.6), 0, 23))]
                num = int(r.integers(1000, 9999))
                a = "%d %s" % (num, road)
                city = town
            if (a, city) not in seen:
                seen.add((a, city))
                out.append((a, city))
                break
    return out


def county_style(addr, r):
    """The county's permit system: upper case, standard abbreviations, the odd period or doubled space."""
    t = addr.upper()
    for full, ab in ABBR.items():
        t = t.replace(" " + full.upper() + " ", " " + ab + " ")
        if t.endswith(" " + full.upper()):
            t = t[: -len(full)] + ab
        if t.startswith(full.upper() + " "):
            t = ab + t[len(full):]
    u = r.random()
    if u < 0.06:
        t = t.replace(" N ", " N. ").replace(" S ", " S. ").replace(" E ", " E. ").replace(" W ", " W. ")
    elif u < 0.10:
        t = t.replace(" ", "  ", 1)
    return t


def norm_address(a):
    """The join key both files reduce to: upper case, abbreviations, no punctuation, single spaces."""
    t = " " + a.upper().replace(".", " ").replace(",", " ") + " "
    t = " ".join(t.split())
    t = " " + t + " "
    for full, ab in ABBR.items():
        t = t.replace(" " + full.upper() + " ", " " + ab + " ")
    return " ".join(t.split())


def premise_numbers(n, r, exclude=()):
    """Nine-digit premise numbers from the 2021 billing conversion, and the old district-route-check form."""
    ex = set(exclude)
    new = []
    while len(new) < n:
        v = int(r.integers(400100000, 499900000))
        if v not in ex:
            ex.add(v)
            new.append(v)
    return new


def old_number(dist, r):
    route = int(r.integers(1000, 48000))
    chk = (route * 7 + int(dist) * 3) % 97
    return "%d-%05d-%02d" % (int(dist) + 1, route, chk)


def local(d, minute, second=0):
    """A local (CDT) wall-clock time on summer day d, minute minutes after 15:00."""
    return dt.datetime(d.year, d.month, d.day, 15, 0, 0, tzinfo=P.CDT) + dt.timedelta(minutes=minute, seconds=second)


def fmt_date(d):
    return d.strftime("%Y-%m-%d")
