"""The register conformed from the shipped files alone: one row per tenancy across the two systems, each tenancy's
dwelling found (by property identifier, or by its premises text parsed and matched), its region, its landlord class,
its recorded rents, and the day it stops covering. Used by the golden, every pass and the rivals; verify.py has its
own code path."""
import os
import re

import numpy as np
import pandas as pd

EPOCH = np.datetime64("1970-01-01")
TYPE_FULL = {"ST": "STREET", "STR": "STREET", "STREET": "STREET", "RD": "ROAD", "ROAD": "ROAD", "AVE": "AVENUE",
             "AV": "AVENUE", "AVENUE": "AVENUE", "TCE": "TERRACE", "TERR": "TERRACE", "TERRACE": "TERRACE",
             "CRES": "CRESCENT", "CR": "CRESCENT", "CRESCENT": "CRESCENT", "PL": "PLACE", "PLACE": "PLACE",
             "DR": "DRIVE", "DRV": "DRIVE", "DRIVE": "DRIVE", "LN": "LANE", "LANE": "LANE", "GR": "GROVE",
             "GROVE": "GROVE", "PDE": "PARADE", "PARADE": "PARADE", "WAY": "WAY", "WY": "WAY", "CL": "CLOSE",
             "CLOSE": "CLOSE"}
OPERATOR_MIN = 500    # landlords holding this many bonds at once are the block operators


def days(s, fmt=None):
    d = pd.to_datetime(s, format=fmt, errors="coerce")
    return ((d - pd.Timestamp("1970-01-01")).dt.days).astype("float")


def load(target):
    f = {n: os.path.join(target, n) for n in os.listdir(target)}
    pick = lambda pre: [v for k, v in f.items() if os.path.basename(k).startswith(pre)][0]
    L = pd.read_csv(pick("tbb_legacy_register_extract"), dtype=str, keep_default_na=False)
    O = pd.read_csv(pick("tbb_bond_events"), dtype=str, keep_default_na=False)
    X = pd.read_csv(pick("tbb_landlord_id_crosswalk"), dtype=str, keep_default_na=False)
    C = pd.read_csv(pick("pso_suburb_region_concordance"), dtype=str, keep_default_na=False)
    PN = pd.read_csv(pick("pso_rent_survey_20"), dtype=str, keep_default_na=False)
    return {"L": L, "O": O, "X": X, "C": C, "PN": PN, "CPI": cpi_release(pick("pso_cpi_")), "files": f}


def cpi_release(path):
    """All-groups annual change by quarter from the CPI release: {(year, quarter): per cent}."""
    import openpyxl
    ws = openpyxl.load_workbook(path, data_only=True).active
    out = {}
    head = None
    for row in ws.iter_rows(values_only=True):
        if row and row[0] == "Quarter":
            head = list(row)
            continue
        if head and row and isinstance(row[0], str) and re.fullmatch(r"\d{4}Q[1-4]", row[0]):
            out[(int(row[0][:4]), int(row[0][-1]))] = float(row[head.index("All groups annual change (%)")])
    return out


# ------------------------------------------------------------------------------------------------ addresses
_P1 = re.compile(r"^(?:U|UNIT|FLAT|APT|ROOM)?\s*(\d+[A-Z]?)\s*/\s*(\d+[A-Z]?)\s+(.+)$")
_P2 = re.compile(r"^(?:UNIT|FLAT|APT|ROOM|U)\s*(\d+[A-Z]?),?\s+(\d+[A-Z]?)\s+(.+)$")
_P3 = re.compile(r"^(\d+[A-Z]?)\s+(.+?)\s*\((?:UNIT|FLAT|APT|ROOM)\s*(\d+[A-Z]?)\)$")
_P4 = re.compile(r"^(\d+[A-Z]?)\s+(.+)$")


