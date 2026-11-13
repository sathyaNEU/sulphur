"""The analysis, written once against the shipped pack and run with switches, so the golden, the careful but
hurried pass, every shortcut and every rival are the same code with different choices.

Choices (opts):
  channels    ("live", "lic") golden: every position the app reports; ("live",) the warehouse roll-up alone
  basis       "position" golden: the counting rule on positions; "seconds": streamed seconds read as hours
  member      "dated" golden: each profile on the account whose charge that month lists it; "today": the profile
              export's current account for the whole history
  cost        "rate27" golden: EUR 0.40 per counted hour; "share26": 52 per cent of net revenue (the 2026 basis)
  dedup       True golden: a re-sent warehouse row dropped; False summed
  lic_month   "renewal" golden: a renewal's position counted in its own month; "next": in the month after
  r6          the 2027 forecast's form: "plan_tenure" golden survival by plan and tenure band, "plan" by plan
              alone; hours "season" golden by plan and calendar month, "flat" the twelve months' mean, "own" each
              account's own twelve months
"""
import os

import numpy as np
import pandas as pd

import params as P
import pack as PK

GOLD = {"channels": ("live", "lic"), "basis": "position", "member": "dated", "cost": "rate27", "dedup": True,
        "lic_month": "renewal", "r6_surv": "plan_tenure", "r6_hours": "season"}


def opts(**kw):
    o = dict(GOLD)
    o.update(kw)
    return o


def midx(label):
    y, m = int(label[:4]), int(label[5:7])
    return (y - P.M0_YEAR) * 12 + m - 1


_CACHE = {}


def load(target):
    if target in _CACHE:
        return _CACHE[target]
    f = lambda k: os.path.join(target, PK.FILES[k])
    acc = pd.read_csv(f("acc"), dtype=str)
    pay = pd.read_csv(f("pay"), dtype={"profiles_on_subscription": str, "account_id": str})
    prof = pd.read_csv(f("prof"), dtype=str)
    live = pd.read_csv(f("live"), dtype={"profile_id": str, "title_id": str})
    lic = pd.read_csv(f("lic"), dtype={"profile_id": str, "title_id": str})
    cat = pd.read_csv(f("cat"), dtype=str)
    plan = pd.read_csv(f("plan"), dtype=str)
    pay["m"] = pay["charged_on"].str[:7].map(midx)
    live["m"] = live["month"].map(midx)
    lic["m"] = lic["renewed_at_utc"].str[:7].map(midx)
    consumer = set(acc.loc[acc["account_type"] == "consumer", "account_id"])
    pay["consumer"] = pay["account_id"].isin(consumer)
    pay["paying"] = pay["status"].isin(["collected", "re-presented"]) & (pay["amount_eur"] > 0) & pay["consumer"]
    licensed = set(cat.loc[cat["rights"] == "licensed", "title_id"])
    rv = pd.read_csv(f("riv"), dtype=str)
    rv = rv[rv["note"].isna()]
    names = {v: k for k, v in P.RIVAL_NAME.items()}
    rivalmap = {}
    for (y, mon) in [(2025, "2024-12"), (2026, "2025-12"), (2027, "2026-10")]:
        sub = rv[rv["scan_month"] == mon]
        for c, rp, pr in zip(sub["country"], sub["rival_plan"], sub["price_eur"]):
            rivalmap[(y, c, names[rp])] = float(pr)
    pk = {"acc": acc, "pay": pay, "prof": prof, "live": live, "lic": lic, "cat": cat, "plan": plan,
          "consumer": consumer, "licensed": licensed, "rival": rivalmap}
    _CACHE[target] = pk
    return pk


# ------------------------------------------------------------------ paying months

def paying_months(pk):
    """One row per consumer account and calendar month with a collected monthly charge, its plan and route."""
    p = pk["pay"]
    q = p[p["paying"]].copy()
    q = q.sort_values(["account_id", "m", "charged_on"]).drop_duplicates(["account_id", "m"], keep="last")
    return q[["account_id", "m", "plan_code", "route", "vat_rate", "amount_eur", "charged_on"]]


def r1(pk):
    pm = paying_months(pk)
    oc = pm[pm["m"] == P.CUT]
    return {pl: int((oc["plan_code"] == pl).sum()) for pl in P.PLANS}


# ------------------------------------------------------------------ counted hours

