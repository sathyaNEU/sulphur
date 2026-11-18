"""Every figure of the answer blocks, computed from the shipped files and nothing else: each pool's stock account at
the four counts, what a dispense line holds, the containers the trade loses, the cold store under the 2027 brew plan,
the weekly path of the 2027 season in the planning case and on each of ten recorded summers, and the cover the fleet
standard puts on the largest weekly shortfall. The same code runs the hurried, direct and standard routes and the
battery of conventions that sets every band. It imports nothing from the world or the core."""
import datetime as dt
import math
import os
import sqlite3

import numpy as np
import pandas as pd
from openpyxl import load_workbook

POOLS = ("K50", "K30", "K20", "FIR", "KIL")
TAGGED = "K20"
NAMES = {"K50": "50 litre keg", "K30": "30 litre keg", "K20": "20 litre keg", "FIR": "firkin", "KIL": "kilderkin"}
PLURAL = {"K50": "50 litre kegs", "K30": "30 litre kegs", "K20": "20 litre kegs", "FIR": "firkins", "KIL": "kilderkins"}
# the fleet standard FS-04, issue 3
FLOAT = 2.0 / 7.0                     # 2.1: the float, two sevenths of the week's deliveries
SEASON_WEEKS = 21                     # 3.1: the 21 weeks from the week beginning on the first Monday of May
HOT_RANK = -2                         # 3.3: the second highest of the ten summers
SUMMERS = list(range(2017, 2027))     # 3.3: the ten summers of the 2027 review
# the maker's quotation Q26-1187: the minimum order run of each type
MIN_RUN = {"K50": 3500, "K30": 1500, "K20": 1200, "FIR": 1200, "KIL": 600}
FILES = {
    "dockets": "delivery_dockets_dec2023_nov2026.csv", "tags": "foundry_keg_tag_reads.sqlite",
    "register": "container_register.csv", "stocktake": "annual_container_counts.xlsx",
    "store": "cold_store_monday_position.csv", "racking": "racking_log.csv", "audits": "cellar_audits_2025_2026.csv",
    "accounts": "trade_accounts.csv", "products": "products.csv", "codes": "container_codes.csv",
    "weather": "calder_vale_station_weekly.csv", "cases": "kegtrace_cases.csv",
    "plan": "brew_plan_2027.xlsx", "schedule": "maplestead_supply_agreement_schedules.xlsx",
    "routes": "route_plan_autumn_2026.xlsx", "depots": "depot_stock_weekly.csv", "wash": "wash_line_daily_log.csv",
}
GOLDEN = dict(swing="lines", store="runs", loss="account", loss_years=1, trade_change=True, fit="ols",
              count_months="all", rate="week", share="record", harmonics=2, hinge=0.0, cover="mean", other="mean",
              level="fit", census=False, account_tagged=False, condemned=True, tag_window="closed", census_scale=True,
              bend=True, trend=True, cover_weeks=104, estate="shaped", run_stat="median", run_from=52, scrap_years=1,
              split="half", ahead="trend", period="year", first="record", accrue="week", estate_temp="week",
              census_lost=False, pair="ended", x_b=1.0, x_cov=1.0, x_lam=1.0, x_del=1.0)
HURRIED = {"S1": {"swing": "prop"}, "S2": {"store": "cover"}, "S3": {"loss": "tag"}}
RIGOROUS = {"swing": "tracked", "store": "regress", "loss": "tag"}
SINGLES = [
    ("the loss over the last two years of the account", {"loss_years": 2}),
    ("the loss over all three years of the account", {"loss_years": 3}),
    ("the customers' own change in stock between the counts left out of the loss", {"trade_change": False}),
    ("the cellar counts fitted one line for each delivery interval", {"fit": "byclass"}),
    ("the bend in the weather response a degree lower", {"hinge": -1.0}),
    ("the bend in the weather response a degree higher", {"hinge": 1.0}),
    ("the summer's cellar counts only", {"count_months": "summer"}),
    ("one seasonal harmonic in the deliveries fit", {"harmonics": 1}),
    ("three seasonal harmonics in the deliveries fit", {"harmonics": 3}),
    ("the store's cover as the median week's", {"cover": "median"}),
    ("the store's cover from the last year's Mondays only", {"cover_weeks": 52}),
    ("the store's cover from all three years' Mondays", {"cover_weeks": 156}),
    ("depots, wash and repair at the last count's weeks of deliveries", {"other": "last"}),
    ("the depots from their weekly stock, wash and repair from the counts", {"other": "weekly"}),
    ("deliveries at each count as the four weeks before it", {"level": 4}),
    ("deliveries at each count as the two weeks before it", {"level": 2}),
    ("deliveries at each count as the week before it", {"level": 1}),
    ("the 20 litre kegs' stock at customers from their own tags", {"census": True}),
    ("the tags' count of kegs at customers not scaled for missed reads", {"census": True, "census_scale": False}),
    ("the 20 litre kegs' loss from the stock account", {"account_tagged": True}),
    ("a line's sales in the count's week from the fitted deliveries", {"rate": "fit"}),
    ("a line's sales in the count's week from four weeks of deliveries", {"rate": "four"}),
    ("a line's share of its type's deliveries from the last year only", {"share": "year"}),
    ("the 20 litre kegs' loss on the year to the last count, open cases as not traced", {"tag_window": "last"}),
    ("the bend in the weather response kept only for the types whose record asks for it", {"bend": "test"}),
    ("a quadratic in temperature in place of the bend", {"bend": "quad"}),
    ("the trend kept only for the types whose record shows one", {"trend": "test"}),
    ("the trend not carried past the count", {"ahead": "hold"}),
    ("the estate's scheduled volume level through the year", {"estate": "flat"}),
    ("the store's stock split by fitting the Monday stock on the deliveries", {"split": "regress", "cover_weeks": 104}),
    ("a beer's racking run as the mean of its rackings", {"run_stat": "mean"}),
    ("the wash line's condemnations over the three years of the account", {"scrap_years": 3}),
    ("the seasonal harmonics on a 52 week year", {"period": "52w"}),
    ("deliveries at the first count from the fit carried back a week", {"first": "back"}),
    ("the cellar counts fitted with a line's level and its movement through the year apart, on all the counts and four weeks of deliveries",
     {"fit": "apart", "rate": "four", "count_months": "all"}),
    ("a line's sales from its own dockets over the thirteen weeks to the count", {"rate": "own13"}),
    ("the 20 litre kegs' response at customers from their tags' rise to summer 2026", {"census": "response"}),
    ("the store's cover as the fitted slope beside half the plan's runs", {"split": "slope", "cover_weeks": 104}),
    ("the wash line's backlog and the repair bay from the wash line's log, week by week", {"other": "log"}),
    ("the loss and the condemnations counted to the end of the week before", {"accrue": "before"}),
    ("the estate's season at the normal in the hot case", {"estate_temp": "normal"}),
]
# readings the files refuse, each by a figure the answer blocks state: never in a band
REFUSED = [
    ("containers condemned at the wash after the count left out", {"condemned": False}),
    ("a single slope in the weather response", {"bend": False}),
    ("no trend in the deliveries fit for any type", {"trend": False}),
    ("the store's stock split fitted on the last year's Mondays alone", {"split": "regress", "cover_weeks": 52}),
    ("deliveries at each count as the eight weeks before it", {"level": 8}),
    ("deliveries at each count as the thirteen weeks before it", {"level": 13}),
    ("a line's sales from its own dockets over the four weeks to the count", {"rate": "own4"}),
    ("the store's stock split fitted with each Monday set against the week beginning", {"split": "regress", "pair": "beginning"}),
    ("the wash line and the repair bay held at the last count's level", {"other": "held"}),
    ("the cellar counts fitted with a line's level and its movement apart, on the count's week", {"fit": "apart"}),
    ("the store's stock split fitted on all three years' Mondays", {"split": "regress", "cover_weeks": 156}),
    ("the fitted slope beside half the plan's runs, on all three years' Mondays", {"split": "slope", "cover_weeks": 156}),
    ("the fitted slope beside half the plan's runs, on the last year's Mondays alone", {"split": "slope", "cover_weeks": 52}),
]


