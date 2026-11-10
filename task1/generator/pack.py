"""Write the data files of the pack from the world's records, with the mess Tekenbord's systems produce: the billing
system's contract lines (nightly re-exports, credit notes and re-issues, onboarding fees), the Team plan's invoices
(card payments that failed and were re-issued), the product's workspace activity and its dated workspace links, the
CRM's account export (parent groups, lead source, names typed several ways), the sales pipeline's month-end snapshots
(re-run exports, amounts typed per month by some owners) and its closed opportunities, the 2026 price book, the
finance team's monthly KPI export, and two files the forecast never reads (support tickets and the third quarter's
NPS responses)."""
import calendar
import csv
import datetime as dt
import math
import os

import numpy as np
from faker import Faker
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import analysis as An
import params as P
import sim
import tables

FILES = {
    "lines": "billing_contract_lines_2022-01_2026-10.csv",
    "team": "team_invoices_2022-01_2026-10.csv",
    "activity": "workspace_monthly_activity_2022-01_2026-10.csv",
    "links": "workspace_account_links.csv",
    "crm": "crm_accounts_export_2026-11-02.xlsx",
    "snap": "pipeline_snapshots_2023-01_2026-10.csv",
    "closed": "opportunities_closed_2022-01_2026-10.csv",
    "price": "price_book_2026.xlsx",
    "policy": "arr_reporting_policy_2026.pdf",
    "kpi": "kpi_monthly_2026-01_2026-09.xlsx",
    "tickets": "support_tickets_2026.csv",
    "nps": "nps_responses_2026-q3.csv",
}
DISTRACTORS = ["tickets", "nps"]
STAGES = P.STAGES
OWNERS = ["Stijn Totwiller", "Isis Kloppert", "Cornelis Adriaansen", "Indy Smits", "Lois Jansen", "Noud Geertsen",
          "Duncan Reed", "Sandra Garner", "Reimund Budig", "Erika Buchholz"]
MONTHLY_TYPERS = {"Duncan Reed", "Erika Buchholz"}
AGENTS = ["Siem Cammel", "Jinthe Kwaadland", "Bente Verbruggen", "Senna Lutterveld"]
INDUSTRIES = ["Architecture", "Engineering services", "Software", "Higher education", "Management consulting",
              "Construction", "Marketing and media", "Logistics", "Public sector", "Industrial design",
              "Financial services", "Healthcare"]


def ymd(m, day):
    y, mo = sim.ym(m)
    return dt.date(y, mo, min(day, calendar.monthrange(y, mo)[1]))


def month_end(m):
    y, mo = sim.ym(m)
    return dt.date(y, mo, calendar.monthrange(y, mo)[1])


def rng_for(*keys):
    return np.random.default_rng([P.SEED] + [int(k) for k in keys])


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)
    return len(rows)


def money(x):
    return "%.2f" % x


def bid(a):
    return "BA-%06d" % a


def tid(t):
    return "TA-%07d" % t


def wid(w):
    import hashlib
    return "WS-" + hashlib.sha1(("tekenbord-ws-%d" % w).encode()).hexdigest()[:8].upper()


def oid(o):
    return "OPP-%07d" % o


def gid(p):
    return "GRP-%05d" % ((p * 37 + 1201) % 99991)