def counted(pk, o):
    """Counted hours by profile and month under the engine's rule: per profile and title, the rise in the furthest
    position any report shows, in the month of the report."""
    key = ("counted", o["channels"], o["basis"], o["dedup"], o["lic_month"])
    if key in pk:
        return pk[key]
    lv = pk["live"]
    if o["dedup"]:
        lv = lv.drop_duplicates()
    lv = lv[lv["title_id"].isin(pk["licensed"])]
    if o["basis"] == "seconds":
        out = lv.groupby(["profile_id", "m"], as_index=False)["seconds_streamed"].sum()
        out["hours"] = out["seconds_streamed"] / 3600.0
        out = out[["profile_id", "m", "hours"]]
        pk[key] = out
        return out
    parts = [lv[["profile_id", "title_id", "m", "furthest_position_s"]].rename(columns={"furthest_position_s": "pos"})]
    if "lic" in o["channels"]:
        lc = pk["lic"]
        lc = lc[lc["title_id"].isin(pk["licensed"])][["profile_id", "title_id", "m", "position_s"]].rename(
            columns={"position_s": "pos"})
        if o["lic_month"] == "next":
            lc = lc.assign(m=lc["m"] + 1)
        parts.append(lc)
    ev = pd.concat(parts, ignore_index=True)
    ev = ev.groupby(["profile_id", "title_id", "m"], as_index=False)["pos"].max()
    ev = ev.sort_values(["profile_id", "title_id", "m"])
    ev["run"] = ev.groupby(["profile_id", "title_id"])["pos"].cummax()
    ev["prev"] = ev.groupby(["profile_id", "title_id"])["run"].shift(1).fillna(0.0)
    ev["hours"] = (ev["run"] - ev["prev"]).clip(lower=0) / 3600.0
    out = ev.groupby(["profile_id", "m"], as_index=False)["hours"].sum()
    out = out[out["hours"] > 0]
    pk[key] = out
    return out


def membership(pk, mode):
    """(profile, month) -> account. Dated: the account whose charge that month lists the profile, else the nearest
    month that lists it (a trial month before the first charge), else the profile export; today: the export."""
    key = ("member", mode)
    if key in pk:
        return pk[key]
    today = dict(zip(pk["prof"]["profile_id"], pk["prof"]["account_id"]))
    if mode == "today":
        pk[key] = ("today", today)
        return pk[key]
    p = pk["pay"]
    q = p[p["profiles_on_subscription"].notna()][["account_id", "m", "profiles_on_subscription"]]
    q = q.assign(profile_id=q["profiles_on_subscription"].str.split(";")).explode("profile_id")
    q = q.drop_duplicates(["profile_id", "m"], keep="last")[["profile_id", "m", "account_id"]]
    pk[key] = ("dated", q.sort_values(["m"]), today)
    return pk[key]


def attribute(pk, o):
    """Counted hours by account and month."""
    key = ("attr", o["channels"], o["basis"], o["dedup"], o["lic_month"], o["member"], o.get("trial_fallback"))
    if key in pk:
        return pk[key]
    c = counted(pk, o)
    mem = membership(pk, o["member"])
    if mem[0] == "today":
        c = c.assign(account_id=c["profile_id"].map(mem[1]))
    else:
        q, today = mem[1], mem[2]
        exact = c.merge(q, on=["profile_id", "m"], how="left").reset_index(drop=True)
        miss = exact["account_id"].isna()
        if miss.any():
            rest = exact.loc[miss, ["profile_id", "m"]].copy()
            rest["row"] = rest.index
            rest = rest.sort_values("m")
            fw = pd.merge_asof(rest, q, on="m", by="profile_id", direction="forward")
            bw = pd.merge_asof(rest, q, on="m", by="profile_id", direction="backward")
            if o.get("trial_fallback") == "today":
                fill = fw["profile_id"].map(today).fillna(fw["account_id"]).fillna(bw["account_id"])
            else:
                fill = fw["account_id"].fillna(bw["account_id"])
                fill = fill.fillna(fw["profile_id"].map(today))
            exact.loc[fw["row"].values, "account_id"] = fill.values
        c = exact
    out = c.groupby(["account_id", "m"], as_index=False)["hours"].sum()
    pk[key] = out
    return out


