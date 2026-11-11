"""task9 (architecture 10): the pack under target/, written from the World as each system would export it.

  the platform's request audit for the desk, in two generations (the April 2025 migration renamed columns, moved
  timestamps from New York time to UTC and stated quantities in thousands; re-sent and amended messages carried);
  the desk's blotter; the public trade tape (dissemination delays, capped sizes, cancels, corrections, late reports,
  dealer-to-dealer trades from both sides); Ashcote's evaluated prices; the security master with its quarterly
  liquidity buckets and the 144A exchange map; issuer ratings; the client list; the auto-quoter's schedule versions
  and the 2027 draft; the desk's month-end summaries; the platform's league tables; the quoting policy; the public
  market series as published.
"""
import datetime as dt
import os
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

import docs as DC
import market as MK
import params as P
import postprocess as PP

UTC = dt.timezone.utc
NY = ZoneInfo(P.ZONE)
ISO = "%Y-%m-%dT%H:%M:%SZ"
F = {
    "rfq1": "tidewell_rfq_audit_brindlemoor_20230103_20250404.csv",
    "rfq2": "tidewell_rfq_audit_brindlemoor_20250407_20261106.csv",
    "blotter": "brindlemoor_credit_blotter_2023_2026.csv",
    "tape": "public_trade_tape_corporates_2023_2026.csv",
    "eval": "ashcote_evaluated_prices_2023_2026.csv",
    "master": "security_master_20261106.csv",
    "buckets": "security_master_liquidity_buckets.csv",
    "ratings": "issuer_ratings_history.csv",
    "clients": "tidewell_client_list_20261106.csv",
    "schedule": "auto_quoter_schedule_versions.xlsx",
    "draft": "auto_quoter_schedule_2027_draft.xlsx",
    "summaries": "credit_desk_month_end_summaries.xlsx",
    "league": "tidewell_dealer_league_tables_2026.xlsx",
    "policy": "Credit_Electronic_Quoting_Policy_2026.pdf",
}
MARKET = [k + ".csv" for k in MK.FRED_IDS] + [k + "_History.csv" for k in MK.CBOE_IDS]
DISTRACTORS = ["SOFR.csv", "SPX_History.csv", F["league"]]
STATUS1 = {"DONE": "Done", "COVER": "Covered", "TRADED_AWAY": "Traded Away", "DNT": "Done Not Traded", "PASSED": "Passed"}
STATUS2 = {"DONE": "D", "COVER": "C", "TRADED_AWAY": "TA", "DNT": "DNT", "PASSED": "P"}
TYPE_NAME = {"AM": "Asset manager", "INS": "Insurer", "HF": "Hedge fund", "RET": "Wealth platform"}
EVAL_HALF = {("IG", "liquid"): 0.02, ("IG", "medium"): 0.04, ("IG", "thin"): 0.07,
             ("HY", "liquid"): 0.06, ("HY", "medium"): 0.12, ("HY", "thin"): 0.22}
EXPORT_TIMES = {
    F["rfq1"]: dt.datetime(2025, 4, 7, 6, 12, 44, tzinfo=UTC), F["rfq2"]: dt.datetime(2026, 11, 9, 11, 31, 5, tzinfo=UTC),
    F["blotter"]: dt.datetime(2026, 11, 9, 11, 36, 52, tzinfo=UTC), F["tape"]: dt.datetime(2026, 11, 9, 11, 48, 20, tzinfo=UTC),
    F["eval"]: dt.datetime(2026, 11, 9, 11, 52, 9, tzinfo=UTC), F["master"]: dt.datetime(2026, 11, 9, 11, 39, 41, tzinfo=UTC),
    F["buckets"]: dt.datetime(2026, 10, 1, 13, 4, 17, tzinfo=UTC), F["ratings"]: dt.datetime(2026, 11, 9, 11, 40, 3, tzinfo=UTC),
    F["clients"]: dt.datetime(2026, 11, 9, 11, 33, 58, tzinfo=UTC),
}
for _k, _name in enumerate(MARKET):   # the review morning's pull, a few seconds apart
    EXPORT_TIMES[_name] = dt.datetime(2026, 11, 9, 12, 2, 0, tzinfo=UTC) + dt.timedelta(seconds=7 * _k + 3)


