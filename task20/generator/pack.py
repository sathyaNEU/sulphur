"""task20 pack: the records Tarrant Hale Securities' systems hold for the Small and Mid Cap Facilitation desk, written
from a simulated World on the published S&P 500 and Nasdaq-100 tape. Every file is what its system would export: the
vendor's closes, the two position systems' nightly extracts, the order management blotter, product control's daily
P&L, the general ledger, the risk engine's run log and mapping, the quarterly backtest and the limit and stress
reports. Nothing here decides a result on its own; analysis.py reads only what this module writes."""
import csv
import datetime as dt
import os
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

import world as W

NY = ZoneInfo("America/New_York")
SEED = 1114
BOOK = "SMCF1"
FBOOK = "SMCF1F"
CUTOVER = pd.Timestamp("2025-01-17")          # the last business day on EQX v1; v2 replays it
TICKER_CHANGE = pd.Timestamp("2023-09-18")
VENDOR_RESENT = (pd.Timestamp("2023-03-14"), pd.Timestamp("2024-11-26"))
BLOTTER_EXPORTED = dt.datetime(2025, 7, 8, 7, 12, 40, tzinfo=NY)

F_VENDOR = "vendor_eod_closes_SMCF_universe_2022-05-31_2025-06-30.csv"
F_SPX = "SPX_History.csv"
F_NDX = "NASDAQ100.csv"
F_SETTLE = "cme_es_nq_daily_settlements_2024-06-27_2025-06-30.csv"
F_MASTER = "smcf_instrument_master_2025-06-30.csv"
F_MAP = "ere_proxy_mapping_vintages_2024Q2_2025Q2.csv"
F_EQX1 = "eqx_position_extract_v1_2024-06-28_2025-01-17.csv"
F_EQX2 = "eqx_position_extract_v2_2025-01-17_2025-06-30.csv"
F_XWALK = "eqx_v2_instrument_crosswalk.csv"
F_FUTS = "futs_position_snapshots_2024-06-28_2025-06-30.csv"
F_BLOTTER = "oms_trade_blotter_SMCF_2024-07-01_2025-06-30.csv"
F_PC = "pc_daily_pnl_SMCF_2024-07-01_2025-06-30.csv"
F_GL = "gl_journal_SMCF_2024-07_2025-06.csv"
F_RUNLOG = "ere_run_log_SMCF_2024-06-28_2025-06-30.csv"
F_LIMITS = "var_limit_utilisation_SMCF_2024-07-01_2025-06-30.csv"

SECTOR_SUFFIX = {
    "Technology": ["Systems", "Software", "Semiconductor", "Networks", "Technologies", "Data"],
    "Health Care": ["Therapeutics", "Biosciences", "Medical", "Pharmaceuticals", "Health", "Diagnostics"],
    "Financials": ["Bancorp", "Financial", "Capital", "Bancshares", "Holdings"],
    "Industrials": ["Industries", "Manufacturing", "Aerospace", "Logistics", "Machinery"],
    "Consumer Discretionary": ["Brands", "Outfitters", "Restaurants", "Home", "Motors", "Leisure"],
    "Communication Services": ["Media", "Communications", "Interactive", "Entertainment"],
    "Energy": ["Energy", "Resources", "Petroleum", "Midstream"],
    "Materials": ["Materials", "Chemicals", "Minerals", "Packaging"],
    "Consumer Staples": ["Foods", "Beverage", "Farms", "Products"],
    "Real Estate": ["Realty", "Properties", "Residential", "Trust"],
}
ROOT_A = ["Al", "Bel", "Cal", "Dor", "El", "Fen", "Gal", "Hal", "Jor", "Kel", "Lor", "Mar", "Nor", "Pel", "Quin", "Ros",
          "Sal", "Tor", "Val", "Wes", "Yor", "Zan", "Ash", "Brin", "Cor", "Dun", "Ever", "Fair", "Glen", "Har", "Kin",
          "Lark", "Mor", "Nev", "Oak", "Pine", "Red", "Stan", "Thorn", "Vern", "Wil", "Ard", "Bram", "Carr", "Del",
          "Esk", "Fal", "Gren", "Hol", "Ing", "Lin", "Mead", "Nash", "Orm", "Pres", "Rand", "Sher", "Tam", "Wyn"]