def parse_address(text, suburb=""):
    """(unit, number, street name, street type) from a premises line as typed or as validated."""
    s = (text or "").upper().replace(".", " ").replace("  ", " ").strip()
    sub = (suburb or "").upper().strip()
    if sub and s.endswith(", " + sub):
        s = s[: -len(sub) - 2].strip()
    s = re.sub(r"\s+", " ", s)
    unit = num = street = None
    m = _P1.match(s)
    if m:
        unit, num, street = m.group(1), m.group(2), m.group(3)
    else:
        m = _P2.match(s)
        if m:
            unit, num, street = m.group(1), m.group(2), m.group(3)
        else:
            m = _P3.match(s)
            if m:
                num, street, unit = m.group(1), m.group(2), m.group(3)
            else:
                m = _P4.match(s)
                if m:
                    num, street = m.group(1), m.group(2)
    if not street:
        return None
    street = street.replace(",", " ").strip()
    parts = street.split()
    stype = ""
    if len(parts) >= 2 and parts[-1] in TYPE_FULL:
        stype = TYPE_FULL[parts[-1]]
        name = " ".join(parts[:-1])
    else:
        name = " ".join(parts)
    return (unit or "", num, name, stype)


def _edit1(a, b):
    """True when a and b differ by one deletion, insertion or substitution."""
    if a == b:
        return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la > lb:
        a, b, la, lb = b, a, lb, la
    i = j = 0
    diff = 0
    while i < la and j < lb:
        if a[i] != b[j]:
            diff += 1
            if diff > 1:
                return False
            if la == lb:
                i += 1
            j += 1
        else:
            i += 1
            j += 1
    return diff + (lb - j) <= 1