def _csv(df, path):
    df.to_csv(path, index=False, lineterminator="\r\n")


def _stamp(day, hour):
    """A New York wall-clock time on a record day, as an aware datetime."""
    secs = int(round(hour * 3600))
    return dt.datetime(day.year, day.month, day.day, tzinfo=NY) + dt.timedelta(seconds=secs)


class Books:
    """Identifiers for the pack, from the World."""

    def __init__(self, W):
        self.W = W
        self.days = W.mk.days
        B = W.B
        self.cusip0 = B.cusip.values
        self.cusip_reg = B.cusip_reg.values
        self.exch = [None if pd.isna(e) else pd.Timestamp(e) for e in B.exchange_date.values]

    def cusip(self, b, t):
        e = self.exch[b]
        if e is not None and self.days[t] >= e:
            return self.cusip_reg[b]
        return self.cusip0[b]


def _num(x, nd=3):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), nd)


def rfq_files(B, tgt, rng):
    W = B.W
    R = W.req
    days = B.days
    rows = []
    for r in R.itertuples(index=False):
        ts = _stamp(days[r.t], r.hour)
        ex = ts + dt.timedelta(seconds=int(rng.integers(15, 75))) if r.status == "DONE" else None
        rows.append(dict(rfq=int(r.rfq), ts=ts, cusip=B.cusip(int(r.bond), int(r.t)), client=W.C.code.values[int(r.client) - 1],
                         side="BUY" if r.side > 0 else "SELL", q=float(r.q), n=int(r.n), quote=_num(r.quote),
                         ref=round(float(r.ref_mid), 3), status=r.status, done=_num(r.done_price), cover=_num(r.cover),
                         ex=ex, version=1))
    df = pd.DataFrame(rows)
    # re-sent messages (identical rows) and amended requests (an earlier version of the request, another size)
    dup = df.sample(frac=0.004, random_state=int(rng.integers(1e9)))
    amd = df.sample(frac=0.003, random_state=int(rng.integers(1e9))).copy()
    df.loc[amd.index, "version"] = 2
    amd["q"] = (amd["q"] * rng.choice([0.5, 2.0], len(amd))).round(-3)
    amd["version"] = 1
    amd["quote"], amd["status"], amd["done"], amd["cover"], amd["ex"] = None, "PASSED", None, None, None
    df = pd.concat([df, dup, amd]).sort_values(["ts", "rfq", "version"], kind="mergesort").reset_index(drop=True)
    cut = pd.Timestamp(P.MIGRATION).tz_localize(NY)
    g1 = df[df.ts < cut]
    g2 = df[df.ts >= cut]

    def et(x):
        return x.strftime("%Y-%m-%d %H:%M:%S") if x is not None and not pd.isna(x) else None

    def ut(x):
        return x.astimezone(UTC).strftime(ISO) if x is not None and not pd.isna(x) else None
    out1 = pd.DataFrame({
        "RFQ_ID": g1.rfq, "MSG_VERSION": g1.version, "RECEIVED_ET": g1.ts.map(et), "CUSIP": g1.cusip,
        "CLIENT_CODE": g1.client, "CLIENT_SIDE": g1.side, "QTY": g1.q.round(0).astype(int), "DEALERS_IN_COMP": g1.n,
        "DESK_RESPONSE_PX": g1.quote, "DESK_REF_MID": g1.ref, "STATUS": g1.status.map(STATUS1), "DONE_PX": g1.done,
        "COVER_PX": g1.cover, "TRADE_TIME_ET": g1.ex.map(et)})
    out2 = pd.DataFrame({
        "rfq_ref": g2.rfq, "msg_version": g2.version, "received_utc": g2.ts.map(ut), "security_id": g2.cusip,
        "client": g2.client, "dir": g2.side.map({"BUY": "CB", "SELL": "CS"}), "quantity_000": (g2.q / 1000.0).round(3),
        "n_dealers": g2.n, "response_price": g2.quote, "ref_mid": g2.ref, "outcome": g2.status.map(STATUS2),
        "executed_price": g2.done, "cover_price": g2.cover, "executed_utc": g2.ex.map(ut)})
    _csv(out1, os.path.join(tgt, F["rfq1"]))
    _csv(out2, os.path.join(tgt, F["rfq2"]))
    return len(out1), len(out2)


