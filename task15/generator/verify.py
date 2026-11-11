"""An independent recomputation of the load-bearing figures from the shipped files alone (target/ and
figures.json), written apart from golden.py: the headline gaps, the units turned away, the in-stock check, the
openings, the waste-saving rate by trading week, each format's saving and the call.

    python3 verify.py [task_dir]"""
import json
import os
import sys

import numpy as np
import pandas as pd

TASK = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TG = os.path.join(TASK, "target")
FG = json.load(open(os.path.join(TASK, "generator", "figures.json")))
DAYS = ["mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"]
out = []


def check(name, mine, theirs, tol):
    good = abs(mine - theirs) <= tol
    out.append(good)
    print("%s %-60s mine %12.2f  figures.json %12.2f" % ("OK  " if good else "DIFF", name, mine, theirs))


def clock(v):
    v = v.fillna("").astype(str)
    parts = v.str.split(":", expand=True)
    h = pd.to_numeric(parts[0], errors="coerce")
    m = pd.to_numeric(parts[1], errors="coerce")
    s = pd.to_numeric(parts[2], errors="coerce").fillna(0) if parts.shape[1] > 2 else 0
    return h + m / 60 + s / 3600


items = pd.read_excel(os.path.join(TG, "vareregister_frisk.xlsx"))
renum = dict(zip(items.iloc[:, 12].dropna().astype(int), items.loc[items.iloc[:, 12].notna()].iloc[:, 0].astype(int)))
cat = dict(zip(items.iloc[:, 0].astype(int), items.iloc[:, 2]))
cost = {2025: dict(zip(items.iloc[:, 0].astype(int), items.iloc[:, 8])), 2026: dict(zip(items.iloc[:, 0].astype(int), items.iloc[:, 10]))}
stores = pd.read_excel(os.path.join(TG, "butiksregister.xlsx"))
fmt = dict(zip(stores.iloc[:, 0].astype(int), stores.iloc[:, 2]))
a = pd.read_csv(os.path.join(TG, "dagssalg_frisk_2025.csv"), sep=";", decimal=",", encoding="cp1252", dtype=str)
a = a.drop_duplicates()
a.columns = ["d", "s", "i", "q", "v", "t", "r", "w", "c"]
a["d"] = pd.to_datetime(a["d"], format="%d-%m-%Y")
b = pd.read_csv(os.path.join(TG, "dagssalg_frisk_2026.csv"), dtype=str)
b.columns = ["d", "s", "i", "q", "v", "t", "r", "w", "c"]
b["d"] = pd.to_datetime(b["d"])
x = pd.concat([a, b], ignore_index=True)
for col in ["s", "i", "q", "w", "c"]:
    x[col] = x[col].astype(int)
x["v"] = x["v"].str.replace(",", ".").astype(float)
x["i"] = x["i"].map(lambda i: renum.get(i, i))
x["t"] = clock(x["t"])
iso = x["d"].dt.isocalendar()
x["y"], x["wk"], x["dow"] = iso["year"].astype(int), iso["week"].astype(int), x["d"].dt.dayofweek
x["f"] = x["s"].map(fmt)
x["cat"] = x["i"].map(cat)
x["wv"] = x["w"] * [cost[y][i] for y, i in zip(x["y"], x["i"])]
fc = pd.read_csv(os.path.join(TG, "ordreforslag_2026.csv"))
pilot = set(fc.loc[fc["order_basis"] == "Kornblomst", "store"])
x["p"] = x["s"].isin(pilot)
x["per"] = np.where((x["y"] == 2025) & x["wk"].between(10, 35), "b", np.where((x["y"] == 2026) & x["wk"].between(10, 35), "n", ""))
x = x[x["per"] != ""].copy()

# R1
g = x.groupby(["p", "per"])[["v", "wv"]].sum()
gs = 100 * ((g.loc[(True, "n"), "v"] / g.loc[(True, "b"), "v"]) - (g.loc[(False, "n"), "v"] / g.loc[(False, "b"), "v"]))
gw = 100 * ((g.loc[(True, "n"), "wv"] / g.loc[(True, "b"), "wv"]) - (g.loc[(False, "n"), "wv"] / g.loc[(False, "b"), "wv"]))
check("R1 sales gap, points", gs, FG["gap_sales_pp"], 0.05)
check("R1 waste gap, points", gw, FG["gap_waste_pp"], 0.05)