ROOT_B = ["ton", "ford", "more", "ridge", "field", "dale", "wick", "stead", "haven", "mont", "bury", "crest", "gate",
          "land", "worth", "view", "brook", "port", "well", "ara", "ion", "ova", "ex", "en", "ar", "ell", "is", "an"]
CLIENTS = ["CL%04d" % i for i in (1012, 1047, 1088, 1103, 1129, 1164, 1190, 1215, 1233, 1260, 1301, 1322, 1359, 1377,
                                   1402, 1418, 1455, 1491, 1517, 1544, 1568, 1590, 1622, 1645, 1671, 1708, 1733, 1756,
                                   1790, 1812, 1845, 1866, 1893, 1920, 1948, 1971)]


def biz_days():
    """the exchange calendar the desk runs on: the record's days and the second half of 2025"""
    return list(W.DATES) + list(W.FUTURE_DAYS)


def ny(d, minutes):
    """an aware New York timestamp on business date d, `minutes` after midnight (seconds resolution)"""
    secs = int(round(minutes * 60.0))
    base = dt.datetime(d.year, d.month, d.day, tzinfo=NY)
    return base + dt.timedelta(seconds=secs)


def iso(t):
    return t.isoformat()


def utc(t):
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def make_names(w):
    """the desk's universe: tickers, issuers, segments, sectors, the vendor's and EQX's ids, the desk start dates"""
    rn = np.random.default_rng(70214)
    used_t, used_n, rows = set(), set(), []
    for i in range(w.N):
        sec = W.SECTORS[w.sec[i]]
        while True:
            root = ROOT_A[int(rn.integers(len(ROOT_A)))] + ROOT_B[int(rn.integers(len(ROOT_B)))]
            if root not in used_n:
                used_n.add(root)
                break
        suf = SECTOR_SUFFIX[sec][int(rn.integers(len(SECTOR_SUFFIX[sec])))]
        form = int(rn.integers(4))
        issuer = "%s %s%s" % (root, suf, {0: " Inc.", 1: " Corp.", 2: ", Inc.", 3: ""}[form])
        letters = [c for c in root.upper() if c.isalpha()]
        while True:
            k = 4
            pick = [letters[0]] + list(rn.choice(letters[1:] + list("ABCDEFGHIKLMNOPRSTVWXY"), k - 1))
            t = "".join(pick)
            if t not in used_t:
                used_t.add(t)
                break
        if w.onboard[i] >= 0:
            start = W.DATES[w.onboard[i]]
        else:
            start = pd.Timestamp("2016-03-01") + pd.Timedelta(days=int(rn.integers(0, 365 * 6)))
            while start.weekday() >= 5:
                start += pd.Timedelta(days=1)
        rows.append(dict(i=i, ticker=t, issuer=issuer, segment="Mid cap" if w.seg[i] == "MID" else "Small cap",
                         sector=sec, vendor_id="VZ%08d" % int(rn.integers(10_000_000, 99_999_999)),
                         eqx_v1="E%06d" % int(rn.integers(100_000, 999_999)),
                         eqx_v2="TH-%07d" % int(rn.integers(1_000_000, 9_999_999)),
                         listing=["Nasdaq GS", "Nasdaq GM", "Nasdaq CM"][0 if w.seg[i] == "MID" else int(rn.integers(1, 3))],
                         desk_start=start.date().isoformat(), prior_ticker="", ticker_changed=""))
    # one legacy mid cap renamed in September 2023: the vendor carries its old ticker before the change
    legacy_mid = [r["i"] for r in rows if w.onboard[r["i"]] < 0 and w.seg[r["i"]] == "MID" and r["i"] not in
                  {p for pr in w.pairs for p in pr}]
    j = legacy_mid[int(rn.integers(len(legacy_mid)))]
    old = rows[j]["ticker"]
    new = old[0] + "".join(rn.choice(list("ABCDEFGHKLMNPRSTVWXZ"), len(old) - 1))
    while new in used_t:
        new = old[0] + "".join(rn.choice(list("ABCDEFGHKLMNPRSTVWXZ"), len(old) - 1))
    rows[j].update(ticker=new, prior_ticker=old, ticker_changed=TICKER_CHANGE.date().isoformat())
    df = pd.DataFrame(rows).set_index("i")
    assert df.ticker.is_unique and df.vendor_id.is_unique and df.eqx_v1.is_unique and df.eqx_v2.is_unique
    return df


