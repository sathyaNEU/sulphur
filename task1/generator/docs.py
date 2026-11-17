"""Zancada's own documents: the growth policy for paid channels (exported from a word processor through the house
writer), the growth team's weekly budget workbook with its change log, the 2027 media plan workbook and the app's
conversion-value schema."""
import datetime as dt
import json
import os
import sys

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
sys.path.insert(0, HERE)
import officepdf as O  # noqa: E402
import core as C  # noqa: E402

ORG = "Zancada Fitness S.L."
CET = dt.timezone(dt.timedelta(hours=1))
CEST = dt.timezone(dt.timedelta(hours=2))
DAY0 = dt.date(2024, 11, 4)
PLAN0 = dt.date(2027, 1, 4)

FILES = {
    "policy": "growth_policy_paid_channels_v3_2026-09.pdf",
    "plan": "media_plan_2027.xlsx",
    "budget": "paid_budgets_weekly_2024-2026.xlsx",
    "schema": "skadnetwork_conversion_values.json",
}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]
WORD = {3: "three", 4: "four", 5: "five"}


def _reason(r, f, eff, k):
    """what the growth team wrote beside a budget move: its own side's reason, in its own hand, sometimes nothing"""
    if r.random() < 0.09:
        return None
    q, mon = (eff.month - 1) // 3 + 1, MONTHS[eff.month - 1]
    nxt, prev = MONTHS[eff.month % 12], MONTHS[(eff.month - 2) % 12]
    if f > 1:
        opts = ["Finance released the Q%d acquisition top-up" % q, "Q%d top-up released, finance" % q,
                "Unspent brand budget moved across for %s" % mon, "Brand budget left over from %s moved over" % prev,
                "CEO asked for a higher run-rate ahead of the %s board pack" % nxt,
                "Agency rebate credited, to be used within %s weeks" % WORD[k],
                "Annual budget phasing brought forward", "Phasing: %s pulled into %s" % (nxt, mon),
                "Carry-over from Q%d released by finance" % (4 if q == 1 else q - 1),
                "Planning asked for more volume before the %s review" % ("half-year" if eff.month in (5, 6, 11, 12)
                                                                         else "quarterly"),
                "Treasury confirmed extra headroom for %s weeks" % WORD[k], "Events budget not used, moved here"]
    else:
        opts = ["Cash plan tightened for %s" % mon, "Cash plan, %s: variable lines down" % mon,
                "Quarter-end freeze on variable spend" if eff.month % 3 == 0 else "Freeze on variable spend, finance",
                "Budget lent to the influencer programme, back in %s" % nxt,
                "Finance asked for a hold while the %s agency invoice is disputed" % prev,
                "Annual budget phasing pushed back", "Phasing: part of %s moved to %s" % (mon, nxt),
                "Planning trimmed %s to stay inside the half-year envelope" % mon,
                "Card limit reached on the ad account, lower run-rate until it is raised",
                "Hiring costs came in over plan, variable spend cut back", "Audit of agency invoices, held while it runs"]
    return str(r.choice(opts))


def _closing(r, f):
    """the note on the row that takes a budget back to its base: most often left empty"""
    u = r.random()
    if u < 0.46:
        return None
    if u < 0.66:
        return "End of the %s" % ("top-up" if f > 1 else "hold-back")
    if u < 0.80:
        return "As planned"
    if u < 0.90:
        return "Top-up used" if f > 1 else "Hold lifted by finance"
    return "Back to the seasonal base"


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.3, leading=12.8, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.8, leading=16.2,
                        spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.0, leading=13.4,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


