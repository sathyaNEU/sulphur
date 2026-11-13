"""The exports under target/, as Kraanvogel's systems write them: the billing system (accounts, plan periods,
payments with the profiles each charge covered), the profile service (profiles as they stand), the analytics
warehouse (the live playback roll-up by profile, title and month), the licence server (renewals of downloaded
titles), the catalogue and the publisher code crosswalk, the remuneration engine's monthly statements to the
publishers, and three exports the solution does not read."""
import csv
import datetime as dt
import os

import numpy as np

import params as P

FILES = {
    "acc": "accounts_export_2026-11-03.csv",
    "plan": "plan_periods_2024-01_2026-10.csv",
    "pay": "payments_2024-01_2026-10.csv",
    "prof": "profiles_export_2026-11-03.csv",
    "live": "listening_monthly_2024-01_2026-10.csv",
    "lic": "licence_server_renewals_2024-01_2026-10.csv",
    "cat": "catalogue_2026-10.csv",
    "xw": "publisher_code_crosswalk_2025.csv",
    "stm": "remuneration_statements_2024-01_2026-10.csv",
    "pod": "podcast_plays_2025-01_2026-10.csv",
    "ebk": "ebook_reading_2025-01_2026-10.csv",
    "rev": "app_reviews_2026.csv",
    "riv": "rival_price_scan_2024-01_2026-10.csv",
}

PUBLISHERS = [
    "Uitgeverij Wolkenveld", "De Zilverreiger", "Uitgeverij Klaproos", "Haverkamp & Daal", "Luistergoed",
    "Uitgeverij Ravelijn", "Boekhuis Ter Steeg", "Het Zoete Woord", "Uitgeverij Marlijn", "De Vlasbloem",
    "Stemmenhuis Gent", "Uitgeverij Nachtegaal", "Brinkveld Audio", "Uitgeverij De Lindeboom", "Kwakkel & Zonen",
    "Uitgeverij Steenuil", "Het Lange Oor", "Verhalenfabriek Leuven", "Uitgeverij Duinzicht", "De Kleine Kraai",
    "Uitgeverij Ooievaarsnest", "Ankerhuis", "Uitgeverij Peperbol", "Van Roosmalen Luisterboeken", "De Hoorn",
    "Uitgeverij Waterhoen", "Tolhuis Antwerpen", "Uitgeverij Beukenlaan", "Mosselman & Jonk", "De Stille Uren",
    "Uitgeverij Kardinaal", "Leeuwerik Media", "Uitgeverij Vossenhol", "De Gouden Klok", "Uitgeverij Zeeland Pers",
    "Heidegrond", "Uitgeverij Oranjeboom", "De Schemerlamp", "Uitgeverij Bolwerk", "Molenaar Hoorspel",
]


def _code(i, old=False):
    return ("U%03d" % (101 + i * 7)) if old else ("PUB-%04d" % (2101 + i * 13 + (i * i) % 11))


RENAMED = (3, 8, 11, 17, 22, 26, 30, 33, 37)
MIGRATION_M = 26            # March 2025


def pub_code(i, m):
    if i in RENAMED and m < MIGRATION_M:
        return _code(i, old=True)
    return _code(i)