def ticker_on(names, i, d):
    r = names.loc[i]
    if r.prior_ticker and d < pd.Timestamp(r.ticker_changed):
        return r.prior_ticker
    return r.ticker


def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)
    return len(rows)


def money(x):
    return "%.2f" % x


def write_vendor(path, w, names):
    rv = np.random.default_rng(91407)
    adv = np.exp(rv.normal(np.log(np.where(w.seg == "MID", 900_000, 260_000)), 0.5))
    rows = []
    for t, d in enumerate(W.DATES):
        day = []
        vol = np.maximum(1000, np.round(adv * np.exp(rv.normal(0, 0.45, w.N))))
        for i in range(w.N):
            day.append([names.loc[i, "vendor_id"], ticker_on(names, i, d), d.date().isoformat(), "%.2f" % w.PX[t, i],
                        "%d" % vol[i], "USD", "XNAS"])
        rows.extend(day)
        if d in VENDOR_RESENT:
            rows.extend([list(r) for r in day])      # the vendor re-sent the day's file; both copies loaded
    return write_csv(path, ["vendor_id", "ticker", "price_date", "close", "volume", "currency", "mic"], rows)


def write_index_files(tgt):
    """the published Cboe and FRED downloads, cut at the quarter end, values untouched"""
    out = {}
    for name in (F_SPX, F_NDX):
        lines = open(os.path.join(W.RAW, name)).read().splitlines()
        keep = [lines[0]]
        for ln in lines[1:]:
            d = ln.split(",")[0]
            day = pd.Timestamp(dt.datetime.strptime(d, "%m/%d/%Y")) if "/" in d else pd.Timestamp(d)
            if day <= W.WIN_END:
                keep.append(ln)
        open(os.path.join(tgt, name), "w").write("\n".join(keep) + "\n")
        out[name] = len(keep) - 1
    return out


def write_settlements(path, w):
    days = [d for d in W.DATES if pd.Timestamp("2024-06-27") <= d <= W.WIN_END]
    rows = []
    for d in days:
        t = W.DATES.get_loc(d)
        live = [(c, x) for c, x, _ in W.SCHED if x >= d][:2]
        for root, lvl in (("ES", W.SPX[t]), ("NQ", W.NDX[t])):
            for code, exp in live:
                rows.append([d.date().isoformat(), root, root + code, exp.date().isoformat(),
                             "%.2f" % W.settlement(root, lvl, d, exp)])
    return write_csv(path, ["trade_date", "product", "contract", "last_trade_date", "settlement"], rows)


def write_master(path, names):
    rows = [[r.eqx_v2, r.eqx_v1, r.vendor_id, r.ticker, r.prior_ticker, r.ticker_changed, r.issuer, r.segment,
             r.sector, r.listing, r.desk_start, "Active"] for _, r in names.sort_values("ticker").iterrows()]
    return write_csv(path, ["instrument_id", "legacy_eqx_id", "vendor_id", "ticker", "prior_ticker",
                            "ticker_changed_on", "issuer", "segment", "gics_sector", "listing", "desk_start",
                            "status"], rows)


def write_mapping(path, w, names):
    """the engine's quarterly mapping vintages: every name's index and beta, and whether the store held enough of its
    own history at the vintage date"""
    rows = []
    vintages = [q for q in w.qstarts if W.DATES[q] >= pd.Timestamp("2024-04-01")]
    for q in vintages:
        d = W.DATES[q]
        _, b = w.betas_at(q)
        prox = w.is_proxy(q)
        old_ids = d < CUTOVER
        for i in names.sort_values("ticker").index:
            r = names.loc[i]
            rows.append([d.date().isoformat(), r.eqx_v1 if old_ids else r.eqx_v2, r.ticker, r.sector, r.desk_start,
                         "PROXY" if prox[i] else "OWN", "NDX" if w.tech[i] else "SPX", "%.3f" % b[i],
                         W.DATES[q - 250].date().isoformat(), W.DATES[q - 1].date().isoformat()])
    return write_csv(path, ["vintage", "eqx_instrument", "ticker", "gics_sector", "store_start", "series_at_vintage",
                            "proxy_index", "beta", "beta_window_from", "beta_window_to"], rows)


