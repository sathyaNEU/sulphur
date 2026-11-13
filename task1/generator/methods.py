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
  the rest are architecture 5's judgments, each named where it is read (forecast() and the functions it calls)
"""
import os

import numpy as np
import pandas as pd

import params as P
import pack as PK

GOLD = {"channels": ("live", "lic"), "basis": "position", "member": "dated", "cost": "rate27", "dedup": True,
        "lic_month": "renewal",
        # architecture 5
        "resp": "model", "window": "first", "control": "other", "announce": True, "who": "band", "ret": "band",
        "sal": "within", "surv": "plan_tenure_band", "dval": "realised", "down": True}


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




# ------------------------------------------------------------------ architecture 5: the January 2027 rises

LOWER = {"STD": "FLEX", "ONB": "STD", "GEZ": "ONB"}
RISE_EVENTS = [(2025, "BE", "STD"), (2025, "BE", "ONB"), (2025, "NL", "FLEX"), (2025, "NL", "GEZ"),
               (2026, "NL", "STD"), (2026, "NL", "ONB"), (2026, "BE", "FLEX"), (2026, "BE", "GEZ")]
BANDS = (3.0, 8.0, 20.0)       # counted hours per paying month: under 3, 3 to 8, 8 to 20, 20 and more
NB = len(BANDS) + 1
TEN = (6, 18)                  # paying months on file: 6 or fewer, 7 to 18, more
KMAX = 30                      # months after a lapse the return model reaches


def _country(pk):
    return dict(zip(pk["acc"]["account_id"], pk["acc"]["country"]))


def lband(h):
    return int(np.searchsorted(BANDS, h, side="right"))


def tband(t):
    return 0 if t <= TEN[0] else 1 if t <= TEN[1] else 2


def _kg(k):
    return k if k <= 12 else 13 if k <= 18 else 14 if k <= 24 else 15


def _hkey(o):
    return (o["channels"], o["basis"], o["dedup"], o["lic_month"], o["member"])


def panel(pk, o):
    """The paying months {(account, month): plan}, the accounts on each plan in each month, each account's counted
    hours {(account, month): hours} and its paying months in order."""
    key = ("panel",) + _hkey(o)
    if key in pk:
        return pk[key]
    pm = paying_months(pk)
    by = dict(zip(zip(pm["account_id"], pm["m"]), pm["plan_code"]))
    on, months = {}, {}
    for a, m, pl in zip(pm["account_id"], pm["m"], pm["plan_code"]):
        on.setdefault((m, pl), []).append(a)
        months.setdefault(a, []).append(m)
    for a in months:
        months[a].sort()
    h = attribute(pk, o)
    hv = dict(zip(zip(h["account_id"], h["m"]), h["hours"]))
    pk[key] = (by, on, hv, months)
    return pk[key]


def _pre(hv, a, m, n=3):
    return sum(hv.get((a, k), 0.0) for k in range(m - n + 1, m + 1)) / n


def _rates(ids, ok, bands):
    n = len(ids)
    nb, kb = [0] * NB, [0] * NB
    k = 0
    for a, b in zip(ids, bands):
        hit = ok(a)
        nb[b] += 1
        kb[b] += hit
        k += hit
    return n, (k / n if n else 0.0), nb, kb


def _diff(kb1, nb1, kb2, nb2):
    return [kb1[b] / nb1[b] - kb2[b] / nb2[b] if nb1[b] and nb2[b] else 0.0 for b in range(NB)]


def profiles_per_charge(pk):
    """{(account, month): the number of profiles the month's collected charge lists}."""
    if "nprof" in pk:
        return pk["nprof"]
    p = pk["pay"]
    q = p[p["paying"]].sort_values(["account_id", "m", "charged_on"]).drop_duplicates(["account_id", "m"], keep="last")
    n = q["profiles_on_subscription"].fillna("").str.split(";").map(lambda x: len([y for y in x if y]))
    pk["nprof"] = dict(zip(zip(q["account_id"], q["m"]), n))
    return pk["nprof"]


def first_bill_model(rows, o):
    """The first bill's extra response per listening band, pooled over the past rises in proportion to the rise in
    per cent (or the log of the price ratio, 'log'): where the new price stayed on its side of the rival's, the extra
    cancellations per band and per unit of the rise, and the extra downgrades per band among the subscriptions whose
    profiles fit the plan below; where it passed the rival's, the extra cancellations beyond that, per band."""
    dose = (lambda r: np.log(1 + r["pct"])) if o.get("dose") == "log" else (lambda r: r["pct"])
    nc = [r for r in rows if not r["cross"]]
    num_c, den_c, num_d, den_d = np.zeros(NB), np.zeros(NB), np.zeros(NB), np.zeros(NB)
    for r in nc:
        w = np.array(r["nb"], float)
        num_c += w * np.array(r["xb_cancel"])
        den_c += w * dose(r)
        if r["plan"] in LOWER:
            wf = np.array(r["nb_fit"], float)
            num_d += wf * np.array(r["xb_down_fit"])
            den_d += wf * dose(r)
    kc = num_c / np.maximum(den_c, 1e-9)
    kd = num_d / np.maximum(den_d, 1e-9)
    num_s, den_s = np.zeros(NB), np.zeros(NB)
    for r in rows:
        if r["cross"]:
            w = np.array(r["nb"], float)
            num_s += w * (np.array(r["xb_cancel"]) - kc * dose(r))
            den_s += w
    ks = num_s / np.maximum(den_s, 1e-9)
    # a band no event holds borrows its neighbour's rate
    for v in (kc, kd, ks):
        for b in range(NB):
            if not np.isfinite(v[b]):
                v[b] = 0.0
    return kc, kd, ks, dose


def response(pk, o):
    """Each past rise's extra cancellations and extra downgrades per subscription at its first bill at the higher
    price (January; or the January and February bills), against the same plan in the other country over the same
    months (or the same country a year before), overall and by listening band (the account's counted hours per paying
    month over the October to December before), and whether the new price passed the rival's comparable plan as
    scanned in the December before."""
    key = ("resp",) + _hkey(o) + (o.get("window", "first"), o.get("control", "other"))
    if key in pk:
        return pk[key]
    by, on, hv, months = panel(pk, o)
    cty = _country(pk)
    nprof = profiles_per_charge(pk)
    rows = []
    for (y, c, pl) in RISE_EVENTS:
        dec = (y - P.M0_YEAR) * 12 - 1
        out = {}
        for grp in ("rise", "other"):
            prior = [a for a in on.get((dec - 12, pl), []) if cty[a] == c] if dec - 12 >= P.REC0 + 2 else []
            if grp == "other" and o.get("control") == "prior" and prior:
                d0 = dec - 12
                ids = prior
            else:
                d0 = dec
                ids = [a for a in on.get((dec, pl), []) if (cty[a] == c) == (grp == "rise")]
            bands = [lband(_pre(hv, a, d0)) for a in ids]
            lo = LOWER.get(pl)
            fits = [lo is not None and nprof.get((a, d0), 1) <= P.MAX_PROFILES[lo] for a in ids]
            if o.get("window") == "two":
                left = lambda a, d0=d0: (a, d0 + 1) not in by and (a, d0 + 2) not in by
            else:
                left = lambda a, d0=d0: (a, d0 + 1) not in by
            down = lambda a, d0=d0: lo is not None and by.get((a, d0 + 1)) == lo
            el = [a for a, f in zip(ids, fits) if f]
            out[grp] = (_rates(ids, left, bands), _rates(ids, down, bands),
                        _rates(el, down, [b for b, f in zip(bands, fits) if f]))
        rv = pk["rival"][(y, c, pl)]
        (n1, c1, nb1, kb1), (_, d1, _, db1), (ne1, _, eb1, eh1) = out["rise"]
        (n2, c2, nb2, kb2), (_, d2, _, db2), (ne2, _, eb2, eh2) = out["other"]
        rows.append({"year": y, "country": c, "plan": pl, "n": n1, "pct": (P.PRICE[pl] - P.PRICE0[pl]) / P.PRICE0[pl],
                     "cross": P.PRICE0[pl] <= rv < P.PRICE[pl], "x_cancel": c1 - c2, "x_down": d1 - d2, "nb": nb1,
                     "xb_cancel": _diff(kb1, nb1, kb2, nb2), "xb_down": _diff(db1, nb1, db2, nb2),
                     "nb_fit": eb1, "xb_down_fit": _diff(eh1, eb1, eh2, eb2), "n_fit": ne1})
    pk[key] = rows
    return rows


def announce(pk, o):
    """Each past rise's extra leaving at the December bill after the price e-mail of 1 December: of the subscriptions
    paying on the plan in November, those not paying in December, against the same plan in the other country,
    overall and by listening band (September to November)."""
    key = ("ann",) + _hkey(o)
    if key in pk:
        return pk[key]
    by, on, hv, months = panel(pk, o)
    cty = _country(pk)
    rows = []
    for (y, c, pl) in RISE_EVENTS:
        dec = (y - P.M0_YEAR) * 12 - 1
        res = {}
        for grp in ("rise", "other"):
            ids = [a for a in on.get((dec - 1, pl), []) if (cty[a] == c) == (grp == "rise")]
            res[grp] = _rates(ids, lambda a: (a, dec) not in by, [lband(_pre(hv, a, dec - 1)) for a in ids])
        (n1, r1, nb1, kb1), (n2, r2, nb2, kb2) = res["rise"], res["other"]
        rows.append({"year": y, "country": c, "plan": pl, "n": n1, "x_announce": r1 - r2, "nb": nb1,
                     "xb": _diff(kb1, nb1, kb2, nb2)})
    pk[key] = rows
    return rows


def gradient(rows, key, sel):
    """The pooled profile of an extra response across listening bands: each band's extra rate over the events
    selected, weighted by the band's subscriptions, against the events' overall extra rate."""
    num, den = np.zeros(NB), np.zeros(NB)
    for r in rows:
        if sel(r):
            num += np.array(r["nb"], float) * np.array(r[key])
            den += np.array(r["nb"], float)
    tot = num.sum() / max(den.sum(), 1.0)
    if tot <= 1e-9:
        return np.ones(NB)
    return np.clip((num / np.maximum(den, 1.0)) / tot, 0.0, None)


def lapses(pk, o):
    """Every stop in a consumer subscription's payments before November 2026: the first month unpaid, the listening
    band before it (counted hours per paying month over the last three paying months), whether that month's debit
    came back unpaid, and the month it paid again if it did. A refund ends a subscription for good and is left out."""
    key = ("lapses",) + _hkey(o)
    if key in pk:
        return pk[key]
    by, on, hv, months = panel(pk, o)
    p = pk["pay"]
    q = p[p["consumer"]]
    st = lambda s: set(zip(q.loc[q["status"] == s, "account_id"], q.loc[q["status"] == s, "m"]))
    failed = st("returned") - st("re-presented")
    refunded = st("refunded")
    rows = []
    for a, ms in months.items():
        for i, m in enumerate(ms):
            nxt = ms[i + 1] if i + 1 < len(ms) else None
            if nxt == m + 1 or m >= P.CUT:
                continue
            first = m + 1
            if (a, first) in refunded:
                continue
            last = ms[max(0, i - 2):i + 1]
            h = sum(hv.get((a, k), 0.0) for k in last) / len(last)
            rows.append((a, first, nxt, lband(h), "failed" if (a, first) in failed else "cancelled", by[(a, m)]))
    pk[key] = rows
    return rows


def return_hazard(pk, o):
    """The monthly chance that a lapsed subscription pays again, from every lapse to October 2026, each at risk
    until it paid again or the records end: for a cancelled subscription a log-linear model in the listening band (or
    none, 'pooled'), the months since the lapse (each of the first twelve, then groups to 30) and the calendar month,
    fitted by iterative proportional fitting (the Poisson maximum likelihood for those margins); for a returned debit
    the months since the lapse alone. Returns (h[band, k, cal], h_failed[k])."""
    key = ("rethaz",) + _hkey(o) + (o.get("ret", "band"),)
    if key in pk:
        return pk[key]
    pooled = o.get("ret") == "pooled"
    ret = np.zeros((NB, 16, 12))
    risk = np.zeros((NB, 16, 12))
    fr, fk = np.zeros(KMAX + 1), np.zeros(KMAX + 1)
    for (a, first, back, b, why, pl) in lapses(pk, o):
        kb = back - first if back is not None else None
        for k in range(1, min(P.CUT - first, KMAX) + 1):
            if kb is not None and k > kb:
                break
            hit = 1.0 if kb == k else 0.0
            if why == "failed":
                fr[k] += hit
                fk[k] += 1
            else:
                bb = 0 if pooled else b
                g, cal = _kg(k), (first + k) % 12
                ret[bb, g, cal] += hit
                risk[bb, g, cal] += 1
    nb = 1 if pooled else NB
    A, B, C = np.ones(nb), np.ones(16), np.ones(12)
    R, X = ret[:nb], risk[:nb]
    for _ in range(200):
        A = R.sum((1, 2)) / np.maximum((X * B[None, :, None] * C[None, None, :]).sum((1, 2)), 1e-12)
        B = np.where(X.sum((0, 2)) > 0, R.sum((0, 2)) / np.maximum((X * A[:, None, None] * C[None, None, :]).sum((0, 2)),
                                                                   1e-12), 0.0)
        C = R.sum((0, 1)) / np.maximum((X * A[:, None, None] * B[None, :, None]).sum((0, 1)), 1e-12)
    h = A[:, None, None] * B[None, :, None] * C[None, None, :]
    if pooled:
        h = np.repeat(h, NB, axis=0)
    hk = np.zeros((NB, KMAX + 1, 12))
    for k in range(1, KMAX + 1):
        hk[:, k, :] = h[:, _kg(k), :]
    hf = np.where(fk > 0, fr / np.maximum(fk, 1), 0.0)
    pk[key] = (np.clip(hk, 0.0, 1.0), np.clip(hf, 0.0, 1.0))
    return pk[key]


def continuation(pk, o):
    """Each month's chance that a paying subscription pays the next month, November 2024 to October 2026: by plan,
    paying months on file and listening band (the three months to the month; 'plan_tenure': by plan and paying months
    alone), leaving out the months a past rise reached the plan in its country (the November before to the February
    after) and each subscription's first three months back after a lapse, which carry their own chance by plan."""
    key = ("cont",) + _hkey(o) + (o.get("surv", "plan_tenure_band"),)
    if key in pk:
        return pk[key]
    by, on, hv, months = panel(pk, o)
    cty = _country(pk)
    rm = {}
    for (y, c, pl) in RISE_EVENTS:
        j = (y - P.M0_YEAR) * 12
        rm.setdefault((c, pl), set()).update(range(j - 2, j + 2))
    back = {}
    for (a, first, nxt, b, why, pl) in lapses(pk, o):
        if nxt is not None:
            for k in range(3):
                back[(a, nxt + k)] = 1
    lb_on = o.get("surv", "plan_tenure_band") == "plan_tenure_band"
    cnt = {}
    cntr = {}
    for a, ms in months.items():
        for i, m in enumerate(ms):
            if not (P.CUT - 24 <= m < P.CUT):
                continue
            pl = by[(a, m)]
            if m in rm.get((cty[a], pl), ()):
                continue
            stay = (a, m + 1) in by
            if (a, m) in back:
                s = cntr.setdefault(pl, [0, 0])
            else:
                kk = (pl, tband(i + 1), lband(_pre(hv, a, m)) if lb_on else 0)
                s = cnt.setdefault(kk, [0, 0])
            s[0] += stay
            s[1] += 1
    rate = {k: v[0] / v[1] for k, v in cnt.items()}
    rr = {pl: v[0] / v[1] for pl, v in cntr.items()}
    pk[key] = (rate, rr)
    return pk[key]


def salience(pk, o):
    """How much more the subscriptions that stayed on the plan listened after each past rise, by months since its
    first bill (1 is January), as a share of what they would have listened: the hours of the accounts paying on the
    plan in December and in every month to that one, against their own October to December hours, the rise country's ratio over
    the other country's (which carries the season and the fade with tenure) ('within'); or every subscription paying
    on the plan in the month against all those paying in October to December ('average'). Per plan the mean of its
    rises; a fade fitted across the plans (a plan's level, one common rate). Returns ({plan: [r_1 .. r_12]},
    {plan: [(k, r, n)]}, tau)."""
    key = ("sal",) + _hkey(o) + (o.get("sal", "within"), o.get("sal_fit", "common"))
    if key in pk:
        return pk[key]
    by, on, hv, months = panel(pk, o)
    cty = _country(pk)
    per = {pl: {} for pl in P.PLANS}
    for (y, c, pl) in RISE_EVENTS:
        dec = (y - P.M0_YEAR) * 12 - 1
        K = 11 if y == 2025 else P.CUT - dec
        base = {}
        for grp in ("rise", "other"):
            ids = [a for a in on.get((dec, pl), []) if (cty[a] == c) == (grp == "rise")]
            base[grp] = {a: _pre(hv, a, dec) for a in ids}
        for k in range(1, K + 1):
            d = {}
            for grp in ("rise", "other"):
                inside = lambda a: (cty[a] == c) == (grp == "rise")
                if o.get("sal") == "average":
                    now = [a for a in on.get((dec + k, pl), []) if inside(a)]
                    bef = [(a, mm) for mm in (dec - 2, dec - 1, dec) for a in on.get((mm, pl), []) if inside(a)]
                    d[grp] = ((sum(hv.get((a, dec + k), 0.0) for a in now) / max(len(now), 1))
                              / max(sum(hv.get(x, 0.0) for x in bef) / max(len(bef), 1), 1e-9))
                else:
                    ids = [a for a in base[grp] if all(by.get((a, dec + j)) == pl for j in range(1, k + 1))]
                    d[grp] = (sum(hv.get((a, dec + k), 0.0) for a in ids)
                              / max(sum(base[grp][a] for a in ids), 1e-9))
            per[pl].setdefault(k, []).append((d["rise"] / d["other"] - 1.0, len(base["rise"])))
    obs = {pl: [(k, sum(u * n for u, n in v) / sum(n for u, n in v), sum(n for u, n in v)) for k, v in sorted(d.items())]
           for pl, d in per.items()}
    best = None
    for tau in np.arange(0.5, 12.01, 0.1):
        sse, amp = 0.0, {}
        for pl, ob in obs.items():
            e = np.array([np.exp(-(k - 1) / tau) for k, u, n in ob])
            u = np.array([u for k, u, n in ob])
            w = np.array([n for k, u, n in ob], float)
            amp[pl] = float((w * u * e).sum() / (w * e * e).sum())
            sse += float((w * (u - amp[pl] * e) ** 2).sum())
        if best is None or sse < best[0]:
            best = (sse, tau, amp)
    _, tau, amp = best
    taus = {pl: tau for pl in P.PLANS}
    if o.get("sal_fit") == "per_plan":
        # each plan its own fade rate as well as its own level
        for pl, ob in obs.items():
            e_best = None
            for tp in np.arange(0.5, 12.01, 0.1):
                e = np.array([np.exp(-(k - 1) / tp) for k, u, n in ob])
                u = np.array([u for k, u, n in ob])
                w = np.array([n for k, u, n in ob], float)
                a_ = float((w * u * e).sum() / (w * e * e).sum())
                sse = float((w * (u - a_ * e) ** 2).sum())
                if e_best is None or sse < e_best[0]:
                    e_best = (sse, float(tp), a_)
            taus[pl], amp[pl] = e_best[1], e_best[2]
    if o.get("sal") == "none":
        path = {pl: [0.0] * 12 for pl in P.PLANS}
    elif o.get("sal_fit") == "observed":
        # the months the past rises observed, as read, and the fitted fade beyond them
        path = {}
        for pl in P.PLANS:
            seen = {k: u for k, u, n in obs[pl]}
            path[pl] = [seen[k] if k in seen else amp[pl] * float(np.exp(-(k - 1) / taus[pl])) for k in range(1, 13)]
    elif o.get("sal") == "persist":
        path = {pl: [float(np.mean([amp[pl] * np.exp(-(k - 1) / taus[pl]) for k in range(1, 7)]))] * 12 for pl in P.PLANS}
    else:
        path = {pl: [amp[pl] * float(np.exp(-(k - 1) / taus[pl])) for k in range(1, 13)] for pl in P.PLANS}
    pk[key] = (path, obs, float(tau))
    return pk[key]


def season(pk, o):
    """Each plan's counted hours per paying month by calendar month over the twelve months to October 2026, against
    the plan's twelve-month mean; and each October 2026 subscription's own counted hours per paying month there."""
    key = ("seas",) + _hkey(o)
    if key in pk:
        return pk[key]
    pm = paying_months(pk)
    h = attribute(pk, o)
    j = pm[pm["m"].isin(P.R2_MONTHS)].merge(h, on=["account_id", "m"], how="left").fillna({"hours": 0.0})
    j["cal"] = j["m"] % 12
    flat = j.groupby("plan_code")["hours"].mean().to_dict()
    by = j.groupby(["plan_code", "cal"])["hours"].mean().to_dict()
    s = {(pl, c): by[(pl, c)] / flat[pl] for (pl, c) in by}
    own = j.groupby("account_id")["hours"].mean().to_dict()
    pk[key] = (s, own)
    return pk[key]


def downgrader_path(pk, o, pl):
    """What a subscription that moved down a plan at a past rise brought over its next twelve months: its paying
    months on the lower plan (or any) re-rated at the 2027 price of the plan paid and the cost basis on its own counted
    hours, and the share still paying in the twelfth month; the mean over the 2025 and 2026 rises."""
    key = ("dpath", pl) + _hkey(o) + (o["cost"],)
    if key in pk:
        return pk[key]
    by, on, hv, months = panel(pk, o)
    lo = LOWER[pl]
    vals, last, rem = [], [], []
    for y in (2025, 2026):
        dec = (y - P.M0_YEAR) * 12 - 1
        for a in on.get((dec, pl), []):
            if by.get((a, dec + 1)) != lo:
                continue
            v = r_ = 0.0
            for k in range(dec + 1, dec + 13):
                if (a, k) in by:
                    net = P.PRICE27[by[(a, k)]] / 1.08
                    c_ = P.SHARE26 * net if o["cost"] == "share26" else P.RATE27 * hv.get((a, k), 0.0)
                    v += net - c_
                    r_ += c_
            vals.append(v)
            rem.append(r_)
            last.append((a, dec + 12) in by)
    out = (float(np.mean(vals)) if vals else 0.0, float(np.mean(last)) if last else 0.0, len(vals),
           float(np.mean(rem)) if rem else 0.0)
    pk[key] = out
    return out


def _resp_rate(rows, pl, cross, c, kind, o):
    """A 2027 rise's extra cancellation and downgrade rates for a plan in a country, read off the past rises:
    'kind' the plan's own rises of the same kind (passing the rival's price or not), 'region' the plan's own rise in
    that country, 'plan' the plan's two rises together, 'pooled' all eight, 'plan_step' each plan's level and one step
    where a rise passes the rival fitted on the eight; and the events it is read from."""
    if kind == "plan_step":
        w = np.array([r["n"] for r in rows], float)
        X = np.column_stack([[1.0 if r["plan"] == q else 0.0 for r in rows] for q in P.PLANS] +
                            [[1.0 if r["cross"] else 0.0 for r in rows]])
        x0 = np.array([1.0 if q == pl else 0.0 for q in P.PLANS] + [1.0 if cross else 0.0])
        out = []
        for k in ("x_cancel", "x_down"):
            yv = np.array([r[k] for r in rows])
            keep = np.array([k == "x_cancel" or r["plan"] != "FLEX" for r in rows])
            b = np.linalg.lstsq((X * np.sqrt(w)[:, None])[keep], (yv * np.sqrt(w))[keep], rcond=None)[0]
            out.append(float(x0 @ b))
        ev = [r for r in rows if r["plan"] == pl and r["cross"] == cross] or [r for r in rows if r["plan"] == pl]
        return out[0], out[1], ev
    if kind == "region":
        ev = [r for r in rows if r["plan"] == pl and r["country"] == c]
    elif kind == "plan":
        ev = [r for r in rows if r["plan"] == pl]
    elif kind == "pooled":
        ev = list(rows)
    else:
        ev = [r for r in rows if r["plan"] == pl and r["cross"] == cross] or [r for r in rows if r["cross"] == cross]
    n = sum(r["n"] for r in ev)
    return sum(r["n"] * r["x_cancel"] for r in ev) / n, sum(r["n"] * r["x_down"] for r in ev) / n, ev


def forecast(pk, o):
    """Each plan's subscriptions paying at 31 October 2026, carried month by month from November 2026 to December 2027
    with the plan's January 2027 rise and with its 2026 price held (the other plans at the price list's 2027 prices),
    each on its own paying months, listening, country and billing route:
      - each month it pays on, or stops, at its plan's continuation for its paying months and listening band;
      - with the rise, the light listeners' extra leaving at the December bill after the 1 December e-mail (the plan's
        own two rises), then the extra cancellations and downgrades at the January bill (the plan's own rise of the
        same kind: passing the rival's price as last scanned or not), each spread over the listening bands by the
        past rises' pooled profile;
      - a stopped subscription pays again at the return model's chance for its band, months since and calendar month,
        at the price then in force, and stops more often in its first three months back;
      - a subscription that moves down pays the lower plan, valued on the past downgraders' own twelve months;
      - the subscriptions that stay through the January bill use the stayers' extra counted hours of the past rises;
      - each paying month brings its price net of VAT and the store's fee, less EUR 0.40 for each counted hour (its
        own hours per paying month, by the plan's calendar months), or 48 per cent of net revenue on the 2026 basis.
    Returns per plan the change in the October subscriptions' 2027 contribution per subscription, how many of them
    pay on any plan in December 2027 with the rise, the January rates per 100 reaching the bill by country, how many of
    every 100 the rise loses are paying again in December 2027, and the stayers' extra counted hours over 2027."""
    by, on, hv, months = panel(pk, o)
    cty = _country(pk)
    rows = response(pk, o)
    ann = announce(pk, o)
    rate, rr = continuation(pk, o)
    path, obs, tau = salience(pk, dict(o, sal=o.get("sal", "within") if o.get("sal") != "none" else "within"))
    if o.get("sal") == "none":
        path = {pl: [0.0] * 12 for pl in P.PLANS}
    seas, own = season(pk, o)
    haz, hfail = return_hazard(pk, o) if o.get("ret", "band") != "none" else (None, None)
    if haz is not None and o.get("scale_ret", 1.0) != 1.0:
        haz = np.clip(haz * o["scale_ret"], 0.0, 1.0)
    pm = paying_months(pk)
    last_route = pm.sort_values("m").drop_duplicates("account_id", keep="last").set_index("account_id")["route"].to_dict()
    nfile = {a: len(ms) for a, ms in months.items()}
    who = o.get("who", "band") == "band"
    g_ann = gradient(ann, "xb", lambda r: True) if who else np.ones(NB)
    g_cn = gradient(rows, "xb_cancel", lambda r: not r["cross"]) if who else np.ones(NB)
    g_cx = gradient(rows, "xb_cancel", lambda r: r["cross"]) if who else np.ones(NB)
    g_dn = gradient(rows, "xb_down", lambda r: r["plan"] in LOWER and not r["cross"]) if who else np.ones(NB)
    g_dx = gradient(rows, "xb_down", lambda r: r["plan"] in LOWER and r["cross"]) if who else np.ones(NB)
    share = o["cost"] == "share26"
    nprof = profiles_per_charge(pk)
    kc, kd, ks, _ = first_bill_model(rows, o)
    out = {}
    for pl in P.PLANS:
        ids_all = [a for a in on.get((P.CUT, pl), [])]
        xa_pl = float(np.mean([r["x_announce"] for r in ann if r["plan"] == pl])) * o.get("scale_announce", 1.0)
        if not o.get("announce", True):
            xa_pl = 0.0
        dval, dlast, _, drem = downgrader_path(pk, o, pl) if pl in LOWER else (0.0, 0.0, 0, 0.0)
        tot_change, end27, n_all = 0.0, 0.0, 0
        cells, xleft, xback, sal_h = {}, 0.0, 0.0, 0.0
        sal_acc = [0.0, 0.0]
        rem_acc = [0.0]
        for c in ("NL", "BE"):
            ids = [a for a in ids_all if cty[a] == c]
            n = len(ids)
            if not n:
                continue
            lb = np.array([lband(_pre(hv, a, P.CUT)) for a in ids])
            h_own = np.array([own.get(a, 0.0) for a in ids])
            t0 = np.array([nfile[a] for a in ids])
            rt = [last_route.get(a, "web") for a in ids]
            vat = P.VAT[c]
            cross27 = P.PRICE[pl] <= pk["rival"][(2027, c, pl)] < P.PRICE27[pl]
            fits = np.array([pl in LOWER and nprof.get((a, P.CUT), 1) <= P.MAX_PROFILES[LOWER[pl]] for a in ids])

            def spread(x, g):
                """Per-account rates with the plan's average x over the October base, spread by the band profile."""
                gi = g[lb]
                return np.clip(x * gi / max(gi.mean(), 1e-9), 0.0, 1.0)
            if o.get("resp", "model") == "model":
                d27 = np.log(P.PRICE27[pl] / P.PRICE[pl]) if o.get("dose") == "log" else (P.PRICE27[pl] - P.PRICE[pl]) / P.PRICE[pl]
                xc_i = np.clip(d27 * kc[lb] + (ks[lb] if cross27 else 0.0), 0.0, 1.0)
                xd_i = np.clip(np.where(fits, d27 * kd[lb], 0.0), 0.0, 1.0)
                ev = [r for r in rows if r["cross"] == cross27]
            else:
                xc, xd, ev = _resp_rate(rows, pl, cross27, c, o.get("resp"), o)
                if not o.get("noclip"):
                    xc, xd = max(xc, 0.0), max(xd, 0.0)
                xc_i, xd_i = spread(xc, g_cx if cross27 else g_cn), spread(xd, g_dx if cross27 else g_dn)
            xc_i = xc_i * o.get("scale_cancel", 1.0)
            xd_i = np.zeros(n) if (pl == "FLEX" or not o.get("down", True)) else xd_i * o.get("scale_down", 1.0)
            if o.get("down_as_exit"):
                xc_i, xd_i = xc_i + xd_i, np.zeros(n)
            xa_i = spread(xa_pl, g_ann)

            def run(rise):
                pay = np.ones(n)                 # paying, never stopped since October
                pr = np.zeros(n)                 # paying again, back for more than three months
                back = np.zeros((4, n))          # paying again, back 0 to 3 months (0: this month)
                lap = np.zeros((KMAX + 2, n))    # stopped, by months since
                xl = np.zeros((KMAX + 2, n))     # the rise's extra leavers, stopped
                xb = np.zeros((4, n))            # the rise's extra leavers, paying again
                xp = np.zeros(n)                 # ... back for more than three months
                down = np.zeros(n)
                stayers = np.zeros(n)
                contrib = np.zeros(n)
                reach = np.zeros(n)
                left_x = np.zeros(n)
                for k, m in enumerate(range(P.CUT + 1, P.END + 1), 1):
                    cal = m % 12
                    t = t0 + k - 1
                    q = np.array([1.0 - rate.get((pl, tband(ti), b if o.get("surv", "plan_tenure_band") ==
                                                  "plan_tenure_band" else 0), 0.95) for ti, b in zip(t, lb)])
                    qr = 1.0 - rr.get(pl, 0.95)
                    # stop or carry on (returned this month do not decide); with the rise, the e-mail's extra
                    # leavers at the December bill and the first bill's extra cancellations and downgrades in January,
                    # each a share of the subscriptions paying into the month, as the past rises were read
                    ex = np.zeros(n)
                    dn = np.zeros(n)
                    if rise and m == P.CUT + 2:
                        ex = xa_i
                    if rise and m == P.CUT + 3:
                        reach = pay + back[1:].sum(0)
                        ex, dn = xc_i, xd_i
                    f_pay = np.minimum(q + ex, 1.0 - dn)
                    f_back = np.minimum(qr + ex, 1.0 - dn)
                    l_pay, e_pay, d_pay = pay * q, pay * (f_pay - q), pay * dn
                    l_back, e_back, d_back = back[1:] * qr, back[1:] * (f_back - qr), back[1:] * dn
                    lx_back, lx_p = xb[1:] * qr, xp * q
                    l_pr = pr * q
                    pr = pr - l_pr
                    pay = pay - l_pay - e_pay - d_pay
                    back[1:] = back[1:] - l_back - e_back - d_back
                    xb[1:], xp = xb[1:] - lx_back, xp - lx_p
                    new_lap = l_pay + l_back.sum(0) + l_pr
                    new_xl = lx_back.sum(0) + lx_p + e_pay + e_back.sum(0)
                    left_x += e_pay + e_back.sum(0)
                    if rise and m == P.CUT + 3:
                        down = d_pay + d_back.sum(0)
                        stayers = pay + back[1:].sum(0)
                    # stopped subscriptions pay again
                    if haz is not None:
                        hk = haz[lb, :, cal]                       # (n, KMAX + 1)
                        r_lap = (lap[1:KMAX + 1] * hk[:, 1:].T).sum(0)
                        r_xl = (xl[1:KMAX + 1] * hk[:, 1:].T).sum(0)
                        lap[1:KMAX + 1] *= (1.0 - hk[:, 1:].T)
                        xl[1:KMAX + 1] *= (1.0 - hk[:, 1:].T)
                    else:
                        r_lap = r_xl = np.zeros(n)
                    back[0], xb[0] = r_lap, r_xl
                    # this month's contribution (2027 only)
                    if m >= P.Y2027[0]:
                        price = P.PRICE27[pl] if rise else P.PRICE[pl]
                        paying = pay + pr + back.sum(0) + xb.sum(0) + xp
                        fee = np.array([0.30 if (r_ == "apple" and t0_ + k <= 12) else (0.15 if r_ in ("apple", "google")
                                        else 0.0) for r_, t0_ in zip(rt, t0)])
                        net = price / (1 + vat) * (1 - fee)
                        cost = 0.52 * net if share else P.RATE27 * h_own * seas.get((pl, cal), 1.0)
                        contrib += paying * (net - cost)
                        if rise:
                            rem_acc[0] += float((paying * (0.52 * net if share else
                                                           P.RATE27 * h_own * seas.get((pl, cal), 1.0))).sum())
                        if rise and not share:
                            u = path[pl][m - P.Y2027[0]] * o.get("scale_sal", 1.0)
                            contrib -= stayers * P.RATE27 * u * h_own * seas.get((pl, cal), 1.0)
                            sal_acc[0] += float((stayers * u * h_own * seas.get((pl, cal), 1.0)).sum())
                            rem_acc[0] += float((stayers * P.RATE27 * u * h_own * seas.get((pl, cal), 1.0)).sum())
                            sal_acc[1] += float(stayers.sum())
                        if rise:
                            stayers *= (1.0 - q)
                    # move the clocks on
                    lap[2:KMAX + 2] = lap[1:KMAX + 1].copy()
                    lap[1] = new_lap
                    xl[2:KMAX + 2] = xl[1:KMAX + 1].copy()
                    xl[1] = new_xl
                    pr = pr + back[3]
                    back[1:4] = back[0:3].copy()
                    back[0] = 0.0
                    xp = xp + xb[3]
                    xb[1:4] = xb[0:3].copy()
                    xb[0] = 0.0
                end = pay + pr + back.sum(0) + xb.sum(0) + xp
                again = pr + back.sum(0) + xb.sum(0) + xp
                return contrib, end, reach, down, left_x, (again, 1.0 - pay - down)
            c_h, e_h, _, _, _, _ = run(False)
            c_r, e_r, reach, down, left_x, (again, stopped) = run(True)
            # the downgraders, valued on the past downgraders' own twelve months (or modelled: their own hours capped at
            # the lower plan's, on the lower plan's continuation for long-standing subscriptions)
            dv = down * dval
            if o.get("dval") == "model" and pl in LOWER:
                lo = LOWER[pl]
                cap = P.CAP[lo] or 1e9
                s_lo = rate.get((lo, 2, 1), rate.get((lo, 2, 0), 0.95))
                vals, surv = np.zeros(n), 1.0
                for m27 in P.Y2027:
                    net_lo = P.PRICE27[lo] / (1 + vat)
                    use = np.minimum(h_own * seas.get((pl, m27 % 12), 1.0), cap)
                    vals += surv * (net_lo - (0.52 * net_lo if share else P.RATE27 * use))
                    surv *= s_lo
                dv = down * vals
            rem_acc[0] += float((down * drem).sum())
            tot_change += float((c_r - c_h + dv).sum())
            end27 += float(e_r.sum() + (down * dlast).sum())
            n_all += n
            rc = float(reach.sum())
            cells[c] = {"cross": bool(cross27), "extra_cancel": float((reach * xc_i).sum() / rc),
                        "extra_down": float((reach * xd_i).sum() / rc), "n": n,
                        "events": ["%d %s" % (r["year"], r["country"]) for r in ev]}
            xleft += float(stopped.sum())
            xback += float(again.sum())
        sal_h = 12.0 * sal_acc[0] / sal_acc[1] if sal_acc[1] else 0.0      # per subscription staying all 2027
        out[pl] = {"change": tot_change / n_all, "end27": end27, "cells": cells, "n": n_all,
                   "back_share": (xback / xleft) if xleft else 0.0,     # of those that stop by December 2027, paying then
                   "sal_hours": sal_h, "xa": xa_pl, "remun": rem_acc[0] / n_all,
                   "tau": tau}
    return out
