"""The golden analysis and the hurried passes, run on the shipped files only (target/), never on the world.

Every figure the answer blocks state comes from here, through figures.json; effort.json carries each pass's figure
at each result from the same functions run with the pass's own methods."""
import json
import os
import re

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
FORMATS = ["Super", "Kvarter", "To Go"]
LICENCE = {"Super": 27000.0, "Kvarter": 20000.0, "To Go": 9000.0}


# ------------------------------------------------------------------------------------------------------------ loading
def hours(s):
    """'HH:MM' or 'HH:MM:SS' as decimal hours; blank as NaN."""
    out = np.full(len(s), np.nan)
    v = s.fillna("").astype(str).values
    for k, t in enumerate(v):
        if t:
            p = t.split(":")
            out[k] = int(p[0]) + int(p[1]) / 60.0 + (int(p[2]) / 3600.0 if len(p) > 2 else 0.0)
    return out


def load(target=TARGET):
    T = {}
    items = pd.read_excel(os.path.join(target, "vareregister_frisk.xlsx"))
    items.columns = ["item", "name", "cat", "subcat", "life", "pack", "pack_togo", "p25", "c25", "p26", "c26",
                     "supplier", "old_no"]
    T["items"] = items
    old2new = {int(r.old_no): int(r.item) for r in items.itertuples() if r.old_no == r.old_no}
    stores = pd.read_excel(os.path.join(target, "butiksregister.xlsx"))
    stores.columns = ["store", "name", "format", "address", "postcode", "town", "hours", "area", "opened"]
    T["stores"] = stores
    d25 = pd.read_csv(os.path.join(target, "dagssalg_frisk_2025.csv"), sep=";", encoding="cp1252", decimal=",",
                      dtype={"Sidste salg": str})
    d25.columns = ["date", "store", "item", "sold", "sales", "last", "received", "waste", "close"]
    d25["date"] = pd.to_datetime(d25["date"], format="%d-%m-%Y")
    n_raw25 = len(d25)
    d25 = d25.drop_duplicates()
    d26 = pd.read_csv(os.path.join(target, "dagssalg_frisk_2026.csv"), dtype={"last_sale": str})
    d26.columns = ["date", "store", "item", "sold", "sales", "last", "received", "waste", "close"]
    d26["date"] = pd.to_datetime(d26["date"], format="%Y-%m-%d")
    d25["item"] = d25["item"].map(lambda x: old2new.get(int(x), int(x)))
    daily = pd.concat([d25, d26], ignore_index=True)
    daily["t"] = hours(daily["last"])
    iso = daily["date"].dt.isocalendar()
    daily["year"] = iso["year"].astype(int)
    daily["week"] = iso["week"].astype(int)
    daily["dow"] = daily["date"].dt.dayofweek
    daily = daily.merge(stores[["store", "format"]], on="store", how="left")
    daily = daily.merge(items[["item", "cat", "subcat", "c25", "c26"]], on="item", how="left")
    daily["cost"] = np.where(daily["year"] == 2026, daily["c26"], daily["c25"])
    daily["waste_val"] = daily["waste"] * daily["cost"]
    daily["unit_price"] = np.where(daily["sold"] > 0, daily["sales"] / daily["sold"].clip(lower=1), np.nan)
    T["daily"] = daily
    T["n_raw25"] = n_raw25
    T["n_dup25"] = n_raw25 - len(d25)
    prof = pd.read_csv(os.path.join(target, "timeprofil_salg_frisk.csv"), sep=";", decimal=",")
    prof.columns = ["format", "cat", "dow", "hour", "share"]
    days = ["mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"]
    prof["dow"] = prof["dow"].map(days.index)
    prof["h0"] = prof["hour"].str.slice(0, 2).astype(int)
    prof["cat"] = prof["cat"].replace({"Frugt og grønt": "Frugt & grønt"})
    T["profile"] = prof
    bi = pd.read_csv(os.path.join(target, "bi_uge_butik_kategori.csv"), sep=";", decimal=",")
    bi.columns = ["yw", "store", "cat", "sales", "waste_val", "units"]
    code = {"BAG": "Bageri", "FOG": "Frugt & grønt", "MEJ": "Mejeri", "KOD": "Kød", "FAE": "Færdigretter",
            "KOL": "Kolonial"}
    bi["cat"] = bi["cat"].map(lambda c: code.get(c, c))
    bi["year"] = bi["yw"].str.slice(0, 4).astype(int)
    bi["week"] = bi["yw"].str.slice(6, 8).astype(int)
    T["bi"] = bi
    comp = pd.read_csv(os.path.join(target, "konkurrentaabninger.csv"), sep=";", decimal=",")
    comp.columns = ["date", "chain", "address", "store", "km", "note"]
    comp["date"] = pd.to_datetime(comp["date"], format="%d-%m-%Y")
    T["comp"] = comp
    fc = pd.read_csv(os.path.join(target, "ordreforslag_2026.csv"))
    fc.columns = ["date", "store", "item", "f_auto", "f_korn", "ss", "order", "basis"]
    fc["date"] = pd.to_datetime(fc["date"])
    T["fc"] = fc
    T["pilot"] = sorted(fc.loc[fc["basis"] == "Kornblomst", "store"].unique().tolist())
    return T