def r2(pk, o):
    """Counted hours per paying subscription-month by plan, November 2025 to October 2026."""
    pm = paying_months(pk)
    pm = pm[pm["m"].isin(P.R2_MONTHS)]
    h = attribute(pk, o)
    j = pm.merge(h, on=["account_id", "m"], how="left").fillna({"hours": 0.0})
    g = j.groupby("plan_code")["hours"].agg(["sum", "count"])
    return {pl: float(g.loc[pl, "sum"] / g.loc[pl, "count"]) for pl in P.PLANS}


# ------------------------------------------------------------------ the spring 2024 trial starts

def cohort(pk):
    a = pk["acc"]
    c = a[a["signup_source"].str.startswith("VJ24-") & (a["account_type"] == "consumer")].copy()
    c["m0"] = c["created_on"].str[:7].map(midx)
    c = c[c["m0"].isin(P.SPRING24)]
    c["plan"] = c["signup_source"].str[5:]
    return c


def net27(pm):
    """Each paying month re-rated at the 2027 list price of the plan held, VAT by country, store fee by route and
    paid month (Apple 30 per cent in a subscription's first 12 paid months, 15 after; Google 15)."""
    pm = pm.sort_values(["account_id", "m"]).copy()
    pm["k"] = pm.groupby("account_id").cumcount() + 1
    price = pm["plan_code"].map(P.PRICE27)
    fee = np.where(pm["route"] == "apple", np.where(pm["k"] <= 12, 0.30, 0.15),
                   np.where(pm["route"] == "google", 0.15, 0.0))
    pm["net27"] = price / (1 + pm["vat_rate"]) * (1 - fee)
    pm["net_paid"] = pm["amount_eur"] / (1 + pm["vat_rate"]) * (1 - fee)
    return pm


def r4_r5(pk, o):
    c = cohort(pk)
    pm = paying_months(pk)
    allpm = net27(pm[pm["account_id"].isin(set(c["account_id"]))])
    allpm = allpm.merge(c[["account_id", "m0"]], on="account_id")
    win = allpm[(allpm["m"] >= allpm["m0"]) & (allpm["m"] < allpm["m0"] + P.HORIZON)]
    h = attribute(pk, o).merge(c[["account_id", "m0"]], on="account_id")
    h = h[(h["m"] >= h["m0"]) & (h["m"] < h["m0"] + P.HORIZON)]
    r4, r5, detail = {}, {}, {}
    for pl in P.PLANS:
        ids = set(c.loc[c["plan"] == pl, "account_id"])
        n = len(ids)
        w = win[win["account_id"].isin(ids)]
        conv = w["account_id"].nunique() / n
        months = len(w) / n
        rev = w["net27"].sum() / n
        hrs = h.loc[h["account_id"].isin(ids), "hours"].sum() / n
        if o["cost"] == "share26":
            cost = P.SHARE26 * w["net_paid"].sum() / n
        else:
            cost = P.RATE27 * hrs
        r4[pl] = {"trial starts": n, "share paying": conv, "paying months": months, "net revenue": rev}
        r5[pl] = rev - cost - P.FEE27[pl]
        detail[pl] = {"counted hours": hrs, "remuneration": cost, "fee": P.FEE27[pl]}
    return r4, r5, detail


# ------------------------------------------------------------------ the 2027 remuneration of the October base