def write_xwalk(path, names):
    rows = [[r.eqx_v1, r.eqx_v2, r.ticker, "2025-01-18"] for _, r in names.sort_values("eqx_v1").iterrows()]
    return write_csv(path, ["eqx_v1_instrument", "eqx_v2_instrument", "ticker", "effective"], rows)


class Times:
    """the engine's nightly schedule: run starts, the position extracts cut as each run starts, the failed attempts"""

    def __init__(self, w):
        rt = np.random.default_rng(55023)
        self.run_day = [W.DATES[w.s - 1 + k] for k in range(w.T + 1)]
        self.start = w.run_start.copy()                       # minutes after midnight, New York
        self.cut = self.start - rt.uniform(0.25, 1.4, w.T + 1)
        stale_days = {k for k in range(w.T + 1) if w.stale[k] > 0}
        cand = [k for k in range(5, w.T) if k not in stale_days and k - 1 not in stale_days]
        self.failed = sorted(int(x) for x in rt.choice(cand, 4, replace=False))
        self.rerun = {k: self.start[k] + rt.uniform(55, 110) for k in self.failed}
        self.finish = {k: (self.rerun.get(k, self.start[k])) + rt.uniform(9, 17) for k in range(w.T + 1)}
        self.mo_batch = self.cut + rt.uniform(6, 38, w.T + 1)  # the middle office's allocation batch, every evening

    def extract_id(self, k):
        d = self.run_day[k]
        return "EQX-%s-%s" % (d.strftime("%Y%m%d"), ny(d, self.cut[k]).strftime("%H%M"))

    def extract_id_v2(self, k):
        d = self.run_day[k]
        return "EQXP2.%s.%s" % (d.strftime("%Y%m%d"), ny(d, self.cut[k]).strftime("%H%M%S"))

    def eqx_id(self, k):
        return self.extract_id(k) if self.run_day[k] <= CUTOVER else self.extract_id_v2(k)

    def futs_id(self, k):
        d = self.run_day[k]
        return "FUTS-%s" % utc(ny(d, self.cut[k])).replace("-", "").replace(":", "")


def write_eqx(tgt, w, names, tm):
    n1 = n2 = 0
    rows1, rows2 = [], []
    for k in range(w.T + 1):
        d = tm.run_day[k]
        t = w.s - 1 + k
        q = w.snap_sh[k]
        cut = ny(d, tm.cut[k])
        held = [i for i in names.sort_values("ticker").index if q[i] != 0]
        if d <= CUTOVER:
            for i in held:
                px = w.PX[t, i]
                rows1.append([tm.extract_id(k), cut.strftime("%m/%d/%Y %H:%M:%S"), BOOK, names.loc[i, "eqx_v1"],
                              names.loc[i, "ticker"], "%d" % q[i], "%.2f" % px, money(q[i] * px)])
        if d >= CUTOVER:
            for i in held:
                px = w.PX[t, i]
                rows2.append([tm.extract_id_v2(k), iso(cut), BOOK, names.loc[i, "eqx_v2"], names.loc[i, "ticker"],
                              "%d" % q[i], "%.4f" % px, money(q[i] * px), "USD"])
    n1 = write_csv(os.path.join(tgt, F_EQX1), ["EXTRACT_ID", "EXTRACT_TS", "BOOK", "INSTR_ID", "TICKER", "POS_QTY",
                                               "CLOSE_PX", "MKT_VAL"], rows1)
    n2 = write_csv(os.path.join(tgt, F_EQX2), ["extract_id", "extracted_at", "book", "instrument_id", "symbol",
                                               "quantity", "mark_price", "market_value_usd", "currency"], rows2)
    return n1, n2


def next_biz(d):
    cal = biz_days()
    return cal[cal.index(d) + 1]


def write_futs(path, w, tm):
    rows = []
    for k in range(w.T + 1):
        d = tm.run_day[k]
        t = w.s - 1 + k
        cut = ny(d, tm.cut[k])
        for (root, code), n in sorted(w.snap_fut[k].items()):
            if n == 0:
                continue
            exp = next(x[1] for x in W.SCHED if x[0] == code)
            stl = w.stl[(root, code)][t]
            rows.append([tm.futs_id(k), utc(cut), d.date().isoformat(), FBOOK, root + code, root,
                         exp.date().isoformat(), "%d" % n, "%.2f" % stl, money(n * W.MULT[root] * stl)])
    return write_csv(path, ["snapshot_id", "snapshot_utc", "position_date", "account", "contract", "root",
                            "last_trade_date", "net_contracts", "settle_px", "notional_usd"], rows)