# ------------------------------------------------------------------------------------------------------- the periods
def periods(daily):
    base = (daily["year"] == 2025) & daily["week"].between(10, 35)
    pil = (daily["year"] == 2026) & daily["week"].between(10, 35)
    return base, pil


# ---------------------------------------------------------------------------------------------------------- results
def headline(T):
    """R1: fresh sales growth and fresh waste change, pilot weeks against the same weeks of 2025, pilot against the
    rest (percentage points)."""
    d = T["daily"]
    base, pil = periods(d)
    isp = d["store"].isin(T["pilot"])
    out = {}
    for g, m in [("pilot", isp), ("other", ~isp)]:
        s0, s1 = d.loc[base & m, "sales"].sum(), d.loc[pil & m, "sales"].sum()
        w0, w1 = d.loc[base & m, "waste_val"].sum(), d.loc[pil & m, "waste_val"].sum()
        out[g] = dict(sales0=s0, sales1=s1, growth=s1 / s0 - 1, waste0=w0, waste1=w1, wchange=w1 / w0 - 1)
    out["gap_sales_pp"] = 100 * (out["pilot"]["growth"] - out["other"]["growth"])
    out["gap_waste_pp"] = 100 * (out["pilot"]["wchange"] - out["other"]["wchange"])
    return out


def cum_profile(T):
    """F(format, cat, dow, t): the share of a day's sales made by clock time t, from the hourly profile."""
    prof = T["profile"]
    tab = {}
    for (f, c, dw), g in prof.groupby(["format", "cat", "dow"]):
        g = g.sort_values("h0")
        h = np.concatenate([[g["h0"].iloc[0]], g["h0"].values + 1])
        F = np.concatenate([[0.0], np.cumsum(g["share"].values)])
        tab[(f, c, dw)] = (h, F / F[-1])
    return tab


def lost_units(T, method="profile"):
    """R2: units customers wanted after the shelf emptied. A store-item-day ran out when it closed with nothing
    on the shelf; what the rest of the day would have sold is the day's sales so far scaled by the share of a day's
    trade still to come after the last sale (the hourly profile of the store's format, category and weekday)."""
    d = T["daily"]
    out = d["close"] <= 0
    sold = d["sold"].values.astype(float)
    lost = np.zeros(len(d))
    if method == "profile":
        tab = cum_profile(T)
        F = np.full(len(d), np.nan)
        keys = d[["format", "cat", "dow"]].values
        tt = d["t"].values
        idx = np.where(out.values & (sold > 0))[0]
        for k in idx:
            h, Fc = tab[(keys[k, 0], keys[k, 1], int(keys[k, 2]))]
            F[k] = np.interp(tt[k], h, Fc)
        f = np.clip(F[idx], 0.02, 1.0)
        lost[idx] = sold[idx] * (1 - f) / f
    elif method == "instock_mean":
        # the same weekday's average sales on days the item did not run out, as that day's demand
        key = ["store", "item", "dow", "year"]
        m = d.loc[~out].groupby(key)["sold"].mean().rename("mu")
        dd = d[key].join(m, on=key)
        lost = np.where(out.values, np.maximum(dd["mu"].values - sold, 0.0), 0.0)
        lost = np.nan_to_num(lost)
    elif method == "flat":
        tab = cum_profile(T)
        idx = np.where(out.values & (sold > 0))[0]
        oh = d["store"].map(dict(zip(T["stores"]["store"], T["stores"]["hours"]))).values
        tt = d["t"].values
        for k in idx:
            a, b = _open_close(oh[k], int(d["dow"].values[k]))
            f = min(max((tt[k] - a) / (b - a), 0.02), 1.0)
            lost[k] = sold[k] * (1 - f) / f
    return lost


def _open_close(txt, dow):
    m = re.findall(r"(\d\d)-(\d\d)", txt)
    if len(m) == 1:
        return int(m[0][0]), int(m[0][1])
    return (int(m[0][0]), int(m[0][1])) if dow < 6 else (int(m[1][0]), int(m[1][1]))


