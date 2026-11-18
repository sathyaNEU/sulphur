"""The exports of Wrenfold's systems, written the way each system writes them: the drivers' handheld dockets, the
tag reads of the 20 litre kegs, the container register, the annual counts, the cold store's Monday position, the
racking log, the reps' cellar audits, the accounts and their dispense lines, the depots' stock, the wash line's log,
the purchases, the recovery agent's cases, the weather station's weeks, and two exports of other departments."""
import csv
import datetime as dt
import os
import sqlite3

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

import core as C
import world as WL

POOLS = WL.POOLS
WH = WL.WH
FILES = {
    "dockets": "delivery_dockets_dec2023_nov2026.csv",
    "tags": "foundry_keg_tag_reads.sqlite",
    "register": "container_register.csv",
    "stocktake": "annual_container_counts.xlsx",
    "store": "cold_store_monday_position.csv",
    "racking": "racking_log.csv",
    "audits": "cellar_audits_2025_2026.csv",
    "accounts": "trade_accounts.csv",
    "lines": "dispense_lines.csv",
    "products": "products.csv",
    "codes": "container_codes.csv",
    "weather": "calder_vale_station_weekly.csv",
    "depots": "depot_stock_weekly.csv",
    "wash": "wash_line_daily_log.csv",
    "purchases": "container_purchases.csv",
    "recovery": "kegtrace_cases.csv",
    "packaging": "packaging_line_shift_log.csv",
}
CODE = {"docket": {"K50": "50L", "K30": "30L", "K20": "20L", "FIR": "9G", "KIL": "18G"},
        "register": {"K50": "50", "K30": "30", "K20": "20", "FIR": "F9", "KIL": "K18"}}
DESCR = {"K50": ("50 litre keg", 50.0), "K30": ("30 litre keg", 30.0), "K20": ("20 litre keg", 20.0),
         "FIR": ("firkin, 9 gallon cask", 40.9), "KIL": ("kilderkin, 18 gallon cask", 81.8)}
SERIAL0 = {"K50": 500001, "K30": 300001, "K20": 200001, "FIR": 900001, "KIL": 180001}
REPS = ["J. Whitaker", "S. Oyelaran", "M. Pickles", "A. Rahman", "D. Hebblethwaite", "C. Marsden"]
DAYNAME = ["Mon", "Tue", "Wed", "Thu", "Fri"]
EPOCH = np.datetime64("1970-01-01")


def sku(p, code):
    return "%s-%s" % ("BIT" if code == "BIK" else code, CODE["docket"][p])


def serial(p, k, prefix=True):
    return "%s%s-%06d" % ("LF" if prefix else "", CODE["register"][p], SERIAL0[p] + int(k))


def acct_ids(WD):
    now = np.array([a["id"] for a in WD.accounts])
    old = np.array([a["former"] or a["id"] for a in WD.accounts])
    swap = np.array([a["swap_week"] if a["swap_week"] is not None else -1 for a in WD.accounts])
    return now, old, swap


def aid(WD, a, i):
    x = WD.accounts[int(a)]
    return x["former"] if x["swap_week"] is not None and i < x["swap_week"] else x["id"]