def r6(pk, o):
    pm = paying_months(pk)
    base = pm[pm["m"] == P.CUT][["account_id", "plan_code"]]
    # tenure: paying months on file to October 2026
    ten = pm[pm["m"] <= P.CUT].groupby("account_id").size()
    base = base.assign(ten=base["account_id"].map(ten))
    band = lambda t: np.where(t <= 6, 0, np.where(t <= 18, 1, 2))
    # monthly continuation from one paying month to the next, November 2024 to October 2026
    pp = pm[["account_id", "m", "plan_code"]].copy()
    pp["ten"] = pp.groupby("account_id").cumcount() + 1
    nxt = set(zip(pp["account_id"], pp["m"] - 1))
    obs = pp[(pp["m"] >= P.CUT - 24) & (pp["m"] < P.CUT)].copy()
    obs["stay"] = [(a, m) in nxt for a, m in zip(obs["account_id"], obs["m"])]
    if o["r6_surv"] == "plan":
        obs["b"] = 0
    else:
        obs["b"] = band(obs["ten"].values)
    rate = obs.groupby(["plan_code", "b"])["stay"].mean().to_dict()
    # counted hours per paying month, by plan and calendar month, the twelve months to October 2026
    h = attribute(pk, o)
    pm12 = pm[pm["m"].isin(P.R2_MONTHS)].merge(h, on=["account_id", "m"], how="left").fillna({"hours": 0.0})
    pm12["cal"] = pm12["m"] % 12
    by = pm12.groupby(["plan_code", "cal"])["hours"].mean().to_dict()
    flat = pm12.groupby("plan_code")["hours"].mean().to_dict()
    own = pm12.groupby("account_id")["hours"].mean().to_dict()
    season = {k: by[k] / flat[k[0]] for k in by}
    total = 0.0
    for a, pl, t in zip(base["account_id"], base["plan_code"], base["ten"]):
        s = 1.0
        tt = t
        for m in range(P.CUT + 1, P.END + 1):
            b = 0 if o["r6_surv"] == "plan" else int(band(np.array([tt]))[0])
            s *= rate.get((pl, b), 0.95)
            tt += 1
            if m < 48:
                continue
            cal = m % 12
            if o["r6_hours"] == "flat":
                hh = flat[pl]
            elif o["r6_hours"] == "own":
                hh = own.get(a, flat[pl]) * season[(pl, cal)]
            else:
                hh = by[(pl, cal)]
            total += s * hh
    if o["cost"] == "share26":
        # the 2026 cost carried: the base's 2027 revenue at 52 per cent
        rev = 0.0
        for a, pl, t in zip(base["account_id"], base["plan_code"], base["ten"]):
            s, tt = 1.0, t
            for m in range(P.CUT + 1, P.END + 1):
                b = 0 if o["r6_surv"] == "plan" else int(band(np.array([tt]))[0])
                s *= rate.get((pl, b), 0.95)
                tt += 1
                if m >= 48:
                    rev += s * P.PRICE27[pl] / 1.082
        return P.SHARE26 * rev
    return P.RATE27 * total


def all_results(pk, o):
    R = {"R1": r1(pk), "R2": r2(pk, o)}
    R["R4"], R["R5"], R["detail"] = r4_r5(pk, o)
    R["R6"] = r6(pk, o)
    R["R7"] = max(R["R5"], key=R["R5"].get)
    return R


# ------------------------------------------------------------------ architecture 5: the January 2027 rises

LOWER = {"STD": "FLEX", "ONB": "STD", "GEZ": "ONB"}
RISE_EVENTS = [(2025, "BE", "STD"), (2025, "BE", "ONB"), (2025, "NL", "FLEX"), (2025, "NL", "GEZ"),
               (2026, "NL", "STD"), (2026, "NL", "ONB"), (2026, "BE", "FLEX"), (2026, "BE", "GEZ")]


def _country(pk):
    return dict(zip(pk["acc"]["account_id"], pk["acc"]["country"]))


def rival(pk):
    """The rival's comparable price by country and plan, as last scanned before each January."""
    r = pk.get("rival")
    return r


def response(pk, o):
    """Extra cancellations and extra downgrades per subscription at the first bill of a January rise, by event,
    against the same plan in the other country over the same months."""
    pm = paying_months(pk)
    cty = _country(pk)
    pm = pm.assign(country=pm["account_id"].map(cty))
    by = {(a, m): pl for a, m, pl in zip(pm["account_id"], pm["m"], pm["plan_code"])}
    rows = []
    for (y, c, pl) in RISE_EVENTS:
        dec = (y - P.M0_YEAR) * 12 - 1
        base = pm[(pm["m"] == dec) & (pm["plan_code"] == pl)]
        out = {}
        for grp, sel in (("rise", base["country"] == c), ("other", base["country"] != c)):
            ids = base.loc[sel, "account_id"]
            n = len(ids)
            left = sum(1 for a in ids if (a, dec + 1) not in by and (a, dec + 2) not in by)
            down = sum(1 for a in ids if LOWER.get(pl) and by.get((a, dec + 1)) == LOWER.get(pl))
            out[grp] = (n, left / n, down / n)
        rv = pk["rival"][(y, c, pl)]
        old, new = P.PRICE0[pl], P.PRICE[pl]
        rows.append({"year": y, "country": c, "plan": pl, "n": out["rise"][0], "pct": (new - old) / old,
                     "cross": old <= rv < new, "x_cancel": out["rise"][1] - out["other"][1],
                     "x_down": out["rise"][2] - out["other"][2]})
    return rows