POLICY = [
    ("1. What this policy is for", [
        "1.1 This policy sets how Zancada places each paid acquisition channel for the coming year. The head of growth "
        "proposes the placements with the media plan in November; the head of financial planning signs the year's "
        "insertion orders with the ad platforms on them. It binds growth, finance and the agencies' briefs.",
        "1.2 The channels placed are the channels of the media plan's growth sheet. A channel is an ad platform on "
        "one operating system. Spend on the brand sheet (Apple Search Ads on Zancada's own name and on generic "
        "workout terms, a fixed budget) is not placed under this policy."]),
    ("2. A channel's return", [
        "2.1 A channel's return for a period is the 12-month net revenue of the installs the period's spend on the "
        "channel buys, per euro of that spend. For a plan year the period is the plan's 52 weeks and the spend is the "
        "plan's weekly spend on the channel, as the platform bills it.",
        "2.2 An install is the first install of a new consumer account. A second device, a reinstall, a staff account "
        "and a test account are not installs. Each install is bought by at most one channel, the one whose ad drove "
        "it, whether or not the attribution partner can name it; an install no ad drove is organic.",
        "2.3 An install's 12-month net revenue is the net revenue of every charge the App Store, Google Play or the "
        "web checkout made on its account in the 365 days from the install, each at the time of the transaction, less "
        "the net revenue of any of those charges refunded.",
        "2.4 The net revenue of a charge is its price less VAT (Spain 21 per cent, Italy 22 per cent, Portugal 23 per "
        "cent, by the storefront) and less, on a store charge, the store's commission of 15 per cent of the price net "
        "of VAT, and on a web checkout charge, the card processor's fee of 3 per cent of the price net of VAT.",
        "2.5 Prices are EUR 9.99 a month and EUR 59.99 a year, each with a seven-day free trial, on both stores and on "
        "the web checkout, and do not change in 2027.",
        "2.6 A channel's marginal return at a stated spend is the 12-month net revenue that one more euro of spend "
        "returns at that spend, every week of the period raised in the same proportion."]),
    ("3. Bands", [
        "3.1 Each channel is placed in one of three bands on its return for the plan year at the plan's weekly spend: "
        "scale when the return is 1.20 or more, hold when it is 0.90 or more and under 1.20, and cut when it is "
        "under 0.90.",
        [["Band", "Return", "What it means for the plan year"],
         ["Scale", "1.20 or more", "the plan's spend is approved and the stretch spend may be released during the year"],
         ["Hold", "0.90 or more and under 1.20", "the plan's spend is approved and the stretch spend is not released"],
         ["Cut", "under 0.90", "the channel is cut back to creative tests"]],
        "3.2 The placements go to the head of financial planning with, for every channel, its return at the plan's "
        "spend and at the stretch spend, the 12-month net revenue per install at the plan's spend and its marginal "
        "return at the plan's spend."]),
    ("4. Timing", [
        "4.1 Placements for a plan year are made in November of the year before, on the media plan's weekly spend and "
        "Zancada's records to the start of November. A plan year's installs are not twelve months old until the year "
        "after it, so each return is an estimate, and it is given as a committed figure.",
        "4.2 The policy is reviewed each September. Version 3 adds the web checkout (2.3, 2.4), the marginal return "
        "(2.6) and the stretch spend (3.1)."]),
]


def write_policy(target):
    body, h1, h2, cell = _styles()
    title = "Growth policy for paid acquisition channels"
    head = [["Document", "Growth policy for paid acquisition channels, version 3"],
            ["Owner", "Magdalena Requena, head of growth"],
            ["Approved", "Bernardo Pombo, head of financial planning, 21 September 2026"],
            ["Replaces", "version 2 of 22 September 2025"]]
    story = [Paragraph(title, h1), _grid(head, [44 * 2.83, 118 * 2.83], cell), Spacer(1, 6)]
    for hd, paras in POLICY:
        story.append(Paragraph(hd, h2))
        for p in paras:
            if isinstance(p, list):
                story.append(_grid(p, [x * 2.83 for x in (26, 44, 92)], cell))
            else:
                story.append(Paragraph(p, body))
    O.build(os.path.join(target, FILES["policy"]), story, title=title, author="Magdalena Requena",
            subject="Growth policy, paid channels", footer="%s, growth policy for paid acquisition channels, v3" % ORG,
            created=dt.datetime(2026, 9, 21, 17, 42, tzinfo=CEST), modified=dt.datetime(2026, 9, 21, 17, 42, tzinfo=CEST),
            font="Liberation Sans")


