"""The Tenancy Bond Board's register as its two systems export it, written from the simulated tenancies.

The legacy system (to 5 March 2023) keyed a bond by a bond number and held the premises as the free text the landlord
or agent typed on the lodgement form, the rent as an amount with a frequency, and landlords by a landlord number. The
online system (from 6 March 2023) validates each new lodgement's address against the national address file and stores
its property identifier, records weekly rents, and re-keyed landlords. Bonds active at the migration were carried
across with their legacy premises text and no property identifier. Nothing here is placed for a result."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import params as P
import world as WD

ABBR = {"Street": ["St", "St.", "Street", "Str"], "Road": ["Rd", "Rd.", "Road"], "Avenue": ["Ave", "Av", "Avenue"],
        "Terrace": ["Tce", "Terrace", "Terr"], "Crescent": ["Cres", "Cr", "Crescent"], "Place": ["Pl", "Place"],
        "Drive": ["Dr", "Drive", "Drv"], "Lane": ["Ln", "Lane"], "Grove": ["Gr", "Grove"], "Parade": ["Pde", "Parade"],
        "Way": ["Way", "Wy"], "Close": ["Cl", "Close"]}
DTYPE_LEGACY = {"H": "H", "T": "T", "A": "F", "R": "R"}
DTYPE_ONLINE = {"H": "house", "T": "townhouse", "A": "apartment", "R": "room"}


def canonical(W, d):
    si = int(W.dw["suburb"][d])
    name, stype = W.streets[si][int(W.dw["street"][d])]
    num = int(W.dw["number"][d])
    unit = W.dw["unit"][d]
    street = "%s %s" % (name, stype)
    return ("%s/%d %s" % (unit, num, street)) if unit else ("%d %s" % (num, street))


def typed_premises(W, d, rng):
    """The premises as one landlord or agent typed them on a paper or legacy lodgement form."""
    si = int(W.dw["suburb"][d])
    name, stype = W.streets[si][int(W.dw["street"][d])]
    num = int(W.dw["number"][d])
    unit = W.dw["unit"][d]
    st = name + " " + str(rng.choice(ABBR[stype], p=_abbr_p(len(ABBR[stype]))))
    u = rng.random()
    if not unit:
        s = "%d %s" % (num, st)
        if u < 0.05:
            s = s + ", " + W.suburbs[si]["name"]
        elif u < 0.08:
            s = s.upper()
        elif u < 0.095:
            s = "%d %s" % (num, _typo(name, rng) + " " + st.split(" ", 1)[1] if " " in st else st)
    else:
        dt_ = W.dw["dtype"][d]
        forms = ["{u}/{n} {s}", "Unit {u}, {n} {s}", "Flat {u} {n} {s}", "{u} / {n} {s}", "U{u} {n} {s}",
                 "{n} {s} (Unit {u})", "Apt {u}, {n} {s}", "{u}/{n} {S}"]
        pw = [0.40, 0.16, 0.08, 0.05, 0.05, 0.04, 0.10 if dt_ in ("A", "R") else 0.02, 0.06]
        if dt_ == "R":
            forms[1] = "Room {u}, {n} {s}"
        pw = np.array(pw) / sum(pw)
        f = forms[int(rng.choice(len(forms), p=pw))]
        s = f.format(u=unit, n=num, s=st, S=st.upper())
        if u < 0.012:
            s = "%d %s" % (num, st)          # the unit left off the form
        elif u < 0.02:
            s = "%d/%s %s" % (num, unit, st)  # number and unit the wrong way round
    return s


def bond_amount(rent, rng):
    """The bond a landlord asks for: four weeks' rent most often, three or two weeks' for some, and a round sum near
    four weeks' for others."""
    u = rng.random()
    if u < 0.70:
        return round(4 * rent)
    if u < 0.82:
        return round(3 * rent)
    if u < 0.90:
        return round(2 * rent)
    if u < 0.97:
        return int(round(4 * rent / 50.0) * 50)
    return int(round(4 * rent / 100.0) * 100 - 100)


def _abbr_p(k):
    w = np.array([0.55] + [0.45 / (k - 1)] * (k - 1)) if k > 1 else np.array([1.0])
    return w / w.sum()


def _typo(name, rng):
    if len(name) < 5:
        return name
    i = int(rng.integers(1, len(name) - 1))
    if rng.random() < 0.5:
        return name[:i] + name[i + 1:]
    return name[:i] + name[i] + name[i:]


def _fmt(n):
    return WD.date_of(n).strftime("%d/%m/%Y")


def _iso(n):
    return WD.date_of(n).isoformat()