def blotter(B, tgt, rng):
    W = B.W
    days = B.days
    rows = []
    for r in W.trades.itertuples(index=False):
        ts = _stamp(days[r.t], r.hour)
        rows.append(dict(trade_id="BC%07d" % int(r.trade), trade_date=days[r.t].strftime("%Y-%m-%d"),
                         exec_time_et=ts.strftime("%H:%M:%S"), cusip=B.cusip(int(r.bond), int(r.t)),
                         desk_side="BUY" if r.side > 0 else "SELL", quantity=int(round(r.q)), price=round(float(r.price), 3),
                         counterparty=("CLIENT" if r.cpty == "client" else "DEALER"),
                         venue=("TIDEWELL" if r.cpty == "client" else "D2D"),
                         rfq_id=(int(r.rfq) if r.rfq is not None and not pd.isna(r.rfq) else None), status="LIVE"))
    df = pd.DataFrame(rows)
    # a few bookings corrected the same day: the first entry cancelled and booked again
    fix = df.sample(frac=0.002, random_state=int(rng.integers(1e9))).copy()
    df.loc[fix.index, "status"] = "CANCELLED"
    fix["trade_id"] = [t + "R" for t in fix.trade_id]
    df = pd.concat([df, fix]).sort_values(["trade_date", "exec_time_et", "trade_id"], kind="mergesort").reset_index(drop=True)
    df["rfq_id"] = df["rfq_id"].astype("Int64")
    _csv(df, os.path.join(tgt, F["blotter"]))
    return len(df)


def tape(B, tgt, rng):
    W = B.W
    days = B.days
    Pr = W.prints.sort_values(["t", "hour"], kind="mergesort")
    ig = W.ig
    msgs = []
    seq = 7_000_000
    for r in Pr.itertuples(index=False):
        b, t = int(r.bond), int(r.t)
        band = "IG" if ig[t, b] else "HY"
        ex = _stamp(days[t], r.hour)
        qty = ("5MM+" if band == "IG" else "1MM+") if r.q > P.CAP[band] else str(int(round(r.q)))
        sides = ["B" if r.dealer_side > 0 else "S"] if r.kind == "C" else ["B", "S"]
        for sd in sides:
            seq += int(rng.integers(1, 4))
            delay = rng.exponential(25) if rng.random() < 0.93 else rng.uniform(60, 900)
            asof = rng.random() < P.ASOF_P
            dis = ex + dt.timedelta(seconds=float(delay)) + (dt.timedelta(days=int(rng.integers(1, 4))) if asof else dt.timedelta(0))
            px = round(float(r.price), 3)
            m = dict(msg_seq=seq, cusip=B.cusip(b, t), exec_date=ex.strftime("%Y-%m-%d"), exec_time=ex.strftime("%H:%M:%S"),
                     dissem_ts=dis.strftime("%Y-%m-%d %H:%M:%S"), price=px, qty=qty, rpt_side=sd,
                     contra=("C" if r.kind == "C" else "D"), asof=("A" if asof else ""), msg_type="T", orig_seq=None)
            u = rng.random()
            if u < P.CORRECT_P:
                wrong = dict(m)
                wrong["price"] = round(px + rng.choice([-1, 1]) * rng.choice([0.1, 0.5, 1.0, 10.0]), 3)
                msgs.append(wrong)
                seq += int(rng.integers(5, 400))
                fixm = dict(m)
                fixm.update(msg_seq=seq, msg_type="C", orig_seq=wrong["msg_seq"],
                            dissem_ts=(dis + dt.timedelta(minutes=int(rng.integers(5, 240)))).strftime("%Y-%m-%d %H:%M:%S"))
                msgs.append(fixm)
            elif u < P.CORRECT_P + P.CANCEL_P:
                msgs.append(m)
                bad = dict(m)
                seq += int(rng.integers(1, 3))
                bad.update(msg_seq=seq, price=round(px + rng.normal(0, 0.4), 3))
                msgs.append(bad)                            # a duplicate report, cancelled later
                seq += int(rng.integers(5, 400))
                x = dict(bad)
                x.update(msg_seq=seq, msg_type="X", orig_seq=bad["msg_seq"],
                         dissem_ts=(dis + dt.timedelta(minutes=int(rng.integers(5, 300)))).strftime("%Y-%m-%d %H:%M:%S"))
                msgs.append(x)
            else:
                msgs.append(m)
    df = pd.DataFrame(msgs)
    df["orig_seq"] = df["orig_seq"].astype("Int64")
    df = df.sort_values(["dissem_ts", "msg_seq"], kind="mergesort").reset_index(drop=True)
    _csv(df, os.path.join(tgt, F["tape"]))
    return len(df)