def _head(ws, row, bold=True):
    for c in ws[row]:
        c.font = Font(bold=bold)
        c.fill = PatternFill("solid", fgColor="DDE6F0")
        c.alignment = Alignment(wrap_text=True, vertical="top")


def moves():
    """the growth team's budget moves as its log holds them: (channel, first week, weeks, factor)"""
    out = []
    for c in C.ORDER:
        for w0, k, f in C.CH[c]["pushes"]:
            out.append((c, w0, k, f))
    return sorted(out, key=lambda x: (x[1], C.ORDER.index(x[0])))


def write_budget(target, W):
    wb = Workbook()
    ws = wb.active
    ws.title = "Weekly budgets"
    ws.append(["Weekly paid budgets by channel, EUR (what we set on the ad accounts each Monday)"])
    ws["A1"].font = Font(bold=True)
    ws.append([])
    ws.append(["Week starting"] + C.ORDER + ["Total"])
    _head(ws, 3)
    for w in range(C.WEEKS):
        vals = [int(W["B"][c]["budget"][w]) for c in C.ORDER]
        ws.append([DAY0 + dt.timedelta(days=7 * w)] + vals + [sum(vals)])
        ws.cell(row=w + 4, column=1).number_format = "dd/mm/yyyy"
        for k in range(2, len(C.ORDER) + 3):
            ws.cell(row=w + 4, column=k).number_format = "#,##0"
    ws.column_dimensions["A"].width = 13
    for k in range(len(C.ORDER) + 1):
        ws.column_dimensions[chr(66 + k)].width = 15
    ws.freeze_panes = "B4"
    lg = wb.create_sheet("Changes")
    lg.append(["Logged", "Channel", "Effective from (week starting)", "Change against the seasonal base",
               "Planned for (weeks)", "Reason", "By"])
    _head(lg, 1)
    r = np.random.default_rng([C.SEED, 13])
    rows = []
    for c, w0, k, f in moves():
        eff = DAY0 + dt.timedelta(days=7 * w0)
        logged = eff - dt.timedelta(days=int(r.choice([3, 3, 4, 5, 6, 7])))
        if logged.weekday() >= 5:
            logged -= dt.timedelta(days=logged.weekday() - 4)
        pct = int(round((f - 1) * 100))
        reason = _reason(r, f, eff, k)
        by = "Rafa Naranjo" if r.random() < 0.72 else "Magdalena Requena"
        rows.append((logged, c, eff, "%+d%%" % pct, k, reason, by))
        end = eff + dt.timedelta(days=7 * k)
        if end < DAY0 + dt.timedelta(days=7 * C.WEEKS):
            lg2 = end - dt.timedelta(days=int(r.choice([3, 3, 4, 5])))
            if lg2.weekday() >= 5:
                lg2 -= dt.timedelta(days=lg2.weekday() - 4)
            rows.append((lg2, c, end, "back to base", None, _closing(r, f),
                         "Rafa Naranjo" if r.random() < 0.88 else "Magdalena Requena"))
    rows.sort(key=lambda x: (x[0], x[2], x[1]))
    for i, row in enumerate(rows):
        lg.append(list(row))
        lg.cell(row=i + 2, column=1).number_format = "dd/mm/yyyy"
        lg.cell(row=i + 2, column=3).number_format = "dd/mm/yyyy"
    for col, wd in zip("ABCDEFG", (12, 18, 16, 18, 12, 62, 20)):
        lg.column_dimensions[col].width = wd
    lg.freeze_panes = "A2"
    wb.save(os.path.join(target, FILES["budget"]))
    return len(rows)


