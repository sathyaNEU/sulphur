"""task9: writes the pack under target/ the way each of Harbourne's systems hands its records over.

The market series ship as FRED and Cboe published them (cut at the record's last day). The rest is the platform's own
paperwork: the risk system's daily P&L in its two generations (the 2023 migration changed the export's units and
layout), the book-code map from the 2022 reorganisation, the administrator's month-end statements, the pod register,
every capital change, the plans the committee approved since 2018, the draft for 2027 and the two documents the
committee works under."""
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

UTC = dt.timezone.utc
ISO = "%Y-%m-%dT%H:%M:%SZ"
F = dict(
    legacy="risk_pnl_daily_legacy_20170103_20230630.csv", current="risk_pnl_daily_20230703_20261106.csv",
    codes="book_code_map_20220401.csv", admin="kestrel_month_end_statements_201701_202610.csv",
    register="pod_register_20261106.csv", changes="capital_changes_20170103_20261106.csv",
    plans="allocation_plans_2018_2026.xlsx", draft="draft_allocation_plan_2027.xlsx",
    policy="Capital_Review_Policy_2026.pdf", riskmodel="Risk_Model_Methodology_2023.pdf",
)
MARKET = [f["file"] for f in MK.manifest()["files"]]
DISTRACTORS = ["DAAA.csv", "IR3TIB01USM156N.csv"]
PREFIX = {"EQLS": "EQ", "QEQ": "QE", "RATES": "RT", "FX": "FX", "CREDIT": "CR", "COMDTY": "CM", "VOLARB": "VL"}
SUB = {"EQLS": ["TMT", "Healthcare", "Industrials", "Consumer", "Financials", "Energy and materials", "Generalist"],
       "QEQ": ["Statistical arbitrage", "Systematic factor", "Systematic event"],
       "RATES": ["US rates relative value", "Global rates", "Swap spreads and basis"],
       "FX": ["G10 currencies", "G10 relative value"],
       "CREDIT": ["Investment grade relative value", "High yield and capital structure", "Credit long/short"],
       "COMDTY": ["Oil and products", "Power and gas", "Metals"],
       "VOLARB": ["Index volatility", "Dispersion", "Volatility relative value"]}
OUTAGES = [pd.Timestamp("2018-08-07"), pd.Timestamp("2020-02-19"), pd.Timestamp("2021-09-08")]   # legacy feed down; caught up next day
EXPORT_TIMES = {F["legacy"]: dt.datetime(2023, 7, 5, 21, 14, 37, tzinfo=UTC), F["current"]: dt.datetime(2026, 11, 9, 11, 42, 8, tzinfo=UTC),
                F["codes"]: dt.datetime(2022, 4, 4, 14, 6, 51, tzinfo=UTC), F["admin"]: dt.datetime(2026, 11, 6, 16, 27, 19, tzinfo=UTC),
                F["register"]: dt.datetime(2026, 11, 9, 11, 44, 30, tzinfo=UTC), F["changes"]: dt.datetime(2026, 11, 9, 11, 45, 2, tzinfo=UTC)}
for k, name in enumerate(MARKET):   # the review morning's pull for the pack, a few seconds apart
    EXPORT_TIMES[name] = dt.datetime(2026, 11, 9, 12, 2, 0, tzinfo=UTC) + dt.timedelta(seconds=7 * k + 3)


def _csv(df, path):
    df.to_csv(path, index=False, lineterminator="\r\n")