def lost_units_os(T, sold_floor=1.0, clip=True):
    """The order-statistic form of the same estimate: the S-th sale of a day falls on average at S/(D+1) of the
    day's trade, so the day's demand is about (S-1)/F(t) and what the empty shelf turned away is that less S."""
    d = T["daily"]
    out = (d["close"] <= 0).values
    S = d["sold"].values.astype(float)
    tab = cum_profile(T)
    idx = np.where(out & (S > 0))[0]
    keys = d[["format", "cat", "dow"]].values
    tt = d["t"].values
    F = np.empty(len(idx))
    for n, k in enumerate(idx):
        h, Fc = tab[(keys[k, 0], keys[k, 1], int(keys[k, 2]))]
        F[n] = np.interp(tt[k], h, Fc)
    f = np.clip(F, 0.02, 1.0)
    lost = np.zeros(len(d))
    est = (S[idx] - sold_floor) / f - S[idx]
    lost[idx] = np.maximum(est, 0.0) if clip else est
    return lost


# ----------------------------------------------------------------------------------------------- store-level tables
def store_period(T, lost):
    """Per store and period (base = the same weeks of 2025, pilot = weeks 10 to 35 of 2026): fresh sales, waste at
    cost, units sold, units turned away and their margin, from the daily record."""
    d = T["daily"].copy()
    d["lost"] = lost
    base, pil = periods(d)
    d["per"] = np.where(base, "base", np.where(pil, "pilot", ""))
    d = d[d["per"] != ""]
    # the margin a turned-away unit would have earned: the item's average shelf price in that store and period
    # less its cost
    pr = d.loc[d["sold"] > 0].groupby(["store", "item", "per"]).agg(sv=("sales", "sum"), su=("sold", "sum"))
    pr["unit_price"] = pr["sv"] / pr["su"]
    d = d.join(pr["unit_price"].rename("avg_price"), on=["store", "item", "per"])
    d["avg_price"] = d["avg_price"].fillna(d["unit_price"]).fillna(0.0)
    d["lost_margin"] = d["lost"] * (d["avg_price"] - d["cost"]).clip(lower=0)
    d["lost_sales"] = d["lost"] * d["avg_price"]
    d["wkend"] = d["dow"] >= 5
    d["gm"] = d["sales"] - d["sold"] * d["cost"]
    g = d.groupby(["store", "per"]).agg(sales=("sales", "sum"), waste=("waste_val", "sum"), units=("sold", "sum"),
                                         lost=("lost", "sum"), lost_margin=("lost_margin", "sum"),
                                         lost_sales=("lost_sales", "sum"), gm=("gm", "sum")).unstack("per")
    g.columns = ["%s_%s" % (a, b) for a, b in g.columns]
    wk = d.loc[d["per"] == "base"].groupby("store").apply(lambda x: x.loc[x["wkend"], "sold"].sum() / x["sold"].sum(),
                                                           include_groups=False)
    g["weekend_share"] = wk
    st = T["stores"].set_index("store")
    g["format"] = st["format"]
    g["pilot"] = g.index.isin(T["pilot"])
    return g


def openings(T):
    """The competitor openings near each store that fall in or before the record (the log's opened rows)."""
    c = T["comp"]
    c = c[c["note"].str.startswith("åbnet")]
    return c[c["date"] <= pd.Timestamp("2026-08-30")]


def competitor_effect(T, ramp_weeks=4):
    """R4: each opening's effect on its store's trade, read from the ambient (non-fresh) weekly sales, which the
    ordering forecast never touches. Each week of 2026 is set against the same week of 2025 (so the seasons and the
    stores' own weekly rhythms cancel) and against the same comparison for the format's stores with no opening; the
    opening shows as a step in that series at its date (an opening in 2026 lowers the weeks after it, an opening in
    2025 lowers the weeks before it, when only 2026 had the competitor)."""
    bi = T["bi"]
    amb = bi[bi["cat"] == "Kolonial"].copy()
    piv = amb.pivot_table(index=["year", "week"], columns="store", values="sales")
    weeks = list(range(10, 36))
    y25 = piv.loc[2025].reindex(weeks)
    y26 = piv.loc[2026].reindex(weeks)
    yoy = np.log(y26) - np.log(y25)
    ops = openings(T)
    hit = set(ops["store"])
    fmt = T["stores"].set_index("store")["format"]
    out = {}
    for r in ops.itertuples():
        s = r.store
        if s not in yoy.columns:
            continue
        clean = [c for c in yoy.columns if c not in hit and fmt[c] == fmt[s]]
        rel = yoy[s] - yoy[clean].mean(axis=1)
        y, wk, _ = r.date.isocalendar()
        if y < 2025 or (y == 2025 and wk < 10) or wk > 35 and y == 2026:
            continue
        if y == 2026:
            pre = rel.loc[10:wk - 1]
            post = rel.loc[min(35, wk + ramp_weeks):35]
            eff = np.exp(post.mean() - pre.mean()) - 1
        else:
            pre = rel.loc[10:wk - 1]                   # 2026 has the competitor, 2025 not yet
            post = rel.loc[min(35, wk + ramp_weeks):35]  # both years have it
            eff = np.exp(pre.mean() - post.mean()) - 1
        if len(pre) < 3 or len(post) < 3:
            continue
        out[s] = dict(date=r.date, km=float(r.km), effect=float(eff), weeks_pre=len(pre), weeks_post=len(post))
    return out