def write_plan(target):
    wb = Workbook()
    ws = wb.active
    ws.title = "Growth channels"
    st = wb.create_sheet("Stretch case")
    br = wb.create_sheet("Brand")
    members = C.MEMBERS
    for sheet, title, lift in ((ws, "Media plan 2027, growth channels: weekly spend, EUR, as the platforms bill it", False),
                               (st, "Media plan 2027, stretch case: weekly spend on each growth channel if its stretch is released, EUR", True)):
        sheet.append([title])
        sheet["A1"].font = Font(bold=True)
        sheet.append(["Draft for the insertion orders, 30 October 2026"])
        sheet.append([])
        sheet.append(["Week starting", "ISO week"] + members + ["Total"])
        _head(sheet, 4)
        tot = np.zeros(len(members))
        for t in range(52):
            vals = [float(C.plan_spend(c)[t]) * (C.CH[c]["stretch"] if lift else 1.0) for c in members]
            vals = [int(round(v)) if abs(v - round(v)) < 1e-9 else round(v, 1) for v in vals]
            sheet.append([PLAN0 + dt.timedelta(days=7 * t), t + 1] + vals + [sum(vals)])
            sheet.cell(row=t + 5, column=1).number_format = "dd/mm/yyyy"
            for k in range(3, len(members) + 4):
                sheet.cell(row=t + 5, column=k).number_format = "#,##0.0" if lift else "#,##0"
            tot += np.array(vals, float)
        sheet.append(["Total 2027", None] + [round(float(x), 1) if lift else int(round(x)) for x in tot]
                     + [round(float(tot.sum()), 1) if lift else int(round(tot.sum()))])
        for c in sheet[sheet.max_row]:
            c.font = Font(bold=True)
            c.number_format = "#,##0"
        sheet.column_dimensions["A"].width = 13
        for k in range(len(members) + 2):
            sheet.column_dimensions[chr(66 + k)].width = 15
        sheet.freeze_panes = "C5"
    br.append(["Media plan 2027, brand: fixed weekly budget, EUR"])
    br["A1"].font = Font(bold=True)
    br.append(["Draft for the insertion orders, 30 October 2026"])
    br.append([])
    br.append(["Week starting", "ISO week", "Apple Search Ads"])
    _head(br, 4)
    sp = C.plan_spend("Apple Search Ads")
    for t in range(52):
        br.append([PLAN0 + dt.timedelta(days=7 * t), t + 1, int(sp[t])])
        br.cell(row=t + 5, column=1).number_format = "dd/mm/yyyy"
        br.cell(row=t + 5, column=3).number_format = "#,##0"
    br.append(["Total 2027", None, int(sp.sum())])
    for c in br[br.max_row]:
        c.font = Font(bold=True)
        c.number_format = "#,##0"
    br.column_dimensions["A"].width = 13
    br.column_dimensions["C"].width = 18
    wb.save(os.path.join(target, FILES["plan"]))


CV_SCHEMA = {
    "app": "Zancada", "bundle_id": "es.zancada.app", "skadnetwork_version": "4.0", "config_version": 3,
    "in_use_since": "2024-11-04",
    "postback": {"sequence": 1, "measurement_window_hours": 48, "sent_after_window_closes_hours": [24, 48],
                 "lock_window": False},
    "fine_value_bits": {
        "0-2": {"name": "sessions_bucket", "event": "workout_session_start", "window": "first 48 hours",
                "values": {"0": "0", "1": "1", "2": "2", "3": "3-4", "4": "5-7", "5": "8-11", "6": "12-17",
                           "7": "18+"}},
        "3": {"name": "trial_started", "event": "free_trial_start", "window": "first 48 hours"},
        "4": {"name": "purchased", "event": "subscription_purchase_without_trial", "window": "first 48 hours"},
        "5": {"name": "reserved", "value": 0}},
    "value_computed": {"by": "backend", "platforms": ["ios", "android"]},
}


def write_schema(target):
    with open(os.path.join(target, FILES["schema"]), "w") as f:
        json.dump(CV_SCHEMA, f, indent=2)
        f.write("\n")


def write_all(target, W):
    write_policy(target)
    write_plan(target)
    n = write_budget(target, W)
    write_schema(target)
    return n