def _w(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def date_of(m, day):
    return P.month_start(m) + dt.timedelta(days=min(day, P.days_in(m)) - 1)


def write(W, target, rng):
    acc = {a["aid"]: a for a in W["accounts"]}
    counts = {}
    # accounts
    rows = []
    for a in W["accounts"]:
        if a["created"][0] > P.CUT:
            continue
        created = a.get("orig_start") or date_of(*a["created"])
        src = a["source"]
        rows.append([a["aid"], created.isoformat(), a["country"], a["kind"], src, a["trial_days"]])
    counts["acc"] = _w(os.path.join(target, FILES["acc"]),
                       ["account_id", "created_on", "country", "account_type", "signup_source", "trial_days"], rows)
    # plan periods (from January 2024)
    rows = []
    for a in W["accounts"]:
        if a["created"][0] > P.CUT:
            continue
        ev = []
        for (m, plan, phase) in a["plan_hist"]:
            if phase == "trial":
                d = a.get("orig_start") or date_of(*a["created"])
            elif a["trial_days"] and ev and ev[-1][2] == "trial":
                d = date_of(*a["first_charge"])
            else:
                d = date_of(m, a["bill_day"]) if m != a["created"][0] or not a["trial_days"] else date_of(*a["first_charge"])
                if a.get("orig_start") and m == 0 and phase == "paid" and not ev:
                    d = a["orig_start"]
            ev.append((d, plan, phase))
        end = None
        if a["end"] is not None:
            em, why = a["end"]
            if why == "trial_not_converted":
                end = (date_of(*a["first_charge"]) - dt.timedelta(days=1), "trial_ended")
            elif a.get("moved_out") == em:
                end = (date_of(em, 1) - dt.timedelta(days=1), "cancelled")
            else:
                end = (date_of(em, a["bill_day"]) - dt.timedelta(days=1), {"cancelled": "cancelled",
                       "debit_returned": "payment_failed", "refunded": "refund"}[why])
        for j, (d, plan, phase) in enumerate(ev):
            nxt = ev[j + 1][0] - dt.timedelta(days=1) if j + 1 < len(ev) else (end[0] if end else None)
            reason = (end[1] if (end and j + 1 == len(ev)) else ("plan_change" if j + 1 < len(ev) else ""))
            if nxt is not None and nxt < P.month_start(P.REC0):
                continue
            if nxt is not None and nxt > dt.date(2026, 10, 31):
                nxt, reason = None, ""
            if d > dt.date(2026, 10, 31):
                continue
            rows.append([a["aid"], plan, d.isoformat(), nxt.isoformat() if nxt else "", phase, reason])
    counts["plan"] = _w(os.path.join(target, FILES["plan"]),
                        ["account_id", "plan_code", "period_start", "period_end", "phase", "end_reason"], rows)
    # payments
    rows = []
    pid = 5100000
    for c in W["charges"]:
        if not (P.REC0 <= c["m"] <= P.CUT):
            continue
        a = acc[c["aid"]]
        pid += int(rng.integers(1, 40))
        vat = P.VAT[c["country"]]
        if c["route"] == "web":
            proceeds = ""
        else:
            fee = P.STORE_FEE[c["route"]][0 if c["paid_idx"] <= 12 else 1]
            proceeds = "%.2f" % (c["price"] / (1 + vat) * (1 - fee))
        rows.append(["BT%07d" % pid, c["aid"], date_of(c["m"], c["day"]).isoformat(), c["plan"],
                     "%.2f" % c["price"], "%.2f" % vat, c["route"], c["status"], proceeds, ";".join(c["profiles"])])
    counts["pay"] = _w(os.path.join(target, FILES["pay"]),
                       ["payment_id", "account_id", "charged_on", "plan_code", "amount_eur", "vat_rate", "route",
                        "status", "store_proceeds_eur", "profiles_on_subscription"], rows)
    # profiles as they stand
    rows = []
    for pr in W["profiles"]:
        if pr.history[0][0] > P.CUT:
            continue
        a = acc[pr.acc]
        cm = pr.created
        if cm < 0:
            created = (acc[pr.history[0][1]].get("orig_start") or P.month_start(0))
        else:
            created = date_of(cm, int(pr.rng.integers(1, 28)) if False else 1 + (int(pr.pid[1:]) % 27))
        status = "removed" if (pr.removed is not None and pr.removed <= P.CUT) else "active"
        rem = date_of(pr.removed, 1 + (int(pr.pid[1:]) % 25)).isoformat() if status == "removed" else ""
        then = [aid for (hm, aid) in pr.history if hm <= P.CUT][-1]      # the account it stood on at the export
        rows.append([pr.pid, then, created.isoformat(), "adult" if pr.adult else "child", status, rem])
    counts["prof"] = _w(os.path.join(target, FILES["prof"]),
                        ["profile_id", "account_id", "created_on", "profile_type", "status", "removed_on"], rows)
    # the warehouse's live playback roll-up, with the rows a re-sync sends twice
    titles = W["titles"]
    rows = []
    for (m, p, t, secs, pos) in W["live"]:
        if not (P.REC0 <= m <= P.CUT):
            continue
        row = [P.month_label(m), p, "T%06d" % (300000 + t * 3), int(round(secs)), int(round(pos * 3600))]
        rows.append(row)
        if rng.random() < 0.011:
            rows.append(list(row))
    counts["live"] = _w(os.path.join(target, FILES["live"]),
                        ["month", "profile_id", "title_id", "seconds_streamed", "furthest_position_s"], rows)
    # the licence server's renewals
    rows = []
    for (m, d, sec, dev, p, t, pos) in W["licences"]:
        if not (P.REC0 <= m <= P.CUT):
            continue
        ts = dt.datetime.combine(date_of(m, d), dt.time()) + dt.timedelta(seconds=sec)
        rows.append([ts.strftime("%Y-%m-%dT%H:%M:%SZ"), dev, p, "T%06d" % (300000 + t * 3), int(round(pos * 3600)),
                     (ts + dt.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")])
    rows.sort(key=lambda r: r[0])
    counts["lic"] = _w(os.path.join(target, FILES["lic"]),
                       ["renewed_at_utc", "device_id", "profile_id", "title_id", "position_s",
                        "licence_valid_until_utc"], rows)
    # catalogue
    rows = []
    for t in titles:
        if t["pub"] >= 0:
            code, rights = _code(t["pub"]), "licensed"
        elif t["own"]:
            code, rights = "KRV-EIGEN", "own_production"
        else:
            code, rights = "PD", "public_domain"
        isbn = "978908%07d" % (1200000 + t["t"] * 37 % 9999999)
        rows.append(["T%06d" % (300000 + t["t"] * 3), isbn, code, int(round(t["dur"] * 3600)),
                     "children" if t["kids"] else "adult", rights])
    counts["cat"] = _w(os.path.join(target, FILES["cat"]),
                       ["title_id", "isbn", "publisher_code", "duration_s", "audience", "rights"], rows)
    counts["xw"] = _w(os.path.join(target, FILES["xw"]), ["old_code", "new_code", "publisher_name", "effective"],
                      [[_code(i, True), _code(i), PUBLISHERS[i], "2025-03-01"] for i in RENAMED])
    return counts


def net_revenue(c):
    """What the company keeps of a collected charge: VAT out, the store's fee out; returned and refunded charges
    are not revenue."""
    if c["status"] not in ("collected", "re-presented") or c["price"] <= 0:
        return 0.0
    vat = P.VAT[c["country"]]
    fee = P.STORE_FEE[c["route"]][0 if c["paid_idx"] <= 12 else 1]
    return c["price"] / (1 + vat) * (1 - fee)


def write_statements(W, target):
    """The 2024 to 2026 statements: 52 per cent of the month's net subscription revenue, divided among the
    publishers in proportion to the seconds of their titles streamed in the month."""
    titles = W["titles"]
    pool = np.zeros(P.CUT + 1)
    for c in W["charges"]:
        if c["m"] <= P.CUT:
            pool[c["m"]] += net_revenue(c)
    secs = np.zeros((P.CUT + 1, P.N_PUBLISHERS))
    for (m, p, t, s, pos) in W["live"]:
        if m <= P.CUT and titles[t]["pub"] >= 0:
            secs[m, titles[t]["pub"]] += round(s)
    rows = []
    for m in range(P.REC0, P.CUT + 1):
        tot = secs[m].sum()
        for i in range(P.N_PUBLISHERS):
            sh = secs[m, i] / tot
            rows.append([P.month_label(m), pub_code(i, m), PUBLISHERS[i], int(secs[m, i]), "%.6f" % sh,
                         "%.2f" % (P.SHARE26 * pool[m]), "%.2f" % (P.SHARE26 * pool[m] * sh)])
    return _w(os.path.join(target, FILES["stm"]), ["statement_month", "publisher_code", "publisher_name",
                                                    "streamed_seconds", "usage_share", "pool_eur", "amount_eur"], rows)


def write_distractors(W, target, rng):
    """Free podcast plays (own production, outside every agreement), e-book reading (schedule C's flat fee per
    title opened) and the app-store reviews."""
    prof = [p for p in W["profiles"] if p.history[0][0] <= P.CUT]
    rows = []
    shows = ["KRV-POD-%03d" % (11 + 4 * i) for i in range(18)]
    for m in range(24, P.CUT + 1):
        for p in prof[:: 9]:
            if rng.random() < 0.18:
                rows.append([P.month_label(m), p.pid, str(rng.choice(shows)), int(rng.lognormal(7.6, 0.9))])
    n_pod = _w(os.path.join(target, FILES["pod"]), ["month", "profile_id", "show_id", "seconds_played"], rows)
    rows = []
    for m in range(24, P.CUT + 1):
        for p in prof[3:: 7]:
            if rng.random() < 0.12:
                rows.append([P.month_label(m), p.pid, "E%06d" % int(rng.integers(500000, 512000)),
                             int(rng.integers(3, 420)), int(rng.random() < 0.3)])
    n_ebk = _w(os.path.join(target, FILES["ebk"]), ["month", "profile_id", "ebook_id", "pages_turned",
                                                    "finished"], rows)
    phrases = ["Prima app, veel keuze", "Offline luisteren werkt goed in de trein", "Te duur geworden",
               "Kinderboeken top", "Onbeperkt is het waard", "App crasht soms bij downloaden", "Mis titels van mijn favoriete auteur",
               "Fijne stemmen", "Gezinsabonnement handig met de kids", "Uren gaan snel op met Flex",
               "Synchronisatie tussen telefoon en tablet hapert", "Goede app", "Prijsverhoging jammer"]
    rows = []
    d0 = dt.date(2026, 1, 1)
    for i in range(int(rng.integers(1400, 1600))):
        d = d0 + dt.timedelta(days=int(rng.integers(0, 303)))
        rows.append([d.isoformat(), str(rng.choice(["App Store", "Google Play"], p=[0.62, 0.38])),
                     int(rng.choice([1, 2, 3, 4, 5], p=[0.08, 0.06, 0.12, 0.3, 0.44])),
                     str(rng.choice(phrases)) if rng.random() < 0.7 else "", str(rng.choice(["NL", "BE"], p=[0.7, 0.3]))])
    rows.sort(key=lambda r: r[0])
    n_rev = _w(os.path.join(target, FILES["rev"]), ["review_date", "store", "stars", "review_text", "storefront"],
               rows)
    return n_pod, n_ebk, n_rev


def write_rival(target, rng):
    """The pricing team's monthly scan of the rival's comparable plans, by country (VAT included); a summer
    promotion now and then, never in the first quarter."""
    rows = []
    for m in range(P.REC0, P.CUT + 1):
        for c in ("NL", "BE"):
            for pl in P.PLANS:
                base = P.rival_of(c, pl, m)
                promo = (m % 12 in (6, 7)) and rng.random() < 0.35
                price = round(base * 0.85 - 0.01, 2) if promo else base
                rows.append([P.month_label(m), c, P.RIVAL_NAME[pl], "%.2f" % price, "promotion" if promo else ""])
    return _w(os.path.join(target, FILES["riv"]), ["scan_month", "country", "rival_plan", "price_eur", "note"], rows)