def blotter_rows(w, names, tm):
    """every ticket the order management system booked for the desk, with its versions"""
    rb = np.random.default_rng(31337)
    tickets = []          # dicts with booked (aware datetime), trade_date, ...

    def eqx_of(i, booked):
        return names.loc[i, "eqx_v1"] if booked < dt.datetime(2025, 1, 18, tzinfo=NY) else names.loc[i, "eqx_v2"]

    for n_tr, tr in enumerate(w.trades):
        if tr["k"] < 0:
            continue
        k = tr["k"]
        d = W.DATES[w.s + k]
        t = w.s + k
        if tr["kind"] == "FUT":
            root, code = tr["root"], tr["code"]
            ex = 16 * 60 + 1 + rb.uniform(0, 13)
            booked = ny(d, ex + rb.uniform(0.02, 0.33))
            stl = w.stl[(root, code)][t]
            tickets.append(dict(trade_date=d, exec=ny(d, ex), booked=booked, source="HEDGE", asset="FUT", symbol=root + code,
                                inst="", qty=tr["qty"], px=stl, cpty="CME", comment="", order=n_tr))
            continue
        i = tr["i"]
        if tr["when"] == "client":
            ex = tr["tmin"]
            if tr.get("late"):
                nd = next_biz(d)
                booked = ny(nd, 8 * 60 + 40 + rb.uniform(0, 110))
                comment = ["booked T+1", "late tkt, trade date per client confirm", "LATE BKG", "bkd next am - client callback",
                           "late booking"][int(rb.integers(5))]
            else:
                booked = ny(d, ex + rb.uniform(0.03, 0.7))
                comment = ""
            cpty = CLIENTS[int(rb.integers(len(CLIENTS)))]
            src = "CLIENT"
        elif tr["when"] == "desk":
            ex = 16 * 60
            booked = ny(d, ex + rb.uniform(0.08, 4.0))
            cpty, src, comment = "STREET", "DESK", ""
        else:                                              # closing-auction allocations, booked by the middle office
            ex = 16 * 60
            booked = ny(d, tm.mo_batch[k + 1] + rb.uniform(0, 95))
            cpty, src, comment = CLIENTS[int(rb.integers(len(CLIENTS)))], "MOC_ALLOC", ""
            assert booked > ny(d, tm.cut[k + 1])
        tickets.append(dict(trade_date=d, exec=ny(d, ex), booked=booked, source=src, asset="EQ",
                            symbol=names.loc[i, "ticker"], inst=eqx_of(i, booked), qty=tr["qty"], px=tr["px"],
                            cpty=cpty, comment=comment, order=n_tr, i=i))
    # versions: fat-finger amendments and duplicate tickets cancelled, all before the evening extract for client flow
    rows = []
    for tk in tickets:
        tk["versions"] = [dict(status="NEW", booked=tk["booked"], qty=tk["qty"], px=tk["px"], comment=tk["comment"],
                               cpty=tk["cpty"])]
    clients = [tk for tk in tickets if tk["source"] == "CLIENT" and not tk["comment"]]
    allocs = [tk for tk in tickets if tk["source"] == "MOC_ALLOC"]
    for tk in [clients[j] for j in sorted(rb.choice(len(clients), int(len(clients) * 0.015), replace=False))]:
        good = tk["versions"][0]
        bad = dict(good)
        if rb.random() < 0.6:
            bad["qty"] = good["qty"] * 10
        else:
            bad["px"] = round(good["px"] * (1.1 if rb.random() < 0.5 else 0.9), 2)
        fix = dict(good, status="AMEND", booked=good["booked"] + dt.timedelta(seconds=int(rb.uniform(60, 2400))),
                   comment=["corrected", "qty fix", "px corr per trader", "fat finger - qty", "amended per client confirm",
                            "corr"][int(rb.integers(6))])
        tk["versions"] = [dict(bad, status="NEW"), fix]
        assert fix["booked"].hour < 18
    for tk in [allocs[j] for j in sorted(rb.choice(len(allocs), int(len(allocs) * 0.03), replace=False))]:
        good = tk["versions"][0]
        bad = dict(good, cpty=CLIENTS[int(rb.integers(len(CLIENTS)))])
        fix = dict(good, status="AMEND", booked=good["booked"] + dt.timedelta(seconds=int(rb.uniform(120, 1800))),
                   comment=["allocation moved to client account", "realloc", "re-alloc to correct acct", "acct fix MO",
                            "allocation corrected - sub-account"][int(rb.integers(5))], cpty=tk["cpty"])
        tk["versions"] = [dict(bad, status="NEW"), fix]
    errors = []
    for tk in [clients[j] for j in sorted(rb.choice(len(clients), int(len(clients) * 0.004), replace=False))]:
        v = tk["versions"][-1]
        b0 = v["booked"] + dt.timedelta(seconds=int(rb.uniform(20, 400)))
        e = dict(tk, booked=b0, comment="", order=tk["order"] + 0.5)
        e["versions"] = [dict(status="NEW", booked=b0, qty=v["qty"], px=v["px"], comment=""),
                         dict(status="CANCEL", booked=b0 + dt.timedelta(seconds=int(rb.uniform(90, 1800))),
                              qty=v["qty"], px=v["px"], comment=["duplicate ticket", "dup tkt", "dupe - see orig",
                                                                  "booked twice", "cxl dup"][int(rb.integers(5))])]
        errors.append(e)
    tickets.extend(errors)
    tickets.sort(key=lambda x: (x["versions"][0]["booked"], x["order"]))
    gaps = np.cumsum(rb.integers(1, 38, len(tickets)))          # the OMS numbers every desk's tickets in one series
    for n, tk in enumerate(tickets):
        tk["id"] = "SMC%08d" % (14812337 + int(gaps[n]))
    for tk in tickets:
        for vno, v in enumerate(tk["versions"], 1):
            q = v["qty"]
            side = "BUY" if q > 0 else "SELL"
            notional = abs(q) * v["px"] * (W.MULT[tk["symbol"][:2]] if tk["asset"] == "FUT" else 1.0)
            rows.append(dict(sort=(v["booked"], tk["id"], vno), row=[
                tk["id"], vno, v["status"], tk["trade_date"].date().isoformat(), tk["exec"].strftime("%H:%M:%S"),
                iso(v["booked"]), tk["source"], FBOOK if tk["asset"] == "FUT" else BOOK, tk["asset"], tk["symbol"],
                tk["inst"], side, "%d" % abs(q), ("%.2f" % v["px"]) if tk["asset"] == "FUT" else ("%.4f" % v["px"]),
                money(notional), v.get("cpty", tk["cpty"]), v["comment"]]))
    rows.sort(key=lambda r: r["sort"])
    out = [r["row"] for r in rows]
    dup = sorted(rb.choice(len(out), 25, replace=False))
    for j in reversed(dup):
        out.insert(j + 1, list(out[j]))           # the export repeats a few lines
    return out