def opening_share(T, eff, ramp_weeks=4):
    """The share of each store's trade the openings took in each period: the settled effect, ramped in over the
    first weeks after the opening date."""
    shares = {}
    for s, e in eff.items():
        for per, (y, w0, w1) in {"base": (2025, 10, 35), "pilot": (2026, 10, 35)}.items():
            tot = 0.0
            for wk in range(w0, w1 + 1):
                monday = pd.Timestamp.fromisocalendar(y, wk, 1)
                dt_w = (monday - e["date"]).days / 7.0
                f = 0.0 if dt_w < 0 else min(1.0, (dt_w + 0.5) / ramp_weeks)
                tot += f
            shares[(s, per)] = -e["effect"] * tot / (w1 - w0 + 1)
    return shares


def decompose(T, sp, eff, lost_value="lost_sales", comp_adjust=True):
    """R5 and R6: each headline gap split into its causes."""
    H = headline(T)
    shares = opening_share(T, eff)
    sp = sp.copy()
    sp["comp_base"] = [shares.get((s, "base"), 0.0) for s in sp.index]
    sp["comp_pilot"] = [shares.get((s, "pilot"), 0.0) for s in sp.index]
    hit = set(eff)
    # each format's own growth and waste change on the stores that kept AutoOrdre and had no opening
    ctrl = sp[(~sp["pilot"]) & (~sp.index.isin(hit))]
    g_f = (ctrl.groupby("format")["sales_pilot"].sum() / ctrl.groupby("format")["sales_base"].sum() - 1)
    w_f = (ctrl.groupby("format")["waste_pilot"].sum() / ctrl.groupby("format")["waste_base"].sum() - 1)
    lm_f = (ctrl.groupby("format")[lost_value + "_pilot"].sum() / ctrl.groupby("format")[lost_value + "_base"].sum())
    out = {"growth_by_format": g_f.to_dict(), "waste_change_by_format": w_f.to_dict()}
    P, O = sp[sp["pilot"]], sp[~sp["pilot"]]
    # format mix: the gap each group's format composition gives at the formats' own growth
    mix_s = (P.groupby("format")["sales_base"].sum() / P["sales_base"].sum() * g_f).sum() - \
            (O.groupby("format")["sales_base"].sum() / O["sales_base"].sum() * g_f).sum()
    mix_w = (P.groupby("format")["waste_base"].sum() / P["waste_base"].sum() * w_f).sum() - \
            (O.groupby("format")["waste_base"].sum() / O["waste_base"].sum() * w_f).sum()
    # the openings: the share of trade they took in the pilot weeks against the same weeks of 2025, each group, on
    # each group's sales (for the sales gap) and on its waste (for the waste gap)
    def comp_part(G, w):
        return ((G["comp_pilot"] - G["comp_base"]) * G[w]).sum() / G[w].sum()
    comp_s = -(comp_part(P, "sales_base") - comp_part(O, "sales_base"))
    comp_w = -(comp_part(P, "waste_base") - comp_part(O, "waste_base"))
    # a pilot store's level on AutoOrdre: its 2025 figure carried by its format's change and by the trade an opening took
    adj = (1 - P["comp_pilot"]) / (1 - P["comp_base"]) if comp_adjust else 1.0
    # the forecast: the pilot stores' sales lost to empty shelves beyond that level
    exp_lost = (P[lost_value + "_base"] * P["format"].map(lm_f) * adj).sum()
    fc_s = -(P[lost_value + "_pilot"].sum() - exp_lost) / P["sales_base"].sum()
    # waste: the pilot stores' waste against that level
    exp_w = (P["waste_base"] * (1 + P["format"].map(w_f)) * adj).sum()
    fc_w = (P["waste_pilot"].sum() - exp_w) / P["waste_base"].sum()
    out["sales"] = dict(gap=H["gap_sales_pp"], forecast=100 * fc_s, competitors=100 * comp_s, format_mix=100 * mix_s)
    out["sales"]["rest"] = out["sales"]["gap"] - out["sales"]["forecast"] - out["sales"]["competitors"] - out["sales"]["format_mix"]
    out["waste"] = dict(gap=H["gap_waste_pp"], forecast=100 * fc_w, competitors=100 * comp_w, format_mix=100 * mix_w)
    out["waste"]["rest"] = (out["waste"]["gap"] - out["waste"]["forecast"] - out["waste"]["competitors"]
                            - out["waste"]["format_mix"])
    out["headline"] = H
    return out