def evaluations(B, tgt):
    W = B.W
    rows = []
    for t, d in enumerate(B.days):
        ds = d.strftime("%Y-%m-%d")
        bk = W.bucket_hist[t][1]
        for b in np.where(W.alive[t])[0]:
            band = "IG" if W.ig[t, b] else "HY"
            mid = float(W.eval_mid[t, b])
            h = EVAL_HALF[(band, bk[b])]
            rows.append((ds, B.cusip(b, t), round(mid - h, 3), round(mid, 3), round(mid + h, 3)))
    df = pd.DataFrame(rows, columns=["eval_date", "cusip", "eval_bid", "eval_mid", "eval_ask"])
    _csv(df, os.path.join(tgt, F["eval"]))
    return len(df)


def master(B, tgt):
    W = B.W
    Bd = W.B
    iss = W.issuers
    rows = []
    for _, b in Bd.iterrows():
        rows.append(dict(cusip=b["cusip"], issuer=iss.name[b["issuer"]], sector=iss.sector[b["issuer"]],
                         coupon_pct=round(b["coupon"] * 100, 3), maturity=b["maturity"].strftime("%Y-%m-%d"),
                         issue_date=b["issue"].strftime("%Y-%m-%d"), amount_outstanding=int(b["amount"]),
                         rule_144a=("Y" if b["is144a"] else "N"), registered_cusip=(b["cusip_reg"] or None),
                         exchange_date=(b["exchange_date"].strftime("%Y-%m-%d") if not pd.isna(b["exchange_date"]) else None)))
    _csv(pd.DataFrame(rows), os.path.join(tgt, F["master"]))
    # the quarterly buckets the security master assigns, from the quarter before's prints
    brows = []
    seen = set()
    for t, (q, bk) in enumerate(W.bucket_hist):
        if q in seen:
            continue
        seen.add(q)
        qdays = np.where(B.days.to_period("Q") == q)[0]
        live = W.alive[qdays].any(axis=0)
        for b in np.where(live)[0]:
            tb = qdays[np.argmax(W.alive[qdays, b])]
            brows.append(dict(quarter=str(q), cusip=B.cusip(b, tb), liquidity_bucket=bk[b]))
    _csv(pd.DataFrame(brows), os.path.join(tgt, F["buckets"]))
    # issuer ratings as they changed
    rrows = []
    for i in range(P.N_ISSUERS):
        last = None
        for t in range(W.T):
            r = W.rating[t, i]
            if r != last:
                rrows.append(dict(issuer=iss.name[i], effective_date=B.days[t].strftime("%Y-%m-%d") if last else "2022-12-30",
                                  rating=r))
                last = r
    _csv(pd.DataFrame(rrows), os.path.join(tgt, F["ratings"]))
    return len(rows), len(brows), len(rrows)


def clients(B, tgt):
    C = B.W.C
    df = pd.DataFrame({"client_code": C.code, "client_type": C.ctype.map(TYPE_NAME),
                       "onboarded": C.onboard.dt.strftime("%Y-%m-%d")}).sort_values("client_code")
    _csv(df, os.path.join(tgt, F["clients"]))
    return len(df)


def schedule_tables():
    v1 = {(b, l, t): P.SCHEDULE_V1[(b, l)][t] for b, l, t in P.SEGMENTS}
    v2 = {**v1, **P.V2_CHANGES}
    v3 = {**v2, **P.V3_CHANGES}
    v4 = {**v3, **P.PROPOSED}
    return v1, v2, v3, v4