def write_blotter(path, w, names, tm):
    rows = blotter_rows(w, names, tm)
    return write_csv(path, ["trade_id", "version", "status", "trade_date", "exec_time", "booked_at", "source", "book",
                            "asset_class", "symbol", "eqx_instrument", "side", "quantity", "price", "notional_usd",
                            "counterparty", "comment"], rows)


class PnL:
    """product control's daily components, rounded as published, and the late fee postings restated next day"""

    def __init__(self, w):
        rp = np.random.default_rng(80431)
        T = w.T
        self.hyp = np.round(w.hyp)
        self.new = np.round(w.newpnl)
        self.comm = np.round(w.comm)
        self.fees = np.round(w.fees)
        self.resv = np.round(w.resv)
        self.fund = np.round(w.fund)
        self.booked = self.hyp + self.new + self.comm + self.fees + self.resv + self.fund
        self.rep = np.round(w.rep)
        margin = np.abs(self.booked + self.rep)
        cand = [k for k in range(T) if margin[k] > 250_000 and abs(self.hyp[k] + self.rep[k]) > 250_000
                and self.fees[k] > 120_000]
        self.restated = sorted(int(x) for x in rp.choice(cand, 9, replace=False))
        self.late_fee = {k: float(np.round(self.fees[k] * rp.uniform(0.15, 0.4))) for k in self.restated}
        # the published equity and futures split of the opening book's revaluation
        hyp_fut = np.zeros(T)
        for k in range(T):
            t = w.s + k
            for key, n in w.fut[k].items():
                hyp_fut[k] += n * W.MULT[key[0]] * (w.stl[key][t] - w.stl[key][t - 1])
        self.hyp_fut = np.round(hyp_fut)
        self.hyp_eq = self.hyp - self.hyp_fut