def store_savings(T, sp, eff, lost_value="lost_margin", recorded=False, comp_adjust=True):
    """Each pilot store's saving over the 26 pilot weeks against the same store on AutoOrdre: the waste at cost its
    format's stores without the forecast (and without an opening) would have let it write off, less what it wrote
    off; plus the margin on the units its empty shelves turned away beyond what the same weeks of 2025 carried by its
    format's change would give, taken off. recorded=True takes the margin part from the recorded gross margin
    instead (the year-on-year change in gross margin against its format's, the openings' share of trade taken out)."""
    hit = set(eff)
    ctrl = sp[(~sp["pilot"]) & (~sp.index.isin(hit))]
    rw = ctrl.groupby("format")["waste_pilot"].sum() / ctrl.groupby("format")["waste_base"].sum()
    P = sp[sp["pilot"]].copy()
    # a pilot store a discounter opened near trades less in the pilot weeks whichever forecast it orders on: what it
    # would have written off and turned away on AutoOrdre is carried by the share of trade the opening took
    shares = opening_share(T, eff)
    cb = np.array([shares.get((s, "base"), 0.0) for s in P.index])
    cp = np.array([shares.get((s, "pilot"), 0.0) for s in P.index])
    adj = (1 - cp) / (1 - cb) if comp_adjust else 1.0
    P["waste_saving"] = P["waste_base"] * P["format"].map(rw) * adj - P["waste_pilot"]
    if recorded:
        rg = ctrl.groupby("format")["gm_pilot"].sum() / ctrl.groupby("format")["gm_base"].sum()
        P["margin_change"] = P["gm_pilot"] - P["gm_base"] * P["format"].map(rg) * (1 - cp) / (1 - cb)
    else:
        rl = ctrl.groupby("format")[lost_value + "_pilot"].sum() / ctrl.groupby("format")[lost_value + "_base"].sum()
        P["margin_change"] = -(P[lost_value + "_pilot"] - P[lost_value + "_base"] * P["format"].map(rl) * adj)
    P["saving"] = P["waste_saving"] + P["margin_change"]
    return P


def trading_type(sp, cut=None):
    """Each store's trading week from its own record: weekend-trading or commuter-week, split at the widest gap in
    the stores' weekend shares (Saturday and Sunday's part of its fresh units in the same weeks of 2025)."""
    ws = np.sort(sp["weekend_share"].values)
    if cut is None:
        gaps = np.diff(ws)
        k = int(np.argmax(gaps))
        cut = (ws[k] + ws[k + 1]) / 2
    return np.where(sp["weekend_share"] >= cut, "weekend", "commuter"), cut


def _rates(P, key, num, den, wmode):
    if wmode == "ratio":
        return P.groupby(key).apply(lambda g: g[num].sum() / g[den].sum(), include_groups=False)
    return P.assign(_r=P[num] / P[den]).groupby(key)["_r"].mean()


def transport(sp, P, key="type", mscale="sales_base", wmode="ratio"):
    """Each store's expected saving over a year (twice the 26 pilot weeks): the waste part carried on its own waste in
    the same weeks of 2025 and the margin part on its own fresh sales there, each at the rate of the pilot stores in
    its group (key: trading type, format, or format within trading type), the pilot stores' rate being their total
    over their total."""
    P = P.copy()
    P["type"] = sp.loc[P.index, "type"]
    if key == "fxt":
        rw_t = _rates(P, "type", "waste_saving", "waste_base", wmode)
        rm_t = _rates(P, "type", "margin_change", mscale, wmode)
        rw = _rates(P, ["format", "type"], "waste_saving", "waste_base", wmode)
        rm = _rates(P, ["format", "type"], "margin_change", mscale, wmode)
        a = np.array([rw.get((f, t), rw_t[t]) for f, t in zip(sp["format"], sp["type"])])
        b = np.array([rm.get((f, t), rm_t[t]) for f, t in zip(sp["format"], sp["type"])])
        rates = {"waste": rw.to_dict(), "margin": rm.to_dict()}
    elif key == "linear":
        a, b = np.zeros(len(sp)), np.zeros(len(sp))
        rates = {}
        for part, num, den, out in [("waste", "waste_saving", "waste_base", a), ("margin", "margin_change", mscale, b)]:
            X = np.column_stack([np.ones(len(P)), P["weekend_share"].values])
            y = (P[num] / P[den]).values
            wt = P[den].values
            beta = np.linalg.solve(X.T @ (X * wt[:, None]), X.T @ (y * wt))
            out[:] = beta[0] + beta[1] * sp["weekend_share"].values
            rates[part] = beta.tolist()
    else:
        rw = _rates(P, key, "waste_saving", "waste_base", wmode)
        rm = _rates(P, key, "margin_change", mscale, wmode)
        a, b = sp[key].map(rw).values, sp[key].map(rm).values
        rates = {"waste": rw.to_dict(), "margin": rm.to_dict()}
    pred = pd.Series((a * sp["waste_base"].values + b * sp[mscale].values) * 2.0, index=sp.index)
    return pred, rates


