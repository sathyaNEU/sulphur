"""task9: writes the pack under target/. The eight index histories ship byte for byte as Cboe published them; the
sleeve's blotter, settlements, dealer valuations, collateral ledger, statements and policy documents are the
foundation's own paperwork, written the way each party writes it."""
import datetime as dt
import os
import shutil

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

import docs as DC
import market as MK
import params as P
import postprocess as PP
import swaps as SW

UTC = dt.timezone.utc
ISO = "%Y-%m-%dT%H:%M:%SZ"
RAW_NAMES = ["SPX_History.csv", "VIX_History.csv", "VIX9D_History.csv", "VIX3M_History.csv", "VIX6M_History.csv",
             "VIX1Y_History.csv", "VVIX_History.csv", "SKEW_History.csv"]
F = dict(
    blotter="CFF_VolPremium_Blotter.xlsx", settlements="CFF_VolPremium_Settlements.csv",
    valuations="Larkhill_DealerValuations_Daily.csv", ledger="Larkhill_CollateralLedger.csv",
    holidays="NYSE_Holidays_2026_2028.csv", policy="IPS_Schedule_D_Volatility_Premium_Sleeve.pdf",
    confirmation="Master_Confirmation_SPX_Variance_Swap.pdf", csa="CSA_Summary_Volatility_Sleeve.pdf",
    terms="Indicative_Terms_3M_6M_Variance_Swaps_2027.pdf", assets="CFF_Statement_of_Net_Assets_FY2026.pdf",
    st_BSS="BreconSound_Statement_20261030.pdf", st_ACM="Altamere_Statement_20261030.pdf", st_WXB="Wexcombe_Statement_20261030.pdf",
)
DISTRACTORS = ["VVIX_History.csv", "SKEW_History.csv"]
# the time each export was written (files with no stamp of their own); the index files at the morning's pull
EXPORT_TIMES = {
    "SPX_History.csv": dt.datetime(2026, 11, 10, 12, 18, 3, tzinfo=UTC), "VIX_History.csv": dt.datetime(2026, 11, 10, 12, 18, 9, tzinfo=UTC),
    "VIX9D_History.csv": dt.datetime(2026, 11, 10, 12, 18, 21, tzinfo=UTC), "VIX3M_History.csv": dt.datetime(2026, 11, 10, 12, 18, 27, tzinfo=UTC),
    "VIX6M_History.csv": dt.datetime(2026, 11, 10, 12, 18, 34, tzinfo=UTC), "VIX1Y_History.csv": dt.datetime(2026, 11, 10, 12, 18, 40, tzinfo=UTC),
    "VVIX_History.csv": dt.datetime(2026, 11, 10, 12, 19, 2, tzinfo=UTC), "SKEW_History.csv": dt.datetime(2026, 11, 10, 12, 19, 8, tzinfo=UTC),
    F["holidays"]: dt.datetime(2026, 11, 10, 12, 31, 7, tzinfo=UTC),
    F["settlements"]: dt.datetime(2026, 11, 9, 23, 5, 31, tzinfo=UTC),
    F["valuations"]: dt.datetime(2026, 11, 2, 11, 20, 14, tzinfo=UTC),
    F["ledger"]: dt.datetime(2026, 11, 2, 11, 20, 52, tzinfo=UTC),
}
# full closures and early closes as the exchange publishes them
EARLY = [("2026-11-27", "Day after Thanksgiving"), ("2026-12-24", "Christmas Eve"), ("2027-11-26", "Day after Thanksgiving"),
         ("2028-07-03", "Day before Independence Day"), ("2028-11-24", "Day after Thanksgiving")]
CLOSED_2026 = [("2026-01-01", "New Year's Day"), ("2026-01-19", "Martin Luther King, Jr. Day"), ("2026-02-16", "Washington's Birthday"),
               ("2026-04-03", "Good Friday"), ("2026-05-25", "Memorial Day"), ("2026-06-19", "Juneteenth National Independence Day"),
               ("2026-07-03", "Independence Day (observed)"), ("2026-09-07", "Labor Day")]
