"""The data files of the pack, written from the world (world.history()).

Each of the group's systems writes its own export: the subscription system (subscriptions, price periods, payment
exceptions, customers, payment methods), the analytics platform (reading by login, the login register), the marketing
system (spend and attributed starts by line and month, its channel codes renamed in March 2025, German number
formats), finance (the monthly KPI workbook, docs.py) and the neighbouring departments' files the analysis does not
use. Each carries what that system really does to its records; none of it decides a graded figure."""
import csv
import datetime as dt
import hashlib

import numpy as np

import params as P
import sim

FILES = {
    "subs": "subscriptions_2023-01_2026-10.csv",
    "periods": "price_periods_2023-01_2026-10.csv",
    "exceptions": "payment_exceptions_2023-01_2026-10.csv",
    "customers": "customers.csv",
    "methods": "payment_methods.csv",
    "reading": "reading_by_login_2024-01_2026-10.csv",
    "logins": "logins.csv",
    "spend": "marketing_spend_2023-01_2026-10.csv",
    "offers": "offer_catalogue.csv",
    "codes": "marketing_channel_codes.csv",
    "plan": "media_plan_2027.xlsx",
    "standard": "digital_subscription_kpi_standard.pdf",
    "prices": "price_list_digital_2027.pdf",
    "kpi": "kpi_digital_2026.xlsx",
    "print": "print_circulation_2023-2026.csv",
    "newsletter": "newsletter_signups_2025-2026.csv",
    "survey": "reader_survey_2026.csv",
    "ads": "digital_ad_revenue_2025-2026.csv",
}
DISTRACTORS = ["print", "newsletter", "survey", "ads"]

STREETS = ["Hauptstraße", "Bahnhofstraße", "Lindenweg", "Kirchstraße", "Schulstraße", "Gartenstraße", "Dorfstraße",
           "Bergstraße", "Mühlenweg", "Birkenweg", "Am Deich", "Hafenstraße", "Marktplatz", "Wiesenweg", "Ringstraße",
           "Lange Straße", "Feldstraße", "Rosenstraße", "Eichenweg", "Weserblick", "Am Markt", "Kiefernweg",
           "Friedhofstraße", "Moorweg", "Ahornweg", "Poststraße", "Brunnenstraße", "Heideweg", "Schillerstraße",
           "Goethestraße", "Am Hafen", "Fischerstraße", "Kanalstraße", "Uferstraße", "Schützenstraße", "Waldweg",
           "Deichstraße", "Kastanienallee", "Im Winkel", "Lüttje Straße", "Bremer Straße", "Hamburger Straße",
           "Querweg", "Sandweg", "Neue Straße", "Kreuzstraße", "Grüner Weg", "Sielstraße", "Kampweg", "Holzweg",
           "Amselweg", "Drosselgang", "Finkenstraße", "Meisenweg", "Lerchenstraße", "Starenweg", "Buchenweg",
           "Erlenstraße", "Tannenweg", "Weidenstraße", "Pappelallee", "Ulmenweg", "Lessingstraße", "Mozartstraße",
           "Beethovenstraße", "Bachstraße", "Händelweg", "Am Sportplatz", "Am Bahnhof", "An der Kirche",
           "Zum Hafen", "Kapitän-Haase-Straße", "Werftstraße", "Ankerweg", "Lotsenstraße", "Fährstraße",
           "Am Wall", "Burgstraße", "Torstraße", "Mittelstraße", "Oststraße", "Weststraße", "Nordstraße",
           "Südstraße", "Industriestraße", "Gewerbering", "Schmiedestraße", "Bäckerstraße", "Gerberstraße",
           "Wassermühle", "Am Mühlenteich", "Heidkamp", "Brookweg", "Fleetstraße", "Marschweg", "Geestweg"]
TOWNS = {"BHR": [("Brückenhafen", 27561, 27583), ("Wremsiel", 27585, 27590)],
         "GAZ": [("Grevenau", 27612, 27624), ("Hollwede", 27627, 27632), ("Lunkhusen", 27633, 27638)],
         "KBO": [("Ostheide", 29640, 29652), ("Rehmsloh", 29654, 29661), ("Kirchdorf an der Aue", 29662, 29668)],
         "ELN": [("Elmsbach", 27711, 27716), ("Ottersande", 27717, 27721)]}
