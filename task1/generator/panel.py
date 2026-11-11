"""The analysis panel: one row per consumer subscription with its months, charges and reading, and the household
links the records support. from_world() builds it from the simulator's record (the prototype and the checks);
from_pack() builds the same panel from the cut files (the golden, the verifier and the effort passes)."""
import numpy as np

import params as P
import sim


def union_find(n_items, pairs):
    parent = list(range(n_items))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    return np.array([find(i) for i in range(n_items)])


def households(customer, fingerprint, address, use=("fingerprint", "address")):
    """Group subscriptions into households: one customer number is one household, and customer numbers sharing a
    payment fingerprint or an address are one household (use= picks the links). fingerprint and address hold one
    key or a tuple of keys per subscription."""
    n = len(customer)
    pairs = []
    keys = [[(k,) for k in customer]]
    if "fingerprint" in use:
        keys.append([k if isinstance(k, tuple) else (k,) for k in fingerprint])
    if "address" in use:
        keys.append([k if isinstance(k, tuple) else (k,) for k in address])
    for key in keys:
        first = {}
        for i, ks in enumerate(key):
            for k in ks:
                if k is None or k == "":
                    continue
                if k in first:
                    pairs.append((first[k], i))
                else:
                    first[k] = i
    return union_find(n, pairs)


def from_world(S):
    keep = np.ones(len(S["start"]), bool)
    pn = {k: S[k][keep] for k in ["start", "title", "channel", "offer", "route", "end", "reason", "L", "ip",
                                  "su_exit", "kind", "tenure0", "customer", "fingerprint", "address"]}
    # the record cannot tell a household's return from a new start: a return is a new subscription
    pn["kind"] = np.where(pn["kind"] == "return", "new", pn["kind"]).astype(object)
    pn["gross"] = S["gross"][keep]
    pn["reading"] = S["reading"][keep].astype(float)
    pn["household"] = households(pn["customer"], pn["fingerprint"], pn["address"])
    pn["hh_customer"] = households(pn["customer"], pn["fingerprint"], pn["address"], use=())
    pn["truth_household"] = S["household"][keep]
    pn["n"] = int(keep.sum())
    return finish(pn)


def finish(pn, months=3, adjust=False):
    """Derived columns every analysis uses."""
    n = pn["n"]
    pn["stepup"] = pn["start"] + pn["L"]
    pn["running"] = pn["end"] == -2
    pn["withdrawn"] = pn["end"] == -1
    pn["last"] = np.where(pn["running"], P.CUT, pn["end"])
    # reading proxy: mean reading days in the subscription's first three months, where all three are in the log
    pr = np.full(n, np.nan)
    ok = (pn["start"] >= P.READ_FROM) & (pn["start"] + months - 1 <= P.CUT) & ~pn["withdrawn"]
    idx = np.where(ok)[0]
    m = pn["start"][idx]
    R = pn["reading"]
    if adjust:
        # each month's reading against that month's average over every running subscription
        act = R > 0
        avg = np.array([R[act[:, q], q].mean() if act[:, q].any() else 1.0 for q in range(R.shape[1])])
        R = R / np.where(avg > 0, avg, 1.0) * np.nanmean(avg[P.READ_FROM:])
    vals = np.stack([R[idx, m + d] for d in range(months)], axis=1)
    alive3 = np.stack([(pn["last"][idx] >= m + d) for d in range(months)], axis=1)
    cnt = alive3.sum(axis=1)
    pr[idx] = np.where(cnt > 0, (vals * alive3).sum(axis=1) / np.maximum(cnt, 1), np.nan)
    pn["proxy"] = pr
    return pn


# ---------------------------------------------------------------- from the shipped files

def months_between(a, b):
    """Whole months from date a to date b (b on the same day of a later month)."""
    return (b.year - a.year) * 12 + (b.month - a.month)


def addr_key(street, no, pc):
    s = street.strip().lower().replace(" ", "")
    for old, new in (("strasse", "straße"), ("str.", "straße")):
        if s.endswith(old):
            s = s[: -len(old)] + new
    return s + "|" + no.strip().lower() + "|" + pc.strip()