class Books:
    """The platform's records derived from the World: codes, the funding charge, payouts, the true-ups."""

    def __init__(self, W):
        self.W = W
        d = W.days
        self.days = d
        bill = W.mk.level.DTB3.reindex(d).ffill().values / 100.0
        gap = np.r_[1.0, (d[1:] - d[:-1]).days].astype(float)
        self.fund = np.where(np.isnan(W.cap), np.nan, W.cap * P.FIN_SHARE * (bill + P.FIN_SPREAD) * gap / 365.0)
        reorg = int(np.searchsorted(d, P.REORG))
        self.reorg = reorg
        seq = 1001
        self.old, self.new = {}, {}
        for p in W.pods:
            self.old[p["n"]] = "%s%03d" % (PREFIX[p["g"]], p["serial"])
        alive = sorted((p for p in W.pods if p["start"] < reorg and (p["end"] is None or p["end"] > reorg)),
                       key=lambda p: (P.GROUP_ORDER.index(p["g"]), p["serial"]))
        for p in alive:
            self.new[p["n"]] = "HC%d" % seq
            seq += 1
        for p in sorted((p for p in W.pods if p["start"] >= reorg), key=lambda p: (p["start"], P.GROUP_ORDER.index(p["g"]), p["serial"])):
            self.new[p["n"]] = "HC%d" % seq
            seq += 1
        rng = np.random.default_rng(P.SEED + 5)
        self.sub = {p["n"]: SUB[p["g"]][int(rng.integers(0, len(SUB[p["g"]])))] for p in W.pods}
        # the risk system's P&L for a month's last trading day is provisional; the next trading day carries the true-up
        last = np.r_[d.month[1:] != d.month[:-1], True]
        self.risk = W.pnl.copy()
        for n in range(len(W.pods)):
            for i in np.where(last & ~np.isnan(W.pnl[n]))[0]:
                if i + 1 >= len(d) or np.isnan(W.pnl[n, i + 1]):
                    continue
                e = float(rng.normal(0.0, 0.04)) * abs(W.pnl[n, i]) + float(rng.normal(0.0, 1500.0))
                self.risk[n, i] += e
                self.risk[n, i + 1] -= e

    def code(self, n, i):
        if n in self.new and (i >= self.reorg or n not in self.old or self.W.pods[n]["start"] >= self.reorg):
            return self.new[n]
        return self.old[n]

    def last_code(self, n):
        return self.new.get(n, self.old[n])

    def years(self):
        """Each pod's calendar-year P&L after funding, and its payout, booked in the month it is paid."""
        W, d = self.W, self.days
        out = []
        for p in W.pods:
            n = p["n"]
            ok = ~np.isnan(W.pnl[n])
            for y in sorted(set(d.year[ok])):
                m = ok & (d.year == y)
                g, f = float(np.nansum(W.pnl[n][m])), float(np.nansum(self.fund[n][m]))
                i_last = int(np.where(m)[0][-1])
                ended = p["end"] is not None and p["end"] - 1 == i_last
                if y == d[-1].year and not ended:
                    continue                                  # the year is not over
                out.append(dict(n=n, year=int(y), gross=g, fund=f, payout=P.PAYOUT * max(g - f, 0.0), paid=d[i_last]))
        return pd.DataFrame(out)


def risk_files(B, tgt):
    W, d = B.W, B.days
    rows_old, rows_new = [], []
    mig = int(np.searchsorted(d, P.MIGRATION))
    outage = {int(np.searchsorted(d, x)) for x in OUTAGES}
    for i in range(len(d)):
        for p in W.active(i):
            n = p["n"]
            x, k = B.risk[n, i], W.cap[n, i]
            if np.isnan(x):
                continue
            if i < mig:
                if i in outage:
                    continue
                if i - 1 in outage and not np.isnan(B.risk[n, i - 1]):
                    x += B.risk[n, i - 1]
                rows_old.append((d[i].strftime("%Y-%m-%d"), B.code(n, i), "%.2f" % x, "%d" % round(k)))
                if d[i] == P.RESENT:
                    rows_old.append(rows_old[-1])
            else:
                rows_new.append((d[i].strftime("%m/%d/%Y"), B.code(n, i), "%.1f" % (x / 1e3), "%.1f" % (k / 1e6)))
    old = pd.DataFrame(rows_old, columns=["cob_date", "pod_code", "gross_pnl_usd", "capital_usd"])
    new = pd.DataFrame(rows_new, columns=["trade_date", "book_id", "pnl_usd_000", "alloc_capital_usd_mm"])
    _csv(old, os.path.join(tgt, F["legacy"]))
    _csv(new, os.path.join(tgt, F["current"]))
    return len(old), len(new)


def code_map(B, tgt):
    rows = [(B.old[n], B.new[n]) for n in sorted(B.new, key=lambda n: B.new[n]) if n in B.old and B.W.pods[n]["start"] < B.reorg]
    df = pd.DataFrame(rows, columns=["old_pod_code", "new_book_id"])
    df.insert(2, "effective_date", P.REORG.strftime("%Y-%m-%d"))
    _csv(df, os.path.join(tgt, F["codes"]))
    return len(df)