# the hourly profile as a cumulative share at each hour boundary
pr = pd.read_csv(os.path.join(TG, "timeprofil_salg_frisk.csv"), sep=";", decimal=",")
pr.columns = ["f", "cat", "dow", "h", "share"]
pr["cat"] = pr["cat"].replace({"Frugt og grønt": "Frugt & grønt"})
pr["dow"] = pr["dow"].map(DAYS.index)
pr["h0"] = pr["h"].str[:2].astype(int)
curve = {}
for key, gg in pr.groupby(["f", "cat", "dow"]):
    gg = gg.sort_values("h0")
    hh = np.r_[gg["h0"].iloc[0], gg["h0"].values + 1]
    cc = np.r_[0, np.cumsum(gg["share"].values)]
    curve[key] = (hh, cc / cc[-1])


def share_by(rows):
    vals = np.empty(len(rows))
    for n, (f, c, d, t) in enumerate(zip(rows["f"], rows["cat"], rows["dow"], rows["t"])):
        hh, cc = curve[(f, c, d)]
        vals[n] = np.interp(t, hh, cc)
    return np.clip(vals, 0.02, 1.0)


# R2: units turned away, one sale fewer than made, unclipped
so = x[(x["c"] <= 0) & (x["q"] > 0)].copy()
so["F"] = share_by(so)
so["lost"] = (so["q"] - 1) / so["F"] - so["q"]
lp = so[so["p"]].groupby("per")["lost"].sum()
check("R2 pilot stores' units turned away, pilot weeks", lp["n"], FG["lost_units"]["pilot_2026"], 0.006 * lp["n"])
check("R2 pilot stores' units turned away, same weeks 2025", lp["b"], FG["lost_units"]["pilot_2025"], 0.006 * lp["b"])

# R3: the check on in-stock days with two or more sales
ins = x[(x["c"] > 0) & (x["q"] >= 2)].copy()
ins["F"] = share_by(ins)
check("R3 plain overstatement on in-stock days, per cent", 100 * ((ins["q"] / ins["F"]).sum() / ins["q"].sum() - 1),
      FG["check_plain_over_pct"], 0.05)

# R4: openings from the ambient weekly sales
bi = pd.read_csv(os.path.join(TG, "bi_uge_butik_kategori.csv"), sep=";", decimal=",")
bi.columns = ["yw", "s", "cat", "v", "wv", "q"]
amb = bi[bi["cat"].isin(["KOL", "Kolonial"])].copy()
amb["y"], amb["wk"] = amb["yw"].str[:4].astype(int), amb["yw"].str[6:8].astype(int)
pv = amb.pivot_table(index=["y", "wk"], columns="s", values="v")
yy = np.log(pv.loc[2026].reindex(range(10, 36))) - np.log(pv.loc[2025].reindex(range(10, 36)))
co = pd.read_csv(os.path.join(TG, "konkurrentaabninger.csv"), sep=";")
co.columns = ["d", "chain", "addr", "s", "km", "note"]
co = co[co["note"].str.startswith("åbnet")].copy()
co["d"] = pd.to_datetime(co["d"], format="%d-%m-%Y")
co = co[co["d"] <= "2026-08-30"]
hit = set(co["s"])                       # every store with an opening on the log is kept out of the comparison
co = co[co["d"] >= "2025-03-03"]
eff = {}
for r in co.itertuples():
    clean = [c for c in yy.columns if c not in hit and fmt[c] == fmt[r.s]]
    rel = yy[r.s] - yy[clean].mean(axis=1)
    y, wk, _ = r.d.isocalendar()
    pre, post = rel.loc[10:wk - 1], rel.loc[min(35, wk + 4):35]
    e = np.exp(post.mean() - pre.mean()) - 1 if y == 2026 else np.exp(pre.mean() - post.mean()) - 1
    eff[r.s] = (e, r.d)
for s_, (e, _) in sorted(eff.items()):
    check("R4 opening at %d, per cent of trade" % s_, 100 * e, FG["competitor_effect_pct"][str(s_)], 0.05)


