"""Zancada's own documents: the growth policy for paid channels (a Word document exported by LibreOffice Writer
through the house writer), the 2027 media plan workbook, the data dictionary of the exports and the app's
conversion-value schema."""
import datetime as dt
import json
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
import officepdf as O  # noqa: E402
import params as P  # noqa: E402

ORG = P.ORG
CET = dt.timezone(dt.timedelta(hours=1))
CEST = dt.timezone(dt.timedelta(hours=2))

FILES = {
    "policy": "growth_policy_paid_channels_v2_2026-09.pdf",
    "plan": "media_plan_2027.xlsx",
}


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.3, leading=12.8, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.8, leading=16.2,
                        spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.0, leading=13.4,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=7.9, leading=10.4, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _doc(path, title, sections, meta, header_rows, author, subject, footer, created, modified, widths=None):
    body, h1, h2, small, cell = _styles()
    story = [Paragraph(title, h1), _grid(header_rows, [44 * 2.83, 118 * 2.83], cell), Spacer(1, 6)]
    for head, paras in sections:
        story.append(Paragraph(head, h2))
        for p in paras:
            if isinstance(p, list):
                n = len(p[0])
                w = widths or {2: [60, 100], 3: [52, 56, 52], 4: [40, 40, 40, 40], 5: [34, 30, 32, 32, 32]}[n]
                story.append(_grid(p, [x * 2.83 for x in w], cell))
            else:
                story.append(Paragraph(p, body))
    if meta:
        story.append(Spacer(1, 8))
        story.append(Paragraph(meta, small))
    O.build(path, story, title=title, author=author, subject=subject, footer=footer, created=created,
            modified=modified, font="Liberation Sans")


POLICY = [
    ("1. What this policy is for", [
        "This policy sets how Zancada places each paid acquisition channel for the coming year. The head of growth "
        "proposes the placements with the media plan in November; the head of financial planning signs the year's "
        "insertion orders with the ad networks on them. It binds growth, finance and the agencies' briefs."]),
    ("2. A channel's return", [
        "2.1 A channel's return for a plan year is the 12-month net revenue of the installs the plan's spend on the "
        "channel buys in that year, per euro of that spend.",
        "2.2 An install is the first install of a new consumer account. A second device, a reinstall, a staff account "
        "and a test account are not installs. Each install is bought by at most one channel: the one whose ads drove it.",
        "2.3 An install's 12-month net revenue is the net revenue of the store charges on its account in the 365 days "
        "from the day of the install, less the net revenue of any of those charges refunded.",
        "2.4 The net revenue of a charge is its price less VAT (Spain 21 per cent, Italy 22 per cent, Portugal 23 per "
        "cent, by the storefront) and less the store's commission of 15 per cent of the price net of VAT (Apple's "
        "Small Business Program; Google Play's rate on subscriptions).",
        "2.5 Prices are EUR 9.99 a month and EUR 59.99 a year, each with a seven-day free trial, and do not change in "
        "2027."]),
    ("3. Bands", [
        "3.1 Each paid channel is placed in one of three bands on its return for the plan year: scale when the return "
        "is 1.20 or more, hold when it is 0.90 or more and under 1.20, and cut when it is under 0.90.",
        [["Band", "Return", "What it means for the plan year"],
         ["Scale", "1.20 or more", "the plan's spend is approved and may be raised during the year"],
         ["Hold", "0.90 or more and under 1.20", "the plan's spend is approved and is not raised"],
         ["Cut", "under 0.90", "the channel is cut back to creative tests"]]]),
    ("4. Timing", [
        "Placements for a plan year are made in November of the year before, on the media plan's weekly spend and "
        "Zancada's records to the start of November. A plan year's installs are not twelve months old until the year "
        "after it, so each return is an estimate."]),
]


def write_policy(target):
    _doc(os.path.join(target, FILES["policy"]), "Growth policy for paid acquisition channels", POLICY, None,
         [["Document", "Growth policy for paid acquisition channels, version 2"],
          ["Owner", "Magdalena Requena, head of growth"],
          ["Approved", "Bernardo Pombo, head of financial planning, 22 September 2026"],
          ["Replaces", "version 1 of 11 November 2024"]],
         author="Magdalena Requena", subject="Growth policy, paid channels",
         footer="%s, growth policy for paid acquisition channels, v2" % ORG,
         created=dt.datetime(2026, 9, 18, 10, 42, tzinfo=CEST), modified=dt.datetime(2026, 9, 22, 16, 5, tzinfo=CEST),
         widths=[26, 44, 92])


def write_plan(target):
    wb = Workbook()
    ws = wb.active
    ws.title = "Weekly spend 2027"
    hdr = ["Week starting", "ISO week"] + P.ORDER + ["Total"]
    ws.append(hdr)
    bold = Font(bold=True)
    for c in ws[1]:
        c.font = bold
        c.fill = PatternFill("solid", fgColor="DDE6F0")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    tot = {c: 0 for c in P.ORDER}
    for w, (mon, m, sp) in enumerate(P.plan_weeks()):
        row = [mon, w + 1] + [sp[c] for c in P.ORDER] + [sum(sp.values())]
        ws.append(row)
        ws.cell(row=w + 2, column=1).number_format = "dd/mm/yyyy"
        for k in range(3, 3 + len(P.ORDER) + 1):
            ws.cell(row=w + 2, column=k).number_format = "#,##0"
        for c in P.ORDER:
            tot[c] += sp[c]
    ws.append(["Total 2027", None] + [tot[c] for c in P.ORDER] + [sum(tot.values())])
    for c in ws[ws.max_row]:
        c.font = bold
        c.number_format = "#,##0"
    ws.column_dimensions["A"].width = 13
    for k in range(len(hdr) - 1):
        ws.column_dimensions[chr(66 + k)].width = 14
    ws.freeze_panes = "C2"
    n = wb.create_sheet("Notes")
    for line in ["Media plan 2027, weekly spend in EUR by channel (spend as the networks bill it).",
                 "Weeks run Monday to Sunday. Prepared by Rafa Naranjo for the November 2026 placements.",
                 "Status: draft for the insertion orders, 30 October 2026."]:
        n.append([line])
    n.column_dimensions["A"].width = 100
    wb.save(os.path.join(target, FILES["plan"]))