# ------------------------------------------------------------------------------------------------ names
class Names:
    """Company names from Faker's Dutch, German and British locales; parent groups typed several ways in the CRM."""

    def __init__(self, w):
        self.f = {"nl": Faker("nl_NL"), "de": Faker("de_DE"), "gb": Faker("en_GB")}
        for i, k in enumerate(sorted(self.f)):
            self.f[k].seed_instance(P.SEED + 50 + i)
        self.used = set()
        self.acc, self.country, self.parent_name = {}, {}, {}
        par = {p["id"]: p for p in w.parents}
        r = np.random.default_rng(P.SEED + 60)
        for p in w.parents:
            if p["group"]:
                loc = "gb" if r.random() < 0.18 else ("de" if r.random() < 0.4 else "nl")
                self.parent_name[p["id"]] = (self.company(loc, group=True), loc)
        for a in sorted(w.bus, key=lambda x: x["id"]):
            p = par[a["parent"]]
            if a["cur"] == "GBP":
                loc = "gb"
            elif p["group"]:
                loc = self.parent_name[p["id"]][1] if self.parent_name[p["id"]][1] != "gb" else \
                    ("nl" if r.random() < 0.6 else "de")
            else:
                loc = "de" if r.random() < 0.38 else "nl"
            if p["group"]:
                base = self.parent_name[p["id"]][0].split(" ")[0]
                self.acc[a["id"]] = self.subsidiary(base, loc, r)
            else:
                self.acc[a["id"]] = self.company(loc)
            self.country[a["id"]] = {"gb": "United Kingdom", "de": "Germany", "nl": "Netherlands"}[loc]
            if loc == "de" and r.random() < 0.12:
                self.country[a["id"]] = "Austria" if r.random() < 0.5 else "Switzerland"
            if loc == "nl" and r.random() < 0.10:
                self.country[a["id"]] = "Belgium"

    def company(self, loc, group=False):
        for _ in range(200):
            n = self.f[loc].company()
            if group:
                stem = n.split(" ")[0].strip(",")
                n = {"nl": "%s Groep" % stem, "de": "%s Gruppe" % stem, "gb": "%s Group plc" % stem}[loc]
            if n not in self.used:
                self.used.add(n)
                return n
        raise RuntimeError("names exhausted")

    def subsidiary(self, base, loc, r):
        tails = {"nl": ["Nederland B.V.", "Ingenieurs B.V.", "Advies B.V.", "Bouw B.V.", "Projecten B.V.",
                        "Infra B.V.", "Vastgoed B.V.", "Digital B.V."],
                 "de": ["Deutschland GmbH", "Engineering GmbH", "Planung GmbH", "Consulting GmbH", "Bau GmbH",
                        "Services GmbH", "Digital GmbH"],
                 "gb": ["UK Ltd", "Engineering Ltd", "Consulting Ltd", "Projects Ltd", "Digital Ltd"]}[loc]
        for _ in range(60):
            n = "%s %s" % (base, tails[int(r.integers(0, len(tails)))])
            if n not in self.used:
                self.used.add(n)
                return n
        return self.company(loc)

    def parent_spelling(self, pid, r):
        n = self.parent_name[pid][0]
        x = r.random()
        if x < 0.70:
            return n
        if x < 0.80:
            return n.upper()
        if x < 0.90:
            return n.replace(" Groep", " Groep B.V.").replace(" Gruppe", " Gruppe GmbH").replace(" Group plc",
                                                                                                    " Group")
        return n.replace(" Groep", " groep").replace(" Gruppe", "-Gruppe").replace(" plc", " PLC")

    def prospect(self, o):
        r = rng_for(7, o["id"])
        loc = "gb" if o["cur"] == "GBP" else ("de" if r.random() < 0.38 else "nl")
        return self.company(loc)


