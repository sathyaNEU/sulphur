"""Every figure of the answer blocks, computed from the shipped files and nothing else: each pool's account at the
count of 30 November 2026, what a dispense line holds (each cellar check rebuilt from the line's own dockets), the
containers the trade loses (the share of each purchase lot found on site against the lot's age), the cold store
under the 2027 brew plan, the weekly path of the 2027 season in the planning case and on each of ten recorded
summers, and the cover the fleet standard puts on the largest weekly shortfall. The same code runs the hurried,
direct, rigorous and run routes, the falsification check, the forcing and the battery of conventions that sets
every band. It imports nothing from the world or the core: the estimators mirror the core's on the pack's records.
"""
import datetime as dt
import math
import os

import numpy as np
import pandas as pd
from openpyxl import load_workbook

POOLS = ("K50", "K30", "K20", "FIR", "KIL")
NAMES = {"K50": "50 litre keg", "K30": "30 litre keg", "K20": "20 litre keg", "FIR": "firkin", "KIL": "kilderkin"}
PLURAL = {"K50": "50 litre kegs", "K30": "30 litre kegs", "K20": "20 litre kegs", "FIR": "firkins", "KIL": "kilderkins"}
# the fleet standard FS-04, issue 3
FLOAT = 2.0 / 7.0                     # 2.1: the float, two sevenths of the week's deliveries
SEASON_WEEKS = 21                     # 3.1: the 21 weeks from the week beginning on the first Monday of May
HOT_RANK = -2                         # 3.3: the second highest of the ten summers
SUMMERS = list(range(2017, 2027))     # 3.3: the ten summers of the 2027 review
# the maker's quotation Q26-1187: the minimum order run of each type (4.1, 4.2)
MIN_RUN = {"K50": 3500, "K30": 1500, "K20": 1200, "FIR": 1200, "KIL": 600}
FILES = {
    "dockets": "delivery_dockets_dec2023_nov2026.csv", "register": "container_register.csv",
    "count": "container_count_30nov2026.xlsx", "store": "cold_store_monday_position.csv",
    "racking": "racking_log.csv", "checks": "cellar_quality_checks_2025_2026.csv",
    "accounts": "trade_accounts.csv", "lines": "dispense_lines.csv", "products": "products.csv",
    "codes": "container_codes.csv", "weather": "calder_vale_station_weekly.csv", "plan": "brew_plan_2027.xlsx",
    "schedule": "maplestead_supply_agreement_schedules.xlsx", "routes": "route_plan_autumn_2026.xlsx",
}

# the golden's conventions (the core's GOLDEN), with the build's own four conventions at their golden readings
GOLDEN = dict(swing="lines", recon="days", store="runs", loss="age", fit="ols", rate="count_rate",
              count_months="all", harmonics=2, hinge=0.0, cover="mean", level=1, age_fit="wls", age_drop=0,
              alive="lots", clock="deliveries", last="account", age_from="purchase", run_stat="median", estate="shaped",
              x_b=1.0, x_cov=1.0, x_lam=1.0, x_del=1.0)
HURRIED = {"S1": {"recon": "face"}, "S2": {"store": "cover"}, "S3": {"loss": "none"}}
OVER = {"S1": {"swing": "prop"}, "S2": {"store": "wholerun"}, "S3": {"loss": "writeoff"}}
RIGOROUS = {"recon": "face", "store": "regress", "loss": "none"}
RUN = {
    "hedge": {"recon": "face", "store": "cover", "loss": "none"},
    "generous": {"recon": "whole", "store": "wholerun", "loss": "writeoff"},
    "calibrated": {"recon": "face", "swing": "level"},
    "cutoff": {"recon": "cut4"},
    "cutoff:three days": {"recon": "cut3"},
    "cutoff:summer counts": {"recon": "face", "count_months": "summer"},
    "cutoff:weekly rounds": {"recon": "face", "fit": "weekly"},
}
# every convention of the fork table marked "in the battery", alone: the core's sixteen and the build's four
SINGLES = [
    ("the cellar checks fitted one line for each delivery interval", {"fit": "byclass"}),
    ("a line's weekly sales from thirteen weeks of its dockets, not four", {"rate": "count_rate13"}),
    ("the summer's cellar checks only", {"count_months": "summer"}),
    ("the bend in the weather response a degree lower", {"hinge": -1.0}),
    ("the bend in the weather response a degree higher", {"hinge": 1.0}),
    ("one seasonal harmonic in the deliveries fit", {"harmonics": 1}),
    ("three seasonal harmonics in the deliveries fit", {"harmonics": 3}),
    ("the store's cover as the median week's, not the mean's", {"cover": "median"}),
    ("deliveries at the count over its last two weeks, not its own week's", {"level": 2}),
    ("deliveries at the count as the fit's value for its week", {"level": "fit"}),
    ("the lots fitted unweighted", {"age_fit": "ols"}),
    ("the lots fitted without the newest lot", {"age_drop": "newest"}),
    ("the lots fitted without the oldest lot", {"age_drop": "oldest"}),
    ("the oldest four lots against the newest four", {"age_fit": "ends"}),
    ("the fleet alive as the count over the fitted share on site", {"alive": "share"}),
    ("the loss carried on the calendar, not on deliveries", {"clock": "calendar"}),
    ("the dray's last call as the line's own last docket, not the account's", {"last": "line"}),
    ("a lot's age from the middle of the year on its stamp", {"age_from": "lotyear"}),
    ("a beer's racking run as the mean of its rackings", {"run_stat": "mean"}),
    ("the estate's scheduled volume level through the year", {"estate": "flat"}),
]