def admin(B, tgt):
    """The administrator's month-end statement per sleeve: gross trading P&L, the funding charge, the PM incentive
    accrued for the year (in December, or in the month a pod closed), net P&L and month-end allocated capital."""
    W, d = B.W, B.days
    yrs = B.years()
    pay = {(int(r.n), r.paid.year, r.paid.month): r.payout for r in yrs.itertuples()}
    month = d.to_period("M")
    rows = []
    last_month = pd.Period(P.LAST_DAY, "M") - 1                 # October 2026 is the last closed month
    for p in W.pods:
        n = p["n"]
        ok = ~np.isnan(W.pnl[n])
        for m in sorted(set(month[ok])):
            if m > last_month:
                continue
            idx = np.where(ok & (month == m))[0]
            g, f = float(W.pnl[n][idx].sum()), float(B.fund[n][idx].sum())
            inc = pay.get((n, m.year, m.month), 0.0)
            i_last = int(idx[-1])
            closed = p["end"] is not None and p["end"] - 1 == i_last
            cap = 0.0 if closed else float(W.cap[n, i_last])
            rows.append((m.to_timestamp(how="end").strftime("%Y-%m-%d"), B.code(n, i_last), "%.2f" % g, "%.2f" % f, "%.2f" % inc,
                         "%.2f" % (g - f - inc), "%.0f" % cap))
    df = pd.DataFrame(rows, columns=["period_end", "sleeve", "gross_trading_pnl", "financing_charge", "incentive_accrual", "net_pnl",
                                     "month_end_capital"])
    df = df.sort_values(["period_end", "sleeve"], kind="stable")
    _csv(df, os.path.join(tgt, F["admin"]))
    return len(df)


def register(B, tgt):
    W, d = B.W, B.days
    rows = []
    for p in sorted(W.pods, key=lambda p: (p["start"], B.last_code(p["n"]))):
        end = "" if p["end"] is None else d[p["end"] - 1].strftime("%Y-%m-%d")
        why = {"stopped": "Closed at the drawdown limit", "left": "PM team left the platform", None: "Active"}[p["why_end"]]
        rows.append((B.last_code(p["n"]), P.GROUPS[p["g"]]["name"], B.sub[p["n"]], d[p["start"]].strftime("%Y-%m-%d"), end, why))
    df = pd.DataFrame(rows, columns=["pod", "strategy_group", "sub_strategy", "first_trading_day", "last_trading_day", "status"])
    _csv(df, os.path.join(tgt, F["register"]))
    return len(df)


def changes(B, tgt):
    W, d = B.W, B.days
    pos = {t: i for i, t in enumerate(d)}
    rows = []
    for n, when, old, new, why in W.reviews:
        i = pos[when]
        eff = d[i + 1] if why.startswith(("halved", "closed", "PM team")) and i + 1 < len(d) else when
        rows.append((eff.strftime("%Y-%m-%d"), B.code(n, pos[eff] if eff in pos else i), "%.0f" % old, "%.0f" % new, why[0].upper() + why[1:]))
    df = pd.DataFrame(rows, columns=["effective_date", "pod", "capital_before_usd", "capital_after_usd", "reason"])
    df = df.sort_values(["effective_date", "pod"], kind="stable")
    _csv(df, os.path.join(tgt, F["changes"]))
    return len(df)