def _schedule_sheet(ws, title, sched, effective):
    ws.append([title])
    ws.append(["Effective from %s" % effective])
    ws.append([])
    ws.append(["Rating band", "Liquidity bucket", "Client type", "Half-spread (cents per 100 face)"])
    for band, bk, ty in P.SEGMENTS:
        ws.append([band, bk, TYPE_NAME[ty], sched[(band, bk, ty)]])
    ws.append([])
    ws.append(["Multiples"])
    ws.append(["Investment grade over 5,000,000 face", 1.30])
    ws.append(["High yield over 1,000,000 face", 1.20])
    ws.append(["Any request under 100,000 face", 1.50])
    ws.append(["VIX at the prior close under 20", 1.0])
    ws.append(["VIX at the prior close from 20 to under 30", 1.3])
    ws.append(["VIX at the prior close of 30 or more", 1.7])
    ws.append([])
    ws.append(["Distance = half-spread x size multiple x VIX multiple x (1 + jitter) x (1 - 0.35 x position / limit x "
               "direction), in cents per 100 face from the reference mid"])
    ws.append(["Jitter: normal, standard deviation 6 per cent, held within 2.5 standard deviations"])
    ws.append(["Direction: +1 when the client buys, -1 when the client sells; position limit 25,000,000 face investment "
               "grade, 10,000,000 high yield; at the limit the desk passes"])
    ws["A1"].font = Font(bold=True)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for col, w in zip("ABCD", (30, 16, 18, 18)):
        ws.column_dimensions[col].width = w


def schedule_workbooks(tgt):
    v1, v2, v3, v4 = schedule_tables()
    wb = Workbook()
    ws = wb.active
    ws.title = "v1"
    _schedule_sheet(ws, "Auto-quoter schedule, version 1", v1, "3 January 2023")
    _schedule_sheet(wb.create_sheet("v2"), "Auto-quoter schedule, version 2", v2, "1 July 2024")
    _schedule_sheet(wb.create_sheet("v3"), "Auto-quoter schedule, version 3", v3, "3 March 2025")
    path = os.path.join(tgt, F["schedule"])
    wb.save(path)
    PP.normalize_ooxml(path, P.STRAT, P.STRAT, dt.datetime(2022, 12, 19, 15, 2, 33, tzinfo=UTC).strftime(ISO),
                       dt.datetime(2025, 2, 27, 21, 18, 6, tzinfo=UTC).strftime(ISO), excel=True, company=P.FIRM)
    wb = Workbook()
    ws = wb.active
    ws.title = "Draft 2027"
    _schedule_sheet(ws, "Auto-quoter schedule, draft for 2027", v4, "4 January 2027, if the committee approves it")
    path = os.path.join(tgt, F["draft"])
    wb.save(path)
    PP.normalize_ooxml(path, P.STRAT, P.HEAD, dt.datetime(2026, 10, 28, 14, 40, 12, tzinfo=UTC).strftime(ISO),
                       dt.datetime(2026, 11, 6, 22, 5, 49, tzinfo=UTC).strftime(ISO), excel=True, company=P.FIRM)