# ------------------------------------------------------------------------------------------------ contract lines
def write_lines(w, path, names):
    """One row per billing line as the billing system exports it each night. Subscription lines are invoiced on their
    service start; a true-up's charge runs to the end of the term; onboarding fees are one-off. About one renewal
    line in twenty-five from 2024 went out at list price without the contract's agreed price, was credited and
    re-issued; the nightly job re-exported part of a day's lines a second time on some nights."""
    r = np.random.default_rng(P.SEED + 70)
    L = sorted(w.log["lines"], key=lambda x: (x["m"], x["day"], x["acc"], x["type"]))
    out = []
    lid = 1400000
    inv = 0
    for x in L:
        a = x["acc"]
        cur = x["cur"]
        m = x["m"]
        if x["type"] == "true_up":
            rr = rng_for(11, a, m + 100)
            start = ymd(m, int(rr.integers(1, 29)))
            # the term the true-up joins ends on the day before the contract's next anniversary
            anniv = ymd(m + x["months"], x["day"])
            end = anniv - dt.timedelta(days=1)
            kind = "Seat true-up"
            qty = x["seats"]
            amount = qty * x["price"] * x["months"]
        elif x["type"] == "onboarding_fee":
            start = ymd(m, x["day"])
            end = start
            kind = "Onboarding fee"
            qty = 1
            amount = x["price"]
        else:
            start = ymd(m, x["day"])
            end = ymd(m + 12, x["day"]) - dt.timedelta(days=1)
            kind = "Subscription - new" if x["type"] == "new" else "Subscription - renewal"
            qty = x["seats"]
            amount = qty * x["price"] * 12
        lid += int(r.integers(1, 6))
        inv += int(r.integers(1, 5))
        invno = "INV-%d-%05d" % (start.year if start.year >= 2022 else 2021, 1000 + inv % 90000)
        row = [lid, invno, bid(a), names.acc[a], kind, start.isoformat(), end.isoformat(),
               qty, money(x["price"]) if kind != "Onboarding fee" else money(x["price"]), cur, money(amount), ""]
        if x["type"] == "renewal" and 24 <= m < P.PRICE_RISE and not x.get("opening") and r.random() < 0.035:
            lst = (P.BUS_LIST_NEW if m >= P.PRICE_RISE else P.BUS_LIST_OLD)[cur]
            if abs(lst - x["price"]) > 0.05:
                wrong = list(row)
                wrong[8] = money(lst)
                wrong[10] = money(qty * lst * 12)
                out.append(wrong)
                lid += int(r.integers(1, 6))
                cn = [lid, "CN-%d-%04d" % (start.year, 100 + inv % 9000), bid(a), names.acc[a], "Credit note",
                      start.isoformat(), end.isoformat(), -qty, money(lst), cur, money(-qty * lst * 12), wrong[0]]
                out.append(cn)
                lid += int(r.integers(1, 6))
                row[0] = lid
                row[1] = "INV-%d-%05d" % (start.year, 1000 + (inv + 45000) % 90000)
        out.append(row)
    # the nightly job's re-exports: a run of consecutive lines written twice
    final = []
    i = 0
    while i < len(out):
        final.append(out[i])
        if r.random() < 0.006:
            k = int(r.integers(2, 9))
            block = out[i + 1:i + 1 + k]
            final.extend(block)
            final.extend(block)
            i += 1 + k
            continue
        i += 1
    n = write_csv(path, ["line_id", "document_no", "billing_account", "customer_name", "line_type", "service_start",
                         "service_end", "quantity", "unit_price", "currency", "line_amount", "credits_line_id"], final)
    return n


# ------------------------------------------------------------------------------------------------ team invoices
def write_team(w, path):
    """The Team plan bills each account monthly in advance on its billing day. A card payment that fails is retried
    under a new invoice a few days later; the failed invoice stays in the export."""
    r = np.random.default_rng(P.SEED + 71)
    rows = []
    n = 3100000
    for x in sorted(w.log["team_inv"], key=lambda z: (z["m"], z["day"], z["acc"])):
        m = x["m"]
        start = ymd(m, x["day"])
        end = ymd(m + 1, x["day"]) - dt.timedelta(days=1)
        price = P.TEAM_PRICE[x["cur"]]
        n += int(r.integers(1, 4))
        base = [tid(x["acc"]), start.isoformat(), end.isoformat(), x["members"], x["seats"], money(price),
                x["cur"], money(price * x["seats"])]
        if r.random() < 0.027:
            rows.append(["T%d" % n, start.isoformat()] + base + ["payment_failed"])
            n += int(r.integers(1, 4))
            retry = min(start + dt.timedelta(days=int(r.integers(3, 8))), dt.date(2026, 11, 2))
            rows.append(["T%d" % n, retry.isoformat()] + base + ["paid"])
        else:
            rows.append(["T%d" % n, start.isoformat()] + base + ["paid"])
    return write_csv(path, ["invoice_no", "invoice_date", "team_account", "period_start", "period_end",
                            "active_members", "seats_billed", "price_per_seat", "currency", "amount", "status"], rows)