def rise_effect(rows, pl, cross, o):
    """The 2027 extra cancellation and downgrade rates for a plan whose new price crosses the rival's or not."""
    if o.get("resp") == "pooled":
        sel = rows
    elif o.get("resp") == "plan":
        sel = [r for r in rows if r["plan"] == pl]
    else:
        sel = [r for r in rows if r["cross"] == cross]
    wc = sum(r["n"] * r["x_cancel"] for r in sel) / sum(r["n"] for r in sel)
    wd = sum(r["n"] * r["x_down"] for r in sel) / sum(r["n"] for r in sel)
    if o.get("resp") != "plan" and pl == "FLEX":
        wd = 0.0
    return max(wc, 0.0), max(wd, 0.0)


def downgrader_value(pk, o, pl):
    """What a subscription that moved down a plan at a past rise brought over the next twelve months, at the
    lower plan's 2027 price and the cost basis: realised paying months and counted hours."""
    lo = LOWER[pl]
    pm = net27(paying_months(pk))
    h = attribute(pk, o)
    hv = {(a, m): x for a, m, x in zip(h["account_id"], h["m"], h["hours"])}
    by = {(a, m): pl_ for a, m, pl_ in zip(pm["account_id"], pm["m"], pm["plan_code"])}
    vals = []
    for y in (2025, 2026):
        dec = (y - P.M0_YEAR) * 12 - 1
        ids = [a for (a, m), p in by.items() if m == dec and p == pl and by.get((a, dec + 1)) == lo]
        for a in ids:
            v = 0.0
            for m in range(dec + 1, dec + 13):
                if (a, m) in by:
                    net = P.PRICE27[by[(a, m)]] / 1.08
                    cost = P.SHARE26 * net if o["cost"] == "share26" else P.RATE27 * hv.get((a, m), 0.0)
                    v += net - cost
            vals.append(v)
    return float(np.mean(vals)) if vals else 0.0


def r5_rises(pk, o):
    """Each plan's change in its October 2026 base's 2027 contribution (EUR per subscription) if its January
    2027 rise goes ahead, against holding the 2026 price; the plans to raise are those that gain."""
    rows = response(pk, o)
    pm = paying_months(pk)
    cty = _country(pk)
    base = pm[pm["m"] == P.CUT].assign(country=lambda d: d["account_id"].map(cty))
    h = attribute(pk, o)
    pm12 = pm[pm["m"].isin(P.R2_MONTHS)].merge(h, on=["account_id", "m"], how="left").fillna({"hours": 0.0})
    hours = pm12.groupby("plan_code")["hours"].mean().to_dict()
    # monthly continuation by plan over the latest two years
    keys = set(zip(pm["account_id"], pm["m"]))
    obs = pm[(pm["m"] >= P.CUT - 24) & (pm["m"] < P.CUT)]
    stay = obs.assign(s=[(a, m + 1) in keys for a, m in zip(obs["account_id"], obs["m"])]).groupby("plan_code")["s"].mean()
    out, detail = {}, {}
    for pl in P.PLANS:
        s = stay[pl]
        surv = [s ** k for k in range(3, 15)]           # paying in Jan to Dec 2027 from October 2026
        S = sum(surv)
        net26, net27 = P.PRICE[pl] / 1.08, P.PRICE27[pl] / 1.08
        cost = (P.SHARE26 * net26) if o["cost"] == "share26" else P.RATE27 * hours[pl]
        cost27 = (P.SHARE26 * net27) if o["cost"] == "share26" else cost
        keep_value = S * (net26 - cost)              # a subscription kept on the plan through 2027, price held
        gain = S * ((net27 - cost27) - (net26 - cost))
        dval = downgrader_value(pk, o, pl) if (pl in LOWER and o.get("down", True)) else 0.0
        tot, xs = 0.0, {}
        for c in ("NL", "BE"):
            n = int((base[base["plan_code"] == pl]["country"] == c).sum())
            cross = P.PRICE[pl] <= pk["rival"][(2027, c, pl)] < P.PRICE27[pl]
            xc, xd = rise_effect(rows, pl, cross, o)
            if not o.get("down", True):
                xd = 0.0
            d = (1 - xc - xd) * gain - xc * keep_value - xd * (keep_value - dval)
            tot += n * d
            xs[c] = {"cross": cross, "extra_cancel": xc, "extra_down": xd, "n": n}
        nb = sum(v["n"] for v in xs.values())
        out[pl] = tot / nb
        detail[pl] = xs
    return out, detail, rows