CLOSED_2028 = [("2028-04-14", "Good Friday"), ("2028-05-29", "Memorial Day"), ("2028-06-19", "Juneteenth National Independence Day"),
               ("2028-07-04", "Independence Day"), ("2028-09-04", "Labor Day"), ("2028-11-23", "Thanksgiving Day"), ("2028-12-25", "Christmas Day")]


def _csv(df, path, **kw):
    df.to_csv(path, index=False, lineterminator="\r\n", **kw)


def holidays(path):
    rows = [(d, h, "Closed") for d, h in CLOSED_2026 + MK.HOLIDAYS + CLOSED_2028] + [(d, h, "Early close 1:00 p.m. ET") for d, h in EARLY]
    df = pd.DataFrame(sorted(rows), columns=["Date", "Holiday", "Market status"])
    _csv(df, path)
    return len(df)


def blotter(book, path):
    t = book.trades.copy()
    dead = book.dead.copy()
    dead["settled"] = False
    rows = pd.concat([t, dead], ignore_index=True)
    rows["order_int"] = rows.ticket.astype(int)
    rows = rows.sort_values("order_int").reset_index(drop=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Tickets"
    head = ["Order No", "Status", "Trade Date", "Expiration Date", "Dealer", "Dealer Reference", "Index", "Tenor",
            "Vega Notional (USD/pt)", "Volatility Strike", "Strike Index", "Booked By", "Remarks"]
    ws.append(head)
    for r in rows.itertuples():
        ws.append([int(r.ticket), r.status, r.sale.to_pydatetime(), r.expiry.to_pydatetime(), r.dealer, r.dealer_ref, "SPX", "12M",
                   float(r.vega), float(r.k), "VIX1Y", "IO-OPS", r.remark or None])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for row in ws.iter_rows(min_row=2):
        row[2].number_format = "mm/dd/yyyy"
        row[3].number_format = "mm/dd/yyyy"
        row[8].number_format = "#,##0"
        row[9].number_format = "0.00"
    for col, w in zip("ABCDEFGHIJKLM", (11, 12, 12, 14, 8, 22, 7, 7, 14, 11, 9, 10, 58)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    wp = wb.create_sheet("Panel")
    wp.append(["Dealer", "Legal name", "Credit support annex", "Statement basis"])
    for code, annex in (("BSS", "June 24, 2021"), ("ACM", "June 28, 2021"), ("WXB", "July 2, 2021 (amended February 9, 2024)")):
        wp.append([code, P.DEALERS[code]["name"], annex, "Variance units, variance" if P.DEALERS[code]["basis"] == "VARIANCE" else "Vega notional, volatility"])
    for c in wp[1]:
        c.font = Font(bold=True)
    for col, w in zip("ABCD", (9, 34, 40, 28)):
        wp.column_dimensions[col].width = w
    wb.save(path)
    PP.normalize_ooxml(path, P.OPS, P.OPS, dt.datetime(2021, 7, 19, 19, 40, 12, tzinfo=UTC).strftime(ISO),
                       dt.datetime(2026, 11, 9, 22, 47, 26, tzinfo=UTC).strftime(ISO), excel=True, company=P.FOUNDATION)
    return len(rows)


def settlements(book, path):
    t = book.trades[book.trades.settled].sort_values(["settle_date", "ticket"])
    df = pd.DataFrame(dict(
        settlement_date=t.settle_date.dt.strftime("%Y-%m-%d"), order_no=t.ticket, dealer=t.dealer, dealer_reference=t.dealer_ref,
        trade_date=t.sale.dt.strftime("%Y-%m-%d"), expiration_date=t.expiry.dt.strftime("%Y-%m-%d"), vega_notional_usd=t.vega.astype(int),
        volatility_strike=t.k.map("{:.2f}".format), observation_days=t.n, realized_volatility=t.rv.map("{:.4f}".format),
        final_realized_volatility=t.rv_cap.map("{:.4f}".format), settlement_amount_usd=t.settle_amt.map("{:.2f}".format)))
    _csv(df, path)
    return len(df)


def valuations(book, path):
    v = book.val.copy()
    for dl, days in P.MISSING.items():
        v = v[~((v.dealer == dl) & v.date.isin(days))]
    dl, day = P.RESENT
    v = pd.concat([v, v[(v.dealer == dl) & (v.date == day)]], ignore_index=True).sort_values(["date", "dealer", "dealer_ref"], kind="stable")
    variance = v.dealer.map(lambda d: P.DEALERS[d]["basis"] == "VARIANCE").values
    out = pd.DataFrame(dict(
        valuation_date=[d.strftime(P.DEALERS[x]["datefmt"]) for d, x in zip(v.date, v.dealer)], dealer=v.dealer.values,
        dealer_reference=v.dealer_ref.values,
        notional=np.where(variance, (v.vega / (2 * v.k)).map("{:.2f}".format), v.vega.map("{:.0f}".format)),
        notional_type=np.where(variance, "VARIANCE_UNITS", "VEGA"),
        strike=np.where(variance, (v.k ** 2).map("{:.4f}".format), v.k.map("{:.2f}".format)),
        days_elapsed=v.n_e.values, days_total=(v.n_e + v.n_r).values,
        realized_to_date=np.where(variance, v.realized.map("{:.2f}".format), v.realized.map("{:.4f}".format)),
        implied_to_expiration=v.implied.map("{:.2f}".format).values,
        quote_type=np.where(variance, "VARIANCE", "VOLATILITY"), value_usd=v.mtm.map("{:.0f}".format).values))
    _csv(out, path)
    return len(out)


def ledger(book, path):
    g = book.ledger
    out = pd.DataFrame(dict(date=g.date.dt.strftime("%Y-%m-%d"), dealer=g.dealer, exposure_usd=g.exposure.map("{:.0f}".format),
                            collateral_posted_usd=g.posted.map("{:.0f}".format), movement_usd=g.movement.map("{:.0f}".format)))
    _csv(out, path)
    return len(out)


def statements(book, tgt):
    n = {}
    for dl in P.DEALERS:
        lines = book.statement(dl)
        led = book.ledger[(book.ledger.date == P.STATEMENT) & (book.ledger.dealer == dl)]
        DC.statement(os.path.join(tgt, F["st_" + dl]), dl, lines, float(led.posted.iloc[0]))
        n[dl] = len(lines)
    return n


def write(A, tgt):
    """A is the Analysis object (its market and its book). Returns the row counts for metadata.json."""
    mk, book = A.mk, A.book
    info = {}
    for n in RAW_NAMES:
        shutil.copyfile(os.path.join(MK.RAW, n), os.path.join(tgt, n))
        info[n] = sum(1 for _ in open(os.path.join(tgt, n), "rb")) - 1
    info[F["holidays"]] = holidays(os.path.join(tgt, F["holidays"]))
    info[F["blotter"]] = blotter(book, os.path.join(tgt, F["blotter"]))
    info[F["settlements"]] = settlements(book, os.path.join(tgt, F["settlements"]))
    info[F["valuations"]] = valuations(book, os.path.join(tgt, F["valuations"]))
    info[F["ledger"]] = ledger(book, os.path.join(tgt, F["ledger"]))
    DC.policy(os.path.join(tgt, F["policy"]))
    DC.confirmation(os.path.join(tgt, F["confirmation"]))
    DC.csa(os.path.join(tgt, F["csa"]))
    cal3, cal6 = A.new_calendar(P.NEW_MAT), A.new_calendar(P.ALT_MAT)
    DC.term_sheet(os.path.join(tgt, F["terms"]), cal3.sale.iloc[0], cal3.expiry.iloc[0], cal6.expiry.iloc[0])
    DC.net_assets(os.path.join(tgt, F["assets"]))
    info["statement_lines"] = statements(book, tgt)
    return info