# the openings' share of each store's trade in each period, ramped over four weeks
def share_taken(s_, y):
    if s_ not in eff:
        return 0.0
    e, d0 = eff[s_]
    f = [min(1.0, max(0.0, ((pd.Timestamp.fromisocalendar(y, wk, 1) - d0).days / 7.0 + 0.5) / 4)) if (pd.Timestamp.fromisocalendar(y, wk, 1) - d0).days >= 0 else 0.0
         for wk in range(10, 36)]
    return -e * np.mean(f)


# R7 and R8: each pilot store's saving, carried by trading week
x["price"] = np.where(x["q"] > 0, x["v"] / x["q"].clip(lower=1), np.nan)
avgp = x[x["q"] > 0].groupby(["s", "i", "per"]).apply(lambda gg: gg["v"].sum() / gg["q"].sum(), include_groups=False)
so2 = x[(x["c"] <= 0) & (x["q"] > 0)].copy()
so2["F"] = share_by(so2)
so2["lost"] = (so2["q"] - 1) / so2["F"] - so2["q"]
so2["unitc"] = [cost[y][i] for y, i in zip(so2["y"], so2["i"])]
so2["ap"] = [avgp.get((s_, i, p_), np.nan) for s_, i, p_ in zip(so2["s"], so2["i"], so2["per"])]
so2["lm"] = so2["lost"] * (so2["ap"].fillna(so2["price"]) - so2["unitc"]).clip(lower=0)
st = pd.DataFrame({
    "wb": x[x["per"] == "b"].groupby("s")["wv"].sum(), "wn": x[x["per"] == "n"].groupby("s")["wv"].sum(),
    "sb": x[x["per"] == "b"].groupby("s")["v"].sum(),
    "lb": so2[so2["per"] == "b"].groupby("s")["lm"].sum(), "ln": so2[so2["per"] == "n"].groupby("s")["lm"].sum(),
    "we": x[x["per"] == "b"].groupby("s").apply(lambda gg: gg.loc[gg["dow"] >= 5, "q"].sum() / gg["q"].sum(), include_groups=False)}).fillna(0.0)
st["f"] = st.index.map(fmt)
st["p"] = st.index.isin(pilot)
ws_ = np.sort(st["we"].values)
k = int(np.argmax(np.diff(ws_)))
cut = (ws_[k] + ws_[k + 1]) / 2
st["type"] = np.where(st["we"] >= cut, "weekend", "commuter")
ctrl = st[(~st["p"]) & (~st.index.isin(set(eff)))]   # the stores an opening in the record touched are left out
rw = ctrl.groupby("f")["wn"].sum() / ctrl.groupby("f")["wb"].sum()
rl = ctrl.groupby("f")["ln"].sum() / ctrl.groupby("f")["lb"].sum()
P = st[st["p"]].copy()
P["adj"] = [(1 - share_taken(s_, 2026)) / (1 - share_taken(s_, 2025)) for s_ in P.index]
P["ws"] = P["wb"] * P["f"].map(rw) * P["adj"] - P["wn"]
P["mc"] = -(P["ln"] - P["lb"] * P["f"].map(rl) * P["adj"])
rate_w = P.groupby("type")["ws"].sum() / P.groupby("type")["wb"].sum()
rate_m = P.groupby("type")["mc"].sum() / P.groupby("type")["sb"].sum()
for t_ in ("weekend", "commuter"):
    check("R7 waste saving rate, %s-trading pilot stores, per cent" % t_, 100 * rate_w[t_], FG["waste_rate_pct"][t_], 0.05)
st["save"] = (st["type"].map(rate_w) * st["wb"] + st["type"].map(rate_m) * st["sb"]) * 2
fs = st.groupby("f")["save"].mean()
lic = FG["licence"]
for f in ("Super", "Kvarter", "To Go"):
    check("R8 %s expected saving per store and year, DKK" % f, fs[f], FG["saving"][f], 75)
call = [f for f in ("Super", "Kvarter", "To Go") if fs[f] > lic[f]]
out.append(call == FG["switch"])
print("%s R10 call %s against %s" % ("OK  " if call == FG["switch"] else "DIFF", call, FG["switch"]))
print("verify: %d of %d agree" % (sum(out), len(out)))
sys.exit(0 if all(out) else 1)