ROUTE_WORD = {"SEPA": "SEPA", "PAYPAL": "PAYPAL", "CARD": "CARD", "APPLE": "APPLE", "GOOGLE": "GOOGLE"}


def add_months(d, k):
    y = d.year + (d.month - 1 + k) // 12
    mo = (d.month - 1 + k) % 12 + 1
    last = (dt.date(y + (mo == 12), mo % 12 + 1, 1) - dt.timedelta(days=1)).day
    return dt.date(y, mo, min(d.day, last))


def hexid(*parts, n=16):
    return hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:n]


def euro_de(x):
    s = f"{x:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def write_csv(path, header, rows, delimiter=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delimiter, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def iso(d):
    return "" if d is None else d.isoformat()


class Pack:
    """Every record the exports are cut from, with dates, identifiers, accounts, addresses and logins."""

    def __init__(self, S, seed):
        self.S = S
        self.rng = np.random.default_rng(seed)
        n = len(S["start"])
        self.n = n
        rng = self.rng
        self.day = rng.integers(1, 29, size=n)
        # subscription ids: drawn, never a sequence
        ids = rng.choice(np.arange(1000000, 9999999), size=n + 3000, replace=False)
        self.sid = ["DA%07d" % x for x in ids[:n]]
        self.spare_ids = ["DA%07d" % x for x in ids[n:]]
        self.start_date = []
        for i in range(n):
            if S["kind"][i] == "base":
                sd = add_months(dt.date(2023, 1, int(self.day[i])), -int(S["tenure0"][i]))
            else:
                y, mo = sim.ym(int(S["start"][i]))
                sd = dt.date(y, mo, int(self.day[i]))
            self.start_date.append(sd)
        self.households()

    def bill(self, i, m):
        """The billing date of subscription i in month m."""
        y, mo = sim.ym(m)
        return dt.date(y, mo, int(self.day[i]))

    def households(self):
        S, rng = self.S, self.rng
        n = self.n
        # an address per address id, a variant spelling now and then on a new account
        self.addr = {}
        self.cust_addr = {}
        self.cust_title = {}
        self.cust_created = {}
        self.email = {}
        for i in range(n):
            c = int(S["customer"][i])
            if c in self.cust_addr:
                continue
            a = int(S["address"][i])
            t = P.TITLES[int(S["title"][i])]
            if a not in self.addr:
                town, lo, hi = TOWNS[t][int(rng.integers(0, len(TOWNS[t])))]
                street = STREETS[int(rng.integers(0, len(STREETS)))]
                no = str(int(rng.integers(1, 260)))
                if rng.random() < 0.08:
                    no += "abc"[int(rng.integers(0, 3))]
                self.addr[a] = (street, no, str(int(rng.integers(lo, hi + 1))), town)
            street, no, pc, town = self.addr[a]
            if S["parent"][i] >= 0 and S["newacc"][i] and rng.random() < 0.5:
                street = variant(street, rng)
            self.cust_addr[c] = (street, no, pc, town)
            self.cust_title[c] = t
            self.cust_created[c] = self.start_date[i]
            self.email[c] = hexid("mail", c, int(rng.integers(0, 10 ** 6)), n=40)

    # ---------------------------------------------------------------- the subscription system
    def subscriptions(self):
        S = self.S
        rows = []
        self.end_date = []
        for i in range(self.n):
            sd = self.start_date[i]
            L = int(S["L"][i])
            e = int(S["end"][i])
            kind = S["kind"][i]
            ch = P.CHANNELS[int(S["channel"][i])]
            if kind == "base":
                code = ""
            else:
                m0 = int(S["start"][i])
                code = P.OLD_CODE[ch] if m0 < P.CODE_SWITCH else ch
            offer = sim.OFFER_CODES[int(S["offer"][i])] if S["offer"][i] >= 0 else ""
            intro_end = add_months(sd, L) - dt.timedelta(days=1) if L > 0 else None
            reason = S["reason"][i]
            if e == -1:
                ed = sd + dt.timedelta(days=int(self.rng.integers(2, 14)))
                req = ed
            elif e == -2:
                ed, req = None, None
            else:
                base_shift = int(S["tenure0"][i]) if kind == "base" else 0
                k_end = e - int(S["start"][i]) + 1 + base_shift
                ed = add_months(sd, k_end) - dt.timedelta(days=1)
                if reason == "PAYMENT_FAILED":
                    req = None
                elif S["rise_exit"][i] == P.RISE_2025 - 1:
                    req = dt.date(2025, 2, 1) + dt.timedelta(days=int(self.rng.integers(9, 46)))
                elif S["su_exit"][i]:
                    req = max(sd, ed - dt.timedelta(days=int(self.rng.integers(1, max(3, 30 * L)))))
                else:
                    req = max(sd, ed - dt.timedelta(days=int(self.rng.integers(3, 40))))
            if req is not None:
                req = min(req, dt.date(2026, 11, 2))
            self.end_date.append(ed)
            rows.append([self.sid[i], int(S["customer"][i]), P.TITLES[int(S["title"][i])], "DIGITAL", code, offer,
                         iso(sd), iso(intro_end), iso(req), iso(ed), reason if e != -2 else "",
                         ROUTE_WORD[sim.ROUTES[int(S["route"][i])]], 1])
        rows += self.texture_subscriptions()
        # the nightly export was re-run on some days and appended
        k = int(round(P.DUP_SHARE * len(rows)))
        dup = self.rng.choice(len(rows), size=k, replace=False)
        rows = rows + [list(rows[j]) for j in sorted(dup)]
        order = self.rng.permutation(len(rows))
        rows = [rows[j] for j in order]
        rows.sort(key=lambda r: (r[6], r[0]))
        return rows

    def texture_subscriptions(self):
        """Staff access, gift subscriptions, company licences and the IT department's test accounts: real rows of the
        same export that are not consumer subscriptions."""
        rng = self.rng
        rows = []
        self.texture_periods = []
        self.texture_customers = []
        nxt = iter(self.spare_ids)
        cno = iter(rng.permutation(rng.choice(np.arange(900000, 989999), size=2200, replace=False)))
        for k in range(P.STAFF):
            t = P.TITLES[int(rng.choice(4, p=[0.45, 0.22, 0.2, 0.13]))]
            sd = dt.date(2015, 1, 1) + dt.timedelta(days=int(rng.integers(0, 4300)))
            ed = None if rng.random() < 0.85 else min(sd + dt.timedelta(days=int(rng.integers(200, 1500))),
                                                       dt.date(2026, 10, 20))
            sid, c = next(nxt), int(next(cno))
            rows.append([sid, c, t, "DIGITAL_STAFF", "", "", iso(sd), "", "", iso(ed), "STAFF_END" if ed else "",
                         "NONE", 1])
            self.texture_periods.append([sid, iso(max(sd, dt.date(2023, 1, 1))), iso(ed), "0.00", "STAFF"])
            self.texture_customers.append((c, sd, "STAFF", t))
        for m in range(0, P.CUT + 1):
            y, mo = sim.ym(m)
            for g in range(int(rng.poisson(P.GIFTS_A_MONTH * (1.8 if mo == 12 else 1.0)))):
                t = P.TITLES[int(rng.choice(4, p=[0.42, 0.24, 0.21, 0.13]))]
                months = int(rng.choice([3, 6, 12], p=[0.5, 0.3, 0.2]))
                sd = dt.date(y, mo, int(rng.integers(1, 29)))
                ed = add_months(sd, months) - dt.timedelta(days=1)
                done = ed <= dt.date(2026, 10, 31)
                sid, c = next(nxt), int(next(cno))
                price = {3: 39.0, 6: 74.0, 12: 139.0}[months]
                rows.append([sid, c, t, "DIGITAL_GIFT", "", "", iso(sd), "", "", iso(ed) if done else "",
                             "GIFT_END" if done else "", "CARD" if rng.random() < 0.6 else "PAYPAL", 1])
                self.texture_periods.append([sid, iso(sd), iso(ed), "%.2f" % (price / months), "GIFT"])
                self.texture_customers.append((c, sd, "CONSUMER", t))
        for k in range(P.GROUPS):
            t = P.TITLES[int(rng.choice(4, p=[0.5, 0.2, 0.2, 0.1]))]
            seats = int(rng.choice([5, 8, 10, 12, 15, 20, 25, 30, 40, 60, 80]))
            sd = dt.date(2019, 1, 1) + dt.timedelta(days=int(rng.integers(0, 2700)))
            sid, c = next(nxt), int(next(cno))
            rows.append([sid, c, t, "DIGITAL_GROUP", "", "", iso(sd), "", "", "", "", "SEPA", seats])
            self.texture_periods.append([sid, iso(max(sd, dt.date(2023, 1, 1))), "", "%.2f" % (seats * 9.90),
                                         "GROUP"])
            self.texture_customers.append((c, sd, "BUSINESS", t))
        for k in range(P.TESTS):
            t = P.TITLES[int(rng.integers(0, 4))]
            sd = dt.date(2023, 1, 9) + dt.timedelta(days=int(rng.integers(0, 1380)))
            ed = None if rng.random() < 0.4 else min(sd + dt.timedelta(days=int(rng.integers(1, 60))),
                                                      dt.date(2026, 10, 30))
            sid, c = next(nxt), int(next(cno))
            off = str(rng.choice(["PM1", "M3E1", "H6"]))
            rows.append([sid, c, t, "DIGITAL", "DIR" if sd >= dt.date(2025, 3, 1) else "ORG", off, iso(sd), "",
                         iso(ed), iso(ed), "CANCELLED" if ed else "", "CARD", 1])
            self.texture_periods.append([sid, iso(sd), iso(ed), "0.99" if off == "PM1" else "1.00", "INTRO"])
            self.texture_customers.append((c, sd, "TEST", t))
        return rows

    def price_periods(self):
        """Contiguous runs of one gross monthly price per subscription, as the billing system stores them."""
        S = self.S
        g = S["gross"]
        rows = []
        for i in range(self.n):
            e = int(S["end"][i])
            if e == -1:
                rows.append([self.sid[i], iso(self.start_date[i]), iso(self.end_date[i]),
                             "%.2f" % S["ip"][i], "INTRO"])
                continue
            st = int(S["start"][i])
            last = P.CUT if e == -2 else e
            L = int(S["L"][i])
            cur, frm, typ = None, None, None
            for m in range(st, last + 1):
                k = m - st
                v = round(float(g[i, m]), 2)
                kind = "INTRO" if k < L else "FULL"
                if cur is None or v != cur or kind != typ:
                    if cur is not None:
                        rows.append([self.sid[i], iso(frm), iso(self.bill(i, m) - dt.timedelta(days=1)),
                                     "%.2f" % cur, typ])
                    cur, frm, typ = v, self.bill(i, m), kind
            if cur is not None:
                rows.append([self.sid[i], iso(frm), "" if e == -2 else iso(self.end_date[i]), "%.2f" % cur, typ])
        rows += self.texture_periods
        rows.sort(key=lambda r: (r[0], r[1]))
        return rows

    def exceptions(self):
        """Debits returned and collected again, debits that ended a subscription, refunds of withdrawals."""
        S, rng = self.S, self.rng
        rows = []
        word = {"SEPA": "RETURN_DEBIT", "PAYPAL": "PAYMENT_DECLINED", "CARD": "CARD_DECLINED",
                "APPLE": "STORE_BILLING_RETRY", "GOOGLE": "STORE_BILLING_RETRY"}
        for i, m in S["recovered"]:
            r = sim.ROUTES[int(S["route"][i])]
            b = self.bill(i, m)
            amt = S["gross"][i, m]
            rows.append([self.sid[i], iso(b + dt.timedelta(days=int(rng.integers(2, 6)))), word[r], "%.2f" % amt])
            rows.append([self.sid[i], iso(b + dt.timedelta(days=int(rng.integers(8, 16)))), "COLLECTED", "%.2f" % amt])
        for i in range(self.n):
            if S["reason"][i] == "PAYMENT_FAILED" and S["end"][i] >= 0:
                r = sim.ROUTES[int(S["route"][i])]
                b = self.end_date[i] + dt.timedelta(days=1)
                price = sim.full_price(np.array([S["title"][i]]), np.array([S["end"][i] + 1]))[0]
                rows.append([self.sid[i], iso(b + dt.timedelta(days=int(rng.integers(2, 6)))), word[r],
                             "%.2f" % price])
                rows.append([self.sid[i], iso(b + dt.timedelta(days=int(rng.integers(20, 30)))), "WRITTEN_OFF",
                             "%.2f" % price])
            if S["end"][i] == -1:
                rows.append([self.sid[i], iso(self.end_date[i] + dt.timedelta(days=int(rng.integers(1, 5)))),
                             "REFUND_WITHDRAWAL", "%.2f" % S["ip"][i]])
        # the export holds what the billing system had booked when it ran (3 November 2026, early morning)
        rows = [r for r in rows if r[1] <= "2026-11-02"]
        rows.sort(key=lambda r: (r[1], r[0]))
        return rows

    def customers(self):
        rows = []
        for c, (street, no, pc, town) in self.cust_addr.items():
            rows.append([c, iso(self.cust_created[c]), "CONSUMER", self.email[c], street, no, pc, town])
        for c, sd, typ, t in self.texture_customers:
            town, lo, hi = TOWNS[t][0]
            rows.append([c, iso(sd), typ, hexid("mail", c, typ, n=40),
                         "Am Pressehaus" if typ in ("STAFF", "TEST") else STREETS[int(self.rng.integers(0, 50))],
                         str(int(self.rng.integers(1, 40))), str(int(self.rng.integers(lo, hi + 1))), town])
        rows.sort(key=lambda r: r[0])
        return rows

    def payment_methods(self):
        """One row per customer and payment method, with the payment fingerprint the payment service provider
        returns (a hash of the IBAN, the card or the PayPal payer; the store's account token)."""
        S = self.S
        seen = {}
        for i in range(self.n):
            c = int(S["customer"][i])
            r = sim.ROUTES[int(S["route"][i])]
            key = (c, r)
            fp = hexid("fp", int(S["fingerprint"][i]), r, n=20)
            sd = self.start_date[i] if S["kind"][i] != "base" else dt.date(2023, 1, 1)
            ed = self.end_date[i] if self.end_date[i] is not None else dt.date(2026, 10, 31)
            ed = min(ed, dt.date(2026, 10, 31))
            if key not in seen:
                seen[key] = [c, r, fp, sd, ed]
            else:
                seen[key][3] = min(seen[key][3], sd)
                seen[key][4] = max(seen[key][4], ed)
        rows = [[c, r, fp, iso(a), iso(b)] for (c, r, fp, a, b) in seen.values()]
        rows.sort(key=lambda x: (x[0], x[1]))
        return rows

    # ---------------------------------------------------------------- the analytics platform
    def logins(self):
        """Each customer's web login, and for some a second login (the app's or an older one) that carries part of
        their reading."""
        rng = self.rng
        self.login_of = {}
        rows = []
        ids = rng.choice(np.arange(10 ** 7, 10 ** 8), size=2 * len(self.cust_addr) + 10, replace=False)
        it = iter(ids)
        for c in sorted(self.cust_addr):
            a = "u%d" % next(it)
            self.login_of[c] = [a]
            rows.append([a, c, iso(self.cust_created[c]), "WEB"])
            if rng.random() < P.SECOND_LOGIN:
                b = "u%d" % next(it)
                self.login_of[c].append(b)
                d0 = self.cust_created[c]
                x = int(rng.integers(0, 200))
                month_end = (dt.date(d0.year + d0.month // 12, d0.month % 12 + 1, 1) - dt.timedelta(days=1))
                rows.append([b, c, iso(min(d0 + dt.timedelta(days=x % 5), month_end, dt.date(2026, 11, 1))), "APP"])
        rows.sort(key=lambda r: r[0])
        return rows

    def reading(self):
        S, rng = self.S, self.rng
        R = S["reading"]
        rows = []
        for i in range(self.n):
            c = int(S["customer"][i])
            logs = self.login_of[c]
            for m in np.nonzero(R[i])[0]:
                d = int(R[i, m])
                y, mo = sim.ym(int(m))
                ms = "%04d-%02d" % (y, mo)
                if len(logs) == 2:
                    d2 = int(rng.binomial(d, 0.3))
                    parts = [(logs[0], d - d2), (logs[1], d2)]
                else:
                    parts = [(logs[0], d)]
                for lg, dd in parts:
                    if dd <= 0:
                        continue
                    art = int(rng.poisson(P.ARTICLES_PER_DAY * dd * np.exp(0.15 * S["h"][i])))
                    app = int(rng.binomial(dd, 0.35 if lg != logs[0] else 0.12))
                    rows.append([lg, ms, dd, max(art, dd), app])
        rows.sort(key=lambda r: (r[1], r[0]))
        return rows

    # ---------------------------------------------------------------- the marketing system
    def spend(self):
        """Spend and the ad platforms' attributed starts by line and month, as the marketing tool exports them."""
        S, rng = self.S, self.rng
        rows = []
        new = S["kind"] != "base"
        for m in range(0, P.CUT + 1):
            y, mo = sim.ym(m)
            for (c, t) in P.LINES:
                sel = new & (S["start"] == m) & (S["channel"] == sim.C_IDX[c]) & (S["title"] == sim.T_IDX[t])
                gross_starts = int(sel.sum())
                season = {11: 1.10, 12: 1.08, 7: 0.95, 8: 0.95}.get(mo, 1.0)
                trend = 0.93 + 0.07 * m / P.CUT
                cost = gross_starts * P.CPA[(c, t)] * season * trend * float(np.exp(rng.normal(0, 0.06)))
                attr = max(0, int(round(gross_starts * float(np.exp(rng.normal(0.02, 0.07))))))
                clicks = int(rng.poisson(max(gross_starts, 1) * {"SOC": 55, "SEA": 38, "PART": 24, "TEL": 0,
                                                                  "APP": 41}[c]))
                code = P.OLD_CODE[c] if m < P.CODE_SWITCH else c
                rows.append(["%02d.%04d" % (mo, y), code, P.TITLE_NAME[t], euro_de(cost), attr,
                             "" if c == "TEL" else clicks])
        return rows

    def offers(self):
        rows = []
        first = {"PM1": "2019-03-01", "M3E1": "2021-09-01", "H6": "2020-06-01", "G3": "2022-02-01",
                 "J12": "2023-02-01"}
        for code, spec in P.OFFERS.items():
            rule = ("fixed %.2f" % spec["fixed"]) if "fixed" in spec else ("%.0f%% of list" % (100 * spec["share"]))
            rows.append([code, spec["name"], spec["months"], rule, first[code]])
        rows.append(["HB3", "3 Monate halber Preis", 3, "50% of list", "2018-11-01"])
        return rows


def variant(street, rng):
    """The same street typed another way on a new account."""
    s = street
    if s.endswith("straße") and rng.random() < 0.7:
        return s[:-6] + ("str." if rng.random() < 0.6 else "strasse")
    if s.endswith("weg") and rng.random() < 0.5:
        return s.lower()
    return s.upper() if rng.random() < 0.2 else s + " "


def write_all(S, target, seed=P.SEED + 101):
    import os
    pk = Pack(S, seed)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    n = {}
    n["subs"] = write_csv(F["subs"], ["subscription_id", "customer_no", "title", "product", "channel", "offer_code",
                                      "start_date", "intro_end_date", "cancel_received", "end_date", "end_reason",
                                      "payment_route", "seats"], pk.subscriptions())
    n["periods"] = write_csv(F["periods"], ["subscription_id", "valid_from", "valid_to", "monthly_price_eur",
                                            "period_type"], pk.price_periods())
    n["exceptions"] = write_csv(F["exceptions"], ["subscription_id", "event_date", "event", "amount_eur"],
                                pk.exceptions())
    n["customers"] = write_csv(F["customers"], ["customer_no", "created", "account_type", "email_sha1", "street",
                                                "house_no", "postcode", "town"], pk.customers())
    n["methods"] = write_csv(F["methods"], ["customer_no", "method", "fingerprint", "first_used", "last_used"],
                             pk.payment_methods())
    n["logins"] = write_csv(F["logins"], ["login_id", "customer_no", "created", "type"], pk.logins())
    n["reading"] = write_csv(F["reading"], ["login_id", "month", "reading_days", "articles", "app_days"],
                             pk.reading())
    n["spend"] = write_csv(F["spend"], ["Monat", "Kanal", "Titel", "Kosten_EUR", "Starts_attribuiert", "Klicks"],
                           pk.spend(), delimiter=";")
    n["offers"] = write_csv(F["offers"], ["offer_code", "offer_name", "intro_months", "intro_price_rule",
                                          "in_use_since"], pk.offers())
    codes = []
    for c in P.CHANNELS:
        codes.append([P.OLD_CODE[c], "2019-01-01", "2025-02-28", c])
        codes.append([c, "2025-03-01", "", ""])
    codes.sort(key=lambda r: (r[1], r[0]))
    n["codes"] = write_csv(F["codes"], ["channel_code", "valid_from", "valid_to", "replaced_by"], codes)
    import distractors
    n.update(distractors.write(S, F, pk.rng))
    return pk, n