def plan_tables(B):
    """Each plan the committee approved, priced the way it always priced them: each pod's return on its capital over
    the three years to the end of November (or since it started), times its planned capital; a pod with less than six
    months of record takes its group's return over the same years."""
    W, d = B.W, B.days
    bill = W.mk.level.DTB3.reindex(d).ffill() / 100.0
    out = {}
    for y in P.PLAN_YEARS:
        plan = W.plans[y]
        cut = pd.Timestamp(y - 1, 11, 30)
        lo = cut - pd.DateOffset(years=3)
        m = (d > lo) & (d <= cut)
        groc = {}
        for g in P.GROUP_ORDER:
            rows = [p["n"] for p in W.pods if p["g"] == g]
            tot, cap = np.nansum(W.pnl[rows][:, m]), np.nansum(W.cap[rows][:, m])
            groc[g] = tot / cap * 252.0 if cap > 0 else 0.0
        b = float(bill[d <= cut].iloc[-1])
        rows = []
        for n in plan["pods"]:
            ok = m & ~np.isnan(W.pnl[n])
            g = W.pods[n]["g"]
            roc = np.nansum(W.pnl[n][ok]) / np.nansum(W.cap[n][ok]) * 252.0 if ok.sum() >= 126 else groc[g]
            k = plan["capital"][n]
            exp = roc * k
            rows.append(dict(n=n, code=B.code(n, plan["day"]), g=g, k=k, roc=roc, exp=exp, fund=P.FIN_SHARE * (b + P.FIN_SPREAD) * k,
                             onboarding=n not in plan["reviewed"] and W.pods[n]["start"] > 0))
        t = pd.DataFrame(rows).sort_values("code")
        pay = P.PAYOUT * float(np.maximum(t.exp - t.fund, 0.0).sum())
        out[y] = dict(table=t, bill=b, payouts=pay, funding=float(t.fund.sum()), costs=P.PLATFORM_COST[y],
                      net=float(t.exp.sum() - t.fund.sum()) - pay - P.PLATFORM_COST[y], approved=committee_date(y - 1))
    return out


def committee_date(year):
    """The allocation committee's December meeting: the second Tuesday of December."""
    t = pd.Timestamp(year, 12, 1)
    while t.weekday() != 1:
        t += pd.Timedelta(days=1)
    return t + pd.Timedelta(days=7)


def plans_workbook(B, tgt, tables):
    wb = Workbook()
    first = True
    for y in P.PLAN_YEARS:
        T = tables[y]
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = "Plan %d" % y
        ws.append(["Harbourne Capital: allocation plan for %d, approved by the allocation committee on %s" % (y, T["approved"].strftime("%-d %B %Y"))])
        ws.append([])
        ws.append(["Pod", "Strategy group", "Capital (USD m)", "Return on capital, record (%)", "Expected P&L (USD m)", "Note"])
        for r in T["table"].itertuples():
            ws.append([r.code, P.GROUPS[r.g]["name"], round(r.k / 1e6, 1), round(r.roc * 100, 2), round(r.exp / 1e6, 2),
                       "On onboarding schedule" if r.onboarding else None])
        ws.append([])
        ws.append(["Expected P&L, pods", None, round(T["table"].k.sum() / 1e6, 1), None, round(T["table"].exp.sum() / 1e6, 2)])
        ws.append(["Funding charge (bill rate %.2f%% plus 0.35%% on 20%% of capital)" % (T["bill"] * 100), None, None, None, round(-T["funding"] / 1e6, 2)])
        ws.append(["PM payouts at 18%", None, None, None, round(-T["payouts"] / 1e6, 2)])
        ws.append(["Platform costs", None, None, None, round(-T["costs"] / 1e6, 2)])
        ws.append(["Expected net P&L", None, None, None, round(T["net"] / 1e6, 2)])
        ws["A1"].font = Font(bold=True)
        for c in ws[3]:
            c.font = Font(bold=True)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        for row in ws.iter_rows(min_row=ws.max_row - 4, max_row=ws.max_row):
            row[0].font = Font(bold=row[0].row == ws.max_row)
        for col, w in zip("ABCDEF", (12, 22, 15, 16, 16, 24)):
            ws.column_dimensions[col].width = w
        ws.freeze_panes = "A4"
    path = os.path.join(tgt, F["plans"])
    wb.save(path)
    PP.normalize_ooxml(path, P.CFO, P.CFO, dt.datetime(2017, 12, 4, 15, 20, 41, tzinfo=UTC).strftime(ISO),
                       dt.datetime(2025, 12, 10, 17, 3, 12, tzinfo=UTC).strftime(ISO), excel=True, company=P.PLATFORM_LEGAL)
    return {y: len(tables[y]["table"]) for y in P.PLAN_YEARS}


def trading_days_2027():
    hol = ["2027-01-01", "2027-01-18", "2027-02-15", "2027-03-26", "2027-05-31", "2027-06-18", "2027-07-05", "2027-09-06",
           "2027-11-25", "2027-12-24"]
    return pd.DatetimeIndex([t for t in pd.bdate_range("2027-01-01", "2027-12-31") if t.strftime("%Y-%m-%d") not in hol])