CV_SCHEMA = {
    "app": "Zancada", "platform": "ios", "skadnetwork_version": "4.0", "window": "postback 1 (0 to 2 days)",
    "schema_version": 3, "in_use_since": "2024-11-04",
    "fine_value_bits": {
        "0-2": {"name": "sessions_bucket", "meaning": "workout sessions started in the first 48 hours",
                "values": {"0": "0", "1": "1", "2": "2", "3": "3-4", "4": "5-7", "5": "8-11", "6": "12-17", "7": "18 or more"}},
        "3": {"name": "trial_started", "meaning": "a seven-day free trial started in the first 48 hours"},
        "4": {"name": "purchased", "meaning": "a paid subscription bought in the first 48 hours without a trial"},
        "5": {"name": "reserved", "meaning": "always 0"}},
    "coarse_value": {"high": "purchased, or trial started with 5 or more sessions", "medium": "trial started",
                     "low": "otherwise"},
    "lock_window": False,
}


DICTIONARY = """# Data dictionary: exports for the 2027 channel placements

Exports pulled 9 November 2026. Times are UTC unless a field says otherwise. Amounts are in euros.

## accounts_2026-11-09.csv
One row per Zancada account (the app creates the account at first open).
- account_id: the account.
- created_at: the account's first open.
- platform: ios or android, the platform of the device that created the account.
- country: the storefront country at creation (ES, IT, PT).
- account_type: consumer, staff or test.
- att_status: iOS only. The answer to Apple's App Tracking Transparency prompt as the app last read it (authorized, denied, not_determined).
- first_48h_value: the conversion value the app computed for the account's first 48 hours under the schema in skan_conversion_value_schema.json, on both platforms.
- last_open_at: the account's most recent app open.
- plan_at_last_open: the account's subscription plan as the app read it at the last open (monthly, annual; blank if none).
- auto_renew_at_last_open: whether that subscription was set to renew as the app read it at the last open (yes, no; blank if none).

## billing_events_2024-11-04_2026-11-08.csv
Zancada's billing events: the store transactions the app has synced for each account.
- event_id: the event.
- account_id: the account.
- store: app_store or google_play.
- environment: production or sandbox.
- product_id: zancada.premium.monthly or zancada.premium.annual.
- event_type: first_charge, renewal or refund.
- transaction_at: the store's time of the charge or refund.
- recorded_at: when the app synced the transaction to Zancada's servers.
- price_eur: the price charged, VAT included (negative for a refund).
- storefront: the storefront country of the transaction.

## attribution_installs_2024-11-04_2026-11-08.csv
The attribution partner's install export: one row per install the partner's SDK reported.
- install_id: the install.
- account_id: the Zancada account the install opened.
- platform: ios or android.
- install_time: the install's first open as the partner recorded it.
- media_source: the source the partner attributed the install to (Meta Ads, TikTok For Business, Apple Search Ads, Google Ads, AppLovin, organic).
- campaign_id: the attributed campaign (blank for organic).
- att_status: iOS only, as the partner's SDK read it.
- is_reinstall: true when the partner saw the device or account before.

## skan_postbacks_2024-11-04_2026-11-08.csv
Apple's SKAdNetwork install postbacks for Zancada's iOS campaigns on Meta and TikTok, as the networks passed them on (first postback).
- postback_id: the postback.
- ad_network: meta or tiktok.
- source_identifier: the campaign's source identifier (four digits, or the last two digits at lower privacy tiers).
- postback_date, postback_time_utc: when the postback arrived.
- conversion_value: the fine conversion value (blank when Apple withheld it).
- coarse_conversion_value: low, medium or high (blank when Apple withheld it).
- fidelity_type: 1 for a click-through install.
- redownload: true when Apple flagged a redownload.

## appstore_subscription_events_daily_2024-11_2026-11.csv
App Store Connect subscription events, by day (Pacific time), product, country and event.
- event: Paid Subscription from Free Trial, Subscribe, Renew or Refund.
- units, customer_price_eur, developer_proceeds_eur.

## googleplay_subscription_transactions_daily_2024-11_2026-11.csv
Google Play Console subscription transactions, by day (UTC), product, country and transaction type.
- transaction_type: charge_new, charge_renewal or refund.
- transactions, amount_eur (VAT included), net_eur (after VAT and the store's fee).

## ad_spend_daily_2024-11-04_2026-11-08.csv
Daily spend by channel and campaign, as the networks billed it.
- installs_reported_by_network: the installs the network's own reporting credited to the campaign that day.

## media_plan_2027.xlsx
The 2027 weekly spend by channel.

## creative_tests_2025-2026.csv
The creative team's A/B tests of ad creatives.

## store_ratings_daily_2024-11_2026-10.csv
Ratings left in the stores, by day, store and country.
"""


def write_all(target):
    write_policy(target)
    write_plan(target)