def check_on_instock_days(T):
    """R3: the turned-away estimate tried on the days the shelf did not run out, where a day's demand is known (it
    is what sold): reading the day's last sale as if the shelf had emptied then, each form's estimate of the day's
    demand against what sold. The plain form, sales so far over the share of the day gone, overshoots by about a
    sale a day; the order-statistic form does not."""
    d = T["daily"]
    tab = cum_profile(T)
    ok = (d["close"] > 0).values & (d["sold"].values >= 2)
    idx = np.where(ok)[0]
    keys = d[["format", "cat", "dow"]].values
    tt = d["t"].values
    S = d["sold"].values.astype(float)
    F = np.empty(len(idx))
    for n, k in enumerate(idx):
        h, Fc = tab[(keys[k, 0], keys[k, 1], int(keys[k, 2]))]
        F[n] = np.interp(tt[k], h, Fc)
    f = np.clip(F, 0.02, 1.0)
    s = S[idx]
    plain = s / f
    os_ = (s - 1) / f
    small = s <= 6
    clip_lost = np.maximum(os_ - s, 0.0)
    return dict(days=int(len(idx)), sold=float(s.sum()), plain=float(plain.sum()), os=float(os_.sum()),
                plain_over=float(plain.sum() / s.sum() - 1), os_over=float(os_.sum() / s.sum() - 1),
                plain_over_small=float(plain[small].sum() / s[small].sum() - 1),
                os_over_small=float(os_[small].sum() / s[small].sum() - 1), small_days=int(small.sum()),
                clip_over=float(clip_lost.sum() / s.sum()))


def bootstrap_formats(T, sp, eff, lost_value="lost_margin", reps=400, seed=11, key="type", mscale="sales_base",
                      money="full", scheme="golden"):
    """R9: the 80 per cent range on each format's yearly saving per store, resampling the stores (the pilot stores
    within their trading type, the others within their format), with every step refitted."""
    rng = np.random.default_rng(seed)
    piv = sp[sp["pilot"]]
    oth = sp[~sp["pilot"]]
    hit = set(eff)
    shares = opening_share(T, eff)
    res = []
    grp = "format" if key == "format" else "type"
    for _ in range(reps):
        parts = []
        for t, g in piv.groupby(grp):
            parts.append(g.sample(len(g), replace=True, random_state=int(rng.integers(1 << 30))))
        if scheme == "golden":
            for f, g in oth.groupby("format"):
                parts.append(g.sample(len(g), replace=True, random_state=int(rng.integers(1 << 30))))
        else:
            parts.append(oth)
        b = pd.concat(parts)
        b = b.reset_index().rename(columns={"index": "store"})
        ctrl = b[(~b["pilot"]) & (~b["store"].isin(hit))]
        rw = ctrl.groupby("format")["waste_pilot"].sum() / ctrl.groupby("format")["waste_base"].sum()
        rl = ctrl.groupby("format")[lost_value + "_pilot"].sum() / ctrl.groupby("format")[lost_value + "_base"].sum()
        P = b[b["pilot"]].copy()
        adj = np.array([(1 - shares.get((s, "pilot"), 0.0)) / (1 - shares.get((s, "base"), 0.0)) for s in P["store"]])
        P["waste_saving"] = P["waste_base"] * P["format"].map(rw) * adj - P["waste_pilot"]
        P["margin_change"] = 0.0 if money == "waste_only" else -(P[lost_value + "_pilot"] - P[lost_value + "_base"] * P["format"].map(rl) * adj)
        P = P.set_index(np.arange(len(P)))
        sp_b = sp.copy()
        if key == "format":
            rw_ = P.groupby("format").apply(lambda g: g["waste_saving"].sum() / g["waste_base"].sum(), include_groups=False)
            rm_ = P.groupby("format").apply(lambda g: g["margin_change"].sum() / g[mscale].sum(), include_groups=False)
            a, bb = sp_b["format"].map(rw_).values, sp_b["format"].map(rm_).values
        else:
            rw_ = P.groupby("type").apply(lambda g: g["waste_saving"].sum() / g["waste_base"].sum(), include_groups=False)
            rm_ = P.groupby("type").apply(lambda g: g["margin_change"].sum() / g[mscale].sum(), include_groups=False)
            a, bb = sp_b["type"].map(rw_).values, sp_b["type"].map(rm_).values
        pred = pd.Series((a * sp_b["waste_base"].values + bb * sp_b[mscale].values) * 2.0, index=sp_b.index)
        res.append(pred.groupby(sp_b["format"]).mean())
    R = pd.DataFrame(res)
    return R.quantile(0.10), R.quantile(0.90), R