# ------------------------------------------------------------------------------------------------ product data
def write_activity(w, path):
    r = np.random.default_rng(P.SEED + 72)
    rows = []
    for x in sorted(w.log["ws"], key=lambda z: (z["m"], z["ws"])):
        y, mo = sim.ym(x["m"])
        boards = int(r.poisson(max(x["active"], 0) * 5.4)) if x["active"] else 0
        rows.append([wid(x["ws"]), "%04d-%02d" % (y, mo), x["active"], boards])
    return write_csv(path, ["workspace_id", "month", "active_users", "boards_edited"], rows)


def write_links(w, path):
    rows = []
    bus = {a["id"]: a for a in w.bus}
    team = {t["id"]: t for t in w.team}
    for x in sorted(w.log["ws_map"], key=lambda z: (z["ws"], z["from"])):
        o = x["owner"]
        if o in bus:
            acc, plan, day = bid(o), "Business", bus[o]["day"]
        else:
            acc, plan, day = tid(o), "Team", team[o]["billing_day"]
        d0 = ymd(x["from"], day)
        if x["to"] is None:
            d1 = ""
        else:
            # the Team link closes the day before the workspace joins its Business account
            nxt = [z for z in w.log["ws_map"] if z["ws"] == x["ws"] and z["from"] == x["to"] + 1]
            d1 = (ymd(x["to"] + 1, bus[nxt[0]["owner"]]["day"]) - dt.timedelta(days=1)).isoformat()
        rows.append([wid(x["ws"]), acc, plan, d0.isoformat(), d1])
    return write_csv(path, ["workspace_id", "account_id", "plan", "linked_from", "linked_to"], rows)


# ------------------------------------------------------------------------------------------------ CRM
def _sheet(ws, header, rows, widths):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DCE6F1")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for row in rows:
        ws.append(row)
    for i, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = "A2"


def write_crm(w, path, names):
    r = np.random.default_rng(P.SEED + 73)
    par = {p["id"]: p for p in w.parents}
    rows = []
    for a in sorted(w.bus, key=lambda x: x["start"] * 100 + x["day"]):
        p = par[a["parent"]]
        if a["source"] == "upgrade":
            src = "Team upgrade"
        else:
            u = r.random()
            src = "Outbound" if u < 0.42 else ("Inbound - website" if u < 0.74 else ("Partner" if u < 0.88 else
                                                                                       "Event"))
        since = ymd(a["start"], a["day"])
        status = "Customer" if a["active"] else "Former customer"
        rows.append(["001%07d" % (a["id"] * 3 + 11), bid(a["id"]), names.acc[a["id"]],
                     names.parent_spelling(p["id"], r) if p["group"] else "", gid(p["id"]) if p["group"] else "",
                     names.country[a["id"]], INDUSTRIES[int(r.integers(0, len(INDUSTRIES)))], src,
                     since.isoformat(), status, OWNERS[int(r.integers(0, len(OWNERS)))]])
    wb = Workbook()
    ws = wb.active
    ws.title = "Accounts"
    _sheet(ws, ["Account ID", "Billing account", "Account name", "Parent account", "Parent account ID", "Country",
                "Industry", "Lead source", "Customer since", "Account status", "Account owner"], rows,
           [13, 12, 34, 30, 12, 13, 20, 16, 12, 15, 18])
    wb.save(path)
    return len(rows)


# ------------------------------------------------------------------------------------------------ pipeline
def opp_dates(o):
    """Created date and the day each stage was entered, fixed per opportunity."""
    rr = rng_for(9, o["id"])
    created = ymd(o["created"], int(rr.integers(1, 29)))
    days = [int(rr.integers(1, 29)) for _ in range(4)]
    return created, days