def from_pack(target, months=3, adjust=False):
    import csv
    import datetime as dt
    import os
    import pack as PK
    F = {k: os.path.join(target, v) for k, v in PK.FILES.items()}
    D = lambda x: dt.date.fromisoformat(x) if x else None  # noqa: E731
    cust_type, cust_addr = {}, {}
    with open(F["customers"], encoding="utf-8") as f:
        for r in csv.DictReader(f):
            c = int(r["customer_no"])
            cust_type[c] = r["account_type"]
            cust_addr[c] = addr_key(r["street"], r["house_no"], r["postcode"])
    rows, seen = [], set()
    with open(F["subs"], encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = tuple(r.values())
            if key in seen:
                continue
            seen.add(key)
            if r["product"] != "DIGITAL" or cust_type.get(int(r["customer_no"])) != "CONSUMER":
                continue
            rows.append(r)
    rows.sort(key=lambda r: r["subscription_id"])
    n = len(rows)
    old_to_new = {v: k for k, v in P.OLD_CODE.items()}
    pn = {k: np.zeros(n, int) for k in ["start", "title", "channel", "offer", "route", "end", "L", "tenure0",
                                        "customer"]}
    pn["ip"] = np.zeros(n)
    pn["reason"] = np.empty(n, dtype=object)
    pn["kind"] = np.empty(n, dtype=object)
    sid_idx = {}
    start_dates = []
    jan23 = dt.date(2023, 1, 1)
    for i, r in enumerate(rows):
        sid_idx[r["subscription_id"]] = i
        sd = D(r["start_date"])
        start_dates.append(sd)
        if sd < jan23:
            pn["kind"][i] = "base"
            pn["start"][i] = 0
            pn["tenure0"][i] = months_between(sd, dt.date(2023, 1, sd.day))
        else:
            pn["kind"][i] = "new"
            pn["start"][i] = (sd.year - P.M0_YEAR) * 12 + sd.month - P.M0_MONTH
        pn["title"][i] = sim.T_IDX[r["title"]]
        code = r["channel"]
        pn["channel"][i] = sim.C_IDX[old_to_new.get(code, code)] if code else sim.C_IDX["DIR"]
        pn["offer"][i] = sim.O_IDX[r["offer_code"]] if r["offer_code"] else -1
        ie = D(r["intro_end_date"])
        pn["L"][i] = months_between(sd, ie + dt.timedelta(days=1)) if ie else 0
        pn["route"][i] = sim.R_IDX[r["payment_route"]]
        pn["customer"][i] = int(r["customer_no"])
        ed = D(r["end_date"])
        reason = r["end_reason"]
        pn["reason"][i] = reason if ed else ""
        if ed is None:
            pn["end"][i] = -2
        elif reason == "WITHDRAWN":
            pn["end"][i] = -1
        else:
            K = months_between(sd, ed + dt.timedelta(days=1))
            pn["end"][i] = (K - pn["tenure0"][i] - 1) if pn["kind"][i] == "base" else pn["start"][i] + K - 1
    T = P.CUT + 1
    G = np.zeros((n, T))
    first_price = {}
    with open(F["periods"], encoding="utf-8") as f:
        for r in csv.DictReader(f):
            i = sid_idx.get(r["subscription_id"])
            if i is None:
                continue
            a = D(r["valid_from"])
            b = D(r["valid_to"]) or dt.date(2026, 10, 31)
            p = float(r["monthly_price_eur"])
            if r["period_type"] == "INTRO" and (i not in first_price or a < first_price[i][0]):
                first_price[i] = (a, p)
            d = a
            while d <= b:
                m = (d.year - P.M0_YEAR) * 12 + d.month - P.M0_MONTH
                if 0 <= m < T:
                    G[i, m] = p
                d = PK.add_months(d, 1)
    for i in range(n):
        if i in first_price:
            pn["ip"][i] = first_price[i][1]
        if pn["end"][i] == -1:
            G[i] = 0.0
    pn["gross"] = G
    # reading: every login's days, summed to its customer, put on the subscription running that month
    login_c = {}
    with open(F["logins"], encoding="utf-8") as f:
        for r in csv.DictReader(f):
            login_c[r["login_id"]] = int(r["customer_no"])
    by_cust = {}
    for i in range(n):
        by_cust.setdefault(pn["customer"][i], []).append(i)
    last = np.where(pn["end"] == -2, P.CUT, pn["end"])
    Rm = np.zeros((n, T))
    with open(F["reading"], encoding="utf-8") as f:
        for r in csv.DictReader(f):
            c = login_c.get(r["login_id"])
            if c is None or c not in by_cust:
                continue
            y, mo = int(r["month"][:4]), int(r["month"][5:7])
            m = (y - P.M0_YEAR) * 12 + mo - P.M0_MONTH
            for i in by_cust[c]:
                if pn["start"][i] <= m <= last[i] and pn["end"][i] != -1:
                    Rm[i, m] += int(r["reading_days"])
                    break
    pn["reading"] = Rm
    fps = {}
    with open(F["methods"], encoding="utf-8") as f:
        for r in csv.DictReader(f):
            fps.setdefault(int(r["customer_no"]), []).append(r["fingerprint"])
    pn["fingerprint"] = np.empty(n, dtype=object)
    pn["address"] = np.empty(n, dtype=object)
    for i in range(n):
        pn["fingerprint"][i] = tuple(fps.get(pn["customer"][i], []))
        pn["address"][i] = cust_addr[pn["customer"][i]]
    pn["household"] = households(pn["customer"], pn["fingerprint"], pn["address"])
    pn["n"] = n
    pn["sid"] = [r["subscription_id"] for r in rows]
    pn["start_date"] = start_dates
    return finish(pn, months=months, adjust=adjust)