def build(W, seed=P.SEED + 11):
    rng = np.random.default_rng(seed)
    T, CH, EV = W.T, W.CH, W.EV
    mig = WD.day(P.MIGRATION)
    scope = WD.day(P.LEGACY_SCOPE)
    cut = WD.day(P.EXTRACT_END)
    regions_from = WD.day(P.REGIONS_FROM)
    n_t = W.n_t

    # identifiers: legacy bond numbers rise with lodgement date with irregular gaps; landlord numbers are drawn
    order = np.argsort(T["lodged"], kind="stable")
    gaps = rng.integers(1, 9, size=n_t)
    legacy_no = np.zeros(n_t, dtype=np.int64)
    legacy_no[order] = 1400000 + np.cumsum(gaps)
    n_owner = len(W.owners)
    ll_legacy = rng.choice(np.arange(100000, 999999), size=n_owner, replace=False)
    ll_online = rng.choice(np.arange(10000000, 99999999), size=n_owner, replace=False)
    agent_no = rng.choice(np.arange(101, 999), size=len(W.agent_names), replace=False)
    prop_id = rng.choice(np.arange(1000000, 9999999), size=W.n_dw, replace=False)

    # each tenancy's owner over time: the owner at the start, then transfers
    tr_by_t = {}
    for t, kind, d, o in zip(EV["tenancy"], EV["kind"], EV["date"], EV["owner"]):
        tr_by_t.setdefault(int(t), []).append((int(d), str(kind), int(o)))
    for v in tr_by_t.values():
        v.sort()

    def agent_of(owner):
        a = W.owners[owner]["agent"]
        return ("AG%03d" % agent_no[a]) if a is not None else ""

    def freq_for(t, op):
        if op:
            return "W"
        u = rng.random()
        return "W" if u < 0.71 else ("F" if u < 0.91 else "M")

    def amount(weekly, f):
        if f == "W":
            return weekly
        if f == "F":
            return 2 * weekly
        return round(weekly * 52 / 12)

    def tenfold(x):
        return x * 10 if rng.random() < P.P_TENFOLD else x

    legacy_rows = []
    online_rows = []
    prem_by_t = {}
    held_at_mig = {}
    legacy_last = {}
    month_ctr = {}
    truth = {"bond_of_tenancy": {}, "migrated": set(), "online_lodged": set()}
    ch_lo = W.ch_index
    landlord_active_at_mig = set()

    for t in range(n_t):
        if not T["bonded"][t]:
            continue
        d = int(T["dwelling"][t])
        start, end, lodged, refund = int(T["start"][t]), int(T["end"][t]), int(T["lodged"][t]), int(T["refund"][t])
        op = W.dw["operator"][d]
        owner0 = int(T["owner0"][t])
        si = int(W.dw["suburb"][d])
        sub = W.suburbs[si]
        dtype = W.dw["dtype"][d]
        beds = int(W.dw["beds"][d])
        rent0 = float(T["rent0"][t])
        lo, hi = ch_lo[t]
        rises = [(int(CH["date"][j]), float(CH["rent"][j]), bool(CH["topup"][j]), int(CH["topup_date"][j]),
                  bool(CH["effective_field"][j])) for j in range(lo, hi)]
        events = tr_by_t.get(t, [])
        in_legacy = lodged < mig and refund >= scope
        in_online_mig = lodged < mig <= refund
        in_online_new = mig <= lodged <= cut
        if not (in_legacy or in_online_mig or in_online_new):
            continue
        f = freq_for(t, op)
        # ----------------------------------------------------------------- legacy rows
        if in_legacy:
            prem = typed_premises(W, d, rng)
            prem_by_t[t] = prem
            bno = "LB%07d" % legacy_no[t]
            truth["bond_of_tenancy"][t] = bno
            bed_s = "" if rng.random() < 0.03 else str(beds)
            amt = tenfold(amount(rent0, f))
            legacy_last[t] = (amt, f)
            row = [bno, "L", _fmt(lodged), _fmt(start), amt, f, bond_amount(rent0, rng),
                   prem, sub["name"], sub["postcode"], sub["area"], DTYPE_LEGACY[dtype], bed_s,
                   "L%06d" % ll_legacy[owner0], agent_of(owner0), int(rng.choice([1, 1, 2, 2, 2, 3, 4]))]
            legacy_rows.append(row)
            if rng.random() < P.P_RESENT:
                legacy_rows.append(list(row))
            cur_owner = owner0
            held = rent0          # the rent the bond held was last calculated on
            for (rd, newr, tp, tdate, eff) in rises:
                if tp and tdate < mig:
                    a_amt = tenfold(amount(newr, f))
                    legacy_last[t] = (a_amt, f)
                    legacy_rows.append([bno, "A", _fmt(tdate), "", a_amt, f,
                                        round(4 * (newr - held)), "", "", "", "", "", "", "", "", ""])
                    held = newr
            held_at_mig[t] = held
            for (ed, kind, o) in events:
                if ed < mig:
                    if kind == "transfer":
                        legacy_rows.append([bno, "T", _fmt(ed), "", "", "", "", "", "", "", "", "", "",
                                            "L%06d" % ll_legacy[o], agent_of(o), ""])
                        cur_owner = o
                    else:
                        legacy_rows.append([bno, "P", _fmt(ed), "", "", "", "", "", "", "", "", "", "", "", "",
                                            int(rng.choice([1, 2, 2, 3]))])
            if refund < mig:
                legacy_rows.append([bno, "R", _fmt(refund), "", "", "", "", "", "", "", "", "", "", "", "", ""])
        # ----------------------------------------------------------------- online rows
        if in_online_mig or in_online_new:
            yymm = WD.date_of(max(lodged, mig)).strftime("%y%m")
            c = month_ctr.get(yymm, int(rng.integers(1000, 4000)))
            c += int(rng.integers(1, 6))
            month_ctr[yymm] = c
            bid = "B%s-%06d" % (yymm, c)
            truth.setdefault("online_bond_of_tenancy", {})[t] = bid
            # owner at the migration (or at lodgement)
            owner = owner0
            for (ed, kind, o) in events:
                if kind == "transfer" and ed < max(lodged, mig):
                    owner = o
            if in_online_mig:
                truth["migrated"].add(t)
                landlord_active_at_mig.add(owner)
                # the legacy record carried across: the premises text and the last rent the legacy system held
                amt_l, f_l = legacy_last.get(t, (rent0, "W"))
                last = round(amt_l if f_l == "W" else (amt_l / 2.0 if f_l == "F" else amt_l * 12.0 / 52.0), 2)
                prem_text = prem_by_t.get(t) or typed_premises(W, d, rng)
                online_rows.append([bid, "MIGRATED", _iso(mig), _iso(start), last, "", "", prem_text, sub["name"],
                                    sub["postcode"], sub["area"], DTYPE_ONLINE[dtype], beds,
                                    "LL%08d" % ll_online[owner], agent_of(owner),
                                    truth["bond_of_tenancy"].get(t, ""), ""])
            else:
                truth["online_lodged"].add(t)
                area = sub["region"] if lodged >= regions_from else sub["area"]
                online_rows.append([bid, "LODGE", _iso(lodged), _iso(start), tenfold(rent0),
                                    bond_amount(rent0, rng), "P%07d" % prop_id[d],
                                    canonical(W, d), sub["name"], sub["postcode"], area, DTYPE_ONLINE[dtype], beds,
                                    "LL%08d" % ll_online[owner], agent_of(owner), "", ""])
            held = held_at_mig.get(t, rent0)
            for (rd, newr, tp, tdate, eff) in rises:
                if tp and mig <= tdate <= cut and tdate >= max(lodged, mig):
                    online_rows.append([bid, "TOPUP", _iso(tdate), "", tenfold(newr), round(4 * (newr - held)), "",
                                        "", "", "", "", "", "", "", "", "", _iso(rd) if eff else ""])
                    held = newr
            for (ed, kind, o) in events:
                if mig <= ed <= cut and ed >= max(lodged, mig):
                    if kind == "transfer":
                        online_rows.append([bid, "TRANSFER", _iso(ed), "", "", "", "", "", "", "", "", "", "",
                                            "LL%08d" % ll_online[o], agent_of(o), "", ""])
                    else:
                        online_rows.append([bid, "PARTIES", _iso(ed), "", "", "", "", "", "", "", "", "", "", "",
                                            "", "", ""])
            if mig <= refund <= cut:
                online_rows.append([bid, "REFUND", _iso(refund), "", "", "", "", "", "", "", "", "", "", "", "", "",
                                    ""])
    legacy_cols = ["BOND_NO", "REC_TYPE", "REC_DATE", "TENANCY_START", "RENT_AMT", "RENT_FREQ", "BOND_AMT",
                   "PREMISES", "SUBURB", "POSTCODE", "AREA_CODE", "DWELLING", "BEDROOMS", "LANDLORD_NO", "AGENT_NO",
                   "TENANTS"]
    online_cols = ["bond_id", "event", "event_date", "tenancy_start", "weekly_rent", "bond_amount", "property_id",
                   "address", "suburb", "postcode", "area_or_region", "dwelling_type", "bedrooms", "landlord_id",
                   "agent_id", "legacy_bond_no", "rent_effective_from"]
    L = pd.DataFrame(legacy_rows, columns=legacy_cols)
    O = pd.DataFrame(online_rows, columns=online_cols)
    # the legacy export lists records by bond number then record date; the online export by event date then bond
    L["_k"] = pd.to_datetime(L["REC_DATE"], format="%d/%m/%Y")
    L = L.sort_values(["BOND_NO", "_k"], kind="stable").drop(columns="_k").reset_index(drop=True)
    O = O.sort_values(["event_date", "bond_id"], kind="stable").reset_index(drop=True)
    # the landlord crosswalk the migration produced: every landlord holding a bond on 5 March 2023
    xw = sorted(("L%06d" % ll_legacy[o], "LL%08d" % ll_online[o]) for o in landlord_active_at_mig)
    X = pd.DataFrame(xw, columns=["legacy_landlord_no", "landlord_id"])
    W.reg_truth = truth
    W.ids = {"legacy_no": legacy_no, "ll_legacy": ll_legacy, "ll_online": ll_online, "prop_id": prop_id,
             "agent_no": agent_no}
    return L, O, X