def stage_entered(o, m, stage, mis, created, days):
    ms = m - mis
    d = ymd(ms, days[stage])
    if d < created:
        d = created
    return d


def opp_owner(o):
    return OWNERS[int(rng_for(13, o["id"]).integers(0, len(OWNERS)))]


def amount_of(seats, cur, m, owner):
    lst = (P.BUS_LIST_NEW if m >= P.PRICE_RISE else P.BUS_LIST_OLD)[cur]
    if owner in MONTHLY_TYPERS:
        return money(seats * lst), "Monthly"
    return money(seats * lst * 12), "Annual"


def write_snapshots(w, path, names, opp_names):
    r = np.random.default_rng(P.SEED + 74)
    rows = []
    rerun = {int(x) for x in r.choice(np.arange(12, P.CUT + 1), 4, replace=False)}
    for m in range(12, P.CUT + 1):
        snap = [x for x in w.log["snap"] if x["m"] == m]
        snap.sort(key=lambda x: x["id"])
        block = []
        for x in snap:
            o = {"id": x["id"], "created": x["created"], "cur": x["cur"]}
            created, days = opp_dates(o)
            owner = opp_owner(o)
            amt, per = amount_of(x["seats"], x["cur"], m, owner)
            block.append([month_end(m).isoformat(), oid(x["id"]), opp_names[x["id"]], owner, STAGES[x["stage"]],
                          stage_entered(o, m, x["stage"], x["mis"], created, days).isoformat(),
                          created.isoformat(), x["seats"], amt, per, x["cur"], P.CRM_PROB[x["stage"]]])
        rows.extend(block)
        if m in rerun:
            # the export was re-run that month and both runs were appended to the archive
            k = int(len(block) * (0.35 + 0.5 * r.random()))
            rows.extend(block[:k])
    return write_csv(path, ["snapshot_date", "opportunity_id", "opportunity_name", "owner", "stage", "stage_entered",
                            "created_date", "seats_quoted", "amount", "amount_period", "currency", "probability_pct"],
                     rows)


def write_closed(w, path, opp_names):
    rows = []
    bus = {a["id"]: a for a in w.bus}
    reasons = ["No decision", "Price", "Competitor", "Timing", "Went dark", "Budget"]
    for x in sorted(w.log["opp_closed"], key=lambda z: (z["closed"][1], z["id"])):
        o = {"id": x["id"], "created": x["created"], "cur": x["cur"]}
        created, days = opp_dates(o)
        owner = opp_owner(o)
        m = x["closed"][1]
        rr = rng_for(17, x["id"])
        if x["closed"][0] == "won":
            a = bus[x["closed"][2]]
            closed = ymd(m, max(1, a["day"] - int(rr.integers(0, 6))))
            acc, outcome, reason = bid(a["id"]), "Closed Won", ""
        else:
            closed = ymd(m, int(rr.integers(1, 29)))
            acc, outcome = "", "Closed Lost"
            reason = reasons[int(rr.integers(0, len(reasons)))]
        if closed < created:
            closed = created
        amt, per = amount_of(x["quote_seats"], x["cur"], m, owner)
        rows.append([oid(x["id"]), opp_names[x["id"]], owner, created.isoformat(), closed.isoformat(), outcome,
                     STAGES[x["stage"]], x["quote_seats"], amt, per, x["cur"], acc, reason])
    return write_csv(path, ["opportunity_id", "opportunity_name", "owner", "created_date", "close_date", "outcome",
                            "last_stage", "seats_quoted", "amount", "amount_period", "currency", "billing_account",
                            "loss_reason"], rows)