def summaries(B, tgt):
    """The desk's month-end summaries by segment: its own next-day view."""
    W = B.W
    R = W.req.copy()
    R["month"] = B.days[R.t.values].to_period("M")
    D = R[R.status == "DONE"].copy()
    t1 = np.minimum(D.t.values + 1, W.T - 1)
    D["edge"] = D.side * (D.done_price - D.ref_mid) * D.q / 100.0
    # the desk's side is the opposite of the client's: its markout is desk_side x (later mid - reference mid)
    D["mk1"] = (-D.side) * (W.eval_mid[t1, D.bond.values] - D.ref_mid) * D.q / 100.0
    wb = Workbook()
    first = True
    for m in sorted(R.month.unique()):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = m.strftime("%Y-%m")
        ws.append(["%s: month-end summary, %s" % (P.DESK, m.strftime("%B %Y"))])
        ws.append(["Next-day markout: the evaluated mid at the next close against the reference mid, on the desk's side"])
        ws.append([])
        ws.append(["Rating band", "Liquidity bucket", "Client type", "Requests", "Done", "Face done (USD m)",
                   "Edge at execution (USD)", "Next-day markout (USD)", "Net, next-day view (USD)"])
        rm = R[R.month == m]
        dm = D[D.month == m]
        for band, bk, ty in P.SEGMENTS:
            a = rm[(rm.band == band) & (rm.bucket == bk) & (rm.ty == ty)]
            d = dm[(dm.band == band) & (dm.bucket == bk) & (dm.ty == ty)]
            ws.append([band, bk, TYPE_NAME[ty], len(a), len(d), round(d.q.sum() / 1e6, 2), round(d.edge.sum(), 0),
                       round(d.mk1.sum(), 0), round(d.edge.sum() + d.mk1.sum(), 0)])
        for c in ws[4]:
            c.font = Font(bold=True)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        ws["A1"].font = Font(bold=True)
        for col, w in zip("ABCDEFGHI", (12, 14, 16, 10, 8, 14, 16, 16, 16)):
            ws.column_dimensions[col].width = w
    path = os.path.join(tgt, F["summaries"])
    wb.save(path)
    PP.normalize_ooxml(path, P.STRAT, P.STRAT, dt.datetime(2023, 2, 1, 23, 14, 5, tzinfo=UTC).strftime(ISO),
                       dt.datetime(2026, 11, 3, 22, 41, 37, tzinfo=UTC).strftime(ISO), excel=True, company=P.FIRM)


def league(B, tgt, rng):
    """Tidewell's monthly dealer league tables for 2026 (shares of the platform's executed face)."""
    wb = Workbook()
    first = True
    base = np.array(P.DEALER_WEIGHT) * 0.86
    for m in pd.period_range("2026-01", "2026-10", freq="M"):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = m.strftime("%Y-%m")
        sh = np.r_[base, 0.105] * np.exp(rng.normal(0, 0.06, len(base) + 1))
        sh = sh / sh.sum() * 100
        names = ["Dealer %s" % d for d in P.DEALERS] + [P.FIRM]
        ws.append(["Tidewell Credit Network: dealer league table, %s (share of executed face, all protocols)" % m.strftime("%B %Y")])
        ws.append([])
        ws.append(["Rank", "Dealer", "Share (%)"])
        for k, j in enumerate(np.argsort(-sh)):
            ws.append([k + 1, names[j], round(float(sh[j]), 1)])
        ws["A1"].font = Font(bold=True)
    path = os.path.join(tgt, F["league"])
    wb.save(path)
    PP.normalize_ooxml(path, "Tidewell Reporting", "Tidewell Reporting", dt.datetime(2026, 2, 3, 9, 0, 12, tzinfo=UTC).strftime(ISO),
                       dt.datetime(2026, 11, 4, 9, 0, 41, tzinfo=UTC).strftime(ISO), excel=True, company=P.PLATFORM)


def market_files(tgt):
    out = {}
    last = pd.Timestamp(P.END)
    for name in MARKET:
        lines = open(os.path.join(MK.RAW, name), newline="").read().splitlines(keepends=True)
        keep = [lines[0]]
        for ln in lines[1:]:
            day = ln.split(",", 1)[0]
            t = pd.Timestamp(dt.datetime.strptime(day, "%m/%d/%Y") if "/" in day else day)
            if t <= last:
                keep.append(ln)
        open(os.path.join(tgt, name), "w", newline="").write("".join(keep))
        out[name] = len(keep) - 1
    return out


def write(W, tgt):
    rng = np.random.default_rng(P.SEED + 7)
    B = Books(W)
    info = {}
    info["rfq_rows"] = rfq_files(B, tgt, rng)
    info["blotter_rows"] = blotter(B, tgt, rng)
    info["tape_rows"] = tape(B, tgt, rng)
    info["eval_rows"] = evaluations(B, tgt)
    info["master_rows"] = master(B, tgt)
    info["client_rows"] = clients(B, tgt)
    schedule_workbooks(tgt)
    summaries(B, tgt)
    league(B, tgt, rng)
    DC.policy(os.path.join(tgt, F["policy"]))
    info["market_rows"] = market_files(tgt)
    PP.own_mtimes(tgt, EXPORT_TIMES)
    return info, B