def conform(D, strict="golden"):
    """strict: 'golden' parses premises and matches them to validated addresses (street-name slips and a reversed
    unit and number tried); 'norm' parses them the same way with no allowance for a slip or a reversal; 'exact'
    matches only identical normalised strings; 'pid' uses property identifiers alone."""
    L, O, X, C = D["L"], D["O"], D["X"], D["C"]
    region_of_pc = dict(zip(C["postcode"], C["region_code"]))
    # ---------------------------------------------------------------- legacy
    L = L.drop_duplicates().copy()
    L["day"] = days(L["REC_DATE"], "%d/%m/%Y")
    lod = L[L["REC_TYPE"] == "L"].copy()
    lod["start"] = days(lod["TENANCY_START"], "%d/%m/%Y")
    amt = pd.to_numeric(lod["RENT_AMT"], errors="coerce")
    freq = lod["RENT_FREQ"]
    weekly = np.where(freq == "F", amt / 2.0, np.where(freq == "M", amt * 12.0 / 52.0, amt))
    bond = pd.to_numeric(lod["BOND_AMT"], errors="coerce").values
    # a rent keyed with an extra zero: the bond (two to four weeks' rent) is a fraction of one week's rent
    ten = (bond > 0) & (weekly > 0) & (bond / weekly < 0.6) & (bond / (weekly / 10.0) >= 1.5)
    weekly = np.where(ten, weekly / 10.0, weekly)
    lod["rent0"] = weekly
    lod["freq"] = freq
    leg = lod[["BOND_NO", "day", "start", "rent0", "freq", "PREMISES", "SUBURB", "POSTCODE", "DWELLING", "BEDROOMS",
               "LANDLORD_NO"]].rename(columns={"BOND_NO": "key", "day": "lodged", "PREMISES": "premises",
                                               "SUBURB": "suburb", "POSTCODE": "postcode", "DWELLING": "dtype",
                                               "BEDROOMS": "beds", "LANDLORD_NO": "landlord_legacy"})
    leg["system"] = "legacy"
    ref = L[L["REC_TYPE"] == "R"].groupby("BOND_NO")["day"].min()
    leg["refund"] = leg["key"].map(ref)
    # additional bonds recorded by the legacy system
    a = L[L["REC_TYPE"] == "A"].copy()
    a = a.merge(lod[["BOND_NO", "freq", "rent0"]], on="BOND_NO", how="left", suffixes=("", "_l"))
    aamt = pd.to_numeric(a["RENT_AMT"], errors="coerce")
    a["rent"] = np.where(a["freq"] == "F", aamt / 2.0, np.where(a["freq"] == "M", aamt * 12.0 / 52.0, aamt))
    a = a.rename(columns={"BOND_NO": "key"})[["key", "day", "rent"]]
    a["effective"] = np.nan
    # ---------------------------------------------------------------- online
    O = O.copy()
    O["day"] = days(O["event_date"])
    mig = O[O["event"] == "MIGRATED"].copy()
    new = O[O["event"] == "LODGE"].copy()
    for df in (mig, new):
        df["start"] = days(df["tenancy_start"])
        df["rent0"] = pd.to_numeric(df["weekly_rent"], errors="coerce")
    nb = pd.to_numeric(new["bond_amount"], errors="coerce").values
    nr = new["rent0"].values
    ten = (nb > 0) & (nr > 0) & (nb / nr < 0.6) & (nb / (nr / 10.0) >= 1.5)
    new["rent0"] = np.where(ten, nr / 10.0, nr)
    online_ref = O[O["event"] == "REFUND"].groupby("bond_id")["day"].min()
    # migrated bonds continue legacy tenancies: their later events attach to the legacy key
    mig_key = dict(zip(mig["bond_id"], mig["legacy_bond_no"]))
    mig_landlord = dict(zip(mig["legacy_bond_no"], mig["landlord_id"]))
    leg["landlord_id"] = leg["key"].map(mig_landlord)
    xw = dict(zip(X["legacy_landlord_no"], X["landlord_id"]))
    leg["landlord_id"] = leg["landlord_id"].fillna(leg["landlord_legacy"].map(xw))
    ref_mig = {mig_key[b]: d for b, d in online_ref.items() if b in mig_key}
    leg["refund"] = leg["refund"].fillna(leg["key"].map(ref_mig))
    leg["migrated"] = leg["key"].isin(set(mig["legacy_bond_no"]))
    onl = new[["bond_id", "day", "start", "rent0", "property_id", "address", "suburb", "postcode", "area_or_region",
               "dwelling_type", "bedrooms", "landlord_id"]].rename(
        columns={"bond_id": "key", "day": "lodged", "address": "premises", "dwelling_type": "dtype",
                 "bedrooms": "beds"})
    onl["system"] = "online"
    onl["refund"] = onl["key"].map(online_ref)
    onl["migrated"] = False
    # additional bonds in the online system (for migrated bonds, keyed to the legacy tenancy)
    t = O[O["event"] == "TOPUP"].copy()
    t["key"] = t["bond_id"].map(lambda b: mig_key.get(b, b))
    t["rent"] = pd.to_numeric(t["weekly_rent"], errors="coerce")
    t["effective"] = days(t["rent_effective_from"])
    t = t[["key", "day", "rent", "effective"]]
    tops = pd.concat([a, t], ignore_index=True)
    # ---------------------------------------------------------------- one tenancy table
    leg["dtype"] = leg["dtype"].map({"H": "house", "T": "townhouse", "F": "apartment", "R": "room"})
    leg["property_id"] = ""
    ten_df = pd.concat([leg.drop(columns=["landlord_legacy", "freq"]), onl.drop(columns=["area_or_region"])],
                       ignore_index=True)
    ten_df["region"] = ten_df["postcode"].map(region_of_pc)
    ten_df["beds"] = pd.to_numeric(ten_df["beds"], errors="coerce")
    # extra-zero rents on additional bonds: ten times the previous recorded rent or more
    tops = tops.sort_values(["key", "day"], kind="stable")
    r0 = ten_df.set_index("key")["rent0"]
    prev = tops.groupby("key")["rent"].shift(1)
    prev = prev.fillna(tops["key"].map(r0))
    bad = tops["rent"] > 5 * prev
    tops.loc[bad, "rent"] = tops.loc[bad, "rent"] / 10.0
    # ---------------------------------------------------------------- dwellings
    ten_df["dwelling"] = _dwellings(ten_df, strict)
    # ---------------------------------------------------------------- landlord class
    held = ten_df.groupby("landlord_id")["key"].nunique()
    ops = set(held[held >= OPERATOR_MIN].index)
    ten_df["operator"] = ten_df["landlord_id"].isin(ops)
    # ---------------------------------------------------------------- the day each tenancy stops covering (2.2)
    ten_df = ten_df.sort_values(["dwelling", "start", "lodged"], kind="stable").reset_index(drop=True)
    nxt = ten_df.groupby("dwelling")["start"].shift(-1)
    end = ten_df["refund"] - 1
    end = np.where(nxt.notna() & (nxt - 1 < end.fillna(1e9)), nxt - 1, end)
    ten_df["end"] = pd.Series(end).fillna(1e9).values
    return ten_df, tops, ops