def family():
    """the golden, each convention alone, and every two that change different choices together"""
    out = [("the golden's conventions", {})] + list(SINGLES)
    for i, (n1, o1) in enumerate(SINGLES):
        for n2, o2 in SINGLES[i + 1:]:
            if not set(o1) & set(o2):
                o = dict(o1)
                o.update(o2)
                out.append((n1 + "; " + n2, o))
    return out


BATTERY = family()
# the core's own variant battery (core.FAMILY) and the build's four conventions alone: the rebuilds that set every band in
# the spec corelib prices (every convention of the fork table alone, and the core's three pairs)
FAMILY = [("the golden's conventions", {})] + list(SINGLES) + [
    ("thirteen weeks of dockets and the lines by interval together", {"rate": "count_rate13", "fit": "byclass"}),
    ("the summer checks and the two-week level together", {"count_months": "summer", "level": 2}),
    ("the unweighted lots and the calendar loss together", {"age_fit": "ols", "clock": "calendar"}),
]
# each fitted input moved by its spread, one at a time: the call has to hold (the core's FORCING)
FORCING = [
    ("what a line holds per container sold, 20 per cent down", {"x_b": 0.8}),
    ("what a line holds per container sold, 20 per cent up", {"x_b": 1.2}),
    ("the store's cover, 20 per cent down", {"x_cov": 0.8}),
    ("the store's cover, 20 per cent up", {"x_cov": 1.2}),
    ("the containers lost in a year, 20 per cent down", {"x_lam": 0.8}),
    ("the containers lost in a year, 20 per cent up", {"x_lam": 1.2}),
    ("the season's deliveries, 5 per cent down", {"x_del": 0.95}),
    ("the season's deliveries, 5 per cent up", {"x_del": 1.05}),
]


class Rec(object):
    pass


def monday(d):
    return d - dt.timedelta(days=d.weekday())


def first_monday_of_may(year):
    d = dt.date(year, 5, 1)
    return d + dt.timedelta(days=(7 - d.weekday()) % 7)


def cover_of(x, p):
    return "nothing" if x <= 0 else "hire" if x < MIN_RUN[p] else "buy"


def band_of(x, lines):
    return sum(1 for ln in lines[1:] if x >= ln) + (1 if x > lines[0] else 0)


def bare_lot(s):
    """a lot as the register and the count both key it, the maker's prefix taken off"""
    s = str(s).strip().upper()
    return s[2:] if s[:2] in ("CC", "LF") else s


def _date(x):
    return x.date() if hasattr(x, "date") else x