# ------------------------------------------------------------------------------------------------- the whole chain
METHODS = {
    "golden": dict(lost="unc", transport="type", competitors=True, money="full"),
    "careful": dict(lost="plain", transport="format", competitors=True, money="full"),
    "quick": dict(lost="none", transport="dashboard", competitors=False, money="waste_only"),
}


def lost_for(T, how):
    if how == "unc":
        return lost_units_os(T, clip=False)
    if how == "os":
        return lost_units_os(T)
    if how == "plain":
        return lost_units(T, "profile")
    if how == "instock":
        return lost_units(T, "instock_mean")
    if how == "flat":
        return lost_units(T, "flat")
    return np.zeros(len(T["daily"]))


def analyse(T, lost="unc", transport="type", competitors=True, money="full", mscale="sales_base", wmode="ratio",
            cut=None, reps=0, cache=None, scheme="golden", comp_adjust=True):
    cache = {} if cache is None else cache
    lk = "unc" if lost == "recorded" else lost
    if lk not in cache:
        cache[lk] = lost_for(T, lk)
    L = cache[lk]
    sp = store_period(T, L)
    eff = competitor_effect(T) if competitors else {}
    typ, cut_ = trading_type(sp, cut)
    sp["type"] = typ
    P = store_savings(T, sp, eff, recorded=(lost == "recorded"), comp_adjust=comp_adjust)
    if money == "waste_only":
        P["margin_change"] = 0.0
        P["saving"] = P["waste_saving"]
    P["type"] = sp.loc[P.index, "type"]
    out = {"sp": sp, "P": P, "eff": eff, "cut": cut_}
    if transport in ("type", "format", "fxt", "linear"):
        pred, rates = _transport_call(sp, P, transport, mscale, wmode)
        out["rates"] = rates
    elif transport == "dashboard":
        # the dashboard read as the forecast's saving: the pilot stores' waste fell this many points of their
        # 2025 waste further than the others', so every store saves that share of its waste
        H = headline(T)
        r = -(H["pilot"]["wchange"] - H["other"]["wchange"])
        pred = r * sp["waste_base"] * 2.0
        out["rates"] = {"dashboard": r}
    elif transport == "single_waste":
        rate = P.groupby("type").apply(lambda g: g["saving"].sum() / g["waste_base"].sum(), include_groups=False)
        pred = sp["type"].map(rate) * sp["waste_base"] * 2.0
    elif transport == "single_sales":
        rate = P.groupby("type").apply(lambda g: g["saving"].sum() / g["sales_base"].sum(), include_groups=False)
        pred = sp["type"].map(rate) * sp["sales_base"] * 2.0
    elif transport == "pooled_sales":
        r = P["saving"].sum() / P["sales_base"].sum()
        pred = r * sp["sales_base"] * 2.0
    out["pred"] = pred
    fs = pred.groupby(sp["format"]).mean()
    out["format_saving"] = fs.to_dict()
    out["switch"] = [f for f in FORMATS if fs[f] > LICENCE[f]]
    D = decompose(T, sp, eff, lost_value="lost_sales", comp_adjust=comp_adjust)
    if lost == "none":
        D["sales"]["forecast"] = D["sales"]["gap"]
        D["sales"]["competitors"] = D["sales"]["format_mix"] = 0.0
        D["sales"]["rest"] = 0.0
    if not competitors:
        D["sales"]["rest"] = D["sales"]["gap"] - D["sales"]["forecast"] - D["sales"]["format_mix"]
    if transport == "dashboard":
        for k in ("sales", "waste"):
            D[k]["forecast"] = D[k]["gap"]
            for kk in ("competitors", "format_mix", "rest"):
                if kk in D[k]:
                    D[k][kk] = 0.0
    out["decomp"] = D
    if reps and transport in ("type", "format"):
        lo, hi, _ = bootstrap_formats(T, sp, eff, reps=reps, key=transport, mscale=mscale, money=money, scheme=scheme)
        out["range"] = {f: (float(lo[f]), float(hi[f])) for f in FORMATS}
    isp = sp["pilot"]
    out["lost_units"] = {"pilot_base": float(sp.loc[isp, "lost_base"].sum()), "pilot_pilot": float(sp.loc[isp, "lost_pilot"].sum()),
                         "other_base": float(sp.loc[~isp, "lost_base"].sum()), "other_pilot": float(sp.loc[~isp, "lost_pilot"].sum())}
    return out


def _transport_call(sp, P, key, mscale, wmode):
    return transport(sp, P, key=key, mscale=mscale, wmode=wmode)