def family():
    """the golden, each convention changed alone, and every two of them together"""
    out = [("the golden's conventions", {})] + list(SINGLES)
    for i, (n1, o1) in enumerate(SINGLES):
        for n2, o2 in SINGLES[i + 1:]:
            if not set(o1) & set(o2):
                o = dict(o1)
                o.update(o2)
                out.append((n1 + "; " + n2, o))
    return out


FAMILY = family()
FORCING = [
    ("what a line holds per container sold, 20 per cent down", {"x_b": 0.8}),
    ("what a line holds per container sold, 20 per cent up", {"x_b": 1.2}),
    ("the store's cover, 20 per cent down", {"x_cov": 0.8}),
    ("the store's cover, 20 per cent up", {"x_cov": 1.2}),
    ("the loss per container delivered, 20 per cent down", {"x_lam": 0.8}),
    ("the loss per container delivered, 20 per cent up", {"x_lam": 1.2}),
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


def doy(d):
    return (d + dt.timedelta(days=3)).timetuple().tm_yday


def cover_of(x, p):
    return "nothing" if x <= 0 else "hire" if x < MIN_RUN[p] else "buy"


# ------------------------------------------------------------------------------------------------- the files
def load(target):
    R = Rec()
    f = lambda k: os.path.join(target, FILES[k])
    codes = pd.read_csv(f("codes"), dtype=str)
    to_pool = {}
    for _, r in codes.iterrows():
        for k in ("container", "docket_code", "register_code"):
            to_pool[r[k]] = r["container"]
    prod = pd.read_csv(f("products"), dtype=str, keep_default_na=False)
    sku_pool = {r["sku"]: to_pool[r["container"]] for _, r in prod.iterrows()}
    acc = pd.read_csv(f("accounts"), dtype=str, keep_default_na=False)
    cur = {r["former_account_no"]: r["account_no"] for _, r in acc.iterrows() if r["former_account_no"]}
    R.n_accounts, R.renumbered = len(acc), len(cur)
    # the dockets: a visit re-sent by a handheld counted once, the container read from the product where it is blank
    dk = pd.read_csv(f("dockets"), dtype={"sku": str, "container": str, "account_no": str}, keep_default_na=False)
    R.docket_rows = len(dk)
    dk = dk.drop_duplicates(["docket_no", "line_no"])
    R.resent_rows = R.docket_rows - len(dk)
    de = dk
    R.del_rows, R.blank_codes = len(de), int((de["container"] == "").sum())
    R.dockets = int(dk["docket_no"].nunique())
    date = pd.to_datetime(de["delivery_date"])
    R.D0 = monday(date.min().date())
    week = ((date - pd.Timestamp(R.D0)).dt.days // 7).to_numpy()
    pool = de["sku"].map(sku_pool).to_numpy()
    acct = de["account_no"].map(lambda x: cur.get(x, x)).to_numpy()
    qty = de["qty"].to_numpy(dtype=float)
    R.WH = int(week.max()) + 1
    WH = R.WH
    R.flow = {p: np.bincount(week[pool == p], weights=qty[pool == p], minlength=WH) for p in POOLS}
    key = np.where(pool == TAGGED, acct + "|GUEST-20L", acct + "|" + de["sku"].to_numpy())
    g = pd.DataFrame({"pool": pool, "key": key, "qty": qty, "yr": np.where(week >= WH - 52, qty, 0.0)})
    tot = g.groupby(["pool", "key"], sort=True)[["qty", "yr"]].sum()
    R.line = {p: tot.loc[p] for p in POOLS}
    lw = pd.DataFrame({"pool": pool, "key": key, "week": week, "qty": qty}).groupby(["pool", "key", "week"], sort=True)["qty"].sum()
    R.line_week = {p: lw.loc[p] for p in POOLS}
    R.week_dates = [R.D0 + dt.timedelta(days=7 * i) for i in range(WH + 60)]
    # the route plan: deliveries a week by account
    ws = load_workbook(f("routes"), read_only=True)["Routes"]
    per = {}
    for r in list(ws.iter_rows(values_only=True))[1:]:
        per[r[4]] = int(r[6])
    R.interval = {a: (0.5 if n == 2 else 1.0) for a, n in per.items()}
    for p in POOLS:
        R.line[p] = R.line[p].assign(iv=[R.interval[k.split("|")[0]] for k in R.line[p].index])
    # the weather station: the week's mean daily maximum temperature and its normal
    wx = pd.read_csv(f("weather"), dtype=str, keep_default_na=False)
    R.temp = {dt.date.fromisoformat(r["week_beginning"]): float(r["mean_daily_max_c"]) for _, r in wx.iterrows() if r["mean_daily_max_c"]}
    R.normal = {dt.date.fromisoformat(r["week_beginning"]): float(r["normal_1991_2020_c"]) for _, r in wx.iterrows()}
    # the annual counts
    wb = load_workbook(f("stocktake"), read_only=True)
    R.takes = {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        d = dt.datetime.strptime(" ".join(str(rows[1][1]).split()[1:]), "%d %b %Y").date()
        b = (d - R.D0).days // 7
        T = {p: dict(onsite=0.0, store=0.0, other=0.0, idle=0.0, depots=0.0, awaiting=0.0, inwash=0.0, repair=0.0)
             for p in POOLS}
        for row in rows[4:]:
            site, area, cont, state, n = row[:5]
            if cont is None:
                continue
            p = to_pool[cont]
            T[p]["onsite"] += n
            T[p]["store" if area == "Cold store" else "idle" if state == "clean empty" else "other"] += n
            if site != "Brighouse":
                T[p]["depots"] += n
            if state in ("awaiting wash", "in wash", "in repair"):
                T[p][{"awaiting wash": "awaiting", "in wash": "inwash", "in repair": "repair"}[state]] += n
        R.takes[b] = T
    R.counts = sorted(R.takes)
    R.asof = R.D0 + dt.timedelta(days=7 * R.counts[-1])
    # the register: bought before the count and not condemned before it
    reg = pd.read_csv(f("register"), dtype=str, keep_default_na=False)
    rp = reg["container"].map(to_pool)
    R.register_rows = len(reg)
    R.register, R.condemned_year, R.condemned_all = {}, {}, {}
    for p in POOLS:
        x = reg[rp == p]
        R.register[p] = {b: int(((x["purchased"] < (R.D0 + dt.timedelta(days=7 * b)).isoformat()) &
                                 ((x["condemned_on"] == "") | (x["condemned_on"] >= (R.D0 + dt.timedelta(days=7 * b)).isoformat()))).sum())
                         for b in R.counts}
        lo, hi = (R.D0 + dt.timedelta(days=7 * (WH - 52))).isoformat(), R.asof.isoformat()
        R.condemned_year[p] = int(((x["condemned_on"] >= lo) & (x["condemned_on"] < hi)).sum())
        R.condemned_all[p] = int(((x["condemned_on"] >= R.D0.isoformat()) & (x["condemned_on"] < hi)).sum())
    # the cold store's Monday position and the racking log
    st = pd.read_csv(f("store"), dtype={"container": str})
    R.store = {}
    for p in POOLS:
        x = st[st["container"].map(to_pool) == p]
        i = ((pd.to_datetime(x["position_date"]) - pd.Timestamp(R.D0)).dt.days // 7).to_numpy()
        v = np.zeros(WH + 1)
        v[i] = x["full_containers"].to_numpy(dtype=float)
        R.store[p] = v
    dp = pd.read_csv(f("depots"), dtype={"container": str})
    dp["pool"] = dp["container"].map(to_pool)
    dp["week"] = (pd.to_datetime(dp["week_beginning"]) - pd.Timestamp(R.D0)).dt.days // 7
    dp["n"] = dp["full"] + dp["empty"]
    R.depot = {p: dp[dp["pool"] == p].groupby("week")["n"].sum().reindex(range(WH + 1)).to_numpy(dtype=float) for p in POOLS}
    wl = pd.read_csv(f("wash"), dtype={"container": str})
    wl["pool"] = wl["container"].map(to_pool)
    wl["week"] = (pd.to_datetime(wl["date"]) - pd.Timestamp(R.D0)).dt.days // 7
    R.awaiting, R.repair = {}, {}
    for p in POOLS:
        x = wl[wl["pool"] == p].sort_values("date", kind="stable")
        R.awaiting[p] = x.groupby("week")["awaiting_wash"].last().reindex(range(WH)).ffill().to_numpy(dtype=float)
        net = (x["to_repair"] - x["back_from_repair"]).groupby(x["week"]).sum().reindex(range(WH)).fillna(0).to_numpy(dtype=float)
        R.repair[p] = R.takes[R.counts[0]][p]["repair"] + np.cumsum(net)      # at the close of each week
    rk = pd.read_csv(f("racking"), dtype={"container": str})
    rk["pool"] = rk["container"].map(to_pool)
    rk["week"] = (pd.to_datetime(rk["racked_on"]) - pd.Timestamp(R.D0)).dt.days // 7
    R.rackings = len(rk)
    R.rk = rk
    R.runs = {p: runs_of(R, p, "median", 52) for p in POOLS}
    # the reps' cellar audits
    au = pd.read_csv(f("audits"), dtype={"account_no": str, "container": str, "product": str}, keep_default_na=False)
    au["pool"] = au["container"].map(to_pool)
    au["acct"] = au["account_no"].map(lambda x: cur.get(x, x))
    au["held"] = au["full"] + au["on_dispense"] + au["empty"]
    ad = pd.to_datetime(au["audit_date"])
    au["week"] = (ad - pd.Timestamp(R.D0)).dt.days // 7
    au["month"] = ad.dt.month
    au["key"] = au["acct"] + "|" + au["product"]
    R.audit_rows, R.audit_visits = len(au), int(au["audit_ref"].nunique())
    R.audits = {p: au[au["pool"] == p] for p in POOLS}
    # the 2027 brew plan and the supply agreement's schedules
    ws = load_workbook(f("plan"), read_only=True).worksheets[0]
    R.plan = {p: [] for p in POOLS}
    for r in list(ws.iter_rows(values_only=True))[4:]:
        if r[0]:
            R.plan[to_pool[r[2]]].append((r[0], r[4].date() if hasattr(r[4], "date") else r[4],
                                          r[5].date() if hasattr(r[5], "date") else r[5], float(r[6])))
    wb = load_workbook(f("schedule"), read_only=True)
    cols = {"K50": 5, "K30": 6, "K20": 7, "FIR": 8}
    R.estate = {p: [] for p in POOLS}
    for r in list(wb.worksheets[0].iter_rows(values_only=True))[4:]:
        if r[0]:
            d = r[3].date() if hasattr(r[3], "date") else r[3]
            for p, c in cols.items():
                if r[c]:
                    R.estate[p].append((d, int(r[c])))
    R.estate_volume = {p: 0.0 for p in POOLS}
    named = {NAMES[p]: p for p in POOLS}
    for r in list(wb.worksheets[1].iter_rows(values_only=True))[3:]:
        if r[0] in named:
            R.estate_volume[named[r[0]]] = float(r[2])
    R.estate_pubs = len(list(wb.worksheets[0].iter_rows(values_only=True))) - 4
    tags(R, f("tags"), f("cases"), cur)
    return R


def tags(R, db, cases, cur):
    """the tracked pool from its tags: its kegs in the trade at each Monday and the kegs not traced"""
    con = sqlite3.connect(db)
    rd = pd.read_sql_query("SELECT tag_id, read_at, read_point FROM tag_reads", con)
    ft = pd.read_sql_query("SELECT serial, tag_id FROM tag_fittings", con)
    con.close()
    R.tag_reads = len(rd)
    rd["serial"] = rd["tag_id"].map(dict(zip(ft["tag_id"], ft["serial"])))
    rd["t"] = pd.to_datetime(rd["read_at"])
    rd = rd.sort_values(["serial", "t"], kind="stable")
    same = (rd["serial"] == rd["serial"].shift()) & (rd["read_point"] == rd["read_point"].shift()) & \
        ((rd["t"] - rd["t"].shift()).dt.total_seconds() < 120)
    rd = rd[~same]
    R.double_reads = int(same.sum())
    nxt = rd["t"].shift(-1).where(rd["serial"].shift(-1) == rd["serial"])
    out = rd[rd["read_point"] == "DELIVER"].assign(until=nxt[rd["read_point"] == "DELIVER"])
    cs = pd.read_csv(cases, dtype=str, keep_default_na=False)
    R.cases = len(cs)
    gone = cs[cs["outcome"] == "NOT TRACED"]
    R.not_traced = len(gone)
    lost = set(zip(gone["keg_serial"], gone["last_delivered_on"]))
    is_lost = np.array([(s, t.date().isoformat()) in lost for s, t in zip(out["serial"], out["t"])])
    kept = out[~(is_lost & out["until"].isna().to_numpy())]
    start = ((kept["t"] - pd.Timestamp(R.D0)).dt.total_seconds() / 86400.0).to_numpy()
    end = ((kept["until"] - pd.Timestamp(R.D0)).dt.total_seconds() / 86400.0).fillna(1e9).to_numpy()
    WH = R.WH
    R.census_raw = np.array([float(((start < 7 * (i + 1)) & (end >= 7 * (i + 1))).sum()) for i in range(WH)])
    start_a = ((out["t"] - pd.Timestamp(R.D0)).dt.total_seconds() / 86400.0).to_numpy()
    end_a = ((out["until"] - pd.Timestamp(R.D0)).dt.total_seconds() / 86400.0).fillna(1e9).to_numpy()
    R.census_all = np.array([float(((start_a < 7 * (i + 1)) & (end_a >= 7 * (i + 1))).sum()) for i in range(WH)])
    week = (start // 7).astype(int)
    seen = np.bincount(((out["t"] - pd.Timestamp(R.D0)).dt.days // 7).to_numpy(), minlength=WH)[:WH]
    R.deliver_reads = int(len(out))
    R.read_share = float(len(out) / R.flow[TAGGED].sum())            # delivery reads over the dockets' deliveries
    cd = pd.to_datetime(cs["last_delivered_on"])
    cw = ((cd - pd.Timestamp(R.D0)).dt.days // 7).to_numpy()
    R.case_week, R.case_outcome = cw, cs["outcome"].to_numpy()


# ------------------------------------------------------------------------------------------------- the estimators
def temps_of(R):
    """temperature by week index: recorded where there is a record, the normal after it"""
    out = []
    for i in range(R.WH + 60):
        d = R.week_dates[i]
        out.append(R.temp.get(d, R.normal.get(d)))
    return out


F_CRIT = 3.06                         # the 5 per cent point of F on 2 and 147 degrees of freedom
T_CRIT = 1.98                         # the two-sided 5 per cent point of t on 147 degrees of freedom


def fit_sales(R, p, harmonics, hinge=0.0, bend=True, trend=True, period="year", cache={}):
    """weekly deliveries on the season, the trend and the week's temperature, with a bend at the temperature the
    record itself fits best"""
    if bend == "test":
        bend = fit_tests(R, p)["bend_F"] > F_CRIT
    if trend == "test":
        trend = abs(fit_tests(R, p)["trend_t"]) > T_CRIT
    k = (id(R), p, harmonics, hinge, bend, trend, period)
    if k in cache:
        return cache[k]
    WH = R.WH
    y = np.log(R.flow[p])
    T = temps_of(R)

    def row(i, temp, h0, level=1.0, it=None):
        x = [level] + ([level * (i if it is None else it) / 52.0] if trend else [])
        ang = 2 * math.pi * (doy(R.D0 + dt.timedelta(days=7 * i)) / 365.0 if period == "year" else i / 52.0)
        for h in range(1, harmonics + 1):
            x += [math.cos(h * ang), math.sin(h * ang)]
        if bend == "quad":
            return x + [temp - 15.0, (temp - 15.0) ** 2]
        return x + ([max(temp - h0, 0.0), min(temp - h0, 0.0)] if bend else [temp])

    def fit(h0):
        X = np.array([row(i, T[i], h0) for i in range(WH)])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        return float(((X @ beta - y) ** 2).sum()), beta
    best = min((fit(h0)[0], h0) for h0 in np.arange(12.0, 22.01, 0.5))[1]
    h0 = best + hinge
    sse, beta = fit(h0)
    Xh = np.array([row(i, T[i], h0) for i in range(WH)])
    cov_b = np.linalg.inv(Xh.T @ Xh) * sse / (WH - Xh.shape[1] - (1 if bend is True else 0))
    predict = lambda i, temp, it=None: float(math.exp(np.dot(beta, row(i, temp, h0, 1.0, it))))
    shape = lambda i, temp: float(math.exp(np.dot(beta, row(i, temp, h0, 0.0))))
    year = float(np.mean([shape(i, R.normal[R.week_dates[i]]) for i in range(WH - 52, WH)]))
    fitted = np.array([predict(i, T[i]) for i in range(WH)])
    t_trend = float(beta[1] / math.sqrt(cov_b[1, 1])) if trend else 0.0
    d_back = R.D0 - dt.timedelta(days=7)                  # the week that ends at the first count, before the record
    back = predict(-1, R.temp.get(d_back, R.normal.get(d_back)))
    cache[k] = (predict, shape, year, fitted, h0, sse, t_trend, float(beta[1]) if trend else 0.0, back)
    return cache[k]


def fit_tests(R, p):
    """two F tests on the deliveries fit: the bend in the weather response against a single slope, and the second
    seasonal harmonic against one"""
    n = R.WH
    full = fit_sales(R, p, 2)[5]
    flat = fit_sales(R, p, 2, bend=False)[5]
    one = fit_sales(R, p, 1)[5]
    df = n - 9                                            # level, trend, four harmonic terms, two slopes and the bend
    g = fit_sales(R, p, 2)
    quad = fit_sales(R, p, 2, bend="quad")[5]
    return dict(quad_sse_pct=100.0 * (quad / full - 1.0), flat_sse_pct=100.0 * (flat / full - 1.0), bend_F=float((flat - full) / 2.0 / (full / df)), harmonic_F=float((one - full) / 2.0 / (full / df)), df=df,
                trend_t=g[6], trend_pct=100.0 * (math.exp(g[7]) - 1.0))


def fit_cellar(R, p, o, sample=None):
    """containers a line holds: a number whatever it sells, a number per container it sells a week and a number per
    container it sells a week and week between deliveries; or one line per delivery interval"""
    au = R.audits[p]
    ln = R.line[p]
    WH = R.WH
    col = "qty" if o["share"] == "record" else "yr"
    weeks = float(WH if o["share"] == "record" else 52)
    base = float(R.flow[p].sum() if o["share"] == "record" else R.flow[p][WH - 52:].sum()) / weeks
    line_rate = ln[col].reindex(au["key"]).fillna(0.0).to_numpy() / weeks
    iv = np.array([R.interval[a] for a in au["acct"]])
    wk = au["week"].to_numpy()
    if o["rate"] == "week":
        flow = R.flow[p][wk]
    elif o["rate"] == "fit":
        flow = fit_sales(R, p, o["harmonics"], o["hinge"], o["bend"], o["trend"], o["period"])[3][wk]
    else:
        flow = np.array([R.flow[p][max(i - 2, 0):i + 2].mean() for i in wk])
    rate = line_rate * flow / base
    if o["rate"].startswith("own"):                                # the line's own dockets over the weeks to the count
        n_w, keys = int(o["rate"][3:]), au["key"].to_numpy()
        rate = sum(R.line_week[p].reindex(pd.MultiIndex.from_arrays([keys, wk - lag])).fillna(0.0).to_numpy()
                   for lag in range(n_w)) / float(n_w)
    mean_rate = line_rate
    held = au["held"].to_numpy(dtype=float)
    keep = np.ones(len(held), dtype=bool)
    if o["count_months"] == "summer":
        keep = au["month"].between(4, 9).to_numpy()
    if sample is not None:
        rate, iv, held, keep, mean_rate = rate[sample], iv[sample], held[sample], keep[sample], mean_rate[sample]
    rate, iv, held, mean_rate = rate[keep], iv[keep], held[keep], mean_rate[keep]
    if o["fit"] == "ols":
        a, b1, b2 = np.linalg.lstsq(np.column_stack([np.ones(len(rate)), rate, rate * iv]), held, rcond=None)[0]
        slope = lambda x: float(b1 + b2 * x)
        return float(a), slope, len(held), slope
    if o["fit"] == "apart":                                        # a line's level and its movement about it, apart
        dev = rate - mean_rate
        a, l1, l2, m1, m2 = np.linalg.lstsq(np.column_stack([np.ones(len(rate)), mean_rate, mean_rate * iv, dev, dev * iv]),
                                            held, rcond=None)[0]
        return float(a), (lambda x: float(m1 + m2 * x)), len(held), (lambda x: float(l1 + l2 * x))
    slope, icpt = {}, {}
    for x in (0.5, 1.0):
        k = iv == x
        slope[x], icpt[x] = np.polyfit(rate[k], held[k], 1)
    by = lambda x: float(slope[x])
    return float(icpt[1.0]), by, len(held), by


def apart_slopes(R, p):
    """the two-slope cellar fit read three ways: a line's level slope and its movement slope on a weekly call, with a
    line's sales at the count from the count's week, from the fitted week and from four weeks of deliveries; and the
    one-slope fit's slope beside them"""
    out = {}
    for name, rate in (("week", "week"), ("fit", "fit"), ("four", "four")):
        o = dict(GOLDEN)
        o.update({"fit": "apart", "rate": rate})
        _a, move, _n, level = fit_cellar(R, p, o)
        o["fit"] = "ols"
        out[name] = dict(level=level(1.0), move=move(1.0), one=fit_cellar(R, p, o)[1](1.0))
    return out


def per_sale(R, p, slope):
    """the trade's containers per container delivered a week: the lines' slopes weighted by their deliveries"""
    ln = R.line[p]
    return float(sum(slope(x) * ln["qty"][ln["iv"] == x].sum() for x in (0.5, 1.0)) / ln["qty"].sum())


def census_of(R, o):
    return (R.census_all if o["census_lost"] else R.census_raw) / (R.read_share if o["census_scale"] else 1.0)


def busiest(R, year=-2):
    """the middle of the three weeks with the most 20 litre kegs delivered, between the count and the next"""
    b, fl = R.counts[year], R.flow[TAGGED]
    return max(range(b + 8, min(b + 52, R.WH) - 8), key=lambda i: fl[i - 1:i + 2].mean())


def tracked_response(R, o):
    """the tracked pool's own response: the share by which its kegs in the trade move when its deliveries move by
    one per cent, from its weekly tag count"""
    c, fl = census_of(R, o)[52:], R.flow[TAGGED][52:]
    slope, icpt = np.polyfit(fl, c, 1)
    return float(slope * fl.mean() / c.mean())


def tag_loss(R, o):
    """the tracked pool's kegs not traced per keg delivered"""
    WH = R.WH
    if o["tag_window"] == "closed":                      # the latest 52 weeks of deliveries whose cases have closed
        late = int(R.case_week[R.case_outcome == "OPEN"].min()) if (R.case_outcome == "OPEN").any() else WH - 26
        lo, hi = late - 52, late
        n = int(((R.case_week >= lo) & (R.case_week < hi) & (R.case_outcome == "NOT TRACED")).sum())
    else:                                                # the year to 26 weeks before the count, open cases counted
        lo, hi = WH - 78, WH - 26
        n = int(((R.case_week >= lo) & (R.case_week < hi) & (R.case_outcome != "AT ACCOUNT")).sum())
    return n / float(R.flow[TAGGED][lo:hi].sum()), n, (lo, hi)


def runs_of(R, p, stat="median", start=52, cache={}):
    """each beer's racking run for one container type: its median (or mean) containers filled since a week"""
    k = (id(R), p, stat, start)
    if k not in cache:
        g = R.rk[(R.rk["pool"] == p) & (R.rk["week"] >= start)].groupby("sku")["containers_filled"]
        cache[k] = (g.median() if stat == "median" else g.mean()).to_dict()
    return cache[k]


def store_pair(R, p, cw, pair="ended"):
    """the last cw Monday positions, each with the deliveries of the week that ended the day before (or, for the
    reading the files refuse, of the week beginning that Monday)"""
    WH = R.WH
    if pair == "ended":
        return R.store[p][WH - cw + 1:WH + 1], R.flow[p][WH - cw:]
    return R.store[p][WH - cw:WH], R.flow[p][WH - cw:]


def split_fit(R, p, cw, pair="ended", full=False):
    """the Monday stock fitted on the week's deliveries over the last cw Mondays: the fixed part and its standard error"""
    st, fl = store_pair(R, p, cw, pair)
    Xm = np.column_stack([np.ones(len(fl)), fl])
    b = np.linalg.lstsq(Xm, st, rcond=None)[0]
    res = st - Xm @ b
    cov = np.linalg.inv(Xm.T @ Xm) * float(res @ res) / (len(fl) - 2)
    if full:
        return float(b[0]), float(math.sqrt(cov[0, 0])), 1.0 - float(res @ res) / float(((st - st.mean()) ** 2).sum())
    return float(b[0]), float(math.sqrt(cov[0, 0]))


def season_of(R):
    """the 2027 season's week indices (FS-04 3.1)"""
    year = R.asof.year + 1
    i0 = (first_monday_of_may(year) - R.D0).days // 7
    return list(range(i0, i0 + SEASON_WEEKS))


def summer_temps(R, year):
    """the 2027 season on the recorded weather of one summer, its 21 weeks taken in order (FS-04 3.3)"""
    d0 = first_monday_of_may(year)
    return {i: R.temp[d0 + dt.timedelta(days=7 * k)] for k, i in enumerate(season_of(R))}


def beers_on_sale(R, p, d):
    return [(s, run) for s, a, b, run in R.plan[p] if a <= d <= b]


def chain(R, p, opt=None, temps=None):
    """one pool's 2027 weeks from the records, with every step's option: the requirement by part, the fleet and
    the shortfall, and the season's largest"""
    o = dict(GOLDEN)
    o.update(opt or {})
    WH = R.WH
    T, flow = R.takes, R.flow[p]
    cnt = R.counts
    tagged = p == TAGGED
    X = {b: R.register[p][b] - T[b][p]["onsite"] for b in cnt}    # off site by the register, lost included
    a, slope, n_counts, slope_level = fit_cellar(R, p, o)
    bm = per_sale(R, p, slope) * o["x_b"]
    cen = census_of(R, o)
    fs = fit_sales(R, p, o["harmonics"], o["hinge"], o["bend"], o["trend"], o["period"])
    predict, shape, year_shape, fitted, h0, _sse = fs[:6]
    if o["level"] == "fit":                                        # the first count has no week of dockets behind it
        lev = {b: float(fitted[b - 1]) if b else float(fs[8] if o["first"] == "back" else fitted[0]) for b in cnt}
    else:
        lev = {b: float(flow[max(b - o["level"], 0):b].mean()) if b else float(flow[:o["level"]].mean()) for b in cnt}
    last = cnt[-1]
    if tagged and o["census"] == "response":                       # the tagged kegs' response as their tags measured it
        mid = busiest(R)
        bm = float(cen[mid - 1:mid + 2].mean() - cen[cnt[-2] - 1]) / float(flow[mid - 1:mid + 2].mean() - lev[cnt[-2]]) * o["x_b"]
    lo = last - 52 * o["loss_years"]
    gone = X[last] - X[lo] - (bm * (lev[last] - lev[lo]) if o["trade_change"] else 0.0)
    lam_acc = gone / float(flow[lo:last].sum())
    lam_tag, n_tag, tag_win = tag_loss(R, o)
    if o["loss"] == "tag" or (tagged and not o["account_tagged"]):
        lam = lam_tag
    else:
        lam = lam_acc
    lam *= o["x_lam"]
    year_loss = lam * float(flow[last - 52:last].sum())
    if not o["condemned"]:
        scr = 0.0
    elif o["scrap_years"] == 1:
        scr = R.condemned_year[p] / float(flow[last - 52:last].sum())
    else:
        scr = R.condemned_all[p] / float(flow[:last].sum())
    alive_out = X[last] - lam * float(flow[:last].sum())           # the trade's containers at the count, alive
    resp = tracked_response(R, o) if o["swing"] == "tracked" else 1.0
    half26 = sum(runs_of(R, p, o["run_stat"], o["run_from"]).values()) / 2.0
    st = R.store[p][53:WH + 1]                                     # the Monday after each week
    reg = np.polyfit(flow[52:], st, 1)
    cw = o["cover_weeks"]
    st_c, fl_c = store_pair(R, p, cw, o["pair"])
    cyc = 1.0
    if o["split"] in ("regress", "slope"):                         # the split fitted: the stock on the deliveries
        cov, icpt = np.polyfit(fl_c, st_c, 1)
        cov, cyc = float(cov), (float(icpt) / half26 if o["split"] == "regress" else 1.0)
    elif o["cover"] == "mean":
        cov = (float(st_c.mean()) - half26) / float(fl_c.mean())
    else:
        cov = float(np.median((st_c - half26) / fl_c))
    cov *= o["x_cov"]
    c2k = 0.0
    if o["other"] == "mean":
        c2 = float(np.mean([T[b][p]["other"] / lev[b] for b in cnt]))
    elif o["other"] == "last":
        c2 = T[last][p]["other"] / lev[last]
    elif o["other"] == "held":                                     # the depots at their weeks, the rest at its level
        c2 = float(np.mean([T[b][p]["depots"] / lev[b] for b in cnt]))
        c2k = float(T[last][p]["other"] - T[last][p]["depots"])
    elif o["other"] == "log":                                      # the depots, the backlog and the bay week by week
        c2 = float((R.depot[p][53:WH + 1].mean() + R.awaiting[p][52:].mean() + R.repair[p][52:].mean()) / flow[52:].mean()) + \
            float(np.mean([T[b][p]["inwash"] / lev[b] for b in cnt]))
    else:                                                          # the depots week by week, the rest at the counts
        c2 = float(R.depot[p][53:WH + 1].mean() / flow[52:].mean()) + \
            float(np.mean([(T[b][p]["other"] - T[b][p]["depots"]) / lev[b] for b in cnt]))
    vol = R.estate_volume[p]
    season = season_of(R)
    path, cum = [], 0.0
    for i in range(WH, season[-1] + 1):
        d = R.week_dates[i]
        j = i - 52
        temp = R.normal[d] if temps is None or i not in temps else temps[i]
        F = predict(i, temp, WH - 1 if o["ahead"] == "hold" else None) * o["x_del"]
        n_live = sum(n for day, n in R.estate[p] if day <= d)
        es = n_live * vol * (shape(i, R.normal[d] if o["estate_temp"] == "normal" else temp) / year_shape
                             if o["estate"] == "shaped" else 1.0)
        est = a * n_live + slope_level(1.0) * o["x_b"] * es
        D = F + es
        if o["swing"] == "lines" or (tagged and o["swing"] == "tracked"):
            if tagged and o["census"] is True:
                swing = cen[j] - cen[WH - 1] + bm * (F - flow[j]) + est
            else:
                swing = bm * (F - lev[last]) + est
        elif tagged:                                               # last season's tag count, moved with deliveries
            swing = cen[j] * D / flow[j] - cen[WH - 1]
        else:                                                      # the trade's stock moved with deliveries
            swing = alive_out * resp * (D / lev[last] - 1.0)
        beers = beers_on_sale(R, p, d)
        if o["store"] == "runs":
            store = cov * D + cyc * sum(run for s, run in beers) / 2.0
        elif o["store"] == "cover":
            store = float(R.store[p][j - 1:j + 4].mean() / flow[j - 2:j + 3].mean()) * D
        else:
            store = float(reg[1] + reg[0] * D)
        before = cum
        cum += (lam + scr) * D
        other, fl = c2 * D + c2k, FLOAT * D
        need = swing + store + other + fl                          # beside the trade's containers at the count
        gone_by = before if o["accrue"] == "before" else cum       # the week's own loss counts in its shortfall
        path.append(dict(i=i, date=d, D=D, F=F, es=es, swing=swing, est=est, store=store, other=other, float=fl,
                         drain=gone_by, short=need - T[last][p]["onsite"] + gone_by, beers=len(beers), temp=temp))
    pick = max((x for x in path if x["i"] in season), key=lambda x: x["short"])
    return dict(short=pick["short"], week=pick["i"], date=pick["date"], swing=pick["swing"], store=pick["store"],
                year_loss=year_loss, lam=lam, lam_acc=lam_acc, lam_tag=lam_tag, n_tag=n_tag, tag_window=tag_win, a=a,
                slope1=slope(1.0), slope_half=slope(0.5), bm=bm, cov=cov, c2=c2, half26=half26, scr=scr, hinge=h0,
                n_counts=n_counts, X=X, lev=lev, gone=gone, alive_out=alive_out, path=path, pick=pick,
                onsite=T[last][p]["onsite"], resp=resp)


def direct(R, p, temps=None):
    """the register as the fleet and its turns: the fleet moved with the busiest week's deliveries over the year's"""
    predict, shape, year_shape, fitted, h0, _sse = fit_sales(R, p, 2)[:6]
    best = 0.0
    for i in season_of(R):
        d = R.week_dates[i]
        temp = R.normal[d] if temps is None or i not in temps else temps[i]
        n_live = sum(n for day, n in R.estate[p] if day <= d)
        best = max(best, predict(i, temp) + n_live * R.estate_volume[p] * shape(i, temp) / year_shape)
    last = R.counts[-1]
    return R.register[p][last] * (best / float(R.flow[p][last - 52:last].mean()) - 1.0)


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


def spreads(R, p, reps=120, seed=11):
    """each fitted input's own measured spread for one pool, as a share of its value"""
    rng = np.random.default_rng(seed)
    n = len(R.audits[p])
    bm = []
    for _ in range(reps):
        bm.append(per_sale(R, p, fit_cellar(R, p, GOLDEN, sample=rng.integers(0, n, n))[1]))
    g = chain(R, p)
    WH = R.WH
    st, fl = R.store[p][53:WH + 1], R.flow[p][52:]
    cv = []
    for _ in range(reps):
        idx = np.concatenate([np.arange(k * 4, k * 4 + 4) for k in rng.integers(0, len(st) // 4, len(st) // 4)])
        cv.append((st[idx].mean() - g["half26"]) / fl[idx].mean())
    lams = [chain(R, p, {"loss_years": y, "account_tagged": True})["lam_acc"] for y in (1, 2, 3)]
    fitted = fit_sales(R, p, 2)[3]
    res = np.log(R.flow[p]) - np.log(fitted)
    return dict(x_b=float(np.std(bm) / np.mean(bm)), x_cov=float(np.std(cv) / abs(np.mean(cv))),
                x_lam=float((max(lams) - min(lams)) / abs(lams[0])) / 2.0,
                x_del=float(np.std(res) / math.sqrt(WH / 8.0)))


def referee(R):
    """the tracked pool's kegs in the trade, from the December 2025 count to the busiest three weeks of summer 2026:
    what its tags count against what each way of sizing the trade's stock says"""
    o = dict(GOLDEN)
    cen, fl = census_of(R, o), R.flow[TAGGED]
    b = R.counts[-2]
    mid = busiest(R)
    g = chain(R, TAGGED)
    lev = g["lev"][b]
    at = float(fl[mid - 1:mid + 2].mean())
    top = float(cen[mid - 1:mid + 2].mean())
    return dict(week=mid, date=R.week_dates[mid], seen=top - float(cen[b - 1]), golden=g["bm"] * (at - lev),
                proportional=float(cen[b - 1] * (at / lev - 1.0)), level=lev, at=at, start=float(cen[b - 1]), top=top)


def level_readings(R):
    """deliveries at the last count read five ways, per pool: the fitted season's value for the count's week, and
    the mean of the one, two, four and eight weeks before it; with the weekly scatter about the fit"""
    out = {}
    for p in POOLS:
        fitted = fit_sales(R, p, 2)[3]
        fl = R.flow[p]
        b = R.counts[-1]
        res = np.log(fl) - np.log(fitted)
        out[p] = dict(fit=float(fitted[b - 1]), w1=float(fl[b - 1]), w2=float(fl[b - 2:b].mean()), w4=float(fl[b - 4:b].mean()),
                      w8=float(fl[b - 8:b].mean()), w13=float(fl[b - 13:b].mean()), scatter=float(np.std(res)),
                      short8=chain(R, p, {"level": 8})["short"], short13=chain(R, p, {"level": 13})["short"],
                      short1=chain(R, p, {"level": 1})["short"], short2=chain(R, p, {"level": 2})["short"])
    return out


def run(target):
    R = load(target)
    lat_o = lattice_opts()
    X = dict(R=R, gold={p: chain(R, p) for p in POOLS}, fam={}, lat={}, hot={}, hot_fam={}, hot_lat={})
    for p in POOLS:
        X["fam"][p] = [chain(R, p, o) for _, o in FAMILY]
        X["lat"][p] = {k: chain(R, p, o) for k, o in lat_o.items()}
        X["hot"][p] = hot(R, lambda t: chain(R, p, None, t)["short"])
        X["hot_fam"][p] = [hot(R, lambda t: chain(R, p, o, t)["short"])[0] for _, o in FAMILY]
        X["hot_lat"][p] = {k: hot(R, lambda t: chain(R, p, o, t)["short"])[0] for k, o in lat_o.items()}
    X["direct"] = {p: direct(R, p) for p in POOLS}
    X["rigorous"] = {p: chain(R, p, RIGOROUS) for p in POOLS}
    X["hot_direct"] = {p: hot(R, lambda t: direct(R, p, t))[0] for p in POOLS}
    X["hot_rigorous"] = {p: hot(R, lambda t: chain(R, p, RIGOROUS, t)["short"])[0] for p in POOLS}
    X["forcing"] = {name: {p: chain(R, p, o)["short"] for p in POOLS} for name, o in FORCING}
    X["spreads"] = {p: spreads(R, p) for p in POOLS}
    X["corners"] = {side: {p: chain(R, p, {k: 1.0 + sign * 2.0 * X["spreads"][p][k] for k in X["spreads"][p]})["short"]
                           for p in POOLS} for side, sign in (("down", -1.0), ("up", 1.0))}
    X["referee"] = referee(R)
    X["levels"] = level_readings(R)
    X["refused"] = {name: {p: chain(R, p, o)["short"] for p in POOLS} for name, o in REFUSED}
    X["refused_hot"] = {name: {p: hot(R, lambda t: chain(R, p, o, t)["short"])[0] for p in POOLS} for name, o in REFUSED}
    X["tests"] = {p: fit_tests(R, p) for p in POOLS}
    X["season"] = season_of(R)
    # the figures that rule on the refused readings
    X["pairing"] = {p: dict(ended=split_fit(R, p, 104, "ended", True), beginning=split_fit(R, p, 104, "beginning", True))
                    for p in POOLS}
    X["apart"] = {p: apart_slopes(R, p) for p in POOLS}
    r, own = X["referee"], {}
    for w in (1, 4, 13):
        o = dict(GOLDEN)
        o["rate"] = "own%d" % w
        own[w] = {p: per_sale(R, p, fit_cellar(R, p, o)[1]) for p in POOLS}
    X["own"] = dict(per_sale=own, rise={w: own[w][TAGGED] * (r["at"] - r["level"]) for w in own})
    b, mid = R.counts[-2], r["week"]
    rise = lambda c: float(c[mid - 1:mid + 2].mean() - c[b - 1])
    X["tag_rules"] = dict(lost_in=rise(R.census_all / R.read_share), unscaled=rise(R.census_raw),
                          response=r["seen"] / (r["at"] - r["level"]), share=r["seen"] / r["proportional"],
                          line=tracked_response(R, GOLDEN))
    cen = census_of(R, GOLDEN)                                     # the tags' count while the tags were still being read in
    X["tag_fill"] = [(R.week_dates[i + 1], float(cen[i])) for i in (0, 12, 28)]
    # the store's fitted fixed part on each window, and the cover beside the log's half runs in each year taken singly
    X["split_windows"] = {p: {cw: split_fit(R, p, cw) for cw in (52, 104, 156)} for p in POOLS}
    X["cover_by_year"] = {p: [(float(R.store[p][R.WH - 52 * y - 51:R.WH - 52 * y + 1].mean()) - X["gold"][p]["half26"]) /
                              float(R.flow[p][R.WH - 52 * y - 52:R.WH - 52 * y].mean()) for y in range(3)] for p in POOLS}
    # off site at the first count beside the stock the cellar relation puts at customers that week
    first = R.counts[0]
    X["first_count"] = {p: dict(off_site=float(X["gold"][p]["X"][first]), lines=int(len(R.line[p])),
                                relation=float(X["gold"][p]["a"] * len(R.line[p]) + X["gold"][p]["bm"] * X["gold"][p]["lev"][first]))
                        for p in POOLS}
    last, pk = R.counts[-1], busiest(R, -2)
    X["washlog"] = {p: dict(awaiting_count=float(R.awaiting[p][last - 1]), awaiting_peak=float(R.awaiting[p][pk - 1:pk + 2].mean()),
                            repair_count=float(R.repair[p][last - 1]), repair_peak=float(R.repair[p][pk - 1:pk + 2].mean()),
                            deliveries_count=float(X["gold"][p]["lev"][last]), deliveries_peak=float(R.flow[p][pk - 1:pk + 2].mean()),
                            repair_at_counts=[float(R.repair[p][c - 1]) for c in R.counts[1:]],
                            repair_counted=[float(R.takes[c][p]["repair"]) for c in R.counts[1:]],
                            awaiting_counted=float(R.takes[last][p]["awaiting"])) for p in POOLS}
    return X


if __name__ == "__main__":
    import sys
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
        print("%-4s a %.2f slope1 %.3f half %.3f bm %.3f cov %.3f c2 %.3f lam %.4f acc %.4f tag %.4f scr %.5f swing %6.0f "
              "store %6.0f yearloss %5.0f hinge %.1f X %s lev %s onsite %.0f" % (
                  p, g["a"], g["slope1"], g["slope_half"], g["bm"], g["cov"], g["c2"], g["lam"], g["lam_acc"], g["lam_tag"],
                  g["scr"], g["swing"], g["store"], g["year_loss"], g["hinge"], {k: int(v) for k, v in g["X"].items()},
                  {k: int(v) for k, v in g["lev"].items()}, g["onsite"]))
    print("referee", {k: (round(v, 1) if isinstance(v, float) else v) for k, v in X["referee"].items()},
          "read share %.3f resp %.3f" % (R.read_share, tracked_response(R, GOLDEN)))
    for name, v in X["forcing"].items():
        print("%-56s %s" % (name, "  ".join("%7.0f" % v[p] for p in POOLS)))
    print("spreads", {p: {k: round(100 * v, 1) for k, v in X["spreads"][p].items()} for p in POOLS})
    print("corners", {s: {p: round(v) for p, v in X["corners"][s].items()} for s in X["corners"]})
    print("variant deviations")
    for k, (name, o) in enumerate(FAMILY[1:]):
        print("  %-66s %s" % (name[:66], " ".join("%6.0f" % (X["fam"][p][k + 1]["short"] - X["gold"][p]["short"]) for p in POOLS)))