def write_csv(path, header, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def routes(WD):
    """each account's route: its depot, its delivery day and a round of about 28 drops"""
    out = {}
    count = {}
    for a in WD.accounts:
        k = a["k"]
        days = [int(WD.day1[k])] + ([int(WD.day1[k]) + 3] if WD.twice[k] else [])
        names = []
        for d in days:
            n = count.get((a["depot"], d), 0)
            count[(a["depot"], d)] = n + 1
            names.append("%s-%s%02d" % (a["depot"], DAYNAME[d][0] if d != 3 else "H", n // 28 + 1))
        out[k] = (days, names, [count[(a["depot"], d)] for d in days])
    return out


def write_dockets(target, WD, rng):
    N = WL.N_ACCOUNTS
    now, old, swap = acct_ids(WD)
    R = routes(WD)
    route_of = np.array([[R[k][1][0], R[k][1][-1]] for k in range(N)])
    depot = np.array([a["depot"] for a in WD.accounts])
    dates = np.array([[np.datetime64(WL.workday(i, d)) for d in range(5)] for i in range(WH)])
    skus, sku_pool = [], []
    cols = {k: [] for k in ("week", "v", "a", "sku", "qty")}
    for p in POOLS:
        P = WD.pools[p]
        base = len(skus)
        codes = [c for c, sh, q in P.beers26]
        skus += [sku(p, c) for c in codes]
        sku_pool += [p] * len(codes)
        line_sku = None if P.guest is not None else np.array([codes.index(c) for c in P.prod])
        for v, d in ((0, P.d1), (1, P.d2)):
            l, i = np.nonzero(d)
            cols["week"].append(i)
            cols["v"].append(np.full(len(l), v))
            cols["a"].append(P.acct[l])
            cols["sku"].append(base + (P.guest[l, i] if P.guest is not None else line_sku[l]))
            cols["qty"].append(d[l, i])
    week, v, a, sk, qty = (np.concatenate(cols[k]) for k in ("week", "v", "a", "sku", "qty"))
    day = WD.day1[a] + 3 * v
    date = dates[week, day]
    key = (week * 2 + v) * N + a
    uk, first, inv = np.unique(key, return_index=True, return_inverse=True)
    order = np.lexsort((a[first], date[first]))                       # dockets numbered by day, then account
    rank = np.empty(len(uk), dtype=int)
    rank[order] = np.arange(len(uk))
    docket = rank[inv]
    up = date[first].astype("datetime64[s]") + rng.integers(14 * 3600 + 1800, 19 * 3600 + 1800, len(uk)).astype("timedelta64[s]")
    o = np.lexsort((sk, docket))                                      # the docket's lines in product order
    week, v, a, sk, qty, date, docket = week[o], v[o], a[o], sk[o], qty[o], date[o], docket[o]
    start = np.r_[0, np.nonzero(np.diff(docket))[0] + 1]
    line_no = np.arange(len(docket)) - np.repeat(start, np.diff(np.r_[start, len(docket)])) + 1
    skus_a = np.array(skus)
    cont_a = np.array([CODE["docket"][p] for p in sku_pool])
    container = cont_a[sk]
    blank = rng.random(len(sk)) < 0.005                               # keyed without the container code
    container = np.where(blank, "", container)
    df = pd.DataFrame({
        "docket_no": np.char.add("DK", np.char.zfill((1000001 + docket).astype(str), 7)),
        "delivery_date": np.datetime_as_string(date, unit="D"),
        "depot": depot[a],
        "route": np.where(v == 0, route_of[a, 0], route_of[a, 1]),
        "account_no": np.where((swap[a] >= 0) & (week < swap[a]), old[a], now[a]),
        "line_no": line_no,
        "sku": skus_a[sk],
        "container": container,
        "qty": qty,
        "uploaded_at": np.datetime_as_string(up[docket], unit="s"),
    })
    n_dockets = len(uk)
    again = np.sort(rng.choice(n_dockets, int(n_dockets * 0.0025), replace=False))   # a handheld re-sync
    dup = df[np.isin(docket, again)].copy()
    late = (date[first][order][again] + np.timedelta64(1, "D")).astype("datetime64[s]") + \
        rng.integers(6 * 3600, 8 * 3600, len(again)).astype("timedelta64[s]")
    late_of = dict(zip((1000001 + again).tolist(), np.datetime_as_string(late, unit="s").tolist()))
    dup["uploaded_at"] = [late_of[int(x[2:])] for x in dup["docket_no"]]
    out = pd.concat([df, dup], ignore_index=True).sort_values(["uploaded_at", "docket_no", "line_no"], kind="stable")
    out.to_csv(os.path.join(target, FILES["dockets"]), index=False, lineterminator="\r\n")
    return dict(rows=len(out), dockets=n_dockets, resent=len(again), resent_rows=len(dup), blank=int(blank.sum()),
                del_rows=len(sk), skus=skus, sku_pool=sku_pool)


def day_date(day, kind):
    i, dd = divmod(int(day), 7)
    if kind == "FILL":
        return WL.workday(i, dd, back=True)
    if kind == "DELIVER":
        return WL.workday(i, dd)
    d = WL.D0 + dt.timedelta(days=int(day))
    while d in WL.HOLIDAYS or d.weekday() == 6:
        d += dt.timedelta(days=1)
    return d


def write_tags(target, WD, rng):
    P = WD.pools["K20"]
    path = os.path.join(target, FILES["tags"])
    if os.path.exists(path):
        os.remove(path)
    n = P.keg_total
    tag_no = rng.permutation(16 ** 6)[:n + 1200]
    new_tag = iter(["E28%07X" % (0x1100000 + int(x)) for x in tag_no])
    tag = [next(new_tag) for _ in range(n)]
    reg = P.reg
    fitted = [[serial("K20", k, prefix=False), tag[k],
               (max(reg["bought"][k], dt.date(2023, 3, 6)) + dt.timedelta(days=int(rng.integers(0, 30)))
                if reg["bought"][k] < WL.D0 else reg["bought"][k]).isoformat(), ""] for k in range(n)]
    cur = list(range(n))                                             # each keg's row in `fitted`
    win = {"FILL": (5 * 3600 + 1800, 7 * 3600 + 1800), "DELIVER": (8 * 3600, 16 * 3600 + 1800),
           "WASH": (7 * 3600, 18 * 3600)}
    reads = []
    last = {}                                                         # keg -> its last read (stamp, point, where, tag)
    for k, bi, fday, l, dday, wday in P.trips:
        a = int(P.acct[l]) if l >= 0 else None
        for point, day, where in (("FILL", fday, "BRG-RACK2"), ("DELIVER", dday, None), ("WASH", wday, "BRG-WASH1")):
            if day is None or (point == "WASH" and int(day) >= 7 * WH):
                continue
            d = day_date(day, point)
            if d >= WL.ASOF:
                continue
            lo, hi = win[point]
            ts = dt.datetime.combine(d, dt.time()) + dt.timedelta(seconds=int(rng.integers(lo, hi)))
            loc = where or aid(WD, a, int(day) // 7)
            t = fitted[cur[k]][1]
            miss = rng.random() < WL.READ_MISS[point]
            if not miss:
                reads.append((ts, t, point, loc))
                if rng.random() < WL.READ_DOUBLE:
                    reads.append((ts + dt.timedelta(seconds=int(rng.integers(2, 40))), t, point, loc))
                last[k] = (ts, point, loc, t)
            if point == "WASH" and rng.random() < WL.TAG_SWAP:       # a damaged tag replaced at the wash
                fitted[cur[k]][3] = d.isoformat()
                cur[k] = len(fitted)
                fitted.append([serial("K20", k, prefix=False), next(new_tag), d.isoformat(), ""])
    reads.sort(key=lambda r: (r[0], r[1], r[2]))
    con = sqlite3.connect(path)
    con.execute("PRAGMA journal_mode=OFF")
    con.execute("CREATE TABLE tag_reads (read_id INTEGER PRIMARY KEY, tag_id TEXT NOT NULL, read_at TEXT NOT NULL, "
                "read_point TEXT NOT NULL, location TEXT NOT NULL)")
    con.execute("CREATE TABLE tag_fittings (serial TEXT NOT NULL, tag_id TEXT NOT NULL, fitted_on TEXT NOT NULL, "
                "removed_on TEXT)")
    con.executemany("INSERT INTO tag_reads VALUES (?,?,?,?,?)",
                    [(j + 1, t, ts.strftime("%Y-%m-%d %H:%M:%S"), pt, loc) for j, (ts, t, pt, loc) in enumerate(reads)])
    con.executemany("INSERT INTO tag_fittings VALUES (?,?,?,?)",
                    [(s, t, f, r or None) for s, t, f, r in sorted(fitted, key=lambda x: (x[0], x[2]))])
    con.execute("CREATE INDEX ix_reads_tag ON tag_reads (tag_id, read_at)")
    con.commit()
    con.execute("VACUUM")
    con.close()
    # the recovery agent's cases
    where = {}
    for k, bi, fday, l, dday, wday in P.trips:
        if dday is not None:
            where[(k, dday)] = l
    out = []
    for j, (k, dday, ref, closed, outcome) in enumerate(P.chase):
        l = where.get((k, dday))
        if l is None:
            continue
        a = aid(WD, int(P.acct[l]), int(dday) // 7)
        d = day_date(dday, "DELIVER")
        out.append([serial("K20", k, prefix=False), d.isoformat(), a,
                    (WL.D0 + dt.timedelta(days=int(ref))).isoformat(),
                    (WL.D0 + dt.timedelta(days=int(closed))).isoformat() if closed is not None else "",
                    outcome or "OPEN"])
    out.sort(key=lambda r: (r[3], r[0]))
    out = [["KT-%05d" % (41207 + j)] + r for j, r in enumerate(out)]
    write_csv(os.path.join(target, FILES["recovery"]),
              ["case_no", "keg_serial", "last_delivered_on", "account_no", "referred_on", "closed_on", "outcome"], out)
    return dict(reads=len(reads), fittings=len(fitted), cases=len(out),
                not_traced=sum(1 for r in out if r[-1] == "NOT TRACED"))


def write_register(target, WD):
    rows = []
    for p in POOLS:
        reg = WD.pools[p].reg
        for k in range(reg["total"]):
            c = reg["condemned"].get(k)
            if c is not None and c >= WL.ASOF:
                c = None
            rows.append([serial(p, k), CODE["register"][p],
                         "Calder Coopers Ltd" if reg["bought"][k].year < 2012 else WL.MAKER, reg["lot"][k],
                         reg["bought"][k].isoformat(), "CONDEMNED" if c else "ACTIVE", c.isoformat() if c else ""])
    rows.sort(key=lambda r: r[0])
    return write_csv(os.path.join(target, FILES["register"]),
                     ["serial", "container", "maker", "lot", "purchased", "status", "condemned_on"], rows)


def depot_split(P, rng):
    """the depots' full and empty stock at each Monday, depot by depot"""
    sh = [x[1] for x in WL.DEPOTS.values()]
    full = np.array([WL.split(int(P.depot_full[i]), np.array(sh) * np.exp(rng.normal(0, 0.06, 3))) for i in range(WH + 1)])
    empty = np.array([WL.split(int(P.parts["depot_empty"][i]), np.array(sh) * np.exp(rng.normal(0, 0.10, 3)))
                      for i in range(WH + 1)])
    return full, empty


def sheet(ws, header, rows, widths):
    ws.append(header)
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w


def write_stocktake(target, WD, DS):
    wb = Workbook()
    wb.remove(wb.active)
    counted = {0: ("Mon 4 Dec 2023", "E. Moss, T. Morley"), 52: ("Mon 2 Dec 2024", "E. Moss, T. Morley"),
               104: ("Mon 1 Dec 2025", "E. Moss, T. Morley"), 156: ("Mon 30 Nov 2026", "E. Moss, T. Morley")}
    names = {0: "Dec 2023", 52: "Dec 2024", 104: "Dec 2025", 156: "Nov 2026"}
    for b in WL.STOCKTAKES:
        ws = wb.create_sheet(names[b])
        ws.append(["Annual container count"])
        ws["A1"].font = Font(bold=True, size=12)
        ws.append(["Counted", counted[b][0], "before the first loads", "", "Signed", counted[b][1]])
        ws.append([])
        rows = []
        for p in POOLS:
            P = WD.pools[p]
            full, empty = DS[p]
            rows += [["Brighouse", "Cold store", p, "full", int(P.store[b])],
                     ["Brighouse", "Packaging hall", p, "clean empty", int(P.idle[b])],
                     ["Brighouse", "Wash line", p, "awaiting wash", int(P.parts["awaiting"][b])],
                     ["Brighouse", "Wash line", p, "in wash", int(P.parts["wash"][b])],
                     ["Brighouse", "Repair bay", p, "in repair", int(P.parts["repair"][b])]]
            for j, dk in enumerate(WL.DEPOTS):
                rows += [[WL.DEPOTS[dk][0] + " depot", "Full store", p, "full", int(full[b, j])],
                         [WL.DEPOTS[dk][0] + " depot", "Empties bay", p, "empty", int(empty[b, j])]]
        rows.sort(key=lambda r: (r[0] != "Brighouse", r[0], r[1], POOLS.index(r[2])))
        sheet(ws, ["site", "area", "container", "state", "count"], rows, [18, 16, 11, 14, 9])
        ws.freeze_panes = "A5"
    wb.save(os.path.join(target, FILES["stocktake"]))


def write_store(target, WD):
    rows = []
    for i in range(WH + 1):
        for p in POOLS:
            rows.append([WL.week_start(i).isoformat(), p, int(WD.pools[p].store[i])])
    return write_csv(os.path.join(target, FILES["store"]), ["position_date", "container", "full_containers"], rows)


def write_racking(target, WD, rng):
    rows = []
    tanks = {"K50": ["BBT1", "BBT2", "BBT3"], "K30": ["BBT2", "BBT4", "BBT5"], "K20": ["BBT6", "BBT7"],
             "FIR": ["RT1", "RT2"], "KIL": ["RT2"]}
    for p in POOLS:
        P = WD.pools[p]
        for i, dd, bi, n in P.rackings:
            d = WL.workday(i, dd, back=True)
            rows.append([d, sku(p, P.beers26[bi][0]), CODE["register"][p], int(n),
                         tanks[p][int(rng.integers(0, len(tanks[p])))], "%02d:%02d" % (int(rng.integers(5, 8)), int(rng.integers(0, 60)))])
    rows.sort(key=lambda r: (r[0], r[5], r[1]))
    out = [["RK%s-%05d" % (str(r[0].year)[2:], j + 1), r[0].isoformat(), r[5], r[1], r[2], r[3], r[4]]
           for j, r in enumerate(rows)]
    return write_csv(os.path.join(target, FILES["racking"]),
                     ["racking_no", "racked_on", "start", "sku", "container", "containers_filled", "tank"], out)


AUDITS_PULLED = dt.date(2026, 12, 1)       # the audits export of 2 December holds the forms keyed to the day before


def write_audits(target, WD, rng):
    style = {0: "docket", 1: "docket", 2: "docket", 3: "pool", 4: "docket", 5: "pool"}
    rows = []
    for r in WD.audits:
        p, P = r["pool"], WD.pools[r["pool"]]
        d = WL.week_start(r["week"]) + dt.timedelta(days=r["day"])
        code = CODE["docket"][p] if style[r["rep"]] == "docket" else p
        prod = "GUEST-20L" if p == "K20" else sku(p, P.prod[r["line"]])
        keyed = d + dt.timedelta(days=r["keyed"])
        if keyed > AUDITS_PULLED:                                     # a form not keyed yet is not in the export
            continue
        rows.append([r["visit"], d, aid(WD, r["acct"], r["week"]), prod, code, r["full"], r["on"], r["empty"],
                     r["foreign"], REPS[r["rep"]], keyed])
    rows.sort(key=lambda r: (r[10], r[0], r[3]))                      # in the order the forms were keyed
    first = {}
    for r in sorted(rows, key=lambda r: (r[1], r[0])):
        first.setdefault(r[0], len(first))
    out = [["CA-%04d" % (2101 + first[r[0]]), r[1].isoformat(), r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9],
            r[10].isoformat()] for r in rows]
    return write_csv(os.path.join(target, FILES["audits"]),
                     ["audit_ref", "audit_date", "account_no", "product", "container", "full", "on_dispense", "empty",
                      "other_brewers", "rep", "keyed_on"], out)


def write_accounts(target, WD):
    rows = []
    for a in WD.accounts:
        rows.append([a["id"], a["name"], a["town"], a["channel"], a["depot"], a["opened"].isoformat(), a["former"] or "",
                     (WL.week_start(a["swap_week"])).isoformat() if a["swap_week"] is not None else ""])
    write_csv(os.path.join(target, FILES["accounts"]),
              ["account_no", "name", "town", "channel", "served_from", "opened", "former_account_no", "renumbered_on"], rows)
    lines = []
    for p in POOLS:
        P = WD.pools[p]
        for l, a in enumerate(P.acct.tolist()):
            lines.append([WD.accounts[a]["id"], "GUEST-20L" if p == "K20" else sku(p, P.prod[l]), CODE["docket"][p]])
    lines.sort()
    seq = {}
    out = []
    for a, s, c in lines:
        seq[a] = seq.get(a, 0) + 1
        out.append([a, seq[a], s, c])
    write_csv(os.path.join(target, FILES["lines"]), ["account_no", "line", "product", "container"], out)
    return len(rows), len(out)


def write_small(target, WD, DS, rng, D):
    prods = []
    abv = {"PIL": 4.6, "GLD": 4.2, "PAL": 4.0, "IPA": 5.4, "HER": 4.4, "BLK": 4.5, "BIT": 3.8, "MLD": 3.4, "SEA": 4.1,
           "SUM": 4.0, "HAR": 4.3}
    for p in POOLS:
        w = C.W[p]
        for c in [x[0] for x in w["beers"]] + [x[0] for x in w["new27"]]:
            beer = "BIT" if c == "BIK" else c
            prods.append([sku(p, c), WL.BEER_NAMES[c], "Foundry series" if c.startswith("F") and c[1:].isdigit() else
                          ("Cask" if p in ("FIR", "KIL") else "Keg"), CODE["docket"][p],
                          abv.get(beer, round(4.0 + (int(c[1:]) * 7 % 23) / 10.0, 1) if c[1:].isdigit() else 4.0)])
    prods.append(["GUEST-20L", "Guest keg line, Foundry series on rotation", "Foundry series", "20L", ""])
    write_csv(os.path.join(target, FILES["products"]), ["sku", "description", "family", "container", "abv"], sorted(prods))
    write_csv(os.path.join(target, FILES["codes"]), ["container", "description", "litres", "docket_code", "register_code"],
              [[p, DESCR[p][0], DESCR[p][1], CODE["docket"][p], CODE["register"][p]] for p in POOLS])
    rows = []
    last = WL.WH - 1
    for i in range(WL.WX0, WH + WL.WF + 1):
        rows.append([WL.week_start(i).isoformat(), ("%.1f" % WD.T[i]) if i <= last else "", "%.1f" % WD.normal[i]])
    write_csv(os.path.join(target, FILES["weather"]), ["week_beginning", "mean_daily_max_c", "normal_1991_2020_c"], rows)
    rows = []
    for i in range(WH + 1):
        for j, dk in enumerate(WL.DEPOTS):
            for p in POOLS:
                rows.append([WL.week_start(i).isoformat(), dk, p, int(DS[p][0][i, j]), int(DS[p][1][i, j])])
    write_csv(os.path.join(target, FILES["depots"]), ["week_beginning", "depot", "container", "full", "empty"], rows)
    # the wash line, day by day: the backlog at close, and what the inspection sent to repair, took back or condemned
    rows = []
    wgt = np.array([0.19, 0.19, 0.18, 0.18, 0.17, 0.09])
    for p in POOLS:
        P = WD.pools[p]
        cond = {}
        for k, d in P.reg["condemned"].items():
            cond[d] = cond.get(d, 0) + 1
        aw, rp = P.parts["awaiting"], P.parts["repair"]
        for i in range(WH):
            days = [WL.week_start(i) + dt.timedelta(days=d) for d in range(6)]
            worked = [d for d in days if d not in WL.HOLIDAYS]
            w = np.array([0.0 if d in WL.HOLIDAYS else x for d, x in zip(days, wgt)])
            n = WL.split(int(P.washed[i]), w * np.exp(rng.normal(0, 0.08, 6)) + 1e-9)
            rep = np.array([int(rng.binomial(int(x), 0.021)) for x in n])
            back_wk = int(rep.sum() - (rp[i + 1] - rp[i]))         # the bay's balance is the count's "in repair"
            if back_wk < 0:
                rep = rep + WL.split(-back_wk, w + 1e-9)
                back_wk = 0
            back = WL.split(back_wk, w * np.exp(rng.normal(0, 0.15, 6)) + 1e-9)
            for j, d in enumerate(days):
                if d in WL.HOLIDAYS:
                    continue
                q = aw[i + 1] if d == worked[-1] else \
                    aw[i] + (aw[i + 1] - aw[i]) * (j + 1) / 6.0 + rng.normal(0, 0.05 * max(aw[i], 1.0))
                rows.append([d, CODE["register"][p], int(max(round(float(q)), 0)), int(rep[j]), int(back[j]), cond.get(d, 0)])
    rows.sort(key=lambda r: (r[0], r[1]))
    write_csv(os.path.join(target, FILES["wash"]), ["date", "container", "awaiting_wash", "to_repair", "back_from_repair", "condemned"],
              [[r[0].isoformat()] + r[1:] for r in rows])
    price = {"K50": 61.40, "K30": 52.80, "K20": 58.90, "FIR": 74.50, "KIL": 96.00}
    rows = []
    for p in POOLS:
        for wk, n in C.W[p]["lots"]:
            d = WL.week_start(wk) + dt.timedelta(days=2)
            rows.append(["PO-%d" % (7300 + wk * 3 + POOLS.index(p)), (d - dt.timedelta(days=int(rng.integers(84, 120)))).isoformat(),
                         d.isoformat(), CODE["register"][p], "%s-%d" % (WL.OLD_LOTS[p][0][0].rsplit("-", 1)[0], d.year),
                         int(n), WL.MAKER, "%.2f" % (price[p] * (1.0 + 0.03 * (d.year - 2024))), "EUR"])
    rows.sort(key=lambda r: r[2])
    write_csv(os.path.join(target, FILES["purchases"]),
              ["order_no", "ordered", "received", "container", "lot", "quantity", "supplier", "unit_price", "currency"], rows)
    # another department's export: the packaging lines, shift by shift
    rows = []
    rated = {"Keg line 1": 240, "Keg line 2": 180, "Cask racker": 60}
    for i in range(WH):
        for dd in range(5):
            d = WL.week_start(i) + dt.timedelta(days=dd)
            if d in WL.HOLIDAYS:
                continue
            for line, rate in rated.items():
                if line == "Keg line 2" and rng.random() < 0.35:
                    continue
                hours = float(rng.choice([6.0, 7.5, 7.5, 7.5, 9.0]))
                planned = int(rng.choice([20, 30, 30, 45, 60]))
                unplanned = int(rng.gamma(1.4, 14))
                speed = rate * float(np.clip(rng.normal(0.9, 0.05), 0.6, 1.0))
                good = int(max(0.0, hours * 60 - planned - unplanned) / 60.0 * speed)
                rows.append([d.isoformat(), line, "%.1f" % hours, planned, unplanned, rate, good, int(rng.binomial(good, 0.006)),
                             int(rng.binomial(good, 0.003))])
    write_csv(os.path.join(target, FILES["packaging"]),
              ["shift_date", "line", "shift_hours", "planned_stops_min", "unplanned_stops_min", "rated_per_hour",
               "good_fills", "underfills_refilled", "leakers_rejected"], rows)


def build(WD, target):
    rs = lambda k: np.random.default_rng([WL.SEED, 100 + k])
    DS = {p: depot_split(WD.pools[p], rs(1 + j)) for j, p in enumerate(POOLS)}
    D = write_dockets(target, WD, rs(10))
    T = write_tags(target, WD, rs(11))
    n_reg = write_register(target, WD)
    write_stocktake(target, WD, DS)
    n_store = write_store(target, WD)
    n_rack = write_racking(target, WD, rs(12))
    n_aud = write_audits(target, WD, rs(13))
    n_acc, n_lines = write_accounts(target, WD)
    write_small(target, WD, DS, rs(14), D)
    counts = dict(docket_rows=D["rows"], dockets=D["dockets"], resent=D["resent"], resent_rows=D["resent_rows"],
                  blank_codes=D["blank"], tag_reads=T["reads"], tag_fittings=T["fittings"], cases=T["cases"],
                  not_traced=T["not_traced"], register=n_reg, store_rows=n_store, rackings=n_rack, audits=n_aud,
                  accounts=n_acc, lines=n_lines)
    return counts, dict(DS=DS, routes=routes(WD))