# ------------------------------------------------------------------------------------------------- the files
def load(target, mess=None):
    """the shipped files read into the records every estimator uses; `mess` mishandles one Layer 1 item on purpose
    (checks.py's neutrality block): dup_dockets, blank_codes, renumbered, lot_prefix, dup_checks"""
    R = Rec()
    f = lambda k: os.path.join(target, FILES[k])
    codes = pd.read_csv(f("codes"), dtype=str)
    to_pool = {}
    for _, r in codes.iterrows():
        for k in ("container", "docket_code", "register_code"):
            to_pool[r[k]] = r["container"]
    R.to_pool = to_pool
    prod = pd.read_csv(f("products"), dtype=str, keep_default_na=False)
    sku_pool = {r["sku"]: to_pool[r["container"]] for _, r in prod.iterrows()}
    acc = pd.read_csv(f("accounts"), dtype=str, keep_default_na=False)
    cur = {r["former_account_no"]: r["account_no"] for _, r in acc.iterrows() if r["former_account_no"]}
    R.n_accounts, R.renumbered = len(acc), len(cur)
    if mess == "renumbered":
        cur = {}
    # the dockets: a docket line re-sent by a handheld counted once, the container read from the product where blank
    dk = pd.read_csv(f("dockets"), dtype={"sku": str, "container": str, "account_no": str}, keep_default_na=False,
                     usecols=["docket_no", "delivery_date", "account_no", "line_no", "sku", "container", "qty"])
    R.docket_rows = len(dk)
    if mess != "dup_dockets":
        dk = dk.drop_duplicates(["docket_no", "line_no"])
    if mess == "blank_codes":
        dk = dk[dk["container"] != ""]
    R.resent_rows = R.docket_rows - len(dk)
    R.del_rows, R.blank_codes = len(dk), int((dk["container"] == "").sum())
    R.dockets = int(dk["docket_no"].nunique())
    date = pd.to_datetime(dk["delivery_date"])
    R.D0 = monday(date.min().date())
    day = (date - pd.Timestamp(R.D0)).dt.days.to_numpy()
    week = day // 7
    pool = dk["sku"].map(sku_pool).to_numpy()
    acct = dk["account_no"].map(lambda x: cur.get(x, x)).to_numpy()
    qty = dk["qty"].to_numpy(dtype=float)
    R.WH = int(week.max()) + 1
    WH = R.WH
    R.flow = {p: np.bincount(week[pool == p], weights=qty[pool == p], minlength=WH)[:WH] for p in POOLS}
    key = np.where(pool == "K20", acct + "|GUEST-20L", acct + "|" + dk["sku"].to_numpy())
    g = pd.DataFrame({"pool": pool, "key": key, "acct": acct, "day": day, "qty": qty})
    R.line_total = {p: g[g["pool"] == p].groupby("key")["qty"].sum() for p in POOLS}
    # each line's and each account's dockets by day, for the cellar checks
    ln = g.groupby(["key", "day"], sort=True)["qty"].sum().reset_index()
    R.line_days = {k: (v["day"].to_numpy(), np.cumsum(v["qty"].to_numpy())) for k, v in ln.groupby("key", sort=False)}
    ad = g.groupby(["acct", "day"], sort=True).size().reset_index()
    R.acct_days = {k: v["day"].to_numpy() for k, v in ad.groupby("acct", sort=False)}
    R.week_dates = [R.D0 + dt.timedelta(days=7 * i) for i in range(WH + 60)]
    # the route plan: deliveries a week by account
    ws = load_workbook(f("routes"), read_only=True)["Routes"]
    per = {}
    for r in list(ws.iter_rows(values_only=True))[1:]:
        per[r[4]] = int(r[6])
    R.interval = {a: (0.5 if n == 2 else 1.0) for a, n in per.items()}
    if mess == "renumbered":
        import collections
        R.interval = collections.defaultdict(lambda: 1.0, R.interval)
    # the dispense lines supplied at the count
    dl = pd.read_csv(f("lines"), dtype=str, keep_default_na=False)
    dl["pool"] = dl["container"].map(to_pool)
    R.lines, R.line_no = {}, {}
    for p in POOLS:
        x = dl[dl["pool"] == p]
        keys = (x["account_no"] + "|" + x["product"]).to_numpy()
        tot = R.line_total[p].reindex(keys).fillna(0.0).to_numpy()
        R.lines[p] = dict(keys=keys, rate=tot / float(WH), iv=np.array([R.interval[a] for a in x["account_no"]]))
    for _, r in dl.iterrows():
        R.line_no[(r["account_no"], int(r["line"]))] = r["product"]
    # the weather station: the week's mean daily maximum temperature and its normal
    wx = pd.read_csv(f("weather"), dtype=str, keep_default_na=False)
    R.temp = {dt.date.fromisoformat(r["week_beginning"]): float(r["mean_daily_max_c"]) for _, r in wx.iterrows()
              if r["mean_daily_max_c"]}
    R.normal = {dt.date.fromisoformat(r["week_beginning"]): float(r["normal_1991_2020_c"]) for _, r in wx.iterrows()}
    R.temp_hist = [R.temp[R.week_dates[i]] for i in range(WH)]
    # the count of 30 November 2026: every site by state, and the tally by lot
    wb = load_workbook(f("count"), read_only=True)
    R.take = {p: dict(onsite=0.0, store=0.0, idle=0.0, other=0.0) for p in POOLS}
    R.tally = {p: {} for p in POOLS}
    R.count_sites = []
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        R.asof = dt.datetime.strptime(" ".join(str(rows[1][1]).split()[1:]), "%d %b %Y").date()
        if ws.title == "Lots":
            for r in rows[4:]:
                if r[0] is not None:
                    p = to_pool[str(r[0])]
                    lot = bare_lot(r[1]) if mess != "lot_prefix" else str(r[1]).strip().upper()
                    R.tally[p][lot] = R.tally[p].get(lot, 0) + int(r[3])
            continue
        R.count_sites.append(ws.title)
        for r in rows[4:]:
            if r[0] is None:
                continue
            area, cont, state, n = r[:4]
            p = to_pool[str(cont)]
            R.take[p]["onsite"] += n
            R.take[p]["store" if area == "Cold store" else "idle" if state == "clean empty" else "other"] += n
    # the register: bought before the count and not condemned before it; the lots and their purchase dates
    reg = pd.read_csv(f("register"), dtype=str, keep_default_na=False)
    reg["pool"] = reg["container"].map(to_pool)
    reg["lot_b"] = reg["lot"].map(bare_lot) if mess != "lot_prefix" else reg["lot"].map(lambda s: str(s).strip().upper())
    R.register_rows = len(reg)
    asof = R.asof.isoformat()
    on = (reg["purchased"] < asof) & ((reg["condemned_on"] == "") | (reg["condemned_on"] >= asof))
    lo = (R.D0 + dt.timedelta(days=7 * (WH - 52))).isoformat()
    R.lots, R.register, R.condemned = {}, {}, {}
    for p in POOLS:
        x = reg[reg["pool"] == p]
        R.register[p] = int(on[reg["pool"] == p].sum())
        R.condemned[p] = int(((x["condemned_on"] >= lo) & (x["condemned_on"] < asof)).sum())
        rows = []
        for lot, y in x.groupby("lot_b", sort=True):
            dates = pd.to_datetime(y["purchased"])
            age = float(((pd.Timestamp(R.asof) - dates).dt.days / 365.25).mean())
            year = int(lot.split("-")[-1])
            if mess == "lot_prefix" and lot not in R.tally[p]:
                continue
            age_y = (R.asof - dt.date(year, 7, 1)).days / 365.25
            rows.append((lot, age, age_y, int(on[y.index].sum()), int(R.tally[p].get(lot, 0)), len(y)))
        R.lots[p] = dict(lot=[r[0] for r in rows], age=np.array([r[1] for r in rows]),
                         age_y=np.array([r[2] for r in rows]), reg=np.array([r[3] for r in rows], dtype=float),
                         ons=np.array([r[4] for r in rows], dtype=float), bought=np.array([r[5] for r in rows]))
    # the cold store's Monday position: the stock at the close of week i is the next Monday's
    st = pd.read_csv(f("store"), dtype={"container": str})
    R.store = {}
    for p in POOLS:
        x = st[st["container"].map(to_pool) == p]
        i = ((pd.to_datetime(x["position_date"]) - pd.Timestamp(R.D0)).dt.days // 7).to_numpy()
        v = np.zeros(WH + 1)
        v[i] = x["full_containers"].to_numpy(dtype=float)
        R.store[p] = v[1:WH + 1]
    rk = pd.read_csv(f("racking"), dtype={"container": str})
    rk["pool"] = rk["container"].map(to_pool)
    rk["week"] = (pd.to_datetime(rk["racked_on"]) - pd.Timestamp(R.D0)).dt.days // 7
    R.rackings = len(rk)
    R.rk = rk
    # the trade quality reps' cellar checks: a line checked twice on one call taken once
    ck = pd.read_csv(f("checks"), dtype={"account_no": str, "container": str, "product": str}, keep_default_na=False)
    R.check_rows = len(ck)
    if mess != "dup_checks":
        ck = ck.drop_duplicates(["check_ref", "account_no", "line"])
    R.check_doubles = R.check_rows - len(ck)
    ck["pool"] = ck["container"].map(to_pool)
    ck["acct"] = ck["account_no"].map(lambda x: cur.get(x, x))
    ck["key"] = np.where(ck["pool"] == "K20", ck["acct"] + "|GUEST-20L", ck["acct"] + "|" + ck["product"])
    ck["full"] = ck["full_in_cellar"].astype(float) + ck["on_dispense"].astype(float)
    cd = pd.to_datetime(ck["check_date"])
    ck["day"] = (cd - pd.Timestamp(R.D0)).dt.days
    ck["month"] = cd.dt.month
    R.check_calls = int(ck["check_ref"].nunique())
    R.counts = {}
    for p in POOLS:
        x = ck[ck["pool"] == p]
        d = x["day"].to_numpy()
        days, days_l, r4, r13, rs = [], [], [], [], []
        ptot = float(R.flow[p].sum())
        for k, a, c in zip(x["key"], x["acct"], d):
            ld, lq = R.line_days[k]
            j = int(np.searchsorted(ld, c)) - 1                     # the line's own last docket before the call
            days_l.append(float(c - ld[j]))
            aj = R.acct_days[a]                                     # the dray's last call at the account
            days.append(float(c - aj[int(np.searchsorted(aj, c)) - 1]))
            q = lambda lo: float(lq[j] - (lq[int(np.searchsorted(ld, lo)) - 1] if np.searchsorted(ld, lo) > 0 else 0.0))
            r4.append(q(c - 28) / 4.0)
            r13.append(q(c - 91) / 13.0)
            # the line's share of its type's deliveries over the record, times the type's deliveries in the week of the call
            rs.append(float(R.line_total[p].get(k, 0.0)) / ptot * float(R.flow[p][min(int(c // 7), WH - 1)]))
        R.counts[p] = dict(count_rate=np.array(r4), count_rate13=np.array(r13), count_rate_share=np.array(rs),
                           count_iv=np.array([R.interval[a] for a in x["acct"]]), count_full=x["full"].to_numpy(),
                           count_days=np.array(days), count_days_line=np.array(days_l),
                           count_month=x["month"].to_numpy(), count_day=d)
    # the 2027 brew plan and the supply agreement's schedules
    ws = load_workbook(f("plan"), read_only=True).worksheets[0]
    R.plan = {p: [] for p in POOLS}
    for r in list(ws.iter_rows(values_only=True))[4:]:
        if r[0]:
            R.plan[to_pool[r[2]]].append((r[0], _date(r[4]), _date(r[5]), float(r[6])))
    wb = load_workbook(f("schedule"), read_only=True)
    cols = {"K50": 5, "K30": 6, "K20": 7, "FIR": 8}
    R.estate = {p: [] for p in POOLS}
    for r in list(wb.worksheets[0].iter_rows(values_only=True))[4:]:
        if r[0]:
            for p, c in cols.items():
                if r[c]:
                    R.estate[p].append((_date(r[3]), int(r[c])))
    R.estate_volume = {p: 0.0 for p in POOLS}
    named = {NAMES[p]: p for p in POOLS}
    for r in list(wb.worksheets[1].iter_rows(values_only=True))[3:]:
        if r[0] in named:
            R.estate_volume[named[r[0]]] = float(r[2])
    R.estate_pubs = len(list(wb.worksheets[0].iter_rows(values_only=True))) - 4
    R.season = season_of(R)
    # by 2027 week: the estate's lines listed by its Monday, and the racking runs of the beers on sale
    R.n_live, R.runs_on, R.beers_on = {}, {}, {}
    for p in POOLS:
        R.n_live[p], R.runs_on[p], R.beers_on[p] = {}, {}, {}
        for i in range(WH, R.season[-1] + 1):
            d = R.week_dates[i]
            R.n_live[p][i] = sum(n for day, n in R.estate[p] if day <= d)
            on = beers_on_sale(R, p, d)
            R.runs_on[p][i], R.beers_on[p][i] = float(sum(run for s, run in on)), len(on)
    return R


def season_of(R):
    """the 2027 season's week indices (FS-04 3.1)"""
    i0 = (first_monday_of_may(R.asof.year + 1) - R.D0).days // 7
    return list(range(i0, i0 + SEASON_WEEKS))


def summer_temps(R, year):
    """the 2027 season on the recorded weather of one summer, its 21 weeks taken in order (FS-04 3.3)"""
    d0 = first_monday_of_may(year)
    return {i: R.temp[d0 + dt.timedelta(days=7 * k)] for k, i in enumerate(R.season)}


# ------------------------------------------------------------------------------------------------- the estimators
_CACHE = {}


def cached(kind, R, p, o, keys, fn):
    k = (kind, id(R), p) + tuple(o[x] for x in keys)
    if k not in _CACHE:
        _CACHE[k] = fn()
    return _CACHE[k]


def doy(R, i):
    return (R.D0 + dt.timedelta(days=7 * i + 3)).timetuple().tm_yday


def fit_sales(R, p, harmonics, hinge=0.0):
    """weekly deliveries on the season, the trend and the week's temperature, with a bend at the temperature the
    record itself fits best (moved by `hinge` degrees in the battery)"""
    WH = R.WH
    y = np.log(R.flow[p])
    T = R.temp_hist

    def row(i, temp, h0, level=1.0):
        x = [level, level * i / 52.0]
        for h in range(1, harmonics + 1):
            ang = 2 * math.pi * h * doy(R, i) / 365.0
            x += [math.cos(ang), math.sin(ang)]
        return x + [max(temp - h0, 0.0), min(temp - h0, 0.0)]

    def fit(h0):
        X = np.array([row(i, T[i], h0) for i in range(WH)])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        return float(((X @ beta - y) ** 2).sum()), beta
    best = min((fit(h0)[0], h0) for h0 in np.arange(12.0, 22.01, 0.5))[1]
    h0 = best + hinge
    sse, beta = fit(h0)
    predict = lambda i, temp: float(math.exp(np.dot(beta, row(i, temp, h0))))
    shape = lambda i, temp: float(math.exp(np.dot(beta, row(i, temp, h0, 0.0))))
    year = float(np.mean([shape(i, R.normal[R.week_dates[i]]) for i in range(WH - 52, WH)]))
    return predict, shape, year, h0, sse


def fit_cellar(R, p, o):
    """containers a line holds: a number whatever it sells (a), a number per container it sells a week (b1) and a
    number per container it sells a week and week between deliveries (b2). A check is of full containers, so what
    the line holds is the count and the containers it has sold since the dray last called at the account, which took
    the empties then (`days`); or the count as
    it stands (`face`), with half a delivery or a whole one added (`half`, `whole`), on the calls soonest after a
    delivery (`cut3`, `cut4`), or with the days since the delivery as a term of the fit (`joint`)"""
    rec = R.counts[p]
    rate, iv, full = rec[o["rate"]], rec["count_iv"], rec["count_full"]
    days = rec["count_days_line"] if o["last"] == "line" else rec["count_days"]
    keep = np.ones(len(rate), bool)
    if o["count_months"] == "summer":
        keep &= (rec["count_month"] >= 4) & (rec["count_month"] <= 9)
    recon = o["recon"]
    if recon.startswith("cut"):
        keep &= days <= np.where(iv == 1.0, float(recon[3:]), 2.0)
    if o["fit"] == "weekly":
        keep &= iv == 1.0
    rate, iv, full, days = rate[keep], iv[keep], full[keep], days[keep]
    sold = rate * days / 7.0
    if recon == "joint":
        a, b1, b2, bd = np.linalg.lstsq(np.column_stack([np.ones(len(rate)), rate, rate * iv, sold]), full,
                                        rcond=None)[0]
        return float(a), (lambda x: float(b1 + b2 * x)), float(bd), int(len(full))
    held = full + {"days": sold, "half": rate * iv / 2.0, "whole": rate * iv}.get(recon, 0.0)
    if o["fit"] == "weekly":                                      # the weekly rounds only: one slope, carried to all
        b, a = np.polyfit(rate, held, 1)
        return float(a), (lambda x: float(b)), None, int(len(full))
    if o["fit"] == "ols":
        a, b1, b2 = np.linalg.lstsq(np.column_stack([np.ones(len(rate)), rate, rate * iv]), held, rcond=None)[0]
        return float(a), (lambda x: float(b1 + b2 * x)), None, int(len(full))
    slope, icpt = {}, {}
    for x in sorted(set(iv.tolist())):                           # one line through the checks of each interval
        k = iv == x
        slope[x], icpt[x] = np.polyfit(rate[k], held[k], 1)
    return float(icpt[1.0]), (lambda x: float(slope[x])), None, int(len(full))


def fit_age(R, p, o):
    """the share of each purchase lot the count found on site against the lot's age: its fall with age is the share
    of the fleet that leaves each year, and its level at age nought the share of the fleet that is on site. Returns
    the yearly rate of leaving (continuous) and the share on site"""
    L = R.lots[p]
    age = L["age_y"] if o["age_from"] == "lotyear" else L["age"]
    reg, ons = L["reg"], L["ons"]
    k = ons > 0
    order = np.argsort(age)
    if o["age_drop"] == "newest":
        k[order[0]] = False
    elif o["age_drop"] == "oldest":
        k[order[-1]] = False
    x, y, wt = age[k], np.log(ons[k] / reg[k]), ons[k]
    if o["loss"] == "origin":                                     # every lot's whole absence from site read as loss
        return float(-(wt * x * y).sum() / (wt * x * x).sum()), 1.0
    if o["age_fit"] == "ols":
        wt = np.ones(len(x))
    if o["age_fit"] == "ends":                                    # the oldest four lots against the newest four
        idx = np.argsort(x)
        lo, hi = idx[:4], idx[-4:]
        rr, oo = reg[k], ons[k]
        lam = (math.log(oo[lo].sum() / rr[lo].sum()) - math.log(oo[hi].sum() / rr[hi].sum())) / \
              (np.average(x[hi], weights=rr[hi]) - np.average(x[lo], weights=rr[lo]))
        f = oo[lo].sum() / rr[lo].sum() * math.exp(lam * np.average(x[lo], weights=rr[lo]))
        return float(lam), float(f)
    sw = np.sqrt(wt)
    b, a = np.linalg.lstsq(np.column_stack([x * sw, sw]), y * sw, rcond=None)[0]
    return float(-b), float(math.exp(a))


def runs_of(R, p, stat="median", start=52):
    """each beer's racking run for one container type over the last two years of the log"""
    def go():
        g = R.rk[(R.rk["pool"] == p) & (R.rk["week"] >= start)].groupby("sku")["containers_filled"]
        return (g.median() if stat == "median" else g.mean()).to_dict()
    return cached("runs", R, p, dict(stat=stat, start=start), ("stat", "start"), go)


def beers_on_sale(R, p, d):
    return [(s, run) for s, a, b, run in R.plan[p] if a <= d <= b]


def chain(R, p, opt=None, temps=None):
    """one pool's shortfall in its busiest week of the 2027 season from the records, with every step's option"""
    o = dict(GOLDEN)
    o.update(opt or {})
    WH = R.WH
    T, flow = R.take[p], R.flow[p]
    L = len(R.lines[p]["keys"])
    a, slope, bd, n_counts = cached("cellar", R, p, o, ("recon", "fit", "rate", "count_months", "last"),
                                    lambda: fit_cellar(R, p, o))
    lr, li = R.lines[p]["rate"], R.lines[p]["iv"]                 # the trade's containers per container sold a week
    ivs = sorted(set(li.tolist()))
    share = {x: float(lr[li == x].sum()) / float(lr.sum()) for x in ivs}
    b, m = slope(1.0) / 2.0, 2.0 * sum(slope(x) * share[x] for x in ivs) / slope(1.0)
    b *= o["x_b"]
    predict, shape, ys, h0, _ = cached("sales", R, p, o, ("harmonics", "hinge"),
                                       lambda: fit_sales(R, p, o["harmonics"], o["hinge"]))
    if o["level"] == "fit":
        lev = predict(WH - 1, R.temp_hist[WH - 1])
    else:
        lev = float(flow[WH - o["level"]:WH].mean())
    year = float(flow[WH - 52:WH].sum())
    lots = R.lots[p]
    lam_y = share_on = None
    # the fleet alive, and the containers the trade loses in a year
    if o["loss"] == "none":                                       # the register read as the fleet
        alive, year_loss = float(R.register[p]), 0.0
    elif o["loss"] == "writeoff":                                 # what the register holds beyond the site and the
        held0 = a * L + b * m * lev                               # cellars, written off over the three years on record
        alive, year_loss = T["onsite"] + held0, max(R.register[p] - T["onsite"] - held0, 0.0) / 3.0
    else:
        lam_y, share_on = cached("age", R, p, o, ("loss", "age_fit", "age_drop", "age_from"), lambda: fit_age(R, p, o))
        age = lots["age_y"] if o["age_from"] == "lotyear" else lots["age"]
        alive = float((lots["reg"] * np.exp(-lam_y * age)).sum()) if o["alive"] == "lots" else T["onsite"] / share_on
        year_loss = alive * (math.exp(lam_y) - 1.0)
    year_loss *= o["x_lam"]
    lam = year_loss / year                                        # per container delivered
    scrap = R.condemned[p] / year                                 # condemned at the wash, per container delivered
    alive_out = alive - T["onsite"]                               # the trade's containers at the count, alive
    if o["loss"] == "none":                                       # no loss known: the counts as they stand, every line
        o2 = dict(o, recon="face")
        af, sf, _, _ = cached("cellar", R, p, o2, ("recon", "fit", "rate", "count_months", "last"),
                              lambda: fit_cellar(R, p, o2))
        alive_out = af * L + sum(sf(x) * share[x] for x in ivs) * lev
    if o["swing"] == "level":                                     # the counts as they stand, scaled to that level
        scale = alive_out / (a * L + b * m * lev)
        a, b = a * scale, b * scale
    # the store: its cover in weeks of deliveries, beside the half run each beer on sale holds on average
    runs26 = runs_of(R, p, o["run_stat"])
    full26 = float(sum(runs26.values()))
    part = 1.0 if o["store"] == "wholerun" else 0.5               # a whole run for each beer, or half of one
    st = R.store[p]
    reg = np.polyfit(flow[52:], st[52:], 1)
    cov = (float(st[52:].mean()) - part * full26) / float(flow[52:].mean()) if o["cover"] == "mean" else \
        float(np.median((st[52:] - part * full26) / flow[52:]))
    cov *= o["x_cov"]
    c2 = T["other"] / lev
    vol = R.estate_volume[p]
    path, cum = [], 0.0
    for i in range(WH, R.season[-1] + 1):
        d = R.week_dates[i]
        j = i - 52
        temp = R.normal[d] if temps is None or i not in temps else temps[i]
        F = predict(i, temp) * o["x_del"]
        n_live = R.n_live[p][i]
        es = n_live * vol * (shape(i, temp) / ys if o["estate"] == "shaped" else 1.0)
        est = a * n_live + b * 2.0 * es
        D = F + es
        if o["swing"] == "prop":                                  # the trade's stock moved with the deliveries
            swing = alive_out * (D / lev - 1.0)
        else:
            swing = b * m * (F - lev) + est
        if o["store"] in ("runs", "wholerun"):
            store = cov * D + part * R.runs_on[p][i]
        elif o["store"] == "cover":
            store = float(st[j - 2:j + 3].mean() / flow[j - 2:j + 3].mean()) * D
        else:
            store = float(reg[1] + reg[0] * D)
        cum += (lam * D if o["clock"] == "deliveries" else year_loss / 52.18) + scrap * D
        other, fl = c2 * D, FLOAT * D
        need = swing + store + other + fl                         # beside the trade's containers at the count
        path.append(dict(i=i, date=d, D=D, F=F, es=es, est=est, swing=swing, store=store, other=other, float=fl,
                         drain=cum, need=need, short=need - T["onsite"] + cum, beers=R.beers_on[p][i], temp=temp))
    season = [x for x in path if x["i"] in R.season]
    pick = max(season, key=lambda x: x["short"])
    return dict(short=pick["short"], week=pick["i"], date=pick["date"], swing=pick["swing"], store=pick["store"],
                year_loss=year_loss, rise=max(x["swing"] for x in season), fullest=max(x["store"] for x in season),
                lam=lam, a=a, b=b, m=m, alive=alive, alive_out=alive_out, days_coef=bd, cov=cov, c2=c2,
                half26=full26 / 2.0, scrap=scrap, lev=lev, hinge=h0, n_counts=n_counts, lam_y=lam_y,
                share_on=share_on, path=path, pick=pick, onsite=T["onsite"], L=L, slope1=slope(1.0),
                slope_half=slope(0.5) if 0.5 in ivs else None)


def direct(R, p, temps=None):
    """the register read as the fleet: the requirement built from the records as they stand (the cellar checks
    carried to every line, the store at its weeks of cover) less every container the register holds"""
    o = dict(GOLDEN, recon="face", store="cover", loss="none")
    g = chain(R, p, o, temps)
    a, slope, _, _ = fit_cellar(R, p, o)
    lr, li = R.lines[p]["rate"], R.lines[p]["iv"]
    ivs = sorted(set(li.tolist()))
    lev = fit_sales(R, p, 2)[0](R.WH - 1, R.temp_hist[R.WH - 1])
    held = a * len(lr) + sum(slope(x) * float(lr[li == x].sum()) / float(lr.sum()) for x in ivs) * lev
    return g["short"] + R.take[p]["onsite"] + held - R.register[p]


def hot(R, fn):
    """a figure in the hot case: the second highest of the ten summers (FS-04 3.3); also the ten"""
    v = sorted(fn(summer_temps(R, y)) for y in SUMMERS)
    return float(v[HOT_RANK]), v


def lattice_opts():
    keys = {}
    ids = sorted(HURRIED)
    for mask in range(1, 2 ** len(ids)):
        o = {}
        for k, s in enumerate(ids):
            if mask >> k & 1:
                o.update(HURRIED[s])
        keys["+".join(s for k, s in enumerate(ids) if mask >> k & 1)] = o
    return keys


def days_check(R):
    """the falsification check: across every pool's cellar checks in one fit, each pool with its own relation to a
    line's sales and delivery interval, the fall in the full containers counted for each container the line has
    sold since its last delivery"""
    X, y = [], []
    for k, p in enumerate(POOLS):
        rec = R.counts[p]
        rate, iv, full, days = rec["count_rate"], rec["count_iv"], rec["count_full"], rec["count_days"]
        blk = np.zeros((len(rate), 3 * len(POOLS) + 1))
        blk[:, 3 * k], blk[:, 3 * k + 1], blk[:, 3 * k + 2], blk[:, -1] = 1.0, rate, rate * iv, rate * days / 7.0
        X.append(blk)
        y.append(full)
    X, y = np.vstack(X), np.concatenate(y)
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    res = y - X @ beta
    se = math.sqrt(float(res @ res) / (len(y) - X.shape[1]) * float(np.linalg.inv(X.T @ X)[-1, -1]))
    return float(beta[-1]), se, int(len(y))


def spreads(R, p, reps=120, seed=11):
    """each fitted input's own measured spread for one pool, as a share of its value: what a line holds per
    container sold (the checks resampled), the store's cover (the weeks resampled in blocks of four), the containers
    lost in a year (the lots resampled) and the worst week's deliveries (the fit's residuals resampled)"""
    rng = np.random.default_rng(seed)
    rec = R.counts[p]
    lr, li = R.lines[p]["rate"], R.lines[p]["iv"]
    n = len(rec["count_full"])
    keep = R.counts[p]
    bm = []
    for _ in range(reps):
        idx = rng.integers(0, n, n)
        R.counts[p] = {k: v[idx] for k, v in keep.items()}
        sl = fit_cellar(R, p, GOLDEN)[1]
        bm.append(sum(sl(x) * float(lr[li == x].sum()) for x in set(li.tolist())) / float(lr.sum()))
    R.counts[p] = keep
    half = sum(runs_of(R, p).values()) / 2.0
    st, fl = R.store[p][52:], R.flow[p][52:]
    cv = []
    for _ in range(reps):
        idx = np.concatenate([np.arange(k * 4, k * 4 + 4) for k in rng.integers(0, len(st) // 4, len(st) // 4)])
        cv.append((st[idx].mean() - half) / fl[idx].mean())
    lots = R.lots[p]
    nl = len(lots["age"])
    lams = []
    for _ in range(reps):
        idx = rng.integers(0, nl, nl)
        R.lots[p] = {k: (np.asarray(v)[idx] if k != "lot" else v) for k, v in lots.items()}
        if len(set(R.lots[p]["age"].tolist())) >= 4:
            lams.append(math.exp(fit_age(R, p, GOLDEN)[0]) - 1.0)
    R.lots[p] = lots
    g = chain(R, p)
    predict = fit_sales(R, p, 2)[0]
    fit = np.array([predict(i, R.temp_hist[i]) for i in range(R.WH)])
    res = np.log(R.flow[p]) - np.log(fit)
    keepf = R.flow[p]
    pk = []
    for _ in range(reps // 3):
        R.flow[p] = fit * np.exp(rng.choice(res, len(res)))
        pk.append(fit_sales(R, p, 2)[0](g["week"], R.normal[R.week_dates[g["week"]]]))
    R.flow[p] = keepf
    return dict(x_b=float(np.std(bm) / np.mean(bm)), x_cov=float(np.std(cv) / abs(np.mean(cv))),
                x_lam=float(np.std(lams) / np.mean(lams)),
                x_del=float(np.std(pk) / predict(g["week"], R.normal[R.week_dates[g["week"]]])))


def run(target):
    R = load(target)
    lat_o = lattice_opts()
    X = dict(R=R, gold={}, fam={}, bat={}, hot_bat={}, lat={}, hot={}, hot_fam={}, hot_lat={}, runs={}, hot_runs={}, over={})
    for p in POOLS:
        X["gold"][p] = chain(R, p)
        X["fam"][p] = [chain(R, p, o) for _, o in FAMILY]
        X["bat"][p] = [chain(R, p, o) for _, o in BATTERY]
        X["lat"][p] = {k: chain(R, p, o) for k, o in lat_o.items()}
        X["runs"][p] = {k: chain(R, p, o) for k, o in RUN.items()}
        X["over"][p] = {s: chain(R, p, o) for s, o in OVER.items()}
        X["hot"][p] = hot(R, lambda t: chain(R, p, None, t)["short"])
        X["hot_fam"][p] = [hot(R, lambda t: chain(R, p, o, t)["short"])[0] for _, o in FAMILY]
        X["hot_bat"][p] = [hot(R, lambda t: chain(R, p, o, t)["short"])[0] for _, o in BATTERY]
        X["hot_lat"][p] = {k: hot(R, lambda t: chain(R, p, o, t)["short"])[0] for k, o in lat_o.items()}
        X["hot_runs"][p] = {k: hot(R, lambda t: chain(R, p, o, t)["short"])[0] for k, o in RUN.items()}
    X["direct"] = {p: direct(R, p) for p in POOLS}
    X["rigorous"] = {p: chain(R, p, RIGOROUS) for p in POOLS}
    X["hot_direct"] = {p: hot(R, lambda t: direct(R, p, t))[0] for p in POOLS}
    X["hot_rigorous"] = {p: hot(R, lambda t: chain(R, p, RIGOROUS, t)["short"])[0] for p in POOLS}
    X["forcing"] = {name: {p: chain(R, p, o)["short"] for p in POOLS} for name, o in FORCING}
    X["spreads"] = {p: spreads(R, p) for p in POOLS}
    X["corners"] = {side: {p: chain(R, p, {k: 1.0 + sign * 2.0 * X["spreads"][p][k] for k in X["spreads"][p]})["short"]
                           for p in POOLS} for side, sign in (("down", -1.0), ("up", 1.0))}
    X["days_check"] = days_check(R)
    X["joint"] = {p: chain(R, p, {"recon": "joint"}) for p in POOLS}
    X["allowances"] = {k: {p: chain(R, p, {"recon": k}) for p in POOLS} for k in ("half", "whole")}
    X["level4"] = {p: chain(R, p, {"level": 4})["short"] for p in POOLS}
    return X


if __name__ == "__main__":
    import sys
    import time
    t0 = time.time()
    X = run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target"))
    R = X["R"]
    print("pool   golden  fam lo  fam hi |     S1      S2      S3 | reflex  direct   rigor |  hot  | cover")
    for p in POOLS:
        g, fam, lat = X["gold"][p], [x["short"] for x in X["fam"][p]], X["lat"][p]
        print("%-4s %8.0f %7.0f %7.0f | %6.0f %7.0f %7.0f | %6.0f %7.0f %7.0f | %5.0f | %s  wk %s" % (
            p, g["short"], min(fam), max(fam), lat["S1"]["short"], lat["S2"]["short"], lat["S3"]["short"],
            lat["S1+S2+S3"]["short"], X["direct"][p], X["rigorous"][p]["short"], X["hot"][p][0],
            cover_of(g["short"], p), g["date"]))
    for p in POOLS:
        g = X["gold"][p]
        print("%-4s a %.2f b %.3f m %.3f cov %.3f c2 %.3f lam_y %.4f share %.3f alive %6.0f yl %5.0f rise %5.0f "
              "fullest %5.0f lev %5.0f onsite %5.0f reg %6d counts %d" % (
                  p, g["a"], g["b"], g["m"], g["cov"], g["c2"], g["lam_y"], g["share_on"], g["alive"], g["year_loss"],
                  g["rise"], g["fullest"], g["lev"], g["onsite"], R.register[p], g["n_counts"]))
    for k, v in sorted(X["runs"]["K50"].items()):
        print("  run %-22s %s" % (k, " ".join("%7.0f" % X["runs"][p][k]["short"] for p in POOLS)))
    for s in ("S1", "S2", "S3"):
        print("  over %s %s" % (s, " ".join("%7.0f" % X["over"][p][s]["short"] for p in POOLS)))
    print("  days check %.3f (se %.3f, n %d)" % X["days_check"])
    print("time %.0fs" % (time.time() - t0))