def write_pc(path, w, P):
    rows = []
    rq = np.random.default_rng(66091)
    for k in range(w.T):
        d = W.DATES[w.s + k]
        pub = ny(d, 19 * 60 + 41 + rq.gamma(3.0, 9.0))
        comp = [P.hyp[k], P.new[k], P.comm[k], P.fees[k], P.resv[k], P.fund[k]]
        if k in P.restated:
            v1 = list(comp)
            v1[3] = P.fees[k] - P.late_fee[k]
            rows.append([d.date().isoformat(), "SMCF", 1, iso(pub)] + ["%.0f" % x for x in v1] + ["%.0f" % sum(v1)])
            pub2 = ny(next_biz(d), 10 * 60 + 50 + rq.uniform(0, 75))
            rows.append([d.date().isoformat(), "SMCF", 2, iso(pub2)] + ["%.0f" % x for x in comp] + ["%.0f" % sum(comp)])
        else:
            rows.append([d.date().isoformat(), "SMCF", 1, iso(pub)] + ["%.0f" % x for x in comp] + ["%.0f" % sum(comp)])
    return write_csv(path, ["business_date", "desk", "version", "published_at", "hypothetical_pnl_usd",
                            "new_trades_pnl_usd", "commissions_usd", "facilitation_fees_usd", "reserves_usd",
                            "funding_usd", "booked_pnl_usd"], rows)


def write_gl(path, w, P):
    accts = [("410100", "Trading revenue - cash equities"), ("410500", "Trading revenue - index futures"),
             ("420100", "Commissions earned"), ("421000", "Facilitation fees"), ("430200", "Valuation reserves"),
             ("510300", "Funding charge - trading inventory")]
    rows = []
    n = 0
    rj = np.random.default_rng(40217)
    for k in range(w.T):
        d = W.DATES[w.s + k]
        amounts = [P.hyp_eq[k] + P.new[k], P.hyp_fut[k], P.comm[k], P.fees[k], P.resv[k], P.fund[k]]
        late = P.late_fee.get(k, 0.0)
        for (acct, nm), amt in zip(accts, amounts):
            if acct == "430200" and amt == 0:
                continue
            if acct == "421000" and late:
                amt = amt - late
            n += int(rj.integers(1, 60))                       # the ledger numbers every cost centre's journals in one series
            rows.append(["JE%08d" % (30_118_000 + n), d.date().isoformat(), d.date().isoformat(), "CC4471", acct, nm,
                         "%.2f" % amt, "SUBLEDGER", "SMCF P&L feed %s %s" % (d.strftime("%Y%m%d"), acct)])
        if late:
            n += int(rj.integers(1, 60))
            nd = next_biz(d)
            rows.append(["JE%08d" % (30_118_000 + n), nd.date().isoformat(), d.date().isoformat(), "CC4471", "421000",
                         "Facilitation fees", "%.2f" % late, "MANUAL",
                         "Fee true-up %s, invoice received after cut-off, value %s" % (CLIENTS[int(rj.integers(len(CLIENTS)))],
                                                                                       d.date().isoformat())])
    rows.sort(key=lambda r: (r[1], r[0]))
    return write_csv(path, ["journal_id", "posting_date", "value_date", "cost_centre", "account", "account_name",
                            "amount_usd", "source", "description"], rows)


def engine_var(w, k):
    return float(W.var(w, w.eng_sh[k], w.eng_fut[k], k))