def opportunity_names(w, names):
    out = {}
    won = {}
    for x in w.log["opp_closed"]:
        if x["closed"][0] == "won":
            won[x["id"]] = x["closed"][2]
    ids = sorted({x["id"] for x in w.log["snap"]} | {x["id"] for x in w.log["opp_closed"]})
    cur = {}
    for x in w.log["snap"]:
        cur[x["id"]] = x["cur"]
    for x in w.log["opp_closed"]:
        cur[x["id"]] = x["cur"]
    for i in ids:
        if i in won:
            out[i] = names.acc[won[i]]
        else:
            out[i] = names.prospect({"id": i, "cur": cur[i]})
    return out


# ------------------------------------------------------------------------------------------------ price book and KPIs
def write_price(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Price book 2026"
    rows = [
        ["Business", "Annual contract", "EUR", 15.00, "per seat per month", "2024-01-01", "2026-02-28", ""],
        ["Business", "Annual contract", "GBP", 13.00, "per seat per month", "2024-01-01", "2026-02-28", ""],
        ["Business", "Annual contract", "EUR", 19.00, "per seat per month", "2026-03-01", "",
         "New contracts from 1 March 2026; existing contracts at their first renewal on or after 1 March 2026"],
        ["Business", "Annual contract", "GBP", 16.50, "per seat per month", "2026-03-01", "",
         "New contracts from 1 March 2026; existing contracts at their first renewal on or after 1 March 2026"],
        ["Business", "Onboarding (one-off)", "EUR", 1500.00, "per contract", "2024-01-01", "", ""],
        ["Business", "Onboarding (one-off)", "GBP", 1300.00, "per contract", "2024-01-01", "", ""],
        ["Team", "Monthly", "EUR", 12.00, "per seat per month", "2023-01-01", "", ""],
        ["Team", "Monthly", "GBP", 10.40, "per seat per month", "2023-01-01", "", ""],
        ["Team", "Minimum billed seats", "", 3, "seats", "2026-04-01", "",
         "From the first invoice dated on or after 1 April 2026; before that date, one seat"],
    ]
    _sheet(ws, ["Plan", "Item", "Currency", "List price", "Unit", "Effective from", "Effective to", "Applies to"],
           rows, [10, 22, 9, 10, 18, 13, 13, 70])
    for row in ws.iter_rows(min_row=2, min_col=4, max_col=4):
        for c in row:
            if isinstance(c.value, float):
                c.number_format = "#,##0.00"
    ws.append([])
    ws.append(["Approved by Naomi Weijters (CFO), 14 January 2026. Prices exclude VAT."])
    wb.save(path)


def kpi_rows(F):
    out = []
    for m in range(P.CUT - 9, P.CUT):
        b, t, nb, nt = An.arr_at(F, m)
        y, mo = sim.ym(m)
        out.append([dt.date(y, mo, 1).strftime("%b %Y"), round(b, 2), round(t, 2), round(b + t, 2), nb, nt])
    return out


def write_kpi(F, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "ARR month end"
    ws.append(["Tekenbord B.V., revenue KPIs at month end (ARR on the ARR reporting policy v4, GBP at the plan rate). "
               "Refreshed 6 October 2026, Finance."])
    ws["A1"].font = Font(bold=True)
    ws.append([])
    rows = kpi_rows(F)
    hdr = ["Month", "Business ARR (EUR)", "Team ARR (EUR)", "Total ARR (EUR)", "Business accounts", "Team accounts"]
    ws.append(hdr)
    for c in ws[3]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DCE6F1")
    for r in rows:
        ws.append(r)
        for c in ws[ws.max_row][1:4]:
            c.number_format = "#,##0"
    for i, wd in enumerate([11, 18, 16, 16, 17, 14], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    wb.save(path)
    return rows


# ------------------------------------------------------------------------------------------------ the two unused files
def write_tickets(w, path):
    r = np.random.default_rng(P.SEED + 75)
    cats = ["Login and SSO", "Billing question", "Export to PDF", "Performance", "Permissions", "Integrations",
            "Templates", "Bug report", "Seat management", "Data import"]
    pr = ["Low", "Normal", "Normal", "Normal", "High", "Urgent"]
    rows = []
    n = 58000
    bus = [a for a in w.bus if a["active"] or (a["end"] is not None and a["end"] >= 48)]
    team = [t for t in w.team if t["active"] or (t["end"] is not None and t["end"] >= 48)]
    for m in range(48, P.CUT + 1):
        y, mo = sim.ym(m)
        dim = calendar.monthrange(y, mo)[1]
        k = int(r.poisson(640 + 25 * (m - 48)))
        for _ in range(k):
            if r.random() < 0.55:
                a = bus[int(r.integers(0, len(bus)))]
                acc, plan = bid(a["id"]), "Business"
            else:
                t = team[int(r.integers(0, len(team)))]
                acc, plan = tid(t["id"]), "Team"
            n += int(r.integers(1, 4))
            d = dt.datetime(y, mo, int(r.integers(1, dim + 1)), int(r.integers(7, 21)), int(r.integers(0, 60)))
            fr = round(float(r.lognormal(1.1, 0.9)), 1)
            res = d + dt.timedelta(hours=float(r.lognormal(3.0, 1.1)))
            status = "Solved" if res < dt.datetime(2026, 10, 31, 23, 59) else "Open"
            rows.append(["SR-%06d" % n, acc, plan, d.strftime("%Y-%m-%d %H:%M"), cats[int(r.integers(0, len(cats)))],
                         pr[int(r.integers(0, len(pr)))], fr, res.strftime("%Y-%m-%d %H:%M") if status == "Solved"
                         else "", status, AGENTS[int(r.integers(0, len(AGENTS)))]])
    return write_csv(path, ["ticket_id", "account_id", "plan", "opened_at", "category", "priority",
                            "first_response_hours", "solved_at", "status", "assignee"], rows)


def write_nps(w, path):
    r = np.random.default_rng(P.SEED + 76)
    rows = []
    act = [a for a in w.bus if a["start"] <= 56 and (a["active"] or (a["end"] or 0) >= 54)]
    tact = [t for t in w.team if t["start"] <= 56 and (t["active"] or (t["end"] or 0) >= 54)]
    roles = ["Admin", "Editor", "Viewer", "Owner"]
    n = 0
    for plan, pool, k in (("Business", act, 1450), ("Team", tact, 980)):
        for _ in range(k):
            x = pool[int(r.integers(0, len(pool)))]
            n += 1
            mm = 54 + int(r.integers(0, 3))
            y, mo = sim.ym(mm)
            d = dt.date(y, mo, int(r.integers(1, calendar.monthrange(y, mo)[1] + 1)))
            score = int(np.clip(round(r.normal(7.6 if plan == "Business" else 7.1, 2.0)), 0, 10))
            rows.append(["R%06d" % (410000 + n * 3 + int(r.integers(0, 3))), bid(x["id"]) if plan == "Business"
                         else tid(x["id"]), plan, d.isoformat(), roles[int(r.integers(0, len(roles)))], score])
    rows.sort(key=lambda z: (z[3], z[0]))
    return write_csv(path, ["response_id", "account_id", "plan", "submitted", "respondent_role", "score"], rows)


def write_tables(w, target):
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    names = Names(w)
    opp_names = opportunity_names(w, names)
    n = {}
    n["lines"] = write_lines(w, F["lines"], names)
    n["team"] = write_team(w, F["team"])
    n["activity"] = write_activity(w, F["activity"])
    n["links"] = write_links(w, F["links"])
    n["crm"] = write_crm(w, F["crm"], names)
    n["snap"] = write_snapshots(w, F["snap"], names, opp_names)
    n["closed"] = write_closed(w, F["closed"], opp_names)
    write_price(F["price"])
    n["kpi"] = write_kpi(tables.frames(w), F["kpi"])
    n["tickets"] = write_tickets(w, F["tickets"])
    n["nps"] = write_nps(w, F["nps"])
    return n