def draft_workbook(B, tgt, draft):
    W = B.W
    days27 = trading_days_2027()
    wb = Workbook()
    ws = wb.active
    ws.title = "Draft 2027"
    ws.append(["Harbourne Capital: draft allocation plan for 2027, for the allocation committee (as of %s)" % P.REVIEW.strftime("%-d %B %Y")])
    ws.append([])
    ws.append(["Pod", "Strategy group", "Capital 2026 (USD m)", "Capital 2027, draft (USD m)", "Change", "Onboarding steps in 2027"])
    rows = []
    for n, r in draft.items():
        steps = ""
        if r["change"] == "onboarding":
            parts = []
            for lo, frac in P.RAMP[1:]:
                k = lo - r["age"]
                if 0 <= k < len(days27):
                    parts.append("%d%% of target from %s" % (round(frac * 100), days27[k].strftime("%-d %B")))
            steps = "; ".join(parts)
        label = {"increase": "Increase", "decrease": "Decrease", "unchanged": "No change", "onboarding": "Onboarding"}[r["change"]]
        rows.append((B.last_code(n), P.GROUPS[W.pods[n]["g"]]["name"], round(r["k2026"] / 1e6, 1), round(r["k2027"] / 1e6, 1), label, steps or None))
    for row in sorted(rows):
        ws.append(list(row))
    ws.append([])
    ws.append(["Total", None, round(sum(r["k2026"] for r in draft.values()) / 1e6, 1), round(sum(r["k2027"] for r in draft.values()) / 1e6, 1)])
    ws["A1"].font = Font(bold=True)
    for c in ws[3]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    for col, w in zip("ABCDEF", (10, 22, 14, 16, 12, 52)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A4"
    wc = wb.create_sheet("Platform costs 2027")
    wc.append(["Platform costs in the 2027 budget"])
    wc.append([])
    wc.append(["Line", "USD m"])
    for name, v in P.COST_LINES_2027:
        wc.append([name, round(v / 1e6, 1)])
    wc.append(["Total", round(P.PLATFORM_COST_2027 / 1e6, 1)])
    wc["A1"].font = Font(bold=True)
    for c in wc[3]:
        c.font = Font(bold=True)
    wc.cell(row=wc.max_row, column=1).font = Font(bold=True)
    wc.column_dimensions["A"].width = 34
    wc.column_dimensions["B"].width = 10
    path = os.path.join(tgt, F["draft"])
    wb.save(path)
    PP.normalize_ooxml(path, P.CIO, P.CFO, dt.datetime(2026, 10, 26, 13, 51, 9, tzinfo=UTC).strftime(ISO),
                       dt.datetime(2026, 11, 9, 14, 37, 55, tzinfo=UTC).strftime(ISO), excel=True, company=P.PLATFORM_LEGAL)
    return len(rows)


def market_files(tgt):
    """Each public series as published, cut at the record's last day."""
    out = {}
    for name in MARKET:
        src = os.path.join(MK.RAW, name)
        lines = open(src, newline="").read().splitlines(keepends=True)
        keep = [lines[0]]
        for ln in lines[1:]:
            day = ln.split(",", 1)[0]
            t = pd.Timestamp(dt.datetime.strptime(day, "%m/%d/%Y") if "/" in day else day)
            if t <= P.LAST_DAY:
                keep.append(ln)
        open(os.path.join(tgt, name), "w", newline="").write("".join(keep))
        out[name] = len(keep) - 1
    return out


def write(W, tgt):
    B = Books(W)
    info = {}
    info["legacy_rows"], info["current_rows"] = risk_files(B, tgt)
    info["code_map_rows"] = code_map(B, tgt)
    info["admin_rows"] = admin(B, tgt)
    info["register_rows"] = register(B, tgt)
    info["change_rows"] = changes(B, tgt)
    tables = plan_tables(B)
    info["plan_rows"] = plans_workbook(B, tgt, tables)
    draft = W.draft(P.BUDGET_PLAN, P.LEAD)
    info["draft_rows"] = draft_workbook(B, tgt, draft)
    DC.policy(os.path.join(tgt, F["policy"]))
    DC.risk_model(os.path.join(tgt, F["riskmodel"]))
    info["market_rows"] = market_files(tgt)
    PP.own_mtimes(tgt, EXPORT_TIMES)
    return info, B, tables, draft