# ------------------------------------------------------------------------------------------- figures for the blocks
def shadow_shape(T, sp):
    """The evidence behind R7: in the pilot weeks, Kornblomst's forecast set against AutoOrdre's (which reads each
    store's own week) in every store, weekend days against working days, by trading type."""
    fc = T["fc"]
    m = fc[(fc["date"] >= "2026-03-02") & fc["f_korn"].notna()].copy()
    m["wkend"] = m["date"].dt.dayofweek >= 5
    g = m.groupby(["store", "wkend"]).agg(k=("f_korn", "sum"), a=("f_auto", "sum")).unstack("wkend")
    ratio = (g[("k", True)] / g[("a", True)]) / (g[("k", False)] / g[("a", False)])
    typ = pd.Series(trading_type(sp)[0], index=sp.index)
    return ratio, ratio.groupby(typ).mean()


RIVALS = {
    # the defensible family for R7, R8 and R9: the estimator (unclipped or clipped), the grouping (trading type, or
    # format within trading type), the scale of the margin part (fresh sales, units, the 2025 turned-away margin)
    "clip_type": dict(lost="os", transport="type"),
    "unc_fxt": dict(lost="unc", transport="fxt"),
    "clip_fxt": dict(lost="os", transport="fxt"),
    "unc_type_units": dict(lost="unc", transport="type", mscale="units_base"),
    "unc_type_lostm": dict(lost="unc", transport="type", mscale="lost_margin_base"),
    "clip_type_units": dict(lost="os", transport="type", mscale="units_base"),
    "clip_type_lostm": dict(lost="os", transport="type", mscale="lost_margin_base"),
    "unc_fxt_units": dict(lost="unc", transport="fxt", mscale="units_base"),
    "unc_fxt_lostm": dict(lost="unc", transport="fxt", mscale="lost_margin_base"),
    "unc_type_mean": dict(lost="unc", transport="type", wmode="mean"),
    "clip_type_mean": dict(lost="os", transport="type", wmode="mean"),
    "unc_linear": dict(lost="unc", transport="linear"),
    "recorded_type": dict(lost="recorded", transport="type"),
    "unc_type_noadj": dict(lost="unc", transport="type", comp_adjust=False),
}
ROUTES = {
    # the shortcuts: each a complete pipeline a hurried pass files
    "by_format": dict(lost="unc", transport="format"),
    "plain_type": dict(lost="plain", transport="type"),
    "instock_type": dict(lost="instock", transport="type"),
    "waste_only_type": dict(lost="unc", transport="type", money="waste_only"),
    "single_sales_type": dict(lost="unc", transport="single_sales"),
    "single_waste_type": dict(lost="unc", transport="single_waste"),
    "pooled_sales": dict(lost="unc", transport="pooled_sales"),
}


def results(T, reps=400):
    cache = {}
    G = analyse(T, cache=cache, reps=reps, **METHODS["golden"])
    C = analyse(T, cache=cache, reps=reps, **METHODS["careful"])
    Q = analyse(T, cache=cache, reps=0, **METHODS["quick"])
    rivals = {nm: analyse(T, cache=cache, **kw) for nm, kw in RIVALS.items()}
    routes = {nm: analyse(T, cache=cache, **kw) for nm, kw in ROUTES.items()}
    chk = check_on_instock_days(T)
    ratio, ratio_type = shadow_shape(T, G["sp"])
    return dict(G=G, C=C, Q=Q, rivals=rivals, routes=routes, check=chk, shadow=ratio, shadow_type=ratio_type,
                H=headline(T), T=T)


def placebo_spread(T, sp, eff):
    """The two ways of reading the margin part, tried on the stores that kept AutoOrdre, where the forecast changed
    nothing: each store's recorded gross margin against its format's other clean stores (the openings' share taken
    out), and its turned-away margin the same way. The spread of each across the stores is the noise that way of
    reading carries into a pilot store's figure (DKK over the 26 weeks)."""
    shares = opening_share(T, eff)
    hit = set(eff)
    non = sp[~sp["pilot"]]
    rows = []
    for s in non.index:
        f = non.loc[s, "format"]
        ctrl = non[(non["format"] == f) & (~non.index.isin(hit)) & (non.index != s)]
        rg = ctrl["gm_pilot"].sum() / ctrl["gm_base"].sum()
        rl = ctrl["lost_margin_pilot"].sum() / ctrl["lost_margin_base"].sum()
        adj = (1 - shares.get((s, "pilot"), 0.0)) / (1 - shares.get((s, "base"), 0.0))
        rows.append((f, non.loc[s, "gm_pilot"] - non.loc[s, "gm_base"] * rg * adj,
                     -(non.loc[s, "lost_margin_pilot"] - non.loc[s, "lost_margin_base"] * rl * adj)))
    df = pd.DataFrame(rows, columns=["format", "recorded", "turned_away"])
    out = {}
    for f, g in df.groupby("format"):
        out[f] = {"recorded_sd": int(round(g["recorded"].std(), -2)), "turned_away_sd": int(round(g["turned_away"].std(), -2)),
                  "stores": int(len(g))}
    return out