def write_runlog(path, w, tm, rep_all):
    rows = []
    for k in range(w.T + 1):
        d = tm.run_day[k]
        t = w.s - 1 + k
        u = w.used[k]
        sh = w.eng_sh[k]
        mv = sh * w.PX[t]
        npos = int((sh != 0).sum()) + sum(1 for v in w.eng_fut[k].values() if v != 0)
        eqx = tm.eqx_id(u)
        futs = tm.futs_id(u)
        cut_used = ny(tm.run_day[u], tm.cut[u])
        msg = ""
        status = "COMPLETE"
        if w.stale[k] > 0:
            status = "COMPLETE_WITH_WARNINGS"
            msg = "EQX/FUTS extract for %s not received by 18:45; last good extract %s used" % (d.date().isoformat(), eqx)
        common = [eqx, iso(cut_used), futs, "%d" % npos, money(mv[mv > 0].sum()), money(-mv[mv < 0].sum())]
        if k in tm.failed:
            rows.append(["ERE-SMCF-%s-1" % d.strftime("%Y%m%d"), d.date().isoformat(), "SMCF", "18:30",
                         iso(ny(d, tm.start[k])), iso(ny(d, tm.start[k] + 4.2)), "FAILED"] + common +
                        ["", "Vendor close file incomplete (%d of %d instruments); run aborted" % (w.N - 7, w.N)])
            rows.append(["ERE-SMCF-%s-2" % d.strftime("%Y%m%d"), d.date().isoformat(), "SMCF", "18:30",
                         iso(ny(d, tm.rerun[k])), iso(ny(d, tm.finish[k])), status] + common +
                        ["%.0f" % rep_all[k], "Rerun after vendor file completed; extract from first attempt"])
        else:
            rows.append(["ERE-SMCF-%s-1" % d.strftime("%Y%m%d"), d.date().isoformat(), "SMCF", "18:30",
                         iso(ny(d, tm.start[k])), iso(ny(d, tm.finish[k])), status] + common +
                        ["%.0f" % rep_all[k], msg])
    return write_csv(path, ["run_id", "business_date", "desk", "scheduled", "started_at", "finished_at", "status",
                            "eqx_extract", "eqx_extract_at", "futs_snapshot", "positions_read", "gross_long_usd",
                            "gross_short_usd", "var_99_1d_usd", "message"], rows)


def write_limits(path, w, P):
    rows = []
    for k in range(w.T):
        d = W.DATES[w.s + k]
        lim = 2_500_000 if d < pd.Timestamp("2025-04-01") else 3_000_000
        v = P.rep[k]
        u = v / lim * 100
        rows.append([d.date().isoformat(), "SMCF", "%.0f" % v, "%d" % lim, "%.1f" % u,
                     "RED" if u > 100 else ("AMBER" if u > 80 else "GREEN"), "LIM-SMCF-VAR-01"])
    return write_csv(path, ["business_date", "desk", "var_99_1d_usd", "limit_usd", "utilisation_pct", "status",
                            "limit_id"], rows)


def write_all(tgt, w):
    names = make_names(w)
    tm = Times(w)
    rep_all = np.array([float(w.rep[k]) for k in range(w.T)] + [engine_var(w, w.T)])
    P = PnL(w)
    rows = {}
    rows[F_VENDOR] = write_vendor(os.path.join(tgt, F_VENDOR), w, names)
    rows.update(write_index_files(tgt))
    rows[F_SETTLE] = write_settlements(os.path.join(tgt, F_SETTLE), w)
    rows[F_MASTER] = write_master(os.path.join(tgt, F_MASTER), names)
    rows[F_MAP] = write_mapping(os.path.join(tgt, F_MAP), w, names)
    rows[F_XWALK] = write_xwalk(os.path.join(tgt, F_XWALK), names)
    rows[F_EQX1], rows[F_EQX2] = write_eqx(tgt, w, names, tm)
    rows[F_FUTS] = write_futs(os.path.join(tgt, F_FUTS), w, tm)
    rows[F_BLOTTER] = write_blotter(os.path.join(tgt, F_BLOTTER), w, names, tm)
    rows[F_PC] = write_pc(os.path.join(tgt, F_PC), w, P)
    rows[F_GL] = write_gl(os.path.join(tgt, F_GL), w, P)
    rows[F_RUNLOG] = write_runlog(os.path.join(tgt, F_RUNLOG), w, tm, rep_all)
    rows[F_LIMITS] = write_limits(os.path.join(tgt, F_LIMITS), w, P)
    return dict(names=names, tm=tm, P=P, rep_all=rep_all, rows=rows)