def _dwellings(T, strict):
    """A dwelling key per tenancy: its property identifier, or the validated address its premises matches."""
    pid = T["property_id"].fillna("")
    keys = np.where(pid != "", pid, "")
    if strict == "pid":
        return np.where(keys != "", keys, "K:" + T["key"])
    # validated addresses of the online lodgements: (postcode, unit, number, name, type) -> property identifier
    val = T[pid != ""]
    vmap = {}
    names_by_pc = {}
    for p, adr, pc in zip(val["property_id"], val["premises"], val["postcode"]):
        pa = parse_address(adr)
        if pa is None:
            continue
        vmap[(pc,) + pa] = p
        vmap.setdefault((pc, pa[0], pa[1], pa[2], ""), p)
        names_by_pc.setdefault(pc, set()).add(pa[2])
    out = []
    for k, p, adr, sub, pc in zip(T["key"], pid, T["premises"], T["suburb"], T["postcode"]):
        if p:
            out.append(p)
            continue
        if strict == "exact":
            # an identical line after case and spacing, against the validated address and its usual abbreviations
            raw = re.sub(r"\s+", " ", (adr or "").upper().strip())
            hit = _exact_index(T).get((pc, raw))
            out.append(hit if hit else "A:%s|%s" % (pc, raw))
            continue
        pa = parse_address(adr, sub)
        if pa is None:
            out.append("K:" + k)
            continue
        unit, num, name, stype = pa
        hit = vmap.get((pc, unit, num, name, stype)) or vmap.get((pc, unit, num, name, ""))
        if hit is None and stype:
            hit = vmap.get((pc, unit, num, name, stype))
        if strict == "norm":
            # the premises parsed and compared field by field, with no allowance for a slip or a reversed unit
            out.append(hit if hit else "A:%s|%s|%s|%s|%s" % (pc, unit, num, name, stype))
            continue
        if hit is None and name not in names_by_pc.get(pc, set()):
            # a slip in the street name: the one validated street in the postcode a single edit away
            near = [n for n in names_by_pc.get(pc, set()) if _edit1(n, name)]
            if len(near) == 1:
                hit = vmap.get((pc, unit, num, near[0], stype)) or vmap.get((pc, unit, num, near[0], ""))
                name = near[0]
        if hit is None and unit:
            # the unit and the number written the wrong way round
            hit = vmap.get((pc, num, unit, name, stype)) or vmap.get((pc, num, unit, name, ""))
        out.append(hit if hit else "A:%s|%s|%s|%s|%s" % (pc, unit, num, name, stype))
    return np.array(out, dtype=object)


_EXACT = {}


def _exact_index(T):
    if id(T) in _EXACT:
        return _EXACT[id(T)]
    pid = T["property_id"].fillna("")
    val = T[pid != ""]
    idx = {}
    for p, adr, pc in zip(val["property_id"], val["premises"], val["postcode"]):
        idx[(pc, re.sub(r"\s+", " ", adr.upper().strip()))] = p
        # the common abbreviations a careful string match expands
        s = re.sub(r"\s+", " ", adr.upper().strip())
        for full, ab in (("STREET", "ST"), ("ROAD", "RD"), ("AVENUE", "AVE"), ("TERRACE", "TCE"), ("CRESCENT", "CRES"),
                         ("PLACE", "PL"), ("DRIVE", "DR"), ("LANE", "LN"), ("GROVE", "GR"), ("PARADE", "PDE"),
                         ("CLOSE", "CL")):
            if s.endswith(" " + full):
                idx[(pc, s[: -len(full)] + ab)] = p
                idx[(pc, s[: -len(full)] + ab + ".")] = p
    _EXACT[id(T)] = idx
    return idx
